from urllib.parse import urlencode, urlparse
import requests


APP_ID = 6352060


def get_access_token():
    auth_url = 'https://oauth.vk.com/authorize'
    auth_data = {
        'client_id': APP_ID,
        'display': 'page',
        'scope': 'friends',
        'response_type': 'token',
        'v': '5.71'
    }
    response = requests.get(auth_url, params=auth_data)


def get_common_friends(first_user_id, second_user_id):
    params = {
        'source_uid': first_user_id,
        'target_uid': second_user_id,
        'access_token': get_access_token()
    }
    response = requests.get('https://api.vk.com/method/friends.getMutual', params)
    user_id_list = response.json()['response']
    print('\n'.join(f'{str(u_id)}: https://vk.com/id{str(u_id)}' for u_id in user_id_list))