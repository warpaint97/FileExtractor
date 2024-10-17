import os, platform
import zipfile
import shutil
import tarfile
from pathlib import Path
import uuid
from py7zr import SevenZipFile

green_tag : str = "\033[32m"
red_tag : str = "\033[31m"
end_tag : str = "\033[0m"

def success_message(message):
    print(f"{green_tag}Error: {message}{end_tag}", end="")

def error_message(message):
    print(f"{red_tag}Success: {message}{end_tag}", end="")

def log_message(message):
    print(message)

import os
import shutil
import zipfile
import tarfile
import uuid
from py7zr import SevenZipFile  # Requires `pip install py7zr`

def log_message(message: str):
    print(message)

def error_message(message: str):
    print(f"Error: {message}")

def success_message(message: str):
    print(f"Success: {message}")

def show_message(message : str):
    print(message)

def extract_file(file_path, extraction_folder):
    """
    Extract files based on their extension type.
    """
    # Handle ZIP files
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_folder)
    # Handle TAR files (.tar, .tar.gz, .tgz, .tar.bz2)
    elif file_path.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
        with tarfile.open(file_path, 'r:*') as tar_ref:
            tar_ref.extractall(extraction_folder)
    # Handle 7z files
    elif file_path.endswith('.7z'):
        with SevenZipFile(file_path, 'r') as z:
            z.extractall(extraction_folder)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

def copy_and_extract_compressed_files(source_directory, target_directory):
    show_message("Processing...")
    log_message("Attempting to copy and extract compressed files.")
    
    try:
        if source_directory == "":
            raise FileNotFoundError(f"A source directory must be specified.")
        if target_directory == "":
            raise FileNotFoundError(f"A target directory must be specified.")

        if not os.path.exists(source_directory):
            raise FileNotFoundError(f"Source directory '{source_directory}' does not exist.")
        if not os.path.exists(target_directory):
            raise FileNotFoundError(f"Target directory '{target_directory}' does not exist.")

        # Step 1: Find all compressed files to process
        compressed_files = [file for file in os.listdir(source_directory) 
                            if file.endswith(('.zip', '.tar', '.tar.gz', '.tgz', '.tar.bz2', '.7z'))]
        
        total_files = len(compressed_files)
        if total_files == 0:
            log_message("No compressed files found to process.")
            return
        
        log_message(f"Found {total_files} compressed file(s) to process.")
        
        # Step 2: Process each compressed file
        for index, file in enumerate(compressed_files, start=1):
            source_file_path = os.path.join(source_directory, file)
            log_message(f"Processing file {index} of {total_files}: {file}")
            
            if source_directory == target_directory:
                extraction_folder = os.path.join(target_directory, file.replace('.zip', '').replace('.7z', '').replace('.tar', '').replace('.gz', '').replace('.bz2', '') + '_' + str(uuid.uuid4()))
                os.makedirs(extraction_folder, exist_ok=True)
                log_message(f"Extracting {source_file_path} to {extraction_folder}")
                
                # Extract the compressed file
                extract_file(source_file_path, extraction_folder)
            else:
                # If source and target directories are different, first copy then extract
                target_file_path = os.path.join(target_directory, file)
                shutil.copy(source_file_path, target_file_path)
                log_message(f"Copied {source_file_path} to {target_file_path}")

                # Extract the copied file
                extract_file(target_file_path, target_directory)
                log_message(f"Extracted {target_file_path}")

                # Delete the copied compressed file after extraction
                os.remove(target_file_path)
                log_message(f"Deleted compressed file: {target_file_path}")

            # Log progress percentage
            progress = (index / total_files) * 100
            log_message(f"Progress: {progress:.2f}% ({index}/{total_files})")
            show_message(f"Extracting compressed files: {index}/{total_files} {progress:.2f}%")
        
        # If everything goes well
        success_message(f"Successfully extracted all compressed files in {source_directory}.")
    
    except FileNotFoundError as fnf_error:
        error_message(fnf_error)
    except PermissionError as perm_error:
        error_message(f"Permission error: {perm_error}")
    except ValueError as value_error:
        error_message(f"Extraction error: {value_error}")
    except Exception as e:
        # Catch any other exceptions
        error_message(f"An unexpected error occurred: {e}")


