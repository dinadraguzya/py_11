import os
import re


def find_files_by_text(target_dir, files_list, text):
    search_result = list()
    file_match_count = 0
    for file in files_list:
        if file.endswith(".sql"):
            with open(os.path.join(target_dir, file)) as opened_file:
                data = opened_file.read()
                if re.search(text, data, re.IGNORECASE):
                    search_result.append(file)
                    file_match_count += 1
                    print(file)
    print('Total count:', file_match_count)
    return search_result


if __name__ == '__main__':
    migrations = 'Migrations'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    search_dir = os.path.join(current_dir, migrations)
    files_list = os.listdir(search_dir)
    while True:
        search_string = input('Enter a search string: ')
        files_list = find_files_by_text(search_dir, files_list, search_string)