import os
from PIL import Image
import copy
import math
import collections
from .config import parent_dir
from .canvas import CanvasBase

from .emoji import EmojiItem
from .util import *


# @timeit
def resize_img_based_weight(im: Image.Image, weight: float) -> Image.Image:
    """resize original image based on its weight

    Args:
        im_read (Image.Image): the image in 2D array with each cell of RGBA
        weight (float): weight of the image 

    Returns:
        im_resize (2D list): the image in 2D array with each cell of RGBA: the image width
    """
    width, height = im.getdata().size
    width_resize = int(width*weight) if int(width*weight) > 0 else 1
    height_resize = int(height*weight) if int(height*weight) > 0 else 1
    im_resize = im.resize((width_resize, height_resize), Image.LANCZOS)
    return im_resize


class OrderedSet(collections.abc.Set):
    def __init__(self, iterable=()):
        self.d = collections.OrderedDict.fromkeys(iterable)

    def __len__(self):
        return len(self.d)

    def __contains__(self, element):
        return element in self.d

    def __iter__(self):
        return iter(self.d)


# @timeit
def rename_emoji_image_in_unicode(dict_weight: dict[str, int]) -> dict[str, int]:
    """rename emoji image name in unicode 

    Args:
        dict_weight (dict): key: emoji by unicode or codepoint, value: emoji weight 

    Returns:
        dict_rename (dict): key: renamed emoji image by codepoint, value: emoji weight 
    """
    dict_rename = {}
    for im_name in dict_weight:
        if im_name[:2].lower() == 'u+':
            dict_rename[im_name + '.png'] = dict_weight[im_name]
            continue
        # replace ',' and ' '
        im_name_proc = im_name.replace(',', '-')
        im_name_proc = im_name_proc.replace(' ', '')
        # emoji by unicode
        if not im_name_proc.replace('-', '').isalnum():
            im_rename = 'U+' + '-U+'.join('{:X}'.format(ord(_))
                                          for _ in im_name_proc) + '.png'
        # emoji by codepoint
        else:
            im_rename = im_name_proc.upper()
            if '.png' not in im_rename:
                im_rename += '.png'
            if 'U+' not in im_rename:
                im_rename = 'U+' + '-U+'.join(im_rename.split('-'))
        dict_rename[im_rename] = dict_weight[im_name]
    return dict_rename


def resize_emoji_list(emoji_list: list[EmojiItem], canvas_area: float, relax_ratio: float = 1.5) -> list[Image.Image]:
    """generate the resized emoji images based on weights

    Args:
        emoji_list (list[EmojiItem]): a list of valid EmojiItem objects needed to be resized
        canvas_area (float): the canvas area 
        relax_ratio (float, optional): control the plotting sparsity. Defaults to 1.5.

    Returns: a list of resized Image objects
    """
    weight_sum = sum([e.weight for e in emoji_list])
    norm_area_sum = 0
    size_cache = {}
    for e in emoji_list:
        size = e.image.getdata().size
        if size in size_cache:
            s = size_cache[size]
        else:
            s = size[0] * size[1]
        norm_weight = e.weight / weight_sum
        norm_area_sum += s * norm_weight ** 2
        e.weight = norm_weight

    zoom_ratio = math.sqrt(canvas_area/norm_area_sum) / relax_ratio

    return [
        resize_img_based_weight(e.image, e.weight * zoom_ratio)
        for e in sorted(emoji_list, key=lambda e: e.weight, reverse=True)
    ]


