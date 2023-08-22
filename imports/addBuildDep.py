import os
import re

def process_build_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # Check if "@Nodes" is in the deps section
        if "@Obsidian" in content:
            print(f"Skipped {file_path}, already contains import Obsidian")
            return

        if "@Nodes" in content:
            # Add "@Obsidian" in the next line after "@Nodes"

            new_content = content.replace("@Nodes", "@Nodes,\n        \"@Obsidian\",")
            
            with open(file_path, 'w') as file:
                file.write(new_content)
            
            print(f"Modified {file_path}")  # Log modification
        else:
            print_error(f"No '@Nodes' found in {file_path}")

def modify_build_files(build_file_paths):
    for file_path in build_file_paths:
        process_build_file(file_path)

def print_error(text):
    print("\033[91m" + text + "\033[0m")

if __name__ == "__main__":
    build_file_list_path = "modified_paths.txt"  # Update with the actual path
    with open(build_file_list_path, 'r') as build_list_file:
        build_file_paths = [line.strip() for line in build_list_file.readlines()]

    modify_build_files(build_file_paths)



