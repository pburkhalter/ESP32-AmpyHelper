MicroPython Project Deployment Script
=====================================

This script is designed to streamline the workflow of developing and deploying projects to MicroPython boards using `ampy`, the Adafruit MicroPython Tool. Working with `ampy` can be cumbersome, especially when dealing with multiple files and directories. This script aims to simplify that process by automating the building, cleaning, and uploading phases of project development.

Features
--------

-   Automatic Build Directory Preparation: Strips comments from Python files to reduce size, preparing them for upload.
-   Clean Device Storage: Clears all non-essential files and directories from the MicroPython board before uploading new files, ensuring a clean state.
-   Efficient File Upload: Uploads the entire project directory to the MicroPython board, maintaining the directory structure.
-   Board Reset: Performs a soft reset of the MicroPython board after uploading files to ensure changes take effect immediately.

Requirements
------------

-   Python 3.9 or later.
-   `ampy` installed in the Python environment.
-   MicroPython board connected via serial to the development machine.

Configuration
-------------

Before using the script, ensure to configure the following variables according to your setup:

-   `PORT`: Serial port to which the MicroPython board is connected. Example: `/dev/tty.usbserial-210`.
-   `SOURCE_DIR`: The source directory on your computer containing the Python project files. Example: `./build`.
-   `TARGET_DIR`: The target directory on your MicroPython board where files will be uploaded. Normally this would be: `/`.
-   `PYTHON_VERSION`: The Python version used for the `ampy` installation path. Set dynamically to match the executing environment.

Usage
-----

1.  Set Up Your Project: Place your Python project files within the `SOURCE_DIR`.
2.  Configure the Script: Adjust the `PORT`, `SOURCE_DIR`, and `TARGET_DIR` variables as needed.
3.  Run the Script with `python3 ampy_helper.py`. Make sure the Python version matches the one used for installing `ampy`.
4. Check the Console: The script provides detailed output for each step, including file uploads and any errors encountered.

Notes
-----

-   The script is designed to be user-friendly, requiring minimal interaction once configured.
-   It performs a clean deployment by default, removing old files from the board to prevent conflicts.
-   Essential files like `boot.py` and `main.py` could optionally be preserved during the clean process to ensure the board remains operational.

Troubleshooting
---------------

-   Ensure the correct serial port is specified for `PORT`.
-   Verify `ampy` is correctly installed and accessible within the specified Python environment.
-   Check the board's connection if uploads fail or if the board does not reset as expected.