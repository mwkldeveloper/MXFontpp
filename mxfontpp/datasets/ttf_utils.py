"""
MX-Font
Copyright (c) 2021-present NAVER Corp.
MIT license
"""

from fontTools.ttLib import TTFont
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import PIL


def get_defined_chars(fontfile):
    ttf = TTFont(fontfile)
    chars = [chr(y) for y in ttf["cmap"].tables[0].cmap.keys()]
    return chars


def get_filtered_chars(fontpath):
    ttf = read_font(fontpath)
    defined_chars = get_defined_chars(fontpath)
    avail_chars = []

    for char in defined_chars:
        img = np.array(render(ttf, char))
        if img.mean() == 255.:
            pass
        else:
            avail_chars.append(char.encode('utf-16', 'surrogatepass').decode('utf-16'))

    return avail_chars


def read_font(fontfile, size=150):
    font = ImageFont.truetype(str(fontfile), size=size)
    return font


def render(font, char, size=(128, 128), pad=20):
    pil_version = PIL.__version__
    # Convert version string to tuple of integers for proper comparison
    version_parts = tuple(map(int, pil_version.split(".")))
    if version_parts > (9, 5, 0):
        bbox = font.getbbox(char)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:
        width, height = font.getsize(char)

    max_size = max(width, height)

    if width < height:
        start_w = (height - width) // 2 + pad
        start_h = pad
    else:
        start_w = pad
        start_h = (width - height) // 2 + pad

    img = Image.new("L", (max_size+(pad*2), max_size+(pad*2)), 255)
    draw = ImageDraw.Draw(img)
    draw.text((start_w, start_h), char, font=font)
    img = img.resize(size, 2)
    return img


# def render(font, char, size=(128,128),pad=20):
#     image_resolution = size[0]
    
#     image = Image.new('L', (image_resolution, image_resolution), color='white')
#     draw = ImageDraw.Draw(image)
    
#     # Calculate the position to center the character in the image
#     text_width, text_height = draw.textsize(char, font)
#     x = (image_resolution - text_width) // 2
#     y = (image_resolution - text_height) // 1.2
    
#     draw.text((x, y), char, font=font, fill='black')
#     return image