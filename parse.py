#!/usr/bin/python3
import os
import pprint
import re
import sys

TARGET_REGEX = r"fromHex|UIColor\.[a-z]|UIColor = \."
COMMENT_REGEX = r"^[ ]*(\/\/|\/\*|\*\/)"
LINT_ANNOTATION = "// swiftlint:disable:next ui_color\n"

regex = re.compile(TARGET_REGEX)
exclude_regex = re.compile(COMMENT_REGEX)


def process_file(path):
    # print('Processing {}'.format(path))
    skip_annotated = False
    found_hexcode = False
    indentation = 0
    lines = []
    with open(path, 'r+') as file:

        previousLine = ""
        for line in file:
            if exclude_regex.search(line):
               pass
            elif regex.search(line):
                # print('found {}'.format(line))
                if LINT_ANNOTATION in previousLine:
                    pass
                else:                    
                    found_hexcode = True
                    indentation = len(line) - len(line.lstrip())
                    lines.append(' ' * indentation + LINT_ANNOTATION)

            lines.append(line)
            previousLine = line

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
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Modules/Domain'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Examples/ObsidianTUIKit/Source'
    path = '/Users/sophialee/Documents/GitHub/tinder_ios/'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Tinder/Tinder/Instrumentation/DevTools/AnalyticsViewer/AnalyticsDebugView/'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Modules/Service/PurchaseService/'

    swift_files = parse_directory(path)  
    # pprint.pprint(swift_files)
    pprint.pprint("Completed!")  

if __name__ == '__main__':
    main()
