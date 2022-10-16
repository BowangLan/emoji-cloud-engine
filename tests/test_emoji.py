from EmojiCloud.util import *
from EmojiCloud.plot import plot_dense_emoji_cloud
from EmojiCloud.emoji import EmojiManager, EmojiItem
from EmojiCloud.canvas import EllipseCanvas, RectangleCanvas, MaskedCanvas
from EmojiCloud.vendors import GOOGLE, TWITTER


def test_check_exists():
    # emoji unicode that exists
    unicode1 = '1f623'
    emoji_item = EmojiItem(unicode=unicode1, weight=1, vendor=TWITTER)
    assert emoji_item.exists()
    assert not EmojiManager.check_exists(unicode1, TWITTER)

    # emoji unicode that don't exists
    unicode2 = '1f62o'
    emoji_item = EmojiItem(unicode=unicode2, weight=1, vendor=TWITTER)
    assert not emoji_item.exists()
    assert not EmojiManager.check_exists(unicode2, TWITTER)


def test_creating_list():
    emoji_list_1 = [
        {
            'unicode': '1f602',
            'vendor': TWITTER,
            'weight': 1.2
        },
        {
            'unicode': '1f604',
            'vendor': GOOGLE,
            'weight': 1.8
        }
    ]

    emoji_item_list_1 = EmojiManager.create_list_from_multiple_vendor(emoji_list_1)
    console.log(emoji_item_list_1)
    assert len(emoji_item_list_1) == len(emoji_list_1)
    assert emoji_item_list_1[0].weight == emoji_list_1[0]['weight']

    # convert a list of EmojiItem to dict
    console.log(EmojiManager.emoji_item_list_to_dict(emoji_item_list_1))