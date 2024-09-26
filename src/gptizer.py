import logging
import os
import pathspec
from .models import File, Project
from .settings import Settings
from .output_builder import OutputBuilder


class GPTizer:
    def __init__(self):
        self._project = None
        self._gitignore = None

    def process_directory(self, target_path: str, repo_root: str, gptize_ignore: str):
        """
        Processes all the files within a given directory. This method initializes
        the Project object for the specified directory, loads the .gitignore patterns
        from the repository root, and populates the project with files that are not
        ignored by .gitignore.

        Parameters:
        target_path (str): The path to the directory that should be processed.
        repo_root (str): The root path of the repository where the .gitignore is located.
        gptize_ignore (str): Path to the second .gitignore file for gptize.

        Raises:
        FileNotFoundError: If the specified directory does not exist.
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

        Parameters:
        file_path (str): The path to the file to be processed.
        repo_root (str): The root path of the repository where the .gitignore is located.
        gptize_ignore (str): Path to the second .gitignore file for gptize.
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
        """Property to access the project object."""
        if self._project is None:
            logging.error("Project has not been initialized.")
            raise AttributeError("Project has not been initialized.")
        return self._project

    def load_gitignore(self, repo_root: str, gptize_ignore: str) -> pathspec.PathSpec:
        """Load both .gitignore from the repo root and a custom .gitignore-gptize for filtering files."""
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

        # Load custom .gitignore-gptize
        try:
            with open(gptize_ignore_path, 'r', encoding='utf-8') as file:
                patterns += file.readlines()
            logging.info(f"Custom .gitignore-gptize loaded from {gptize_ignore_path}")
        except FileNotFoundError:
            logging.warning(f"Custom .gitignore-gptize not found at {gptize_ignore_path}, proceeding without it")
        except Exception as e:
            logging.error(f"An unexpected error occurred when loading custom .gitignore-gptize: {e}")

        # Return the combined pathspec
        return pathspec.PathSpec.from_lines('gitwildmatch', patterns)

    def populate_files(self) -> None:
        """Populate the project with files, excluding those matched by .gitignore and inside ignored directories."""
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
                self.load_file_content(file_obj)
                self.project.files.append(file_obj)

    def load_file_content(self, file: File) -> None:
        """Load content from a file and detect binary files."""
        try:
            with open(file.directory, 'rb') as f:
                if b'\0' in f.read(1024):
                    file.is_binary = True
                    logging.info(f"Binary file detected: {file.file_name}")
                    return None
        except IOError as e:
            logging.error(f"Error reading file {file.directory}: {e}")
            return None

        for encoding in Settings.DEFAULT_ENCODINGS:
            try:
                with open(file.directory, 'r', encoding=encoding) as f:
                    file.content = f.read()
                    self.calculate_content_size(file)
                    logging.info(f"Content of {file.file_name} loaded with encoding {encoding}")
                    return None
            except UnicodeDecodeError:
                continue
            except IOError as e:
                logging.error(f"Error reading file {file.directory}: {e}")
                return None
            except Exception as e:
                logging.error(f"An unexpected error occurred while reading {file.file_name}: {e}")
                return None

        logging.error(f"Failed to read {file.file_name} in any known encoding")
        return None

    def calculate_content_size(self, file: File) -> None:
        """Calculate the size of the content of a file in bytes."""
        file.content_size = len(file.content.encode('utf-8'))

    def combine_files(self) -> str:
        """Combine the content of all files into a single string using OutputBuilder."""
        builder = OutputBuilder()
        builder.write_common_header()
        builder.write_project_header(self.project)

        total_size = 0
        total_tokens = 0

        for file in self.project.files:
            if file.is_binary:
                continue  # Skip binary files

            file_size = len(file.content.encode('utf-8'))
            file_tokens = len(file.content.split())  # Simple token count based on whitespace

            total_size += file_size
            total_tokens += file_tokens

            builder.write_file_content(file)
            builder.write_separator()

        return builder.get_content()
