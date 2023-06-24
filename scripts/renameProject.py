import os
import sys
import fileinput
import re

def get_app_name():
    cmake_lists_path = 'CMakeLists.txt'
    with open(cmake_lists_path, 'r') as file:
        contents = file.read()

    match = re.search(r'set\(APP_NAME\s+(\S+)\)', contents)
    if match:
        app_name = match.group(1)
        return app_name

    return None

def replace_string_in_file(file_path, old_string, new_string):
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            print(line.replace(old_string, new_string), end='')

def rename_project(new_name):
    # Change string in CMakeLists.txt
    replace_string_in_file('CMakeLists.txt', 'set(APP_NAME some-random-app-name)', f'set(APP_NAME {new_name})')

    # Change string in AndroidManifest.xml
    replace_string_in_file('proj.android/app/AndroidManifest.xml', 'com.organization.random-app-name', new_name)

    # Change string in build.gradle
    replace_string_in_file('proj.android/app/build.gradle', 'applicationId "com.organization.random-app-name"', f'applicationId "com.organization.{new_name}"')

    # Change string in strings.xml
    replace_string_in_file('proj.android/app/res/values/strings.xml', '<string name="app_name">random-app-name</string>', f'<string name="app_name">{new_name}</string>')

    # Change string in settings.gradle
    replace_string_in_file('proj.android/settings.gradle', "include ':random-app-name'", f"include ':{new_name}'")
    replace_string_in_file('proj.android/settings.gradle', "project(':random-app-name').projectDir = new File(settingsDir, 'app')", f"project(':{new_name}').projectDir = new File(settingsDir, 'app')")

    # Change string in Info.plist
    replace_string_in_file('proj.ios_mac/ios/Info.plist', '<string>random-app-name</string>', f'<string>{new_name}</string>')

if __name__ == '__main__':
    app_name = get_app_name()
    if app_name:
        print(f'App name: {app_name}')
    else:
        print('Failed to retrieve the app name from CMakeLists.txt')
    if len(sys.argv) < 2:
        print('Please provide a new name for the project, for example "com.company-name.app-name"')
        sys.exit(1)

    new_name = sys.argv[1]
    rename_project(new_name)