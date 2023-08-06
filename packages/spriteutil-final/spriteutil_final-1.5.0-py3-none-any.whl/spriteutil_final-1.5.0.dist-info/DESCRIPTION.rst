# Image Sprite Detection Module
## What is it?
This is a Python module used for detection sprites from an image

## Why use this module?
* **Easy to use:** You just need to pass an image an get the result
* **Time saving:** This module is already built so you don't need to spend time for it anymore!


## Usage:
#### &ensp; Create a SpriteSheet object using:
##### &ensp;&nbsp; SpriteSheet(fd, background_color=None):

	@fd: the name and path (a string) that references an image file in the local file system;
	OR a pathlib.Path object that references an image file in the local file system ; a file object that MUST implement read(), seek(), and tell() methods, and be opened in binary mode;
	OR a Image object.

	@background_color: an integer if the mode is grayscale;
	OR a tuple (red, green, blue) of integers if the mode is RGB;
	OR a tuple (red, green, blue, alpha) of integers if the mode is RGBA. The alpha element is optional. If not defined, while the image mode is RGBA, the constructor considers the alpha element to be 255.

#### &ensp; Class SpriteSheet provides following methods:

##### &ensp;&nbsp; SpriteSheet.find_most_common_color(image):

	Find most used color in an Image object
	arg: image: MUST be an Image object
	Return most used color in the image with the same format image's mode

##### &ensp;&nbsp; SpriteSheet.object.create_sprite_labels_image():

	Create a mask image of initial image, and add a bounding box around each sprite,
	each sprite also have an unique random uniform color.
	Return an Image object.

##### &ensp;&nbsp; SpriteSheet.object.find_sprites():

	Detect sprites inside the image
	Return a 2D label map and a dict that stores:
	key: sprite's label
	value: its Sprite's object
	arg: image: MUST be an Image object

## Installation:
The project require Python 3.7+ to run

#### &ensp; FOR USER:
##### &emsp; In Terminal, use command:

	pip3 install spriteutil_final

#### &ensp; FOR DEVELOPMENT:
##### &emsp; Clone or Downloads the project, using this command and then edit anything you want:

	git clone https://github.com/intek-training-jsc/sprite-detection-longlamduc.git

## A Simple Example

	from spriteutil_final.spriteutil import SpriteSheet
	spritesheet = SpriteSheet('islands.png')
	sprites, label_map = spritesheet.find_sprites()
	img_mask = spritesheet.create_sprite_labels_image()
	img_mask.save('islands_label_mask.png')
	img_mask_with_border = spritesheet.make_sprite_border_image()
	img_mask.save('islands_label_mask_with_border.png')

## Contact:
&emsp;&emsp;&emsp; During the usage of the project, if you have any question, please contact me personally at INTEK HCM City or via my email: long.lam@f4.intek.edu.vn

## Contributors:
&emsp;&emsp;&emsp; Long LAM DUC from INTEK Institute, HCM City


