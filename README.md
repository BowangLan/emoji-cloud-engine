# emoji-cloud-engine

## Introduction

This is an edited version of [EmojiCloud](https://github.com/YunheFeng/EmojiCloud). This version provides a more powerful API than Yunhe's version.

## Set up

The emoji files have to be downloaded from Yunhe's original repository:

```bash
chmod 777 ./update_data_from_github.sh
./update_data_from_github.sh
```

## Basic Usage

```python
from EmojiCloud.plot import plot_dense_emoji_cloud
from EmojiCloud.emoji import EmojiManager
from EmojiCloud.canvas import EllipseCanvas, RectangleCanvas, MaskedCanvas

# set emoji weights by a dict with key: emoji in unicode, value: weight
dict_weight = {'1f1e6-1f1e8': 1.1, '1f4a7': 1.2, '1f602': 1.3, '1f6f4': 1.4, '1f6f5': 1.5, '1f6f6': 1.6, '1f6f7': 1.7, '1f6f8': 1.8, '1f6f9': 1.9, '1f6fa': 2.0, '1f6fb': 2.1, '1f6fc': 2.2, '1f7e0': 2.3, '1f9a2': 2.4, '1f9a3': 2.5, '1f9a4': 2.6, '1f9a5': 2.7, '1f9a6': 2.8, '1f9a8': 2.9, '1f9a9': 3.0}

# emoji vendor 
emoji_vendor = 'Twtr'
emoji_list = EmojiManager.create_list_from_single_vendor(dict_weight, emoji_vendor)

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

Our paper has been accepted at the 5th International Workshop on Emoji Understanding and Applications in Social Media (EMOJI@NAACL 2022). Online EmojiCloud services will be available soon at www.emojicloud.org.

## Citations

```python
@inproceedings{feng2022emojicloud,
  title={EmojiCloud: a Tool for Emoji Cloud Visualization},
  author={Feng, Yunhe and Guo, Cheng and Wen, Bingbing and Sun, Peng and Yue, Yufei and Tao, Dingwen},
  booktitle={The 5th International Workshop on Emoji Understanding and Applications in Social Media at 2022 Annual Conference of the North American Chapter of the Association for Computational Linguistics (EMOJI@NAACL)},
  year={2022}
}
```
