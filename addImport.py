import os
import re


def process_file(file_path, modified_paths):
    with open(file_path, 'r') as file:
        content = file.read()
        new_import = "import Obsidian"

    if "TUIColor." in content or "TUIGradient." in content:

        # Skip processing if "import Obsidian" is already in the file
        if new_import in content:
            print(f"Skipped {file_path}, already contains import Obsidian")
            return

        existing_imports = re.findall(r'^\s*import\s+.*$', content, re.MULTILINE)

        # Remove any existing "import Obsidian" statements
        existing_imports = [imp.strip() for imp in existing_imports if imp.strip() != new_import]

        existing_imports = [imp for imp in existing_imports if "import class" not in imp]
        existing_imports = [imp for imp in existing_imports if "import struct" not in imp]
        existing_imports = [imp for imp in existing_imports if "@testable import" not in imp]
        existing_imports = [imp for imp in existing_imports if "import enum" not in imp]
        existing_imports = [imp for imp in existing_imports if "import protocol" not in imp]

        # print(f"existing_imports: {existing_imports}")

        # Find the start and end positions of the original import section
        import_start = content.find(existing_imports[0])
        import_end = content.find(existing_imports[-1]) + len(existing_imports[-1])

        # Append the new import and sort alphabetically
        existing_imports.append(new_import)
        sorted_imports = sorted(existing_imports, key=lambda imp: imp.strip())  # Sort without leading/trailing whitespace
        new_import_section = "\n".join(sorted_imports)

        # Reconstruct the content with sorted imports
        new_content = content[:import_start] + new_import_section + content[import_end:]

        with open(file_path, 'w') as file:
            file.write(new_content)


        # Check if the path contains "Tinder/Tinder" and replace it with "Tinder/Tinder/BUILD"
        if "Tinder/Tinder" in file_path:
            modified_path = file_path.split("Tinder/Tinder")[0] + "Tinder/Tinder/BUILD"
        elif "/Source" in file_path:
            modified_path = file_path.split("/Source")[0] + "/Source/BUILD"
        else:
            print_error(f"No /Source in path. handle this path manually:{file_path}")
            return

        modified_paths.add(modified_path)  # Add the modified path to the set

        print(f"Added import in: {file_path}")  # Log match and replacement

def print_error(text):
    print("\033[91m" + text + "\033[0m")


def crawl_directory(directory_path, modified_paths):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".swift"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    content = file.read()
                existing_imports = re.findall(r'^\s*import\s+.*$', content, re.MULTILINE)
                process_file(file_path, modified_paths)

if __name__ == "__main__":
    # target_directory = "/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Modules/Domain/International/"
    target_directory = "/Users/sophialee/Documents/GitHub/tinder_ios/"
    modified_paths = set()  # To store modified paths

    crawl_directory(target_directory, modified_paths)

    # Save modified paths to a text file
    script_directory = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_directory, 'modified_paths.txt'), 'w') as txt_file:
        for path in modified_paths:
            txt_file.write(f"{path}\n")
