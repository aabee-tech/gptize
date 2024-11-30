
# GPTize

**GPTize** is a tool for merging the contents of project files into a single text document. It is specifically designed to create datasets that can be loaded into ChatGPT for analysis or training. I, [Aleksei Svetlov](https://www.linkedin.com/in/svetlovtech/), created this tool because I was tired of copying file contents and paths to make GPT understand the context of my project. With GPTize, this process is now automated and streamlined.

## Features
- **Clipboard functionality**: The combined content of project files is automatically copied to the clipboard after generation using `pyperclip`.
- **Custom output file naming**: Output file names now include the project name along with the date and time for better traceability.
- **Exception handling for files based on `.gitignore`** (including custom `.gptignore`).
- **Support for specifying a target directory with repository root `.gitignore`**.
- **Support for various encodings when reading files**.
- **Customizable output file naming** based on the input file or directory name.
- **Report generation including all processed files**.
- **Enhanced limit checks for file size and token count**, with warnings logged instead of errors raised when limits are exceeded.
- **Detailed Git integration**: Includes the current branch, last commit, and file status in the generated report.
- **Tokenization support**: Integrated with `tiktoken` for accurate token counting and analysis.
- **File statistics**: Provides detailed information on line count, character count, token count, file size, last modified date, and permissions for every processed file.
- **Warnings for large files**: Alerts if files exceed a predefined line count threshold.

## Installation
To install GPTize, simply use pip:

```bash
pip install gptize
```

This command will install GPTize and all its dependencies. After installation, you can use GPTize from the command line anywhere.

## Usage
To run GPTize, you have several options:

### Basic Usage
Simply invoke GPTize in the command line to process the current directory:

```bash
gptize
```

This will process all files in the current directory and generate a report with a default name like `gptize-output-PROJECT_NAME-YYYYMMDD-HHMMSS.txt`. The content will also be copied to your clipboard.

### Specifying a Directory
To process a specific directory, use:

```bash
gptize /path/to/directory
```

This will process all files in the specified directory and create a report named `gptize-output-PROJECT_NAME-YYYYMMDD-HHMMSS.txt`, and the content will be copied to your clipboard.

### Specifying a Single File
For processing a single file:

```bash
gptize /path/to/file.txt
```

This will process only the specified file and generate a report named `gptize-output-file_name-YYYYMMDD-HHMMSS.txt`, where `file_name` is the name of the input file. The result will also be copied to your clipboard.

### Specifying Repository Root for `.gitignore`
If your `.gitignore` is located in the root of the repository but you want to process files in a different subdirectory, you can use the `--repo-root` option:

```bash
gptize /path/to/directory --repo-root /path/to/repo_root
```

This will apply the `.gitignore` from the repository root to files in the specified directory, and the result will be copied to your clipboard.

### Custom Output File
If you want to specify a custom output file name, use the `-o` or `--output` option:

```bash
gptize -o custom_output.txt
```

This command will override the default naming convention and use `custom_output.txt` as the output file name. The content will still be copied to your clipboard.

### Uploading to ChatGPT
After generating the merged file using GPTize, you can upload it to ChatGPT for improved context understanding. When making requests to ChatGPT, explicitly reference the uploaded file, for instance, using a phrase like `... based on the imported txt file.` This approach significantly enhances the quality of ChatGPT's responses by providing it with specific context.

### Analyzing Statistics
GPTize provides detailed statistics for all processed files:
- Line count, character count, and token count.
- Total project statistics including total lines, tokens, and percentage of GPT-4o context usage.
- Warnings for files exceeding predefined line count thresholds.

### Git Integration
The generated report includes Git details such as:
- Current branch.
- Last commit message, author, and timestamp.
- Untracked or modified files.

## Components
- `gptizer.py`: The main class for file processing.
- `main.py`: The entry point of the application.
- `models.py`: Data models for files and projects.
- `output_builder.py`: Output constructor for report generation.
- `settings.py`: Project settings.

## Author and Maintainer
[Aleksei Svetlov](https://www.linkedin.com/in/svetlovtech/) - Creator and main maintainer.

### Contact Information
- [LinkedIn](https://www.linkedin.com/in/svetlovtech/)
- [Telegram](https://t.me/SvetlovTech)
- Email: svetlovtech@aabee.tech

## License
The project is distributed under the [MIT License](LICENSE).
