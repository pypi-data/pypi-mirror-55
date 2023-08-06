# -*- encoding: utf-8 -*-
"""TODO: Not working usefully."""

from liar.ijusthelp import rewrite_dict

# import gizeh
# from PIL import Image
# import math
# import numpy as np
# from liar.iamprimitive import IAmPrimitive
# from liar.ijusthelp import rewrite_dict


class IPictureIt(object):
    """IPictureIt to make simple images. """

    # white_areas = (red == 255) & (blue == 255) & (green == 255)
    # red_areas = (red == 255) & (blue == 0) & (green == 0)
    # green_areas = (red == 0) & (blue == 0) & (green == 255)
    # blue_areas = (red == 0) & (blue == 255) & (green == 0)
    #
    # def person(path):
    #     im = Image.open(path)
    #     im = im.convert('RGBA')
    #     im.show()
    #     data = np.array(im)
    #     #red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
    #     # Replace white with red... (leaves alpha values alone...)
    #     data[..., :-1][red_areas.T] = choice(hair_color)
    #     im2 = Image.fromarray(data)
    #     data[..., :-1][green_areas.T] = choice(accessory_color)
    #     im2 = Image.fromarray(data)
    #     data[..., :-1][blue_areas.T] = choice(skin_tones)
    #     im2 = Image.fromarray(data)
    #     im2.show()

    class Convert(object):
        def htmlhex_2_rgba(htmlhex):
            htmlhex = htmlhex.replace("#", "")
            return tuple(c for c in bytes.fromhex(htmlhex))

        def htmlhex_2_rgb1(htmlhex):
            htmlhex = htmlhex.replace("#", "")
            return tuple(c / 255 for c in bytes.fromhex(htmlhex))

        # don't need this but Tim finds it useful to have for reference
        def rgba_2_htmlhex(rgba):
            return "".join(map(chr, rgb)).encode("hex")

    class Draw(object):
        def draw_shape_list(shape_list, width, height, filename):
            surface = (
                None
            )  # gizeh.Surface(width=width, height=height) # in pixels
            for shape in shape_list:
                shape.draw(surface)
            surface.write_to_png("liar/faces/{}.png".format(filename))

    class Values(object):
        def get_rgba_col():
            return (
                IAmPrimitive.Values.get_int(0, 255),
                IAmPrimitive.Values.get_int(0, 255),
                IAmPrimitive.Values.get_int(0, 255),
            )

        def get_rgb1_col():
            return (
                IAmPrimitive.Values.get_dec(0, 1),
                IAmPrimitive.Values.get_dec(0, 1),
                IAmPrimitive.Values.get_dec(0, 1),
            )

        def get_htmlhex_col():
            return IPictureIt.Convert.rgba_2_htmlhex(
                IPictureIt.Values.get_rgba_col()
            )

        def get_col_from_list(color_list):
            return randint(min, max)
