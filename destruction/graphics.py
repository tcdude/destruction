"""
MIT License

Copyright (c) 2019 tcdude

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import ctypes

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sdl2.ext


sdl2.ext.init()
d, h, v = ctypes.c_float(0.0), ctypes.c_float(0.0), ctypes.c_float(0.0)
_ = sdl2.SDL_GetDisplayDPI(
    0, 
    ctypes.byref(d),
    ctypes.byref(h),
    ctypes.byref(v)
)

BASE_DPI = 200
if d.value > 0:
    SCALE = d.value / BASE_DPI
elif h.value > 0:
    SCALE = h.value / BASE_DPI
elif v.value > 0:
    SCALE = v.value / BASE_DPI
else:
    SCALE = 1.0

FONT_SMALL = ImageFont.truetype('resources/437tt.ttf', size=int(20 * SCALE))
FONT_MEDIUM = ImageFont.truetype('resources/437tt.ttf', size=int(36 * SCALE))
FONT_LARGE = ImageFont.truetype('resources/437tt.ttf', size=int(64 * SCALE))
WHITE = 255, 255, 255, 255
BLACK = 0, 0, 0, 255
GREY = 70, 70, 70, 255
LIGHTGREY = 160, 160, 160, 255
RED = 255, 0, 0, 255
GREEN = 0, 255, 0, 255
BLUE = 0, 0, 255, 255
TRANSPARENT = 0, 0, 0, 0


def build_text(text, fg=WHITE, bg=BLACK, font=FONT_MEDIUM):
    """Return a PIL.Image() of the text."""
    sx, sy = font.getsize_multiline(text)
    img = Image.new('RGBA', (sx, int(sy * 1.5)), bg)
    draw = ImageDraw.Draw(img)
    draw.multiline_text((0, 0), text, fill=fg, font=font)
    return img


def build_button(
        text, 
        fg=WHITE, 
        bg=BLACK, 
        font=FONT_MEDIUM, 
        hover_fg=BLACK, 
        hover_bg=WHITE,
        line_width=2
    ):
    """Return a tuple of 2 PIL.Image() objects (normal/hover)."""
    text_size = font.getsize_multiline(text)
    img = Image.new('RGBA', (text_size[0] + 20, text_size[1] + 30), bg)
    draw = ImageDraw.Draw(img)
    if line_width:
        draw.rectangle(
            [1, 1, img.size[0] - 2, img.size[1] - 2], 
            outline=fg, 
            width=line_width
        )
    draw.multiline_text((10, 10), text, fill=fg, font=font)
    img_hover = Image.new(
        'RGBA', 
        (text_size[0] + 20, text_size[1] + 30), 
        hover_bg
    )
    draw = ImageDraw.Draw(img_hover)
    if line_width:
        draw.rectangle(
            [1, 1, img_hover.size[0] - 2, img_hover.size[1] - 2], 
            outline=hover_fg, 
            width=line_width
        )
    draw.multiline_text((10, 10), text, fill=hover_fg, font=font)
    return img, img_hover


def build_grid(
        width, 
        height, 
        h_cells, 
        v_cells, 
        fg=WHITE, 
        bg=TRANSPARENT, 
        line_width=2
    ):
    """Returns a PIL.Image() of a grid of quads."""
    c_width = int(width / h_cells)
    c_height = int(height / v_cells)
    c_sidelen = min(c_width, c_height)
    img = Image.new(
        'RGBA', 
        (h_cells * c_sidelen + line_width, v_cells * c_sidelen + line_width), 
        bg
    )
    draw = ImageDraw.Draw(img)
    for x in range(h_cells + 1):
        lx = min(x * c_sidelen, img.size[0] - line_width)
        draw.line(
            [lx, 0, lx, img.size[1] - line_width], 
            fill=fg, 
            width=line_width
        )
    for y in range(v_cells + 1):
        ly = min(y * c_sidelen, img.size[1] - line_width)
        draw.line(
            [0, ly, img.size[0] - line_width, ly], 
            fill=fg, 
            width=line_width
        )
    return img


def build_rect(width, height=None, color=GREY):
    size = width, height or width
    return Image.new('RGBA', size, color)

