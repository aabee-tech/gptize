from typing import List


class File:
    """Class representing a file in the project."""

    def __init__(self, file_name: str, directory: str):
        self.file_name = file_name
        self.directory = directory
        self.content = ""
        self.content_size = 0
        self.is_binary = False
        self.size = 0
        self.last_modified = None
        self.permissions = None

    def __str__(self):
        return f"File(name={self.file_name}, size={self.size} bytes, modified={self.last_modified})"

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
