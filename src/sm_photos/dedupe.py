import imagehash
from PIL import Image

from sm_photos import filesys, photos
from sm_photos._utils import log


def dedupe_photos(photo_file_list):

    hash_to_photo_file = {}
    for photo_file in photo_file_list:
        image = Image.open(photo_file)
        hash = str(imagehash.colorhash(image))

        if hash not in hash_to_photo_file:
            hash_to_photo_file[hash] = []
        hash_to_photo_file[hash].append(photo_file)

    deduped_photo_file_list = list(
        map(
            lambda x: x[1][0],
            sorted(hash_to_photo_file.items(), key=lambda x: x[0]),
        )
    )
    n_photo_file_list = len(photo_file_list)
    n_deduped_photo_file_list = len(deduped_photo_file_list)
    log.info(
        f'Deduped {n_photo_file_list}'
        + f' to {n_deduped_photo_file_list} photos'
    )

    return deduped_photo_file_list


if __name__ == '__main__':
    filesys.init()
    photo_file_list = photos.get_photo_file_list()
    deduped_photo_file_list = dedupe_photos(photo_file_list)
