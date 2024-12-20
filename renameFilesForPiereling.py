import os
import re
import shutil

#NOTE: Do not use Piereling for conversion of files to folia.xml for the purpose of AutoSearch or HitPaRank/HitPyRank
#You need the rule-based tokenization of UCTO

# Define the forbidden characters
FORBIDDEN_CHARS = r"[\/&|<>`{};']"

def clean_filename(filename):
    # Remove forbidden characters
    filename = re.sub(FORBIDDEN_CHARS, "_", filename)
    
    # Ensure the filename is not longer than 75 characters
    if len(filename) > 75:
        name, ext = os.path.splitext(filename)
        filename = name[:75 - len(ext)] + ext
    
    return filename

def ensure_unique_filename(directory, filename):
    # Check if the filename already exists and make it unique if necessary
    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_name}_{counter}{ext}"
        counter += 1

    return new_filename

def rename_and_move_files_in_directory(source_dir, destination_dir):
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir, topdown=False):  # Start from leaf nodes
        # Rename and move files
        for file_name in files:
            old_path = os.path.join(root, file_name)
            new_file_name = clean_filename(file_name)
            new_file_name = ensure_unique_filename(destination_dir, new_file_name)  # Ensure the new filename is unique
            new_path = os.path.join(destination_dir, new_file_name)

            if old_path != new_path:
                print(f"Moving file: {old_path} -> {new_path}")
                shutil.move(old_path, new_path)

        # Optionally, rename and move directories (if necessary)
        for dir_name in dirs:
            old_path = os.path.join(root, dir_name)
            new_dir_name = clean_filename(dir_name)
            new_path = os.path.join(destination_dir, new_dir_name)

            if old_path != new_path:
                print(f"Moving directory: {old_path} -> {new_path}")
                shutil.move(old_path, new_path)

# Specify the source directory and destination directory
source_directory = r"C:\Users\dutoi\Documents\RAR\EPUB"
destination_directory = r"D:\Theology too big to back up\All Puritan EPUB files renamed"

rename_and_move_files_in_directory(source_directory, destination_directory)

