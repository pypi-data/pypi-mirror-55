#!/usr/bin/python3

from PIL import Image
import numpy as np
import random


class Sprite():
    """
        Create a sprite object wihth label and position
    """
    def __init__(self, label, x1, y1, x2, y2, pxl_count):
        """
        Arguments:
            label {int} -- Sprite label
            x1 {int} -- left position of sprite
            y1 {int} -- top position of sprite
            x2 {int} -- right position of sprite
            y2 {int} -- bottom position of sprite
        
        Raises:
            ValueError: Arguments is not type int
            ValueError: Arguments contains negative number
            ValueError: x1 < x2 or y1 < y2
        """
        if any(not isinstance(e, int) for e in (label, x1, y1, x2, y2)):
            raise ValueError('Invalid coordinates')
        if any(e < 0 for e in (label, x1, y1, x2, y2)):
            raise ValueError('Invalid coordinates')
        if x1 > x2 or y1 > y2:
            raise ValueError('Invalid coordinates')
        self.__label = label
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__width = self.__x2 - self.__x1 + 1
        self.__height = self.__y2 -  self.__y1 + 1
        self.__pxl_count = pxl_count

    @property
    def label(self):
        return self.__label 

    @property
    def total_pixel(self):
        return self.__pxl_count

    @property
    def center(self):
        center_x = (self.__x1 + self.__x2) // 2
        center_y = (self.__y1 + self.__y2) // 2
        return (center_x, center_y)

    @property
    def top_left(self):
        return (self.__x1, self.__y1)

    @property
    def bottom_right(self):
        return (self.__x2, self.__y2)

    @property
    def width(self) :
        return self.__width

    @property
    def height(self):
        return self.__height