@timeit
def plot_emoji_cloud_given_relax_ratio(emoji_list: list[EmojiItem], canvas: CanvasBase, list_canvas_pix, thold_alpha_bb: float, relax_ratio: float) -> tuple[Image.Image, int]:
    """plot emoji cloud

    Args:
        path_img_raw (string): the path of raw emoji images 
        canvas_img: the image of canvas
        canvas_w (int): the canvas width
        canvas_h (int): the canvas height
        canvas_area: the area of canvas 
        dict_weight (dict): key: emoji image name in unicode, value: weight
        list_canvas_pix (list): a list of tuple (x,y) sorted by its distance to the canvas center
        map_occupied (list): a 2D list of whether the pixel is occupied or not 
        dict_customized (dict): key: emoji image name in unicode, value: the path of customized emoji image
        thold_alpha_bb: the threshold to distinguish white and non-white colors for bounding box detection 
        relax_ratio (float): the ratio >=1, controlling the sparsity of emoji plotting

    Returns:
        canvas_img: the final image of canvas
        count_plot: the count of plotted emojis 
    """
    # new_list_canvas_pix = list_canvas_pix.copy()
    new_list_canvas_pix = copy.deepcopy(list_canvas_pix)
    # new_canvas_img = canvas_img.copy()
    new_canvas_img = copy.deepcopy(canvas.img)
    # new_map_occupied = map_occupied.copy()
    new_map_occupied = copy.deepcopy(canvas.map_occupied)

    list_sorted_emoji = resize_emoji_list(emoji_list, canvas.area, relax_ratio) 

    # plot each emoji
    count_plot = 0
    for index, im in enumerate(list_sorted_emoji):
        # fail to plot the last emoji image
        if (index != count_plot):
            break
        # remove pixel outside bounding box
        img_within_bb = remove_pixel_outside_bb(im, thold_alpha_bb)
        # parse emoji image
        dict_opacity = parse_image_by_array(img_within_bb)

        # get the center point of the emoji image
        list_x = []
        list_y = []
        for (x, y) in dict_opacity:
            list_x.append(x)
            list_y.append(y)
        center = sum(list_x)/len(list_x), sum(list_y)/len(list_y)
        img_center_x = int(center[0])
        img_center_y = int(center[1])

        # sort opacity point by distant to the center point
        dict_dist_img_center = {}  # key: point, value: point to the image center
        for (x, y) in dict_opacity:
            # dist = distance_between_two_points(x, y, img_width/2, img_height/2)
            dist = distance_between_two_points(
                x, y, img_center_x, img_center_y)
            dict_dist_img_center[(x, y)] = dist
        list_img_pix_dist = sort_dictionary_by_value(
            dict_dist_img_center, reverse=True)
        list_img_pix = [x_y for (x_y, dist) in list_img_pix_dist]

        # check the possibility of each pixel starting from the center
        for x_y in new_list_canvas_pix:
            canvas_x, canvas_y = x_y
            # check all points
            flag = True
            for (x, y) in list_img_pix:
                # adding offset
                offset_x = x - img_center_x
                offset_y = y - img_center_y
                # candidate x, y on canvas
                candidate_x = canvas_x + offset_x
                candidate_y = canvas_y + offset_y
                # check validity
                if (candidate_x < canvas.w and candidate_x >= 0 and candidate_y < canvas.h and candidate_y >= 0):
                    # the pixel on canvas has been occupied
                    if (new_map_occupied[canvas_x + offset_x][canvas_y + offset_y] == 1):
                        flag = False
                        break
                # out of the canvas
                else:
                    flag = False
                    break
            # plot emoji image
            if (flag):
                list_occupied = []
                for (x, y) in dict_opacity:
                    # adding offset
                    offset_x = x - img_center_x
                    offset_y = y - img_center_y
                    # candidate x, y on canvas
                    candidate_x = canvas_x + offset_x
                    candidate_y = canvas_y + offset_y
                    # plot the emoji
                    new_canvas_img.putpixel(
                        (candidate_x, candidate_y), dict_opacity[(x, y)])
                    new_map_occupied[candidate_x][candidate_y] = 1
                    list_occupied.append((candidate_x, candidate_y))
                # continue processing the next emoji
                count_plot += 1
                break
            else:
                list_occupied = []

        # remove occupied tuple
        new_list_canvas_pix = list(OrderedSet(
            new_list_canvas_pix) - OrderedSet(list_occupied))
    return new_canvas_img, count_plot



# @timeit
# def generate_resized_emoji_images(path_img_raw, dict_weight, canvas_area, dict_customized, relax_ratio=1.5):
#     """generate the resized emoji images based on weights

#     Args:
#         path_img_raw (string): the path of raw emojis 
#         dict_weight (dict): key: emoji image name in unicode, value: emoji weight 
#         canvas_area (float): the canvas area 
#         dict_customized (dict): key: emoji image name in unicode, value: the path of customized emoji image
#         relax_ratio (float, optional): control the plotting sparsity. Defaults to 1.5.

#     Returns:
#         list_sorted_emoji: a list of sorted emojis by their weights
#         list_resize_img: a list of resize image array 
#     """
#     # process emoji image name in unicode
#     dict_weight = rename_emoji_image_in_unicode(dict_weight)
#     dict_customized = rename_emoji_image_in_unicode(dict_customized)
#     # normalize weight
#     weight_sum = sum([v for v in dict_weight.values()])
#     # calculate zoom in/out ratio
#     im_list = []
#     norm_area_sum = 0
#     for im_name in dict_weight:
#         if im_name not in dict_customized:
#             im_read = Image.open(parent_dir + '/' +
#                                  os.path.join(path_img_raw, im_name))
#         else:
#             im_read = Image.open(dict_customized[im_name])
#         normalized_weight = dict_weight[im_name] / weight_sum
#         im_list.append({
#             'im': im_read.convert('RGBA'),
#             'weight': normalized_weight
#         })
#         width, height = im_read.getdata().size
#         norm_area_sum += width*height*(normalized_weight**2)
#     zoom_ratio = math.sqrt(canvas_area/norm_area_sum)/relax_ratio
#     return [
#         resize_img_based_weight(i['im'], i['weight'] * zoom_ratio)
#         for i in sorted(im_list, key=lambda im_data: im_data['weight'], reverse=True)
#     ]


# @timeit
# def plot_emoji_cloud_given_relax_ratio(path_img_raw, canvas_img, canvas_w, canvas_h, canvas_area, dict_weight, list_canvas_pix, map_occupied, dict_customized, thold_alpha_bb, relax_ratio):
#     """plot emoji cloud

