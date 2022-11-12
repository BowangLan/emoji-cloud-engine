# emoji-cloud-engine

## Introduction

EmojiCloud is an open-source Python-based emoji cloud visualization tool that generates a quick and straightforward understanding of emojis from the perspective of frequency and importance. EmojiCloud is flexible enough to support diverse drawing shapes, such as rectangles, ellipses, and image masked canvases. We also follow inclusive and personalized design principles to cover the unique emoji designs from seven emoji vendors (e.g., Twitter, Apple, and Windows) and allow users to customize plotted emojis and background colors. We hope EmojiCloud can benefit the whole emoji community due to its flexibility, inclusiveness, and customizability.

## Basic Usage

```python
from EmojiCloud.plot import plot_dense_emoji_cloud
from EmojiCloud.emoji import EmojiManager
from EmojiCloud.canvas import EllipseCanvas, RectangleCanvas, MaskedCanvas
from EmojiCloud.vendors import TWIITER

# set emoji weights by a dict with key: emoji in unicode, value: weight
dict_weight = {'1f1e6-1f1e8': 1.1, '1f4a7': 1.2, '1f602': 1.3, '1f6f4': 1.4, '1f6f5': 1.5, '1f6f6': 1.6, '1f6f7': 1.7, '1f6f8': 1.8, '1f6f9': 1.9, '1f6fa': 2.0, '1f6fb': 2.1, '1f6fc': 2.2, '1f7e0': 2.3, '1f9a2': 2.4, '1f9a3': 2.5, '1f9a4': 2.6, '1f9a5': 2.7, '1f9a6': 2.8, '1f9a8': 2.9, '1f9a9': 3.0}

# emoji vendor 
emoji_list = EmojiManager.create_list_from_single_vendor(dict_weight, TWITTER)

# masked canvas 
print("Plotting masked cloud")
img_mask = 'twitter-logo.png'
thold_alpha_contour = 10 
contour_width = 5
contour_color = (0, 172, 238, 255)
saved_emoji_cloud_name = 'emoji_cloud_masked.png'
m_canvas = MaskedCanvas(img_mask, contour_width, contour_color, thold_alpha_contour)
im = plot_dense_emoji_cloud(m_canvas, emoji_list)
im.save(saved_emoji_cloud_name)

# rectangle canvas 
print("Plotting rectangle cloud")
canvas_w = 72*10
canvas_h = 72*4
canvas = RectangleCanvas(canvas_w, canvas_h)
saved_emoji_cloud_name = 'emoji_cloud_rectangle.png'
im = plot_dense_emoji_cloud(canvas, emoji_list)
im.save(saved_emoji_cloud_name)

# ellipse canvas
print("Plotting ellipse cloud")
canvas_w = 72*10
canvas_h = 72*4
saved_emoji_cloud_name = 'emoji_cloud_ellipse.png'
canvas = EllipseCanvas(canvas_w, canvas_h)
im = plot_dense_emoji_cloud(canvas, emoji_list)
im.save(saved_emoji_cloud_name)
```

Results:

![Masked Result Image](https://raw.githubusercontent.com/BowangLan/emoji-cloud-engine/main/examples/results/emoji_cloud_masked.png)

![Rectangle Result Image](https://raw.githubusercontent.com/BowangLan/emoji-cloud-engine/main/examples/results/emoji_cloud_rectangle.png)

![Ellipse Result Image](https://raw.githubusercontent.com/BowangLan/emoji-cloud-engine/main/examples/results/emoji_cloud_ellipse.png)

All available vendors is stored in `EmojiCloud.vendors.vendor_dir_list` as a Python list:

```python
from EmojiCloud.vendors import vendor_dir_list
print(vendor_dir_list)
```

You can check if an emoji with a specific unicode of a specific vendor exists using `EmojiManager.check_exists(unicode, vendor)` method.

## Authors

Contributors names and contact info

* [Yunhe Feng](https://yunhefeng.me/)

* [Bowang Lan](https://github.com/BowangLan)

## License

See the LICENSE.md file for details

## Paper

This project is inspired by [Yunhe Feng](https://yunhefeng.me/)'s paper [EmojiCloud: a Tool for Emoji Cloud Visualization](https://aclanthology.org/2022.emoji-1.8/).
