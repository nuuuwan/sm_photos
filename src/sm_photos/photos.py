import os

from sm_photos._constants import DIR_TWTR_DATA

WIDTH, HEIGHT = 80, 45


def get_photo_file_list():
    photo_file_list = []
    for file_only in os.listdir(DIR_TWTR_DATA):
        ext = file_only.split('.')[-1]
        if ext not in ['png', 'jpg']:
            continue
        photo_file_list.append(os.path.join(DIR_TWTR_DATA, file_only))
    photo_file_list = list(reversed(list(sorted(photo_file_list))))
    return photo_file_list
