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

def get_package_name():
    manifest_path = 'proj.android/app/AndroidManifest.xml'
    with open(manifest_path, 'r') as file:
        contents = file.read()

    match = re.search(r'package="([^"]+)"', contents)
    if match:
        package_name = match.group(1)
        return package_name

    return None

def extract_app_name(package_name):
    app_name = package_name.split('.')[-1]
    return app_name

def validate_package_name(package_name):
    pattern = r'^[a-z0-9][a-z0-9\-.]*[a-z0-9]$'
    return re.match(pattern, package_name) is not None

def replace_string_in_file(file_path, old_string, new_string):
    print 'Replacing "{}" with "{}" in {}'.format(old_string, new_string, file_path)
    with open(file_path, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace(old_string, new_string)

    with open(file_path, 'w') as file:
        file.write(filedata)

def rename_project(old_app_name, old_package_name, new_app_name, new_package_name):
    # Change string in CMakeLists.txt
    print 'set(APP_NAME {})'.format(old_app_name)
    replace_string_in_file('CMakeLists.txt', 'set(APP_NAME {})'.format(old_app_name), 'set(APP_NAME {})'.format(new_app_name))

    # Change string in AndroidManifest.xml
    replace_string_in_file('proj.android/app/AndroidManifest.xml', old_package_name, new_package_name)

    # Change string in build.gradle
    replace_string_in_file('proj.android/app/build.gradle', 'applicationId "{}"'.format(old_package_name), 'applicationId "{}"'.format(new_package_name))

    # Change string in strings.xml
    replace_string_in_file('proj.android/app/res/values/strings.xml', '<string name="app_name">{}</string>'.format(old_app_name), '<string name="app_name">{}</string>'.format(new_app_name))

    # Change string in settings.gradle
    replace_string_in_file('proj.android/settings.gradle', "include ':{}'".format(old_app_name), "include ':{}'".format(new_app_name))
    replace_string_in_file('proj.android/settings.gradle', "project(':{}').projectDir = new File(settingsDir, 'app')".format(old_app_name), "project(':{}').projectDir = new File(settingsDir, 'app')".format(new_app_name))

    # Change string in Info.plist files
    replace_string_in_file('proj.ios_mac/ios/Info.plist', '<string>{}</string>'.format(old_package_name), '<string>{}</string>'.format(new_package_name))
    replace_string_in_file('proj.ios_mac/mac/Info.plist', '<string>{}</string>'.format(old_package_name), '<string>{}</string>'.format(new_package_name))

if __name__ == '__main__':
    app_name = get_app_name()
    if app_name:
        print 'App name:', app_name
    else:
        print 'Failed to retrieve the app name from CMakeLists.txt'
        sys.exit(1)
    package_name = get_package_name()
    if package_name and validate_package_name(package_name):
        print 'Package name:', package_name
    else:
        print 'Failed to retrieve the package name from proj.android/app/AndroidManifest.xml'
        sys.exit(1)
    if len(sys.argv) < 2:
        print 'Please provide a new name for the project, for example "com.company-name.app-name"'
        sys.exit(1)
    if not validate_package_name(sys.argv[1]):
        print 'The new name is not valid, please provide a name like "com.company-name.app-name"'
        sys.exit(1)

    new_package_name = sys.argv[1]
    print 'New package name:', new_package_name
    new_app_name = extract_app_name(new_package_name)
    if not new_app_name:
        print 'Failed to extract the app name from the package name'
        sys.exit(1)
    print 'New app name:', new_app_name
    rename_project(app_name, package_name, new_app_name, new_package_name)
    sys.exit(0)