# Function to search for files with a certain extension recursively and copy them to target directory
def copy_files_to_target(source_directory, target_directory, exts: list):
    extensions_string = ", ".join(exts)
    show_message("Processing...")
    log_message(f"Attempting to copy files by extensions to the target directory.")

    try:
        if source_directory == "":
            raise FileNotFoundError(f"A source directory must be specified.")
        if target_directory == "":
            raise FileNotFoundError(f"A target directory must be specified.")
        if exts is None or len(exts) == 0 or exts[0] == "" or exts[0] == '.':
            raise FileNotFoundError(f"The desired file extensions must be specified.")
        
        if not os.path.exists(source_directory):
            raise FileNotFoundError(f"Source directory '{source_directory}' does not exist.")
        if not os.path.exists(target_directory):
            raise FileNotFoundError(f"Target directory '{target_directory}' does not exist.")
    
        # Step 1: Gather all files with the desired extensions
        matching_files = []
        for root, dirs, files in os.walk(source_directory, topdown=False):
            for file in files:
                if Path(file).suffix in exts:
                    matching_files.append(os.path.join(root, file))

        total_files = len(matching_files)
        if total_files == 0:
            error_message(f"No files of type {extensions_string} were found to copy.")
            return
        
        log_message(f"Found {total_files} matching file(s) to copy.")

        # Step 2: Copy each file and track progress
        for index, found_file in enumerate(matching_files, start=1):
            file_name = os.path.basename(found_file)
            dest_path = os.path.join(target_directory, file_name)

            # Check if the file already exists in the target directory
            if os.path.exists(dest_path):
                # Add a counter to the filename if it already exists
                base, ext = os.path.splitext(file_name)
                counter = 1
                new_dest_path = f"{base}_{counter}{ext}"
                
                while os.path.exists(os.path.join(target_directory, new_dest_path)):
                    counter += 1
                    new_dest_path = f"{base}_{counter}{ext}"
                
                dest_path = os.path.join(target_directory, new_dest_path)

            # Copy the file to the target directory
            shutil.copy(found_file, dest_path)
            log_message(f"Copied: {found_file} to {dest_path}")

            # Log progress as a percentage
            progress = (index / total_files) * 100
            log_message(f"Progress: {progress:.2f}% ({index}/{total_files})")
            show_message(f"Extracting desired files: {index}/{total_files} {progress:.2f}%")

        # If everything goes well
        success_message(f"Successfully extracted all {', '.join(exts)} files from {source_directory} and copied to {target_directory}.")
    
    except FileNotFoundError as fnf_error:
        error_message(fnf_error)
    except PermissionError as perm_error:
        error_message(f"Permission error: {perm_error}")
    except shutil.SameFileError as same_file_error:
        error_message(f"Source and destination represent the same file: {same_file_error}")
    except Exception as e:
        # Catch any other exceptions
        error_message(f"An unexpected error occurred: {e}")

def clear_screen():
    # Check the operating system
    if platform.system() == "Windows":
        os.system("cls")  # Windows
    else:
        os.system("clear")  # Linux and macOS

def dir_prompt(prompt : str = "Enter a directory: "):
    dir : str = ''
    while True:
        dir = input(prompt)
        if os.path.isdir(dir):
            break
        print(f"{red_tag}Could not find {dir}{end_tag}")
        print("Please try again.")
    return dir

def accept_prompt(prompt : str = "Enter input: ", yes_action : callable = None, no_action : callable = None, again_text : str = f"{red_tag}Invalid input{end_tag}\nPlease try again.\n", continue_loop : bool = False):
    while True:
        answer = input(prompt)
        if answer == 'y':
            if (yes_action != None):
                yes_action()
            if continue_loop:
                continue
            break
        elif answer == 'n':
            if no_action != None:
                no_action()
            break
        else:
            print(again_text, end='')

def addExtension(exts, repeat: bool = False):
    extension = input("Add an extension (e.g. \".mp3\"): ")
    exts.append('.' + extension.replace('.', ''))

def extension_prompt(src, trgt, exts):
    addExtension(exts)
    accept_prompt("Add another extension (y/n): ", lambda: addExtension(exts), continue_loop=True, again_text='')
    copy_files_to_target(src, trgt, exts)

def extract_zips_prompt():
    global source_dir
    source_dir = dir_prompt("Source directory: ")
    copy_and_extract_compressed_files(source_dir, source_dir)

def extract_extensions_prompt():
    extensions = []
    global source_dir
    if source_dir == None:
        source_dir = dir_prompt("Source directory: ")
    target_dir = dir_prompt("Target directory: ")
    extension_prompt(source_dir, target_dir, extensions)

# Main program
if __name__ == '__main__':
    clear_screen()
    print("File Extractor")
    source_dir = None
    accept_prompt("Extract all zip files (y/n): ", extract_zips_prompt)
    accept_prompt("Extract files (y/n): ", extract_extensions_prompt)
    input(f"{green_tag}Completed.{end_tag} Press \"Enter\" to exit: ")