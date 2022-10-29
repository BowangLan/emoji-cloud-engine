from .util import *

class CanvasBase():
    """the base class for all canvas objects
    Subclassing this class to create new canvas classes.
    To subclass, inside the subclass's `__init__` method, user has to define at least the following:
    * `self.w` , `self.h` - the width and height of the canvas
    * `self.img` - the Image object
    * `self.area` - the area of the canvas
    * `self.map_occupied` - a 2D list of whether the each pixel in the canvas is occupied or not 
    """
    @property
    def center_x(self) -> int:
        return int(self.w/2)

    @property
    def center_y(self) -> int:
        return int(self.h/2)

    def calculate_sorted_canvas_pix_for_plotting(self):
        """calculate a sorted list of canvas pixels based its distance to the canvas center point

        Returns:
            list_canvas_pix: a list of tuple (x,y) sorted by its distance to the canvas center
        """
        # points to be checked in an order determined by its distance from the center point of the image center
        # key: (x, y), value: the distance to the center of canvas
        dict_dist_canvas_center = {}
        for x in range(self.w):
            for y in range(self.h):
                if (self.map_occupied[x][y] == 0):
                    dist = distance_between_two_points(
                        x, y, self.center_x, self.center_y)
                    dict_dist_canvas_center[(x, y)] = dist
        list_canvas_pix_dist = sort_dictionary_by_value(
            dict_dist_canvas_center, reverse=False)
        list_canvas_pix = [x_y for (x_y, dist) in list_canvas_pix_dist]
        return list_canvas_pix


class RectangleCanvas(CanvasBase):
    def __init__(self, w: int, h: int, color: str = 'white'):
        self.w = w
        self.h = h
        self.color = color
        self.img = Image.new('RGBA', (w, h), color=color)
        self.map_occupied = [[0 for i in range(h)] for j in range(w)]

    @property
    def area(self):
        return self.w * self.h


def check_point_within_ellipse(center_x, center_y, x, y, radius_x, radius_y):
    """check whether a point is within a given ellipse

    Args:
        center_x (int): the center x of the ellipse
        center_y (int): the center y of the ellipse
        x (int): the x of point 
        y (int): the y of the point
        radius_x (int): the radius of x-axis 
        radius_y (int): the radius of y-axis

    Returns:
        bool: True or False
    """
    # ellipse with the given point
    p = ((math.pow((x - center_x), 2) / math.pow(radius_x, 2)) +
         (math.pow((y - center_y), 2) / math.pow(radius_y, 2)))
    if (p <= 1):
        return True
    else:
        return False


class EllipseCanvas(CanvasBase):
    def __init__(self, w: int = 72*10, h: int = 72*10, color: str = 'white'):
        self.w = w
        self.h = h
        self.color = color
        self.img = Image.new('RGBA', (w, h), color=color)
        self.map_occupied = [[1 for i in range(h)] for j in range(w)]
        for x in range(w):
            for y in range(h):
                flag = check_point_within_ellipse(self.center_x, self.center_y, x, y, w/2, h/2)
                if (flag):
                    self.map_occupied[x][y] = 0

    @property
    def area(self):
        return (self.w/2) * (self.h/2) * math.pi


def calculate_contour(im, thold_alpha=10):
    """calculate the contour of the given image

    Args:
        im (2D list): the image in 2D array with each cell of RGBA
        thold_alpha: the threshold to distinguish the colors on the contour and outside the contour

    Returns:
        list_contour: the list of (x, y) on the contour
    """
    # read image
    img_data = im.getdata()
    width, height = im.size
    dict_pixel = {}  # key: coordinate, value: RGB value
    # check pixels
    for index, pixel in enumerate(img_data):
        x = index % width
        y = int(index / width)
        dict_pixel[tuple([x, y])] = pixel
    # identify contour by row
    list_contour = []
    for x in range(width):
        prev_alpha = dict_pixel[tuple([x, 0])][3]
        for y in range(1, height):
            if (abs(dict_pixel[tuple([x, y])][3] - prev_alpha) > thold_alpha):
                list_contour.append(tuple([x, y]))
                prev_alpha = dict_pixel[tuple([x, y])][3]
    # identify contour by column
    for y in range(1, height):
        prev_alpha = dict_pixel[tuple([0, y])][3]
        for x in range(width):
            if (abs(dict_pixel[tuple([x, y])][3] - prev_alpha) > thold_alpha):
                list_contour.append(tuple([x, y]))
                prev_alpha = dict_pixel[tuple([x, y])][3]
    return list_contour


class MaskedCanvas(CanvasBase):
    def __init__(self, img_mask: str, contour_width, contour_color, thold_alpha_contour: int = 10, thold_alpha_bb: int = 0):
        """
        Args:
            img_mask (path of a masked image): the path of a masked image 
            contour_width: the contour width
            contour_color: the contour color
            thold_alpha_contour: the threshold to distinguish the colors on the contour and outside the contour
            thold_alpha_bb: the threshold to distinguish white and non-white colors for bounding box detection
        """
        self.thold_alpha_bb = thold_alpha_bb

        im = Image.open(img_mask).convert('RGBA')
        self.w = im.size[0] + contour_width*2
        self.h = im.size[1] + contour_width*2

        img_mask_within_bb = remove_pixel_outside_bb(im, thold_alpha_bb)
        # parse masked image
        self.dict_opacity = parse_image_by_array(img_mask_within_bb)
        self.img = Image.new('RGBA', (self.w, self.h), color="white")

        self.map_occupied = [[1 for i in range(self.h)] for j in range(self.w)]
        # set pixels in the mask image as unoccupied
        for (x, y) in self.dict_opacity:
            self.map_occupied[x][y] = 0

        # process contour 
        list_contour = calculate_contour(img_mask_within_bb, thold_alpha_contour)
        # contour width 
        for (x, y) in list_contour:
            for i in range(contour_width):
                for j in range(contour_width):
                    self.img.putpixel((x + i, y + j), contour_color)
                    self.map_occupied[x + i][y + j] = 1

    @property
    def area(self):
        return len(self.dict_opacity)
