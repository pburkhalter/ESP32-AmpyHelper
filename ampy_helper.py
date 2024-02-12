import fnmatch
import os
import subprocess
import re
import shutil


# Configuration
PORT = '/dev/tty.usbserial-210'  # Your board's serial connection (COM port on Windows)
SOURCE_DIR = './build'  # The source directory on your computer
TARGET_DIR = '/'  # The target directory on your MicroPython board
PYTHON_VERSION = "3.11"

EXCLUDE_FILES_FROM_STRIPPING = ['source.py', '*.config.py']
EXCLUDE_FILES_FROM_COPY = ['README.md', 'LICENSE', 'ampy_helper.py', '.gitignore', '._DS_Store']
EXCLUDE_DIRS_FROM_COPY = ['build', '.idea', '.git']

AMPY_CMD = 'ampy --port {} '.format(PORT)  # Base ampy command with port
PATH = os.path.expanduser(f'~/Library/Python/{PYTHON_VERSION}/bin')


def strip_comments_from_py(content):
    # Regular expression to match comments
    pattern = re.compile(r'#.*?$|\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"', re.MULTILINE)
    return re.sub(pattern, '', content)


def should_exclude(filename):
    for pattern in EXCLUDE_FILES_FROM_STRIPPING:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def copy_and_strip_files(src, dest):
    os.makedirs(dest, exist_ok=True)
    for root, dirs, files in os.walk(src, topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS_FROM_COPY]
        files = [f for f in files if
                 f not in EXCLUDE_FILES_FROM_COPY]

        for file in files:
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest, os.path.relpath(root, src), file)
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

            if file.endswith('.py') and not should_exclude(file):
                with open(src_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                stripped_content = strip_comments_from_py(content)
                with open(dest_file_path, 'w', encoding='utf-8') as f:
                    f.write(stripped_content)
            else:
                shutil.copy(src_file_path, dest_file_path)


def run_ampy_command(command, capture_output=False, as_text=False):
    try:
        # Adjust subprocess.run based on whether output capture and text conversion are needed
        if capture_output:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=as_text)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None


def reset_board():
    run_ampy_command(f'{AMPY_CMD} reset')


def clear_device():
    essential_files = {}  # files to keep, if necessary...
    output = run_ampy_command(f'{AMPY_CMD} ls')
    if output:
        items = output.splitlines()

        for item in items:
            item_name = os.path.basename(item)
            if item_name in essential_files:
                print(f"Skipping essential file: {item}")
                continue

            if '.' in item_name:  # Assuming it's a file
                run_ampy_command(f'{AMPY_CMD} rm "{item}"')
            else:  # Assuming it's a directory
                run_ampy_command(f'{AMPY_CMD} rmdir "{item}"')


def upload_files(source_dir, target_dir):
    # Iterate over items in the source directory
    for item in os.listdir(source_dir):
        item_path = os.path.abspath(os.path.join(source_dir, item))
        # It's simpler to just use 'put' for both files and directories without specifying the target path
        cmd = f'{AMPY_CMD} put "{item_path}"'
        print("Uploading:", item)
        run_ampy_command(cmd, capture_output=False, as_text=False)


if __name__ == '__main__':
    os.environ['PATH'] = PATH + os.pathsep + os.environ['PATH']

    print('Building python project...')
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(current_dir, 'build')
        copy_and_strip_files(current_dir, build_dir)
        print('Done building python project.')
    except Exception as e:
        print('Failed building python project...')
        print(e)

    print('Deleting files from board...')
    clear_device()
    print('Done deleting files from board.')

    print('Uploading files to board...')
    upload_files(SOURCE_DIR, TARGET_DIR)
    print('Done uploading files to board.')

    print('Resetting board...')
    reset_board()
    print('Done resetting board.')