from typing import List


class FileMetadata:
    """Class representing a file metadata in the project."""

    def __init__(self, size=0, last_modified=None, permissions=None):
        self.size = size
        self.last_modified = last_modified
        self.permissions = permissions
        self.lines = 0
        self.tokens = 0


class FileStats:
    """Class to store file statistics."""

    def __init__(self):
        self.line_count: int = 0
        self.char_count: int = 0
        self.token_count: int = 0


class File:
    """Class representing a file in the project."""

    def __init__(self, file_name: str, directory: str):
        self.file_name = file_name
        self.directory = directory
        self.content = ""
        self.content_size = 0
        self.is_binary = False
        self.metadata = FileMetadata()
        self.stats = FileStats()

    def __str__(self):
        return f"File(name={self.file_name}, size={self.metadata.size} bytes, modified={self.metadata.last_modified})"

    def __repr__(self):
        return f"<File '{self.file_name}' at {self.directory}>"


class Project:
    """Class representing the project."""

    def __init__(self, name: str, root_path: str):
        self.name: str = name
        self.files: List[File] = []
        self.root_path: str = root_path

    def __str__(self):
        file_list = ', '.join(file.file_name for file in self.files)
        return f"Project '{self.name}' with files: {file_list}"

    def __repr__(self):
        return f"<Project '{self.name}' with {len(self.files)} files>"
