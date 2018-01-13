import re
import collections
import os
import sys
import chardet
import json


def load_data(file_path):
    with open(file_path, 'rb') as opened_file:
        data = opened_file.read()
        encoding = chardet.detect(data)
        encoded_data = data.decode(encoding['encoding'])
        json_data = json.loads(encoded_data)
        return json_data['rss']['channel']['items']


def get_most_frequent_words(json_data):
    text_list = list()
    for item in json_data:
        text_list.append(item['description'])
    words_list = re.sub('[\W]', ' ', ' '.join(text_list)).lower().split()
    sorted_words_list = list(filter(lambda x: len(x) > 6, words_list))
    counter = collections.Counter(sorted_words_list)
    words_count = 10
    return counter.most_common(words_count)


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
    except IndexError:
        print('The file path parameter is missing. Please try again.')
    else:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            json_data = load_data(file_path)
            words_list = get_most_frequent_words(json_data)
            print('The top 10 most frequent words:\n')
            for word, count in words_list:
                print('{} : {}'.format(word, count))
        else:
            print("The file doesn't exist!")