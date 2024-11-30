from datetime import datetime
import os


class Settings:
    DEFAULT_ENCODINGS = ['utf-8', 'latin-1', 'cp1252']
    IGNORED_DIRECTORIES = ['.git', '.svn', '__pycache__']
    GITIGNORE_PATH = '.gitignore'
    MAX_FILE_SIZE_BYTES_LIMIT = 512 * 1024 * 1024  # 512 MB
    MAX_TOKEN_COUNT_LIMIT = 2000000  # 2 million tokens
    WARN_LINES_COUNT = 700
    GPT4O_CONTEXT_WINDOW = 128000  # Token context window for GPT-4o
    TOKEN_MODEL_NAME = 'o200k_base'

    @staticmethod
    def default_output_file():
        """Returns the default output file name with the current date and time."""
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"gptize-output-{current_time}.txt"

    @staticmethod
    def custom_output_file(project_name: str, target: str):
        """
        Returns the output file name, including the project name and the current date and time.

        Parameters:
        project_name (str): The name of the project to be included in the file name.
        target (str): The target file or directory path.
        """
        base_name = os.path.basename(target).replace(' ', '_')
        if not base_name or os.path.isdir(target):
            base_name = 'folder' if os.path.isdir(target) else 'file'

        # Use the project name in the output file name if provided
        project_part = project_name.replace(' ', '_') if project_name else base_name

        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"gptize-output-{project_part}-{current_time}.txt"