#     Args:
#         path_img_raw (string): the path of raw emoji images 
#         canvas_img: the image of canvas
#         canvas_w (int): the canvas width
#         canvas_h (int): the canvas height
#         canvas_area: the area of canvas 
#         dict_weight (dict): key: emoji image name in unicode, value: weight
#         list_canvas_pix (list): a list of tuple (x,y) sorted by its distance to the canvas center
#         map_occupied (list): a 2D list of whether the pixel is occupied or not 
#         dict_customized (dict): key: emoji image name in unicode, value: the path of customized emoji image
#         thold_alpha_bb: the threshold to distinguish white and non-white colors for bounding box detection 
#         relax_ratio (float): the ratio >=1, controlling the sparsity of emoji plotting

#     Returns:
#         canvas_img: the final image of canvas
#         count_plot: the count of plotted emojis 
#     """
#     # new_list_canvas_pix = list_canvas_pix.copy()
#     new_list_canvas_pix = copy.deepcopy(list_canvas_pix)
#     # new_canvas_img = canvas_img.copy()
#     new_canvas_img = copy.deepcopy(canvas_img)
#     # new_map_occupied = map_occupied.copy()
#     new_map_occupied = copy.deepcopy(map_occupied)
#     list_sorted_emoji = generate_resized_emoji_images(
#         path_img_raw, dict_weight, canvas_area, dict_customized, relax_ratio)
#     # plot each emoji
#     count_plot = 0
#     for index, im in enumerate(list_sorted_emoji):
#         # fail to plot the last emoji image
#         if (index != count_plot):
#             break
#         # remove pixel outside bounding box
#         img_within_bb = remove_pixel_outside_bb(im, thold_alpha_bb)
#         # parse emoji image
#         dict_opacity = parse_image_by_array(img_within_bb)

#         # get the center point of the emoji image
#         list_x = []
#         list_y = []
#         for (x, y) in dict_opacity:
#             list_x.append(x)
#             list_y.append(y)
#         center = sum(list_x)/len(list_x), sum(list_y)/len(list_y)
#         img_center_x = int(center[0])
#         img_center_y = int(center[1])

#         # sort opacity point by distant to the center point
#         dict_dist_img_center = {}  # key: point, value: point to the image center
#         for (x, y) in dict_opacity:
#             # dist = distance_between_two_points(x, y, img_width/2, img_height/2)
#             dist = distance_between_two_points(
#                 x, y, img_center_x, img_center_y)
#             dict_dist_img_center[(x, y)] = dist
#         list_img_pix_dist = sort_dictionary_by_value(
#             dict_dist_img_center, reverse=True)
#         list_img_pix = [x_y for (x_y, dist) in list_img_pix_dist]

#         # check the possibility of each pixel starting from the center
#         for x_y in new_list_canvas_pix:
#             canvas_x, canvas_y = x_y
#             # check all points
#             flag = True
#             for (x, y) in list_img_pix:
#                 # adding offset
#                 offset_x = x - img_center_x
#                 offset_y = y - img_center_y
#                 # candidate x, y on canvas
#                 candidate_x = canvas_x + offset_x
#                 candidate_y = canvas_y + offset_y
#                 # check validity
#                 if (candidate_x < canvas_w and candidate_x >= 0 and candidate_y < canvas_h and candidate_y >= 0):
#                     # the pixel on canvas has been occupied
#                     if (new_map_occupied[canvas_x + offset_x][canvas_y + offset_y] == 1):
#                         flag = False
#                         break
#                 # out of the canvas
#                 else:
#                     flag = False
#                     break
#             # plot emoji image
#             if (flag):
#                 list_occupied = []
#                 for (x, y) in dict_opacity:
#                     # adding offset
#                     offset_x = x - img_center_x
#                     offset_y = y - img_center_y
#                     # candidate x, y on canvas
#                     candidate_x = canvas_x + offset_x
#                     candidate_y = canvas_y + offset_y
#                     # plot the emoji
#                     new_canvas_img.putpixel(
#                         (candidate_x, candidate_y), dict_opacity[(x, y)])
#                     new_map_occupied[candidate_x][candidate_y] = 1
#                     list_occupied.append((candidate_x, candidate_y))
#                 # continue processing the next emoji
#                 count_plot += 1
#                 break
#             else:
#                 list_occupied = []

#         # remove occupied tuple
#         new_list_canvas_pix = list(OrderedSet(
#             new_list_canvas_pix) - OrderedSet(list_occupied))
#     return new_canvas_img, count_plot


@timeit
def plot_dense_emoji_cloud(canvas: CanvasBase, emoji_list: list[EmojiItem], thold_alpha_bb: int = 4, num_try: int = 20, step_size: float = 0.1) -> Image.Image:
    # a sorted list of available pixel positions for plotting
    list_canvas_pix = canvas.calculate_sorted_canvas_pix_for_plotting()
    # plot emoji cloud with an increasing relax_ratio with a fixed step size
    for i in range(num_try):
        relax_ratio = 1 + step_size*i
        canvas_img_plot, count_plot = plot_emoji_cloud_given_relax_ratio(
            emoji_list, canvas, list_canvas_pix, thold_alpha_bb, relax_ratio)
        # plot all emojis successfully
        if (count_plot == len(emoji_list)):
            return canvas_img_plot
