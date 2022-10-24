#!/usr/bin/python3
import os
import pprint
import re
import sys

#TARGET_REGEX = r"fromHex|UIColor\.[a-z]|UIColor = \."
TARGET_REGEX = r'\s(UIColor|Color)?\.(white|black|clear)(\.|$)'
UICOLOR_REGEX = r'(UIColor|Color)?\.(white|black|clear)'
COMMENT_REGEX = r"^[ ]*(\/\/|\/\*|\*\/)"
LINT_ANNOTATION = "// swiftlint:disable:next ui_color\n"

regex = re.compile(TARGET_REGEX)
uicolor_regex = re.compile(UICOLOR_REGEX)
exclude_regex = re.compile(COMMENT_REGEX)

dict = {
    "black"   :".black",
    "white"   :".white",
    "clear"   :".transparent",
}

matchCount = 0 
dictMatchCount = 0
basePath = "/Users/sophialee/Documents/GitHub/tinder_ios"
exclude_paths = [
"/Projects/Examples/",
"/Projects/LocalPods/",
# "/Projects/Modules/Service/",
# "/Projects/Tinder/",
# "/Projects/Modules/Domain/Boost/",
# "/Projects/Modules/Domain/Paywall/",
# "/Projects/Modules/Domain/Revenue/",
# "/Projects/Modules/Domain/Collectibles/",
# "/Projects/Modules/Service/PurchaseService/",
# "/Projects/Modules/Domain/Dionysus/",
# "/Projects/Modules/Domain/Onboarding/",
# "/Projects/Modules/Domain/Referral/",
# "/Projects/Modules/Domain/International/"
]


def process_file(path):
    global matchCount

    # print('Processing {}'.format(path))
    skip_annotated = False
    indentation = 0
    lines = []
    found_token = False
    with open(path, 'r+') as file:

        for line in file:
            has_hex = regex.search(line)
            has_color = uicolor_regex.search(line)
            if has_hex and has_color:
                matchCount += 1
                print('match regex: {}'.format(has_color))
                token = getNewLine(has_color.group(2),line)

                if token:
                    found_token = True
                    previousLine = lines[-1]
                    if LINT_ANNOTATION in previousLine:
                        # remove the lint comment
                        lines.pop()

                    print('---ori line:{}'.format(line))
                    newCode = 'TUI.shared.currentColor({})'.format(token)

                    new_line = uicolor_regex.sub(newCode, line)
                    print('===new line:{}'.format(new_line))
                    lines.append(new_line)
                    continue

            lines.append(line)


        # Only rewrite if hexcode is found and there's a token match
        if found_token:
            file.seek(0)
            file.writelines(lines)
            file.truncate()

def getNewLine(oldHex,line):
    global dictMatchCount
    print('here:{}'.format(oldHex))
    cleanedHex = oldHex

    val = dict.get(cleanedHex)
    if val:
        dictMatchCount = dictMatchCount + 1
        print('found value in dict!{}'.format(val))
        return val
    return None

def should_exclude(path):
    for list in exclude_paths:
        if list in path:
            return True
    return False

def parse_directory(path, recursive=True):
    # print('Parsing {}'.format(path))

    result = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if should_exclude(file_path):
                continue

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

# /Projects/Modules/Domain/Profile/ @TinderApp/seal-team-ios
# /Projects/Modules/Domain/ProfileDetail/ @TinderApp/seal-team-ios
# /Projects/Modules/Domain/ProfileElements/ @TinderApp/seal-team-ios
# /Projects/Modules/Domain/ContentCreator/ @TinderApp/seal-team-ios
# /Projects/Tinder/Tinder/*EditActivity.swift @TinderApp/seal-team-ios
# /Projects/Tinder/Tinder/EditProfileViewController.swift @TinderApp/seal-team-ios

    path = '/Users/sophialee/Documents/GitHub/tinder_ios/'

    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Examples/ObsidianTUIKit/Source'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Tinder/Tinder/Instrumentation/DevTools/AnalyticsViewer/AnalyticsDebugView/'
    # path = '/Users/sophialee/Documents/GitHub/tinder_ios/Projects/Modules/Service/TinderKit/Source/TUI/'

    swift_files = parse_directory(path)  
    print("Completed! token count/total Hex count:{}/{}".format(dictMatchCount, matchCount)) 

if __name__ == '__main__':
    main()
