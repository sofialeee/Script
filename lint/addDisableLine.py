import os
import re
import fileinput

def insert_line_before_match(directory, regex_pattern, lint_rule):
    # The basic disable comment format
    disable_base = '// swiftlint:disable:next'

    # Compile the regex pattern for better performance
    pattern = re.compile(regex_pattern)

    # Initialize the match counter
    match_count = 0

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".swift"):  # Filter for Swift files
                file_path = os.path.join(root, file)
                # Modify the file in-place
                previous_line = ""
                disable_line_added = False
                with fileinput.FileInput(file_path, inplace=True) as file:
                    for line in file:
                        # Check if the current line matches the regex pattern
                        if pattern.search(line):
                            leading_whitespace = re.match(r"\s*", line).group()  # Extract leading whitespace
                            # Check if the previous line is a swiftlint comment, and manage it
                            if previous_line.strip().startswith(disable_base):
                                # Parse existing rules from the previous line
                                existing_rules = previous_line.strip().split(disable_base + ': ')[-1].split()
                                if lint_rule in existing_rules:
                                    # If rule is already in the comment, skip adding it
                                    print(previous_line, end='')
                                    disable_line_added = False
                                else:
                                    # Append new rule if not already included
                                    new_comment = f"{previous_line.strip()} {lint_rule}"
                                    print(new_comment)
                                    disable_line_added = True
                            else:
                                # Print new disable comment if no suitable comment exists
                                disable_comment = f'{leading_whitespace}{disable_base} {lint_rule}'
                                print(f"{disable_comment}", end='\n')
                                disable_line_added = True

                            # Count only new disable lines added
                            if disable_line_added:
                                match_count += 1
                        # Print the original line
                        print(line, end='')
                        # Update previous_line to the current line for the next iteration
                        previous_line = line

    # Print the final count of matches
    print(f"Total new disable lines added: {match_count}")

# Example usage
directory = '/Users/sophialee/Documents/GitHub/tinder_ios'
regex_pattern = r'UIBezierPath\.'
lint_rule = 'design_system_iconography'

insert_line_before_match(directory, regex_pattern, lint_rule)
