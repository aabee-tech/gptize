# GPTize

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Specifying a Directory](#specifying-a-directory)
  - [Specifying a Single File](#specifying-a-single-file)
  - [Custom Output File](#custom-output-file)
- [Advanced Features](#advanced-features)
  - [Git Integration](#git-integration)
  - [Tokenization](#tokenization)
  - [File Statistics](#file-statistics)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

## Overview

GPTize is a tool for merging project files into a single document, optimized for ChatGPT analysis and training. Created by [Aleksei Svetlov](https://www.linkedin.com/in/svetlovtech/).

## Features

### Core Functionality
- Merge project files into a single document
- Automatic clipboard copy of results
- Custom output file naming

### Git Integration
- Includes branch info, last commit, and file status
- Supports custom `.gptignore` files

### Advanced Analysis
- Token counting using `tiktoken`
- Detailed file statistics (lines, chars, tokens)
- Warnings for large files

## Installation

```bash
pip install gptize
```

## Usage

### Basic Usage
```bash
gptize
```

### Specifying a Directory
```bash
gptize /path/to/directory
```

### Specifying a Single File
```bash
gptize /path/to/file.txt
```

### Custom Output File
```bash
gptize -o custom_output.txt
```

## Advanced Features

### Git Integration
Includes:
- Current branch
- Last commit details
- File status

### Tokenization
- Accurate token counting
- GPT-4 context window analysis
- Top token-consuming files report

### File Statistics
For each file:
- Line count
- Character count
- Token count
- Size and permissions

## FAQ

**Q: How to exclude files?**
A: Use `.gitignore` or create a `.gptignore` file

**Q: What tokenizer is used?**
A: GPTize uses OpenAI's `tiktoken`

**Q: How to contribute?**
A: See [Contributing](#contributing)

## Contributing

We welcome contributions! Please open an issue or pull request on GitHub.

## License

MIT License - See [LICENSE](LICENSE)
