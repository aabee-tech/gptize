import os
import subprocess
import logging
from datetime import datetime
import pathspec
import pyperclip
import tiktoken
from .models import File, Project
from .settings import Settings
from .output_builder import OutputBuilder


class GPTizer:
    def __init__(self):
        self._project = None
        self._gitignore = None

        try:
            logging.info(f"Loading tiktoken {Settings.TOKEN_MODEL_NAME} model")
            self.encoder = tiktoken.get_encoding(Settings.TOKEN_MODEL_NAME)
            logging.info(f"Loading tiktoken {Settings.TOKEN_MODEL_NAME} model complete")
        except Exception as e:
            self.encoder = None
            logging.error(f"Failed to initialize tiktoken encoder: {e}")

    def process_directory(self, target_path: str, repo_root: str, gptize_ignore: str):
        """
        Processes all the files within a given directory. This method initializes
        the Project object for the specified directory, loads the .gitignore patterns
        from the repository root, and populates the project with files that are not
        ignored by .gitignore.
        """
        project_name = os.path.basename(target_path)
        self._project = Project(project_name, target_path)
        self._gitignore = self.load_gitignore(repo_root, gptize_ignore)
        self.populate_files()

    def process_file(self, file_path: str, repo_root: str, gptize_ignore: str):
        """
        Processes a single file. This method creates a Project object for the file,
        treating the file as an individual project. It loads .gitignore from the
        repository root to determine which files to ignore.
        """
        root_path, file_name = os.path.split(file_path)
        project_name = os.path.basename(root_path) if root_path else 'SingleFileProject'
        self._project = Project(project_name, root_path or '.')
        self._gitignore = self.load_gitignore(repo_root, gptize_ignore)

        file_obj = File(file_name, file_path)
        self.load_file_content(file_obj)
        self._project.files.append(file_obj)

    @property
    def project(self) -> Project:
        """
        Property to access the project object.
        """
        if self._project is None:
            logging.error("Project has not been initialized.")
            raise AttributeError("Project has not been initialized.")
        return self._project

    def load_gitignore(self, repo_root: str, gptize_ignore: str) -> pathspec.PathSpec:
        """
        Load both .gitignore from the repo root and a custom .gptignore for filtering files.
        """
        gitignore_path = os.path.join(repo_root, Settings.GITIGNORE_PATH)
        gptize_ignore_path = os.path.join(repo_root, gptize_ignore)

        patterns = []

        # Load .gitignore from repo root
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as file:
                patterns += file.readlines()
            logging.info(f".gitignore loaded from {gitignore_path}")
        except FileNotFoundError:
            logging.warning(f".gitignore not found at {gitignore_path}, proceeding without it")
        except Exception as e:
            logging.error(f"An unexpected error occurred when loading .gitignore: {e}")

        # Load custom .gptignore
        try:
            with open(gptize_ignore_path, 'r', encoding='utf-8') as file:
                patterns += file.readlines()
            logging.info(f"Custom .gptignore loaded from {gptize_ignore_path}")
        except FileNotFoundError:
            logging.warning(f"Custom .gptignore not found at {gptize_ignore_path}, proceeding without it")
        except Exception as e:
            logging.error(f"An unexpected error occurred when loading custom .gptignore: {e}")

        return pathspec.PathSpec.from_lines('gitwildmatch', patterns)

    def populate_files(self) -> None:
        """
        Populate the project with files, excluding those matched by .gitignore and inside ignored directories.
        """
        for root, dirs, files in os.walk(self.project.root_path):
            dirs[:] = [d for d in dirs if d not in Settings.IGNORED_DIRECTORIES]
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Use the full path relative to the project root directory, not the current working directory
                relative_path = os.path.relpath(file_path, self.project.root_path)

                if self._gitignore.match_file(relative_path):
                    logging.debug(f"File {relative_path} is ignored")
                    continue

                file_obj = File(file_name, file_path)
                try:
                    stat = os.stat(file_path)
                    file_obj.metadata.size = stat.st_size
                    file_obj.metadata.last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    file_obj.metadata.permissions = oct(stat.st_mode)[-3:]
                except Exception as e:
                    logging.error(f"Failed to retrieve metadata for {file_path}: {e}")
                self.load_file_content(file_obj)
                self.project.files.append(file_obj)

    def load_file_content(self, file: File) -> None:
        """
        Load content from a file and detect binary files.
        Warn if the file contains more than 700 lines.
        """
        relative_path = os.path.relpath(file.directory, self.project.root_path)

        try:
            with open(file.directory, 'rb') as f:
                if b'\0' in f.read(1024):
                    file.is_binary = True
                    logging.info(f"Binary file detected: {relative_path}")
                    return None
        except IOError as e:
            logging.error(f"Error reading file {relative_path}: {e}")
            return None

        for encoding in Settings.DEFAULT_ENCODINGS:
            try:
                with open(file.directory, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                    file.content = ''.join(lines)
                    self.calculate_content_size(file)

                    file.stats.line_count = len(lines)
                    file.stats.char_count = len(file.content)

                    if self.encoder:
                        file.stats.token_count = len(self.encoder.encode(file.content))
                    else:
                        file.stats.token_count = 0

                    if len(lines) > Settings.WARN_LINES_COUNT:
                        logging.warning(f"File {relative_path} exceeds 700 lines ({len(lines)} lines).")
                    logging.info(f"Content of {relative_path} loaded with encoding {encoding}")
                    logging.info(f"File {relative_path}: {file.stats.line_count} lines, {file.stats.char_count} characters, {file.stats.token_count} tokens.")
                    return None
            except UnicodeDecodeError:
                continue
            except IOError as e:
                logging.error(f"Error reading file {relative_path}: {e}")
                return None
            except Exception as e:
                logging.error(f"An unexpected error occurred while reading {relative_path}: {e}")
                return None

        logging.error(f"Failed to read {relative_path} in any known encoding")
        return None

    def calculate_content_size(self, file: File) -> None:
        """
        Calculate the size of the content of a file in bytes.
        """
        file.content_size = len(file.content.encode('utf-8'))

    def summarize_stats(self):
        """
        Summarize total tokens, lines, characters, and percentage of context usage.
        """
        total_chars = 0
        for file in self.project.files:
            total_chars += file.stats.char_count
        total_lines = 0
        for file in self.project.files:
            total_lines += file.stats.line_count
        total_tokens = 0
        for file in self.project.files:
            total_tokens += file.stats.token_count
        max_context = Settings.GPT4O_CONTEXT_WINDOW

        files_with_tokens = []
        for f in self.project.files:
            if hasattr(f, 'stats'):
                file_stats = f.stats
                if hasattr(file_stats, 'token_count') and file_stats.token_count > 0:
                    files_with_tokens.append(f)

        files_with_tokens.sort(key=lambda x: x.stats.token_count, reverse=True)
        top_by_token_files = files_with_tokens[:Settings.TOP_TOKEN_FILES_COUNT]

        logging.info(f"Top {Settings.TOP_TOKEN_FILES_COUNT} files by token count:")
        for i, file in enumerate(top_by_token_files, start=1):
            token_percentage = (file.stats.token_count / max_context) * 100 if total_tokens > 0 else 0
            logging.info(
                f"{str(i).zfill(2)}. {file.file_name} - {file.stats.token_count} tokens "
                f"({token_percentage:.2f}% of context), "
                f"{file.stats.line_count} lines, {file.stats.char_count} characters"
            )

        logging.info(f"Total lines: {total_lines}")
        logging.info(f"Total tokens: {total_tokens}")
        logging.info(f"Total characters: {total_chars}")
        context_usage_percent = (total_tokens / max_context) * 100
        logging.info(f"GPT-4o context usage: {context_usage_percent:.2f}%")

        if context_usage_percent > 100:
            logging.error("CONTEXT WINDOW EXCEEDED: Total tokens exceed the maximum allowed by GPT-4o.")
        elif context_usage_percent > 50:
            logging.warning("Context usage exceeds 50%. GPT response quality may degrade.")

    def get_git_status(self):
        """
        Fetch detailed git status for the project directory.
        """
        try:
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                cwd=self.project.root_path,
                check=True
            )
            branch = branch_result.stdout.strip()

            last_commit_result = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%H - %s (%an, %ar)'],
                capture_output=True,
                text=True,
                cwd=self.project.root_path,
                check=True
            )
            last_commit = last_commit_result.stdout.strip()

            status_result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                cwd=self.project.root_path,
                check=True
            )
            status = status_result.stdout.strip()

            return f"Branch: {branch}\nLast Commit: {last_commit}\n\nGit Status:\n{status}"
        except subprocess.CalledProcessError as e:
            logging.warning(f"Git command failed: {e}")
            return "Git information not available."
        except Exception as e:
            logging.warning(f"Could not fetch git details: {e}")
            return "Git information not available."

    def combine_files(self) -> str:
        """
        Combine the content of all files into a single string using OutputBuilder.
        """
        builder = OutputBuilder()
        builder.write_common_header()
        builder.write_project_header(self.project)

        git_status = self.get_git_status()
        if git_status:
            builder.write_git_status(git_status)

        self.summarize_stats()

        for file in self.project.files:
            if file.is_binary:
                continue  # Skip binary files
            builder.write_file_content(file)
            builder.write_separator()

        combined_content = builder.get_content()

        try:
            pyperclip.copy(combined_content)
        except FileNotFoundError:
            logging.warning("Clipboard tool 'clip.exe' not found.")
            try:
                logging.info("Attempting to use 'xclip' as the clipboard tool.")
                pyperclip.set_clipboard("xclip")
                pyperclip.copy(combined_content)
            except Exception:
                logging.warning("Failed to copy content to clipboard even with 'xclip'")

        logging.info("Processing completed.")
        return combined_content
