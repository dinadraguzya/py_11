import requests
import json
import sys
import os


def get_request_parameters(file_path):
    with open(file_path) as opened_file:
        data = opened_file.read()
        return json.loads(data)


def get_user_friends_list(params):
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return response.json()['response']


def get_user_groups_list(params):
    response = requests.get('https://api.vk.com/method/groups.get', params)
    return response.json()['response']


def find_unique_groups(user_groups_list, user_friend_list, params):
    all_friend_groups = list()
    for friend in user_friend_list:
        try:
            params['user_id'] = friend
            friend_groups_list = requests.get('https://api.vk.com/method/groups.get', params).json()['response']
            print('-', end=' ')
            sys.stdout.flush()
            all_friend_groups += friend_groups_list
        except KeyError:
            continue
    unique_groups_list = list(set(user_groups_list) - set(all_friend_groups))
    return unique_groups_list


def get_formatted_groups(groups_list, params):
    params['fields'] = 'members_count'
    required_keys = ['gid', 'name', 'members_count']
    json_group_list = list()
    for group in groups_list:
        params['group_id'] = group
        group_info = requests.get('https://api.vk.com/method/groups.getById', params).json()['response']
        print('.', end=' ')
        sys.stdout.flush()
        json_group_list += group_info
    for item in json_group_list:
        for key in list(item):
            if key not in required_keys:
                del item[key]
    return json_group_list


def save_data_into_file(data, file_path):
    with open(file_path, 'w', encoding='utf8') as opened_file:
        json.dump(data, opened_file, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == '__main__':
    try:
        params_file_path = sys.argv[1]
    except IndexError:
        print('The path to parameters file is missing. Please try again.')
    else:
        if os.path.exists(params_file_path) and os.path.isfile(params_file_path):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            result_file_path = os.path.join(current_dir, 'unique_groups.json')
            request_params = get_request_parameters(params_file_path)
            friend_list = get_user_friends_list(request_params)
            group_list = get_user_groups_list(request_params)
            print('Extracting user\'s groups. Please wait.')
            unique_groups = find_unique_groups(group_list, friend_list, request_params)
            print('\nCreating a user\'s group list. Please wait.')
            formatted_groups_info = get_formatted_groups(unique_groups, request_params)
            save_data_into_file(formatted_groups_info, result_file_path)
            print('\nThe execution is finished. Please find a file with the '
                    f'list of unique user\'s groups at {result_file_path}')
        else:
            print("The file doesn't exist!")