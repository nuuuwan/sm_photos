import argparse
import os

from PIL import Image, ImageDraw, ImageFont

from sm_photos._constants import DIR_DATA
from sm_photos._utils import log

WIDTH, HEIGHT = 640, 360


def generate(text, font_size):
    font = ImageFont.truetype(
        os.path.join(os.environ['DIR_FONTS'], 'Menlo.ttc'), font_size
    )
    image = Image.new(mode="RGBA", size=(WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.text(
        (WIDTH / 2, HEIGHT / 2),
        text,
        anchor='mm',
        font=font,
        fill="black",
        stroke_fill="black",
        stroke_width=4,
    )

    text_id = text.replace(' ', '-')
    image_file = os.path.join(DIR_DATA, f'text.{text_id}.{font_size}.png')
    image.save(image_file)
    log.info(f'Wrote {image_file}')
    os.system(f'open -a firefox {image_file}')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', type=str)
    parser.add_argument('--font_size', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    options = get_options()
    generate(options.text, options.font_size)
