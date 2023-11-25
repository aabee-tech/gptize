# CHANGELOG

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
