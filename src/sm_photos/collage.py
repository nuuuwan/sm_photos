import math
import os

from PIL import Image

from sm_photos import dedupe, photos
from sm_photos._constants import DIR_DATA
from sm_photos._utils import log

WIDTH, HEIGHT = 320, 180


def build_collage():
    photo_file_list = dedupe.dedupe_photos(photos.get_photo_file_list())
    n = len(photo_file_list)
    dim = math.ceil(math.sqrt(n))

    image_collage = Image.new(mode="RGBA", size=(dim * WIDTH, dim * HEIGHT))
    for i, photo_file in enumerate(photo_file_list):
        image = Image.open(photo_file)
        image = image.resize(size=(WIDTH, HEIGHT))

        ix = i % dim
        iy = (int)(i / dim)

        image_collage.paste(image, (ix * WIDTH, iy * HEIGHT))
    collage_file = os.path.join(DIR_DATA, 'collage.png')
    image_collage.save(collage_file)
    log.info(f'Wrote {n} images to {collage_file}')

    for f_resize in [2, 4]:
        width, height = (int)(WIDTH / f_resize), (int)(HEIGHT / f_resize)
        image_resized = image_collage.resize((width, height))

        collage_resized_file = os.path.join(
            DIR_DATA, f'collage-{width}x{height}.png'
        )
        image_resized.save(collage_resized_file)
        log.info(f'Wrote images to {collage_resized_file}')


if __name__ == '__main__':
    build_collage()
