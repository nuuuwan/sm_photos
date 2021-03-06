"""Constants."""
import os

URL_GIT_REPO = 'https://github.com/nuuuwan/sm_photos'
DIR_DATA = '/tmp/sm_photos.data'
DIR_TWTR_DATA = os.path.join(DIR_DATA, 'twtr_data')

URL_REMOTE_TWTR_DATA = os.path.join(
    'https://raw.githubusercontent.com',
    'nuuuwan/sm_photos',
    'data/twtr_data',
)

USER_BLACKLIST = [
    'udeshan',
    'Sharkboys14',
    'ami_anonymous',
]
