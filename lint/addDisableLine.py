import os
import re
import fileinput

def insert_line_before_match(directory, regex_pattern, lint_rule):
    # The full disable comment is constructed from the lint rule
    disable_comment = f'// swiftlint:disable:next {lint_rule}'
    
    # Compile the regex pattern for better performance
    pattern = re.compile(regex_pattern)
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".swift"):  # Filter for Swift files
                file_path = os.path.join(root, file)
                # We will check and modify the file in-place
                previous_line = ""
                with fileinput.FileInput(file_path, inplace=True) as file:
                    for line in file:
                        # Check if the current line matches the regex pattern
                        if pattern.search(line):
                            # Capture leading whitespace
                            leading_whitespace = re.match(r'\s*', line).group(0)
                            # Check if the previous line already contains the disable comment
                            if not previous_line.strip().startswith(disable_comment.strip()):
                                # Print the disable comment line with the same indentation
                                print(f"{leading_whitespace}{disable_comment}", end='\n')
                        # Print the original line
                        print(line, end='')
                        # Update previous_line to the current line for the next iteration
                        previous_line = line

# Example usage
directory = '/Users/sophialee/Documents/GitHub/tinder_ios'
regex_pattern = r'\.(fillColor|strokeColor|shadowColor|borderColor|backgroundColor)\s*=\s*TUIColor\.Semantic\.[a-zA-Z]+\.cgColor'
lint_rule = 'no_semantic_token_on_caLayer'

insert_line_before_match(directory, regex_pattern, lint_rule)