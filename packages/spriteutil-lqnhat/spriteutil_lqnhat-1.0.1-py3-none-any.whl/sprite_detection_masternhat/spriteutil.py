#!/usr/bin/env python3
import random

from PIL import Image


class Sprite:
    """
    Initialize the coordinates (x1, y1) (a tuple) of the top-left corner,
    the coordinates (x2, y2) (a tuple) of the right-most corner and 
    the number of pixels horizontally and vertically of the sprite.
    """

    def __init__(self, label, x1, y1, x2, y2, pixels):
        self.__argument_type_checker(label, x1, y1, x2, y2, pixels)

        self.__label = label
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__pixels = pixels

    def __argument_type_checker(self, label, x1, y1, x2, y2, pixels):
        """
        Check coordinates element of class's arguments and raise ValueError 
        if any element in the arguments was not satisfying conditions.
        """
        # If one or more arguments x1, y1, x2, and y2 is not positive integer.
        first_condition = any([not isinstance(arg, int)
                               for arg in [label, x1, y1, x2, y2, pixels]])

        # If the arguments x2 is not equal or greater x1.
        second_condition = x1 > x2

        # If the arguments y2 is not equal or greater y1.
        third_condition = y1 > y2

        if first_condition or second_condition or third_condition:
            raise ValueError('Invalid coordinates.')

    @property
    def bottom_right(self):
        return self.__x2, self.__y2

    @property
    def height(self):
        return (self.__y2 - self.__y1) + 1

    @property
    def label(self):
        return self.__label

    @property
    def top_left(self):
        return self.__x1, self.__y1

    @property
    def width(self):
        return (self.__x2 - self.__x1) + 1

    @property
    def pixels(self):
        return self.__pixels


class LabelMap:
    """
    Initialize a 2D array of integers of equal dimension (width and height) as
    the original image where the sprites are packed in.

    The label_map array maps each pixel of the image passed to the 
    function to the label of the sprite this pixel corresponds to, or
    0 if this pixel doesn't belong to a sprite (e.g., background color).
    """

    def __init__(self):
        self.__label_map = []
        self.__max_x = 0
        self.__max_y = 0

    @property
    def max_x(self):
        """
        Get the max value of the row.
        """
        return self.__max_x

    @property
    def max_y(self):
        """
        Get the max value of the column.
        """
        return self.__max_y

    @property
    def label_map(self):
        """
        Get the label map.
        """
        return self.__label_map

    def check_pixel(self, x, y):
        """
        Check a pixel's position is have label or not. 
        """
        return self.__label_map[x][y] == 0

    def init_map(self, amount_row, amount_column):
        """
        Initialize a map follow amount provided 
        and set the max value for row and column.
        """
        self.__max_x = amount_row
        self.__max_y = amount_column
        self.__label_map = [[0 for _ in range(amount_column)] for _ in range(amount_row)]

    def set_pixel_label(self, x, y, label):
        """
        Set label for a pixel.
        """
        self.__label_map[x][y] = label


