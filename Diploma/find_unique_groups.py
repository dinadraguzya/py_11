import requests
import json
import sys
import os


def make_request(method):
    def wrapper(*args, **kwargs):
        while True:
            try:
                result = method(*args, **kwargs)
                return result['response']
            except KeyError:
                if result['error']['error_code'] == 7 or result['error']['error_code'] == 18:
                    return []
                else:
                    continue
    return wrapper


class VkApi:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.73'):
        self.token = token
        self.version = version

    @make_request
    def get_friends(self, user_id):
        params = {
            'user_id': user_id,
            'access_token': self.token,
            'version': self.version
        }
        return requests.get(self.base_url + 'friends.get', params).json()

    @make_request
    def get_groups(self, user_id):
        params = {
            'user_id': user_id,
            'access_token': self.token,
            'version': self.version
        }
        return requests.get(self.base_url + 'groups.get', params).json()

    @make_request
    def get_group_info(self, group_id):
        params = {
            'group_id': group_id,
            'access_token': self.token,
            'fields': 'members_count',
            'version': self.version
        }
        return requests.get(self.base_url + 'groups.getById', params).json()


def get_request_parameters(file_path):
    with open(file_path) as opened_file:
        data = opened_file.read()
        return json.loads(data)


def get_user_friends_list(api, user_id):
    return api.get_friends(user_id)


def get_user_groups_list(api, user_id):
    return api.get_groups(user_id)


def find_unique_groups(api, user_groups_list, user_friend_list):
    all_friend_groups = list()
    for friend in user_friend_list:
        friend_groups_list = api.get_groups(friend)
        print('-', end=' ')
        sys.stdout.flush()
        all_friend_groups += friend_groups_list
    unique_groups_list = list(set(user_groups_list) - set(all_friend_groups))
    return unique_groups_list


def get_formatted_groups(api, groups_list):
    json_group_list = list()
    for group in groups_list:
        json_group = dict()
        group_info = api.get_group_info(group)
        print('.', end=' ')
        sys.stdout.flush()
        json_group['name'] = group_info[0]['name']
        json_group['gid'] = group_info[0]['gid']
        json_group['members_count'] = group_info[0]['members_count']
        json_group_list.append(json_group)
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
            vk_api = VkApi(request_params['access_token'], request_params['version'])
            friend_list = get_user_friends_list(vk_api, request_params['user_id'])
            group_list = get_user_groups_list(vk_api, request_params['user_id'])
            print("Extracting user's groups. Please wait.")
            unique_groups = find_unique_groups(vk_api, group_list, friend_list)
            print("\nCreating a user's group list. Please wait.")
            formatted_groups_info = get_formatted_groups(vk_api, unique_groups)
            save_data_into_file(formatted_groups_info, result_file_path)
            print('\nThe execution is finished. Please find a file with the '
                    f"list of unique user's groups at {result_file_path}")
        else:
            print("The file doesn't exist!")