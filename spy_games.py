import os
import sys
import time
import vk


USER_ID = 5030613
ACCESS_TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'
VERSION = '5.73'


def get_authorized(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session)


def get_user_friends_list(user_id, api):
    response = api.friends.get(user_id=user_id, v=VERSION)
    return response['items']


def get_user_groups_list(user_id, api):
    response = api.groups.get(user_id=user_id, count=1000, v=VERSION)
    return response['items']


def find_unique_groups(user_groups_list, user_friend_list, api):
    for friend in user_friend_list:
        try:
            friend_groups_list = api.groups.get(user_id=friend, count=1000, v=VERSION)['items']
            print('-', end=' ')
            sys.stdout.flush()
            unique_groups_list = list(set(user_groups_list) - set(friend_groups_list))
            time.sleep(0.4)
        except vk.exceptions.VkAPIError:
            continue
    return unique_groups_list


def get_formatted_groups(groups_list, api):
    json_group_list = list()
    for group in groups_list:
        json_group = dict()
        group_info = api.groups.getById(group_id=group, fields='members_count', v=VERSION)
        print('.', end=' ')
        sys.stdout.flush()
        json_group['name'] = group_info[0]['name']
        json_group['gid'] = group_info[0]['id']
        json_group['members_count'] = group_info[0]['members_count']
        json_group_list.append(json_group)
        time.sleep(0.4)
    return json_group_list


def save_data_into_file(data, file_path):
    with open(file_path, 'w') as opened_file:
        return opened_file.write(str(data))


if __name__ == '__main__':
    vk_api = get_authorized(ACCESS_TOKEN)
    friends_list = get_user_friends_list(USER_ID, vk_api)
    groups_list = get_user_groups_list(USER_ID, vk_api)
    print('Extracting user\'s groups. Please wait.')
    unique_groups = find_unique_groups(groups_list, friends_list, vk_api)
    print('\nCreating a user\'s group list. Please wait.')
    formatted_groups_info = get_formatted_groups(unique_groups, vk_api)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'unique_groups.json')
    save_data_into_file(formatted_groups_info, file_path)
    print(f'The execution is finished. Please find a file with the list of unique user\'s groups at {file_path}')


