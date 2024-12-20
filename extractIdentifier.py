import os
import re

# Define folder path and output subfolder
folder_path = r"D:\Theology too big to back up\All EPUB Puritans Converted to txt\Final TXT files from the Puritan Epubs - Copy"  # Change this to your folder path
output_folder = os.path.join(folder_path, "IDs and problem files")  # Subfolder for output
ID_file = os.path.join(output_folder, "IDs.tsv")  # File for extracted IDs
Lack_file = os.path.join(output_folder, "Files without IDs.tsv")  # File for missing IDs

# Regular expression to match the identifier "A08816" or "N12345" part of the ID
id_pattern = r"https://quod\.lib\.umich\.edu/e/eebo2?/([AN][A-Za-z0-9]+)\."

# Function to extract identifiers and log files without them
def process_files(folder_path):
    extracted_ids = []
    files_without_ids = []

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize or create output files
    if not os.path.exists(ID_file):
        with open(ID_file, 'w', encoding='utf-8') as out_file:
            out_file.write("Identifier\tFile Name\n")

    if not os.path.exists(Lack_file):
        with open(Lack_file, 'w', encoding='utf-8') as lack_file:
            lack_file.write("File Name\n")
    
    # Process each .txt file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

                # Search for the identifier in the document
                match = re.search(id_pattern, text)
                if match:
                    identifier = match.group(1)
                    extracted_ids.append((identifier, filename))
                else:
                    files_without_ids.append(filename)

    # Write extracted IDs to the ID file
    with open(ID_file, 'a', encoding='utf-8') as out_file:
        for identifier, filename in extracted_ids:
            out_file.write(f"{identifier}\t{filename}\n")
    
    # Write filenames without IDs to the Lack file
    with open(Lack_file, 'a', encoding='utf-8') as lack_file:
        for filename in files_without_ids:
            lack_file.write(f"{filename}\n")

# Run the function
process_files(folder_path)
