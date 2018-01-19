import os
import subprocess


def create_result_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dir_name = 'Result'
    result_dir = os.path.join(current_dir, dir_name)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    return result_dir


def resize_images(source_dir, result_dir):
    images_list = os.listdir(source_dir)
    for image in images_list:
        subprocess.run(['sips', '--resampleWidth', '200', '--out', os.path.join(result_dir, 'UPD_' + image),
                        os.path.join(source_dir, image)])


if __name__ == '__main__':
    source_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Source')
    result_directory = create_result_dir()
    resize_images(source_directory, result_directory)