# CHANGELOG

## [0.3.0] - 2024-09-26
- [Feature] Support for specifying a target directory with repository root .gitignore
  - Now `gptize` can be executed from any directory, while still applying `.gitignore` rules from the root of the repository.
  - Added the `--repo-root` argument to specify the root directory of the repository where the `.gitignore` is located.
  - Example usage: `gptize src/py_module/ --repo-root .` allows processing files in `src/py_module/` while applying `.gitignore` rules from the repository root.
- [Feature] Added support for a custom .gitignore for GPTize
  - Now, you can use an additional custom `.gitignore-gptize` file along with the repository root `.gitignore`.
  - The custom `.gitignore-gptize` can be specified and will be applied in addition to the main `.gitignore`.
  - Example usage: `gptize src/py_module/ --repo-root .` will apply both `.gitignore` and `.gitignore-gptize`.

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
