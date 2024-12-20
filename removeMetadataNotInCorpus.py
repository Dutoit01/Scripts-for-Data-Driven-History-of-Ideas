import os

# Define paths
valid_ids_file = r"D:\Theology too big to back up\All EPUB Puritans Converted to txt\Final TXT files from the Puritan Epubs - Copy\IDs and problem files\IDs.tsv"  # Path to the file with valid IDs
metadata_folder = r"D:\Theology too big to back up\Early-Print Metadata\epmetadata-master\header"  # Path to the folder containing metadata files
unmatched_ids_file = os.path.join(metadata_folder, "unmatched_ids.tsv")  # Output file for unmatched IDs

# Function to process metadata files
def clean_metadata_folder(valid_ids_file, metadata_folder, unmatched_ids_file):
    # Load valid IDs into a set for fast lookup
    with open(valid_ids_file, 'r', encoding='utf-8') as f:
        valid_ids = {line.strip() for line in f if line.strip() and not line.startswith("Identifier")}

    # Initialize a set to track matched IDs
    matched_ids = set()

    # Iterate through metadata files
    for filename in os.listdir(metadata_folder):
        if filename.endswith("_header.xml"):
            # Extract the ID from the filename
            file_id = filename.split("_")[0]  # Get the part before '_header.xml'

            if file_id in valid_ids:
                matched_ids.add(file_id)  # Mark the ID as matched
            else:
                # Delete the file if the ID is not valid
                os.remove(os.path.join(metadata_folder, filename))

    # Find unmatched IDs (valid IDs not in metadata folder)
    unmatched_ids = valid_ids - matched_ids

    # Write unmatched IDs to a file
    with open(unmatched_ids_file, 'w', encoding='utf-8') as out_file:
        out_file.write("Unmatched Identifier\n")
        for id in sorted(unmatched_ids):  # Sorting for easier readability
            out_file.write(f"{id}\n")

# Run the function
clean_metadata_folder(valid_ids_file, metadata_folder, unmatched_ids_file)
