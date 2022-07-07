import os
import random

from PIL import Image

from sm_photos import dedupe, photos
from sm_photos._constants import DIR_DATA
from sm_photos._utils import log

DIM = 128
WIDTH, HEIGHT = 80, 45


def get_average(pixels):
    n = len(pixels)
    n_black = len(list(filter(lambda pixel: pixel[0] < 32, pixels)))
    return n_black / n


def build_text_collage(base_image_file, photo_file_list):
    base_image = Image.open(base_image_file)
    width, height = base_image.size

    pixels = base_image.load()
    text_collage_image_pixels = {}
    for x in range(width):
        ix = (int)(x * DIM / width)
        for y in range(height):
            iy = (int)(y * DIM / height)

            k = f'{ix},{iy}'
            if k not in text_collage_image_pixels:
                text_collage_image_pixels[k] = []
            text_collage_image_pixels[k].append(pixels[x, y])

    text_collage_image_lights = dict(
        list(
            map(
                lambda item: [
                    item[0],
                    get_average(item[1]) + random.random() * 0.0000001,
                ],
                text_collage_image_pixels.items(),
            )
        )
    )

    text_collage_image_light_values = list(text_collage_image_lights.values())
    light_value_to_rank = dict(
        list(
            map(
                lambda x: [x[1], x[0]],
                enumerate(sorted(text_collage_image_light_values)),
            )
        )
    )
    text_collage_image_ranks = dict(
        list(
            map(
                lambda item: [item[0], light_value_to_rank[item[1]]],
                text_collage_image_lights.items(),
            )
        )
    )

    n_photos = len(photo_file_list)
    photo_image_list = []
    for photo_file in photo_file_list:
        photo_image = Image.open(photo_file).resize(size=(WIDTH, HEIGHT))
        photo_image_list.append(photo_image)

    text_collage_image = Image.new(
        mode="RGBA", size=(DIM * WIDTH, DIM * HEIGHT)
    )
    for k, rank in text_collage_image_ranks.items():
        ix, iy = list(map(lambda x: (int)(x), k.split(',')))
        i_photo = (int)(rank * n_photos / DIM / DIM)
        photo_image = photo_image_list[i_photo]
        text_collage_image.paste(
            photo_image,
            (ix * WIDTH, iy * HEIGHT),
        )

    text_collage_image_file = os.path.join(DIR_DATA, 'text_collage_image.png')
    text_collage_image.save(text_collage_image_file)
    log.info(f'Wrote {text_collage_image_file}')

    for width in [720, 1080, 2160, 4320]:
        height = (int)(width * 9 / 16)
        text_collage_image_resized_file = os.path.join(
            DIR_DATA, f'text_collage_image-{width}x.png'
        )
        text_collage_image.resize((width, height)).save(
            text_collage_image_resized_file
        )
        log.info(f'Wrote {text_collage_image_resized_file}')


if __name__ == '__main__':
    # from sm_photos import filesys
    # filesys.init()
    base_image_file = 'media/text.sketch.png'
    photo_file_list = dedupe.dedupe_photos(photos.get_photo_file_list())
    build_text_collage(base_image_file, photo_file_list)
