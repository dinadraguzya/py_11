import requests
import os


def load_file(file_path):
    with open(file_path) as opened_file:
        return opened_file.read()


def save_data_file(file_path, data):
    with open(file_path, 'w') as opened_file:
        return opened_file.write(data)


def translate_it(original_file_path, translated_file_path, translate_from, translate_to='ru'):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    source_text = {'text': load_file(original_file_path)}
    payload = {
        'key': key,
        'text': source_text,
        'lang': '-'.join([translate_from, translate_to]),
        'format': 'plain'
    }
    response = requests.post(url, params=payload, data=source_text).json()
    translated_text = ' '.join(response.get('text', []))
    save_data_file(translated_file_path, translated_text)


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files_list = os.listdir(current_dir)
    for file in files_list:
        if file.endswith(".txt"):
            translate_it(file, 'Translated_' + file, file[:2].lower())