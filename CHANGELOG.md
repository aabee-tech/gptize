# CHANGELOG

## [0.5.1] - 2024-12-01
- [Fix] Fixed console summary statistics display

## [0.5.0] - 2024-12-01
- [Feature] Added support for tokenization using `tiktoken`
  - Integrated `tiktoken` for accurate token counting.
  - Introduced new tokenization settings in `Settings` class, including `TOKEN_MODEL_NAME`, `GPT4O_CONTEXT_WINDOW`, and `TOP_TOKEN_FILES_COUNT`.

- [Feature] Git status integration
  - Added functionality to include Git branch, last commit, and file status in the combined output.

- [Feature] Custom `.gptignore` support
  - Implemented a `.gptignore` file to specify additional patterns for file exclusion alongside `.gitignore`.

- [Enhancement] Expanded Python version support
  - Updated GitHub Actions CI to include testing on Python 3.13.

- [Enhancement] Metadata and statistics for processed files
  - File metadata now includes size, last modified timestamp, and permissions.
  - Statistics for line count, character count, and token count added for each file.
  - Enhanced logging to display detailed file statistics and warnings for files exceeding predefined limits.

- [Enhancement] Detailed statistics summary
  - Added summary for total lines, tokens, and characters, along with the percentage of GPT-4o context usage.

- [Enhancement] Clipboard support improvements
  - Enhanced compatibility for clipboard operations, including fallback to `xclip` if default tools are unavailable.

- [Refactor] Cleaned up code and improved maintainability
  - Simplified method parameters and removed redundant comments.
  - Introduced `FileStats` and `FileMetadata` classes for structured storage of file-related data.

- [Fix] Updated requirements
  - Added `tiktoken` and its dependencies to `requirements.in` and `requirements.txt`.

- [Fix] Enhanced error handling
  - Improved error messages and handling for file reading, Git commands, and clipboard operations.

## [0.4.0] - 2024-09-27
- [Feature] Added clipboard copy functionality
  - The combined output file content is now automatically copied to the clipboard using `pyperclip` after the content is generated.
- [Enhancement] Improved output file naming
  - Output file names now include the project name in addition to the date and time. This provides better traceability for output files.
- [Enhancement] Updated `Settings.custom_output_file`
  - The method now accepts the project name as an argument and uses it in the output file name.
- [Enhancement] Reorganized the main logic in `main.py`
  - Fixed a bug where the `gptizer` object was used before initialization.
  - Ensured that output file name generation happens after `gptizer` is properly initialized.

## [0.3.0] - 2024-09-26
- [Feature] Support for specifying a target directory with repository root .gitignore
  - Now `gptize` can be executed from any directory, while still applying `.gitignore` rules from the root of the repository.
  - Added the `--repo-root` argument to specify the root directory of the repository where the `.gitignore` is located.
  - Example usage: `gptize src/py_module/ --repo-root .` allows processing files in `src/py_module/` while applying `.gitignore` rules from the repository root.
- [Feature] Added support for a custom .gitignore for GPTize
  - Now, you can use an additional custom `.gptignore` file along with the repository root `.gitignore`.
  - The custom `.gptignore` can be specified and will be applied in addition to the main `.gitignore`.
  - Example usage: `gptize src/py_module/ --repo-root .` will apply both `.gitignore` and `.gptignore`.

## [0.2.5] - 2023-11-25
- [Modification] Updated File Size and Token Count Checks
  - Modified the `combine_files` method in `gptizer.py` to log a warning instead of raising an error when the total size of the combined content exceeds the `MAX_FILE_SIZE_BYTES_LIMIT` or `MAX_TOKEN_COUNT_LIMIT` defined in `settings.py`.

## [0.2.4] - 2023-11-16
- [Feature] Custom Output File Naming
  - Output files now include the name of the processed file or directory, enhancing traceability and identification.
- [Enhancement] Settings Method for Custom File Names
  - Updated the `Settings` class with a new method to generate output file names incorporating the name of the input file or directory.
- [Modification] Main File Processing Logic
  - Modified `main.py` to adopt the new output file naming scheme.
- [Fix] Minor Bug Fixes and Performance Improvements
  - Addressed various minor bugs and optimized performance.

## [0.2.3] - 2023-11-12
- [Enhancement] Detect binary files and handle errors gracefully
  - Added binary file detection logic in load_file_content method.
  - Improved error handling for file reading.
  - Updated the OutputBuilder to handle binary files properly.