class SpriteSheet:
    """
    Detect all the information of the image represented by sprites.

    The class accepts an argument fd that corresponds to either:

    + The name and path (a string) that references an image file 
    in the local file system;
    + A pathlib.Path object that references an image file in the 
    local file system ;
    + A file object that MUST implement read(), seek(), and tell() 
    methods, and be opened in binary mode;
    + A Image object.

    This constructor also accepts an optional argument background_color 
    that identifies the background color (i.e., transparent color) of 
    the image. The type of background_color argument depends on the 
    images' mode:

    + An integer if the mode is grayscale;
    + A tuple (red, green, blue) of integers if the mode is RGB;
    + A tuple (red, green, blue, alpha) of integers if the mode is RGBA. 
    The alpha element is optional. If not defined, while the image mode 
    is RGBA, the constructor considers the alpha element to be 255.
    """

    def __init__(self, fd, background_color=None):
        self.__image = fd if isinstance(fd, Image.Image) else Image.open(fd)
        self.__background_color = background_color
        self.__sprites = {}
        self.__label_map = []
        self.__sprite_labels_image = []

    @property
    def background_color(self):
        """
        Check the background_color argument.

        Return:
        + The background color: the background_color argument is not None.
        + The most common color: the background_color argument is None.
        """
        return self.__background_color or self.find_most_common_color(self.__image)

    @staticmethod
    def find_most_common_color(image):
        """
        Find the most common color of an image and return a tuple of color
        upon the mode of the image.

        Return:
        + An integer if the mode is grayscale;
        + A tuple (red, green, blue) of integers (0 to 255) if the mode is RGB;
        + A tuple (red, green, blue, alpha) of integers (0 to 255) if the mode is RGBA.
        """
        colors_info = image.getcolors(image.width * image.height)
        _, most_common_color = max(colors_info, key=lambda item: item[0])

        return most_common_color

    def __draw_boundary_box(self, image, value, color):
        """
        Draw the boundary box of a sprite.
        
        Arguments:
            image {object} -- an image object.
            value {object} -- an sprite object.
            color {tuple} -- a color tuple.
        
        Returns:
            object -- an image object with the input sprite has had a boundary box.
        """
        for x in range(value.top_left[0], value.bottom_right[0]):
            image.putpixel((x, value.top_left[1]), color)
            image.putpixel((x, value.bottom_right[1]), color)

        for y in range(value.top_left[1], value.bottom_right[1]):
            image.putpixel((value.top_left[0], y), color)
            image.putpixel((value.bottom_right[0], y), color)

        return image

    def __change_bounding_boxes_color(self, sprites, label_color, image,
        min_surface_area=None, similarity_threshold=None, density_threshold=None):
        """
        Change the color of each pixel which is the bounding box
        of the sprite corresponding with the color each label.
        """
        special_value = [min_surface_area, similarity_threshold, density_threshold]
        is_special_case = False

        if any(special_value):
            is_special_case = True
            conditions = [index for index, item in enumerate(special_value) if item is not None]

        for key, value in sprites.items():
            if is_special_case and self.__sprite_checker(conditions, value, special_value):
                color = (0, 0, 0)
                image = self.__draw_boundary_box(image, value, color)

            if not is_special_case:
                color = label_color[key]
                image = self.__draw_boundary_box(image, value, color)

        return image

    def __change_image_pixel_color(self, max_row, max_column, label_map, label_color, image):
        """
        Change the color of each pixel corresponding with the color of label in the label_map.
        """
        for row in range(max_row):
            for column in range(max_column):
                color = label_color[label_map[row][column]]
                image.putpixel((column, row), color)

        return image

    def __check_pixel_neighbours(self, pixel, next_pixels, sprites, label_map, background_color, label):
        """
        Check neighbours of a pixel in 8 directions, update
        the value inside next_pixels, sprites and label_map.
        """
        directions = [[1, 0], [1, 1], [0, 1], [-1, 1],
                      [-1, 0], [-1, -1], [0, -1], [1, -1]]

        #    ______________ ______________ ______________
        #   | (x - 1, y - 1) | (x - 1 ,  y  ) | (x - 1, y + 1) |
        #   |________________|________________|________________|
        #   | (x,   y - 1  ) | (  x  ,   y  ) | (x ,   y + 1 ) |
        #   |________________|________________|________________|
        #   | (x + 1, y - 1) | (  x + 1 , y ) | (x + 1, y + 1) |
        #   |________________|________________|________________|
        #

        max_x = label_map.max_x
        max_y = label_map.max_y

        for each in directions:
            # The current order if pixel is (column, row)
            # => x = pixel[1] (row)
            # => y = pixel[0] (column)

            x, y = pixel[1], pixel[0]
            x += each[0]
            y += each[1]

            if 0 <= x < max_x and 0 <= y < max_y:
                if self.__image.getpixel((y, x)) != background_color and \
                        label_map.check_pixel(x, y):

                    label_map.set_pixel_label(x, y, label)
                    new_pixel = (y, x)
                    sprites[label].append(new_pixel)
                    next_pixels.append(new_pixel)

        return next_pixels, sprites, label_map

    def __generate_color_dict(self, sprites, background_color):
        """
        Generate a dictionary of color corresponding with each label in the sprites.
        """
        label_color = {0: background_color}

        for key in sprites.keys():
            label_color[key] = self.__random_color(label_color)

        return label_color

    def __get_background_color(self):
        """
        Detect the background color of an image.
        """
        if self.__image.mode == 'RGBA':
            return (0, 0, 0, 0)

        return self.find_most_common_color(self.__image)

    def __is_valid_surface_area(self, sprite, min_surface_area):
        """
        Check sprite's surface area is equal to or larger than the specified minimal surface.
        
        Arguments:
            sprite {sprite onject} -- a sprite object
            min_surface_area {integer} -- An integer representing the minimal surface
            area of a sprite's bounding box to consider this sprite as visible.
        
        Returns:
            boolean -- a boolean value represents that the sprite is valid or not.
        """
        return sprite.height * sprite.width >= min_surface_area

    def __is_square_sprite(self, sprite, similarity_threshold):
        """
        Check sprite's boundary box is almost a square or not.
        
        Arguments:
            sprite {sprite onject} -- a sprite object.
            similarity_threshold {float} -- a float number between 0.0 and 1.0
            of the relative difference of the width and height of the sprite's 
            boundary box over which the sprite is not considered as a square.
        
        Returns:
            boolean -- a boolean value represents that the sprite is valid or not.
        """
        return 1 - similarity_threshold <= sprite.width / sprite.height <= 1 + similarity_threshold

    def __is_dense_sprite(self, sprite, density_threshold):
        """
        Check sprite is considered as a dense or not.
        
        Arguments:
            sprite {sprite onject} -- a sprite object.
            density_threshold {float} -- a float number between 0.0 and 1.0 representing
            the relative difference between the number of pixels of a sprite and the surface
            area of the boundary box of this sprite, over which the sprite is considered as dense.
        
        Returns:
            boolean -- a boolean value represents that the sprite is valid or not.
        """
        return sprite.pixels / (sprite.width * sprite.height) > density_threshold

    def __random_color(self, label_color):
        """
        Generate a tuple of color which is not in the value of label_color dict.
        """
        color = tuple([random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255)])

        while color in label_color.values():
            color = tuple([random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255)])

        return color

    def __sprite_checker(self, conditions, value, special_value):
        """
        Detect all the special case for draw the boundary box.
        
        Arguments:
            conditions {array} -- a list represents for the special cases.
            value {object} -- a sprite object.
            special_value {array} -- a list of value in the special cases.
        
        Returns:
            boolean -- a boolean value represents that the sprite is valid or not.
        """
        data = {0: self.__is_valid_surface_area, 
                1: self.__is_square_sprite,
                2: self.__is_dense_sprite}

        return all([data[element](value, special_value[element]) for element in conditions])

    def __update_sprites(self, sprites):
        """
        Map each value of each key (label) to Sprite object and return it.
        """
        for label, value in sprites.items():
            min_y = min(value, key=lambda x: x[0])[0]
            min_x = min(value, key=lambda x: x[1])[1]

            max_y = max(value, key=lambda x: x[0])[0]
            max_x = max(value, key=lambda x: x[1])[1]

            sprites[label] = Sprite(label, min_y, min_x, max_y, max_x, len(value))

        return sprites

    def create_sprite_labels_image(self, min_surface_area=None,
        similarity_threshold=None, density_threshold=None, background_color=()):
        """
        Create an image of equal dimension (width and height) 
        as the original image that was passed to the class.

        Draws the masks of the sprites at the exact same position
        that the sprites were in the original image with
        a random uniform color (one color per sprite mask).
        """
        if not self.__sprite_labels_image:
            if len(background_color) == 0:
                background_color = (255, 255, 255)

            # Find all sprites and get the label map of the image.
            sprites, label_map = self.find_sprites()

            max_row = len(label_map)
            max_column = len(label_map[0])

            # Create an image equal dimension (width and height) as the original image
            image = Image.new('RGB', (max_column, max_row), background_color)

            label_color = self.__generate_color_dict(sprites, background_color)

            image = self.__change_image_pixel_color(
                max_row, max_column, label_map, label_color, image)

            image = self.__change_bounding_boxes_color(sprites, label_color, image,
            min_surface_area, similarity_threshold, density_threshold)

            self.__sprite_labels_image = image

        return self.__sprite_labels_image

    def find_sprites(self):
        """
        Detect all the sprites of the image.

        The function returns a tuple (sprites, label_map) where:

        + Sprites: A collection of key-value pairs (a dictionary) 
        where each key-value pair maps the key (the label of a sprite)
        to its associated value (a Sprite object);

        + Label_map: A 2D array of integers of equal dimension 
        (width and height) as the original image where the sprites 
        are packed in. The label_map array maps each pixel of the 
        image passed to the function to the label of the sprite this 
        pixel corresponds to, or 0 if this pixel doesn't belong
        to a sprite (e.g., background color).
        """
        if not self.__sprites and not self.__label_map:
            label_map = LabelMap()
            width, height = self.__image.width, self.__image.height
            label_map.init_map(height, width)

            sprites = {}
            label = 1
            background_color = self.background_color

            # Scan all pixels in the image.
            for row in range(height):
                for column in range(width):
                    current_p = (column, row)
                    color = self.__image.getpixel(current_p)

                    # Check the pixel is background color or not and
                    # is it has the label in the label map or not.
                    if color != background_color and label_map.check_pixel(row, column):
                        sprites[label] = [current_p]
                        next_pixels = [current_p]

                        # Check all pixels related with the point under consideration.
                        while(next_pixels):
                            pixel = next_pixels.pop(0)
                            next_pixels, sprites, label_map = self.__check_pixel_neighbours(
                                pixel, next_pixels, sprites, label_map, background_color, label)

                        label += 1

            # Update the value for sprites to return.
            self.sprites = self.__update_sprites(sprites)

            # Get the label map for return.
            self.label_map = label_map.label_map

        return self.sprites, self.label_map