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

    def process_directory(self, root_path: str):
        """
        Processes all the files within a given directory. This method initializes
        the Project object for the specified directory, loads the .gitignore patterns,
        and populates the project with files that are not ignored by .gitignore.

        The method traverses through the directory recursively and adds all relevant
        files to the project's file list, ensuring that binary files and files
        specified in .gitignore are not included.

        Parameters:
        root_path (str): The path to the root of the directory to be processed.

        Raises:
        FileNotFoundError: If the specified directory does not exist.
        Exception: For any other issues encountered during the directory processing.
        """
        project_name = os.path.basename(root_path)
        self._project = Project(project_name, root_path)
        self._gitignore = self.load_gitignore(root_path)
        self.populate_files()

    def process_file(self, file_path: str):
        """
        Processes a single file. This method creates a Project object for the file,
        treating the file as an individual project. It bypasses .gitignore processing,
        as it is assumed that the specific file is intentionally selected for processing.

        The method creates a File object for the specified file, reads its content,
        and adds it to the project's file list. It handles binary and text files
        accordingly.

        Parameters:
        file_path (str): The path to the file to be processed. This includes both
        the directory path and file name.

        Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an issue reading the file.
        Exception: For any other unexpected issues encountered during file processing.
        """
        root_path, file_name = os.path.split(file_path)
        project_name = os.path.basename(root_path) if root_path else 'SingleFileProject'
        self._project = Project(project_name, root_path or '.')
        self._gitignore = pathspec.PathSpec.from_lines('gitwildmatch', [])

        file_obj = File(file_name, file_path)
        self.load_file_content(file_obj)
        self._project.files.append(file_obj)

    @property
    def project(self) -> Project:
        """Property to access the project object."""
        return self._project

    def load_gitignore(self, root_path: str) -> pathspec.PathSpec:
        """Load .gitignore patterns for filtering files."""
        gitignore_path = os.path.join(root_path, Settings.GITIGNORE_PATH)
        try:
            with open(gitignore_path, 'r') as file:
                gitignore = pathspec.PathSpec.from_lines('gitwildmatch', file)
            logging.info(".gitignore loaded")
            return gitignore
        except FileNotFoundError:
            logging.warning(
                ".gitignore not found, all files will be processed")
            return pathspec.PathSpec.from_lines('gitwildmatch', [])
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def populate_files(self) -> None:
        """Populate the project with files, excluding those matched by .gitignore and inside ignored directories."""
        for root, dirs, files in os.walk(self.project.root_path):
            dirs[:] = [d for d in dirs if d not in Settings.IGNORED_DIRECTORIES]
            for file_name in files:
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(
                    file_path, self.project.root_path)

                if self._gitignore.match_file(relative_path):
                    logging.debug(f"File {relative_path} is ignored")
                    continue

                file_obj = File(file_name, relative_path)
                self.load_file_content(file_obj)
                self.project.files.append(file_obj)

    def load_file_content(self, file: File) -> None:
        try:
            with open(file.directory, 'rb') as f:
                if b'\0' in f.read(1024):
                    file.is_binary = True
                    logging.info(f"Binary file detected: {file.file_name}")
                    return
        except IOError as e:
            logging.error(f"Error reading file {file.directory}: {e}")
            return

        for encoding in Settings.DEFAULT_ENCODINGS:
            try:
                with open(file.directory, 'r', encoding=encoding) as f:
                    file.content = f.read()
                    self.calculate_content_size(file)
                    logging.info(
                        f"Content of {file.file_name} loaded with encoding {encoding}")
                    break
            except UnicodeDecodeError:
                continue
            except IOError as e:
                logging.error(f"Error reading file {file.directory}: {e}")
                break
            except Exception as e:
                logging.error(
                    f"An unexpected error occurred while reading {file.file_name}: {e}")
                break
        else:
            logging.error(
                f"Failed to read {file.file_name} in any known encoding")

    def calculate_content_size(self, file: File) -> None:
        """Calculate the size of the content of a file in bytes."""
        file.content_size = len(file.content.encode('utf-8'))

    def combine_files(self) -> str:
        """Combine the content of all files into a single string using OutputBuilder."""
        builder = OutputBuilder()
        builder.write_common_header()
        builder.write_project_header(self.project)

        for file in self.project.files:
            builder.write_file_content(file)
            builder.write_separator()

        return builder.get_content()
