# GPTize

**gptize** is a tool for merging the contents of project files into a single text document. It is specifically designed to create datasets that can be loaded into ChatGPT for analysis or training. I, [Aleksey Svetlov](https://www.linkedin.com/in/svetlovtech/), created this tool because I was tired of copying file contents and paths to make GPT understand the context of my project. With gptize, this process is now automated and streamlined.

## Features
- Exception handling for files based on `.gitignore`.
- Support for various encodings when reading files.
- Report generation including all processed files.

## Installation
To install `gptize`, simply use pip:

```bash
pip install gptize
```

This command will install `gptize` and all its dependencies. After installation, you can use `gptize` from the command line anywhere.

## Usage
To run gptize, use the command line:
```bash
gptize
```

If you need additional options:
```bash
gptize [path] [-o output_path] [--debug]
```

- `path`: Path to the project directory (default is the current directory).
- `-o, --output`: Path to the output file (default `gptize-output-[timestamp].txt`).
- `--debug`: Enable debug logging.
- All args are optional.

## Uploading to ChatGPT
After generating the merged file using `gptize`, you can upload it to ChatGPT for improved context understanding. When making requests to ChatGPT, explicitly reference the uploaded file, for instance, using a phrase like `... based on the imported txt file.` `See project file for context` This approach significantly enhances the quality of ChatGPT's responses by providing it with specific context.

## Components
- `gptizer.py`: The main class for file processing.
- `main.py`: The entry point of the application.
- `models.py`: Data models for files and projects.
- `output_builder.py`: Output constructor for report generation.
- `settings.py`: Project settings.

## Author and Maintainer
[Alexey Svetlov](https://www.linkedin.com/in/svetlovtech/) - Creator and main maintainer.

### Contact Information
- [LinkedIn](https://www.linkedin.com/in/svetlovtech/)
- [Telegram](https://t.me/SvetlovTech)
- Email: alexeysvetlov92@gmail.com

## License
The project is distributed under the [MIT License](LICENSE).
