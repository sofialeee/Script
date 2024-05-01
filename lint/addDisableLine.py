import os
import re
import fileinput

def insert_line_before_match(directory, regex_pattern, line_to_insert):
    # Compile the regex pattern for better performance
    pattern = re.compile(regex_pattern)
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".swift"):  # Filter for Swift files
                file_path = os.path.join(root, file)
                # We will check and modify the file in-place
                with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
                    for line in file:
                        # Check if the current line matches the regex pattern
                        if pattern.search(line):
                            # If it matches, print the inserted line first
                            print(line_to_insert, end='\n')
                        # Print the original line
                        print(line, end='')

# Example usage
directory = '/Users/sophialee/Documents/GitHub/tinder_ios'
regex_pattern = r'\.(fillColor|strokeColor|shadowColor|borderColor|backgroundColor)\s*=\s*TUIColor\.Semantic\.[a-zA-Z]+\.cgColor'
line_to_insert = '// swiftlint:disable:next no_semantic_token_on_caLayer'

insert_line_before_match(directory, regex_pattern, line_to_insert)
