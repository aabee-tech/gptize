from datetime import datetime


class Settings:
    DEFAULT_ENCODINGS = ['utf-8', 'latin-1', 'cp1252']
    IGNORED_DIRECTORIES = ['.git', '.svn', '__pycache__']
    GITIGNORE_PATH = '.gitignore'
    MAX_FILE_SIZE_BYTES_LIMIT = 512 * 1024 * 1024  # 512 MB
    MAX_TOKEN_COUNT_LIMIT = 2000000  # 2 million tokens

    @staticmethod
    def default_output_file():
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"gptize-output-{current_time}.txt"
