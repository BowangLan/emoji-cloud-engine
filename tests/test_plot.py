from EmojiCloud.util import *
from EmojiCloud.plot import plot_dense_emoji_cloud
from EmojiCloud.emoji import EmojiManager
from EmojiCloud.canvas import EllipseCanvas, RectangleCanvas, MaskedCanvas
from EmojiCloud.vendors import GOOGLE, vendor_dir_list


# def test_plot():
#     emoji_name_to_weight = {'U+1F600': 1.1, 'U+1F601': 1.2, 'U+1F602': 1.3, 'U+1F603': 1.4, 'U+1F604': 1.5, 'U+1F605': 1.6, 'U+1F606': 1.7, 'U+1F607': 1.8, 'U+1F608': 1.9, 'U+1F609': 2.0, 'U+1F610': 2.1, 'U+1F612': 2.2, 'U+1F613': 2.3, 'U+1F614': 2.4, 'U+1F616': 2.5, 'U+1F617': 2.6, 'U+1F618': 2.7, 'U+1F619': 2.8, 'U+1F620': 2.9, 'U+1F621': 3.0, 'U+1F622': 3.1, 'U+1F624': 3.2, 'U+1F625': 3.3, 'U+1F628': 3.4, 'U+1F629': 3.5, 'U+1F630': 3.6, 'U+1F631': 3.7, 'U+1F632': 3.8, 'U+1F633': 3.9, 'U+1F634': 4.0, 'U+1F635': 4.1, 'U+1F637': 4.2, 'U+1F638': 4.3, 'U+1F639': 4.4, 'U+1F640': 4.5, 'U+1F641': 4.6, 'U+1F642': 4.7, 'U+1F643': 4.8, 'U+1F644': 4.9, 'U+1F910': 5.0, 'U+1F911': 5.1, 'U+1F912': 5.2, 'U+1F913': 5.3, 'U+1F914': 5.4, 'U+1F915': 5.5, 'U+1F917': 5.6, 'U+1F920': 5.7, 'U+1F921': 5.8, 'U+1F922': 5.9, 'U+1F923': 6.0, 'U+1F924': 6.1, 'U+1F925': 6.2, 'U+1F927': 6.3, 'U+1F929': 6.4, 'U+1F970': 6.5, 'U+1F971': 6.6, 'U+1F973': 6.7, 'U+1F974': 6.8, 'U+1F975': 6.9, 'U+1F976': 7.0, 'U+1FAE1': 7.1, 'U+1FAE2': 7.2, 'U+1FAE3': 7.3}
#     w = 72*10 
#     h = 72*10 
#     canvas = EllipseCanvas(w, h)
#     for v in vendor_dir_list:
#         print("Plotting usingn %s" % v)
#         emoji_list = EmojiManager.create_list_from_single_vendor(emoji_name_to_weight, v)
#         im = plot_dense_emoji_cloud(canvas, emoji_list)
#         im.save('im1-%s.png' % v)


def test_plot():
    pass