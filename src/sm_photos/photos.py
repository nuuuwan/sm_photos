import math
import os

from PIL import Image

from sm_photos._constants import DIR_TWTR_DATA
from sm_photos._utils import log

WIDTH, HEIGHT = 80, 45


def get_photo_file_list():
    photo_file_list = []
    for file_only in os.listdir(DIR_TWTR_DATA):
        ext = file_only.split('.')[-1]
        if ext not in ['png', 'jpg']:
            continue
        photo_file_list.append(os.path.join(DIR_TWTR_DATA, file_only))
    return photo_file_list


def build_collage():
    photo_file_list = get_photo_file_list()
    n = len(photo_file_list)
    dim = math.ceil(math.sqrt(n))

    image_collage = Image.new(mode="RGBA", size=(dim * WIDTH, dim * HEIGHT))
    for i, photo_file in enumerate(photo_file_list):
        image = Image.open(photo_file)
        image = image.resize(size=(WIDTH, HEIGHT))

        ix = i % dim
        iy = (int)(i / dim)

        image_collage.paste(image, (ix * WIDTH, iy * HEIGHT))
    collage_file = os.path.join(DIR_TWTR_DATA, 'collage.png')
    image_collage.save(collage_file)

    log.info(f'Wrote {n} images to {collage_file}')


if __name__ == '__main__':
    build_collage()
