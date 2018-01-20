import os
import re

dir_name = 'Migrations'


def find_files_by_text(files_list, text):
    search_result = list()
    file_match_count = 0
    for file in files_list:
        if file.endswith(".sql"):
            with open(os.path.join(dir_name, file)) as opened_file:
                data = opened_file.read()
                if re.search(text, data, re.IGNORECASE):
                    search_result.append(file)
                    file_match_count += 1
                    print(file)
    print('Total count:', file_match_count)
    return search_result


def recursive_search(files):
    search_string = input('Enter a search string: ')
    files_list = find_files_by_text(files, search_string)
    if files_list:
        recursive_search(files_list)


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    search_dir = os.path.join(current_dir, dir_name)
    files_list = os.listdir(search_dir)
    recursive_search(files_list)