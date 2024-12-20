# Define input and output folders
$inputFolder = "D:\Theology too big to back up\All EPUB Puritans Converted to txt\All Puritan EPUB files renamed\Section 1 "
$outputFolder = "D:\Theology too big to back up\All EPUB Puritans Converted to txt\Converted Output 1"  # Final cleaned files

#NOTE: make sure that the output folder is different from the input folder

# Ensure the output folder exists
If (-Not (Test-Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder
}

# Function to clean text content and preserve paragraphs
Function Clean-TextContent {
    param([string[]]$content)

    # Remove inline formatting artifacts (like {.rend-italic})
    $content = $content -replace '\[\s*([^\]]+)\s*\]\{[^\}]*\}', '$1'  # Removes [ ... ]{...} blocks
    $content = $content -replace '\[([^\]]+)\]', '$1'  # Removes [ ... ] (text only in brackets)
    $content = $content -replace "\\'s", "'s"  # Fixes apostrophe encoding artifacts

    # Preserve bullet points and special characters (no changes here for bullet points)
    # Remove other special characters (if needed) except common punctuation
    $content = $content -replace '[^\w\s.,;?!-•]', ''  # Keep bullet points and common punctuation

    # Merge unwanted newlines and extra spaces
    # Remove excessive newlines (make sure at least one newline remains between paragraphs)
    $content = $content -replace "(\r?\n){2,}", "`r`n"  # Keep single newlines between paragraphs
    # Replace newlines within paragraphs with a space to merge the text into a single paragraph
    $content = $content -replace "(\r?\n)(?=\S)", " "  # Merge newlines between words in a paragraph
    $content = $content -replace "\s{2,}", " "  # Replace multiple spaces with a single space

    # Add double newlines between paragraphs (ensure that a paragraph ends with a newline)
    $content = $content -replace "(?<=\S)(\r?\n)(?=\S)", "`r`n`r`n"  # Ensure double newlines between paragraphs

    return $content.Trim()  # Remove leading/trailing spaces
}

# Initialize counter
$fileCounter = 0

# Convert and clean all EPUB files directly to the output folder
Get-ChildItem -Path $inputFolder -Filter *.epub | ForEach-Object {
    $inputFile = $_.FullName
    $outputFile = Join-Path -Path $outputFolder -ChildPath "$($_.BaseName).txt"

    # Convert EPUB to plain text in memory
    $rawContent = pandoc $inputFile -t plain --strip-comments --no-highlight --wrap=none

    # Clean the raw content
    $cleanedContent = Clean-TextContent -content $rawContent

    # Save the cleaned content to the output file
    Set-Content -Path $outputFile -Value $cleanedContent

    # Increment the counter
    $fileCounter++

    # Print message every 100 files processed
    If ($fileCounter % 100 -eq 0) {
        Write-Host "$fileCounter files processed and cleaned..."
    }
}
