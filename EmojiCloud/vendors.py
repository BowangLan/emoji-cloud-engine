import os

dict_vendor = {'Apple': 'Appl', 'Google': 'Goog', 'Meta': 'FB',
               'Windows': 'Wind', 'Twitter': 'Twtr', 'JoyPixels': 'Joy', 'Samsung': 'Sams'}


def get_emoji_vendor_path(vendor: str):
    return os.path.join('data', dict_vendor[vendor])


data_dir = 'data'

APPLE = os.path.join(data_dir, 'Appl')
GOOGLE = os.path.join(data_dir, 'Goog')
META = os.path.join(data_dir, 'FB')
WINDOWS = os.path.join(data_dir, 'Wind')
TWITTER = os.path.join(data_dir, 'Twtr')
JOYPIXEL = os.path.join(data_dir, 'Joy')
SAMSUNG = os.path.join(data_dir, 'Sams')
