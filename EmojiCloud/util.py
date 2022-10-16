import math
from PIL import Image
from rich.console import Console
from timeit import default_timer as timer
import numpy as np

global console
console = Console()


def timeit(f):
    def wrapper(*args, **kwargs):
        start = timer()
        r = f(*args, **kwargs)
        dur = timer() - start
        console.log("{} took {:.4f}".format(f.__name__, dur))
        return r
    return wrapper


def distance_between_two_points(x_1, y_1, x_2, y_2):
    """calculate the distance between two points

    Args:
        x_1 (float): x of the first point
        y_1 (float): y of the first point
        x_2 (float): x of the second point
        y_2 (float): y of the second point

    Returns:
        float: the distance between two points
    """
    if (x_1 != x_2):
        dist = math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)
    else:
        dist = math.fabs(y_1 - y_2)
    return dist


def sort_dictionary_by_value(dict_sort, reverse=True):
    """sort dictionary based on the value

    Args:
        dict_sort (dictionary): a dictionary to be sorted
        reverse (bool, optional): in a reverse order. Defaults to True.

    Returns:
        list of tuple (key, value): a list of sorted tuple
    """
    list_tuple_sorted = [(k, dict_sort[k]) for k in sorted(
        dict_sort, key=dict_sort.get, reverse=reverse)]
    return list_tuple_sorted


# @timeit
def parse_image_by_array(im):
    """parse the given image 

    Args:
        im (2D list): the image in 2D array with each cell of RGBA

    Returns:
        dict_opacity: key: coordinate, value: the RGB value
    """
    # read image
    im_data = im.getdata()
    width, height = im.size
    # identify transparent pixels
    dict_opacity = {}  # key: coordinate, value: RGB value
    for index, pixel in enumerate(im_data):
        # opacity coordinates along with RGB values
        if (pixel[3] != 0):
            x = index % im.width
            y = int(index / width)
            dict_opacity[tuple([x, y])] = pixel
    return dict_opacity


# @timeit
def remove_pixel_outside_bb(im, thold_alpha):
    """remove all pixels outside the bounding box

    Args:
        im (2D list): the image in 2D array with each cell of RGBA
        thold_alpha (float): the threshold to distinguish white and non-white colors

    Returns:
        im_dense: the new image after removing bounding box
    """
    # read image
    im_data = im.getdata()
    width, height = im.size
    dict_pixel = {}  # key: coordinate, value: RGB value
    # check pixels
    for index, pixel in enumerate(im_data):
        x = index % width
        y = int(index / width)
        dict_pixel[tuple([x, y])] = pixel
    # remove transparent rows
    list_row = []
    for x in range(width):
        flag = True
        for y in range(height):
            if (dict_pixel[tuple([x, y])][3] >= thold_alpha):
                flag = False
                break
        if (not flag):
            list_row.append([dict_pixel[tuple([x, y])] for y in range(height)])
    # remove transparent columns
    column_count = len(list_row[0])
    list_column = []
    for y in range(column_count):
        flag = True
        for row in list_row:
            if (row[y][3] >= thold_alpha):
                flag = False
                break
        if (not flag):
            list_column.append([row[y] for row in list_row])
    # reorganize new image
    width = len(list_column[0])
    height = len(list_column)
    im_dense = Image.new('RGBA', (width, height))
    for i in range(width):
        for j in range(height):
            im_dense.putpixel((i, j), list_column[j][i])
    return im_dense


# def remove_pixel_outside_bb(im, thold_alpha):
#     """remove all pixels outside the bounding box
#     improved version

#     Args:
#         im (2D list): the image in 2D array with each cell of RGBA
#         thold_alpha (float): the threshold to distinguish white and non-white colors

#     Returns:

#     """
#     im_array = np.array(im.convert('RGBA'))
#     s = np.dstack(np.meshgrid(np.arange(72), np.arange(72), indexing='ij'))
#     im_array = np.dstack((im_array, s))
#     return im_array[im_array[:, :, 3] >= thold_alpha, :]
    
