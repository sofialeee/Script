#!/usr/bin/python3
import os
import pprint
import re
import sys

REGEX_PATTERN = r"UIColor = (\.|{)|fromHex"  #r".*UIColor = \..*"
LINT_ANNOTATION = "// swiftlint:disable:next ui_color\n"

regex = re.compile(REGEX_PATTERN)


def process_file(path):
    # print('Processing {}'.format(path))
    skip_annotated = False
    found_hexcode = False
    indentation = 0
    lines = []
    with open(path, 'r+') as file:
        for line in file:
            if skip_annotated:
                # Skip linter annotated line
                skip_annotated = False
                lines.append(line)
                continue
            else:
                if LINT_ANNOTATION in line:
                    skip_annotated = True
                if regex.search(line):
                    # print('found {}'.format(line))
                    found_hexcode = True
                    indentation = len(line) - len(line.lstrip())
                    lines.append(' ' * indentation + LINT_ANNOTATION)
                lines.append(line)

        # Only rewrite if hexcode is found, i.e. lint annotation needed
        if found_hexcode:
            file.seek(0)
            file.writelines(lines)
            file.truncate()


def parse_directory(path, recursive=True):
    # print('Parsing {}'.format(path))

    result = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file)[-1] == '.swift':
                process_file(file_path)
                result.add(file_path)

        if recursive:
            # Recursively walk directories
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.path.islink(dir_path):
                    result.union(parse_directory(dir_path))
                # else:
                #     print("{} is a sym link".format(dir_path))

    return result
        
def main():

    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Modules/Domain/DomainReusable/Source/Descriptors/DescriptorView'
    path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Modules/Domain'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Examples/ObsidianTUIKit/Source'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Examples'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios'

    # path = argv[1]
    swift_files = parse_directory(path)  
    # pprint.pprint(swift_files)
    pprint.pprint("Completed!")  

if __name__ == '__main__':
    main()
