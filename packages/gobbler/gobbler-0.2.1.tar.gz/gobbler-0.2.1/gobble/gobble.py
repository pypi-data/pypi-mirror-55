#!/usr/bin/env python

# __author__ = "Ray Sharma"
# __copyright__ = "Copyright 2019, Ray Sharma"
# __maintainer__ = "Ray Sharma"
# __email__ = "ramon.sharma1@gmail.com"

from PIL import Image
from os import path
from glob import glob
from random import choice
from sys import exit


def gobble(image_number=None):
    """Displays a gobble image

    Pulls a gobble image from the ./assets/ directory and displays the image. If given an integer argument, attempts to
    pull the corresponding image, otherwise pulls a random image.

    Args:
        image_number (int, optional): Image number to show, defaults to None.
    """
    image_name = None
    assets_dir = path.join(path.dirname(__file__), 'assets')
    all_images = glob(path.join(assets_dir, '*.png'))
    if image_number is None:
        image_name = choice(all_images)
    else:
        try:
            image_name = all_images[image_number - 1]
        except (TypeError, IndexError) as err:
            print(err)
            exit()

    im_file = path.join(assets_dir, image_name)
    Image.open(im_file).show()
    print('gobble')


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=
        'A turkey-themed image catalog featuring over 99 hand-picked images to boost the holiday mood.'
    )
    parser.add_argument('-n', '--num', dest='num', default=None, type=int,
                        help='Specify image number')
    arguments = parser.parse_args()
    gobble(arguments.num)
