import os
from .config import data_dir

dict_vendor = {'Apple': 'Appl', 'Google': 'Goog', 'Meta': 'FB',
               'Windows': 'Wind', 'Twitter': 'Twtr', 'JoyPixels': 'Joy', 'Samsung': 'Sams'}


def get_emoji_vendor_path(vendor: str):
    return os.path.join('data', dict_vendor[vendor])


APPLE = 'Appl'
APPLE_PATH = os.path.join(data_dir, APPLE)

GOOGLE = 'Goog'
GOOGLE_PATH = os.path.join(data_dir, GOOGLE)

META = 'FB'
META_PATH = os.path.join(data_dir, META)

WINDOWS = 'Wind'
WINDOWS_PATH = os.path.join(data_dir, WINDOWS)

TWITTER = 'Twtr'
TWITTER_PATH = os.path.join(data_dir, TWITTER)

JOYPIXEL = 'Joy'
JOYPIXEL_PATH = os.path.join(data_dir, JOYPIXEL)

SAMSUNG = 'Sams'
SAMSUNG_PATH = os.path.join(data_dir, SAMSUNG)

vendor_dir_list = os.listdir(data_dir)