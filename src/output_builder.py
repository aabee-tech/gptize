from .models import Project, File


class OutputBuilder:
    def __init__(self):
        self.content = ""

    def write_common_header(self):
        """Write a common header to the content."""
        self.content += "This file was generated using third party tool 'gptize'. For more information, visit https://github.com/svetlovtech/gptize\n"
        self.content += "=" * 40 + "\n"

    def write_project_header(self, project: Project):
        """Write a header for the project."""
        self.content += f"Project Name: {project.name}\n"
        self.content += f"Total Files: {len(project.files)}\n"
        self.content += "=" * 40 + "\n"

    def write_git_status(self, git_status: str):
        """Write git status to the content."""
        self.content += "Git Status:\n"
        self.content += git_status + "\n"
        self.content += "=" * 40 + "\n"

    def write_file_content(self, file: File):
        """Write the content of a file."""
        if file.is_binary:
            self.content += f"File: {file.directory} (Binary file present)\n"
        else:
            self.content += f"File: {file.directory}\n"
            self.content += file.content + "\n"

    def write_separator(self):
        """Write a separator."""
        self.content += "=" * 40 + "\n"

    def get_content(self) -> str:
        """Get the final combined content."""
        return self.content

    def __str__(self):
        """String representation of the OutputBuilder."""
        return f"OutputBuilder with {len(self.content)} characters of content"

    def __repr__(self):
        """Formal string representation of the OutputBuilder."""
        return f"<OutputBuilder with {len(self.content)} characters>"