class SpriteSheet():
    """Container of all Image Sprite Detection Method
    
    Raises:
        FileNotFoundError: When file path is not found
    """
    def __init__(self, fd, background_color=None):
        if isinstance(fd, Image.Image):
            self.image = fd
        else:
            self.image = Image.open(fd)
        if not background_color and self.image.mode != 'RGBA':
            background_color = self.find_most_common_color(self.image)
        self.__background_color = background_color
        self.sprites = None
        self.__label_map = None
        self.__sprite_colors = {}
        self.__mask = None
    
    @property
    def background_color(self):
        return self.__background_color

    @staticmethod
    def find_most_common_color(img):
        """Find the most commonly used color in the image
        
        Arguments:
            img {Image} -- PIL Image object
        
        Returns:
            tuple or int -- The most commly used color of image, tuple or int based on type
        """
        colors = img.getcolors(maxcolors=img.width*img.height)
        return max(colors, key=lambda item: item[0])[1]

    def __is_background(self, point):
        """Check if an image pixel is background or not
        
        Arguments:
            point {tuple} -- Color of the pixel
            background_color {tuple} -- Color of the image backgrounf
        
        Returns:
            boolean -- Pixel is background or not
        """
        background = self.background_color
        mode = self.image.mode
        if not background and mode == 'RGBA':
            if point[3] == 0:
                return True
            else: 
                return False
        if mode not in ['RGB', 'RGBA'] and point == background:
            return True
        elif mode not in ['RGB', 'RGBA']: 
            return False
        if list(point) == list(background):
            return True
        else:
            return False
        
    def __create_sprite(self, label, label_map, sprite_info):
        """Create a Sprite object with specified label and label_map
        
        Arguments:
            label {int} -- Sprite label
            label_map {2d list} -- Label map contains sprite label
        
        Returns:
            Sprite -- Sprite object with label argument
        """
        sprite = {'label': label}
        sprite['x1'] = sprite_info[1]
        sprite['y1'] = sprite_info[2]
        sprite['x2'] = sprite_info[3]
        sprite['y2'] = sprite_info[4]
        sprite['pxl_count'] = sprite_info[0]
        return Sprite(sprite['label'], sprite['x1'], sprite['y1'], 
                    sprite['x2'], sprite['y2'], sprite['pxl_count'])

    def __find_whole_sprite(self, label_map, lst_pixel, check_map, r_idx, c_idx, label):
        """Check out whole sprite from specified spite pixel
        
        Arguments:
            label_map {2d list} -- List corresponding to sprite label in image
            lst_pixel {2d list} -- List of all pixel in the image
            check_map {2d list} -- List of checked point 
            r_idx {int} -- Row index of found pixel
            c_idx {int} -- Col index of found pixel
            label {int} -- Label of the new sprite
        """
        sprite_point = [(r_idx, c_idx)]
        pxl_count = 0
        img_height = len(lst_pixel)
        img_width = len(lst_pixel[0])
        min_x = max_x = r_idx
        min_y = max_y = c_idx

        while len(sprite_point) > 0:
            row, col = sprite_point.pop(0)
            # Find all points which are the neighbor of this point
            # and belong to the sprite
            label_map[row][col] = label 
            pxl_count += 1

            for x, y in [(row - 1, col), (row + 1, col),
                        (row, col - 1), (row, col + 1),
                        (row - 1, col - 1), (row - 1, col + 1), 
                        (row + 1, col - 1), (row + 1, col + 1)]:
                # Check up, down, left, right

                if x in range(img_height) and \
                    y in range(img_width) and \
                    not check_map[x][y] and \
                    not self.__is_background(lst_pixel[x][y]):
                    check_map[x][y] = True
                    sprite_point.append((x, y))
                    
                    if x < min_x:
                        min_x = x 
                    if max_x < x:
                        max_x = x 
                    if y < min_y:
                        min_y = y
                    if max_y < y:
                        max_y = y 

        return pxl_count, min_x, min_y, max_x, max_y

    def find_sprites(self):
        """Get an image as argument and then find all sprites in that image 
        by checking each pixel's color
        
        Arguments:
            image {Image} -- Image to find sprites
        
        Returns:
            tuple -- Dictionary of sprite information and label_map of 
                corresponding sprites found
        """
        image = self.image
        width, height = image.size
        lst_pixel = np.asarray(image)
        label = 0 
        sprites = {}
        label_map = np.zeros((len(lst_pixel), len(lst_pixel[0])))
        check_map = np.zeros((len(lst_pixel), len(lst_pixel[0])), dtype=bool)


        for row_idx in range(height):
            for col_idx in range(width):   
                # Loop through an image
                point = lst_pixel[row_idx][col_idx]
                if not self.__is_background(point) and \
                    not check_map[row_idx][col_idx]: 
                    # Find the point that is not the background
                    label += 1
                    check_map[row_idx][col_idx] = True
                    sprite_info = self.__find_whole_sprite(label_map, lst_pixel, 
                                        check_map, row_idx, col_idx, label)
                    sprites[label] = self.__create_sprite(label, label_map, sprite_info)

        self.sprites = sprites
        self.__label_map = label_map
        return sprites, label_map

    def create_sprite_labels_image(self):
        """Create an image containing mask for all sprite based on label_map
        
        Arguments:
            sprites {dictionary} -- Container of all Sprite object
            label_map {2d list} -- Label_map of image
        
        Keyword Arguments:
            background_color {tuple} -- Background color of new image (default: {None}) 
        
        Returns:
            Image -- Image of all sprite mask
        """
        background_color = self.background_color
        if not background_color and not isinstance(background_color, int):
            mode = 'RGBA'
        elif isinstance(background_color, tuple) and len(background_color) == 4:
            mode = 'RGBA'
        else: 
            mode = 'RGB'
        
        if self.image.mode == 'L':
            background_color = (255, 255, 255)

        if not self.sprites:
            sprites, label_map = self.find_sprites()
        else:
            sprites = self.sprites
            label_map = self.__label_map
        image_size = (len(label_map[0]), len(label_map))
        self.__mask = Image.new(mode, image_size, background_color)
        self.__sprite_colors = {'0': background_color}

        for label in sprites.keys():
            # Create the dictionary of unique color for each sprite
            while True:
                red = random.randint(0, 255)
                green = random.randint(0, 255)
                blue = random.randint(0, 255)
                if not (red, green, blue) in [self.__sprite_colors[key] 
                        for key in self.__sprite_colors.keys()]:
                    if mode == 'RGBA':
                        self.__sprite_colors[label] = (red, green, blue, 255)
                    else:
                        self.__sprite_colors[label] =  (red, green, blue)
                    break 

        width, height = self.__mask.size

        for x in range(width):
            for y in range(height):
                # Fill the sprite with specific color based on label
                if label_map[y][x] != 0:
                    self.__mask.putpixel((x, y), self.__sprite_colors[label_map[y][x]])
        return self.__mask

    def make_sprite_border_image(self, sprites=None):
        if not self.__mask:
            self.create_sprite_labels_image()

        if not sprites:
            sprites = [self.sprites[key] for key in self.sprites.keys()]

        for sprite in sprites:
            label = sprite.label
            for x in range(sprite.top_left[0], sprite.bottom_right[0] + 1):
                self.__mask.putpixel((sprite.bottom_right[1], x), self.__sprite_colors[label])
                self.__mask.putpixel((sprite.top_left[1], x), self.__sprite_colors[label])

            for x in range(sprite.top_left[1], sprite.bottom_right[1] + 1):
                self.__mask.putpixel((x, sprite.top_left[0]), self.__sprite_colors[label])
                self.__mask.putpixel((x, sprite.bottom_right[0]), self.__sprite_colors[label])
        
        return self.__mask
            
