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

import sdl2
import sdl2.ext
from sdl2 import endian, surface, pixels

import fol
from . import graphics
from . import node
from .event_handler import EventHandler
from .render import HWRenderer
from .menu import MainMenu
from .species import SpeciesSelection
from .placement import Placement
from .simulation import Simulation


class Game(object):
    def __init__(self, resolution=(1280, 720), grid=(100, 100), max_food=100):
        self._resolution = (
            int(resolution[0] * graphics.SCALE), 
            int(resolution[1] * graphics.SCALE)
        )
        self._grid = grid
        self._max_food = max_food
        
        self._scenes = {
            'MainMenu': MainMenu(self),
            'SpeciesSelection': SpeciesSelection(self),
            'Placement': Placement(self),
            'Simulation': Simulation(self),
        }
        self._active_scene = None
        self._scene_data = {}

        # self._world = sdl2.ext.World()
        self._nodes = []
        self._window = None
        self._factory = None
        self._renderer = None

        self._grid = None
        self._cells = {}
        self._food = {}
        self._grid_slen = 0

        self._clean_exit = False
        self._running = False
        self._active_sprites = []
        self._mouse_pos = 0, 0

        self._event_handler = EventHandler(self.quit)
        self._species_a = fol.Species()
        self._species_b = fol.Species()
        self._placement = [[], []]

    @property
    def mouse_pos(self):
        return self._mouse_pos

    @property
    def event_handler(self):
        return self._event_handler

    @property
    def factory(self):
        return self._factory

    @property
    def resolution(self):
        return self._resolution

    @property
    def render(self):
        return self._renderer.render

    @property
    def species_a(self):
        return self._species_a

    @property
    def species_b(self):
        return self._species_b

    @property
    def placement(self):
        return self._placement

    @property
    def scene_data(self):
        if self._active_scene is None:
            raise ValueError('No active scene set.')
        if self._active_scene not in self._scene_data:
            self._scene_data[self._active_scene] = {}
        return self._scene_data[self._active_scene]

    @property
    def grid(self):
        return self._grid

    @property
    def cells(self):
        return self._cells

    @property
    def food(self):
        return self._food

    @property
    def grid_slen(self):
        return self._grid_slen

    def setup_grid(self):
        rx, ry = self.resolution
        im_grid = graphics.build_grid(rx * 0.9, ry * 0.7, 48, 21)
        slen = int(im_grid.size[0] / 48 - 2)
        start_x = int(rx / 2 - im_grid.size[0] / 2)
        start_y = int(ry / 2 - im_grid.size[1] / 2)
        pop_y = int(start_y + im_grid.size[1] * 1.05)
        self._grid = self.new_node(
            im_grid,
            start_x,
            start_y
        )
        self._grid.hide()
        im_rects = [
            graphics.build_rect(slen),
            graphics.build_rect(slen, color=graphics.BLACK),
            graphics.build_rect(slen, color=graphics.RED),
            graphics.build_rect(slen, color=graphics.BLUE),
            graphics.build_rect(slen, color=graphics.GREEN),
        ]
        for x in range(48):
            for y in range(21):
                self._cells[(x, y)] = self.new_multi_node(
                    im_rects,
                    start_x + (x + 1) * 2 + x * slen,
                    start_y + (y + 1) * 2 + y * slen
                )
                self._cells[(x, y)].hide()
                self._cells[(x, y)].depth = 0
        self._grid_slen = slen
        sred = 150
        sgreen = 70
        dred = 130
        dgreen = -150
        im_rects = []
        for i in range(10):
            im_rects.append(
                graphics.build_rect(
                    slen, 
                    color=(
                        sred - dred // 9 * i,
                        sgreen - dgreen // 9 * i,
                        0,
                        255
                    )
                )
            )

        for x in range(48):
            for y in range(21):
                self._food[(0, x, y)] = self.new_multi_node(
                    im_rects,
                    start_x + (x + 1) * 2 + x * slen,
                    start_y + (y + 1) * 2 + y * slen
                )
                self._food[(0, x, y)].hide()
                self._food[(0, x, y)].depth = 1

    def request(self, scene):
        if scene not in self._scenes:
            raise ValueError(f'Unknown scene: "{scene}"')
        if self._active_scene is not None:
            self._active_scene.exit()
        self._active_scene = self._scenes[scene]
        self._active_scene.enter()

    def log(self, msg, *args):
        print(msg, *args)

    def quit(self):
        self._running = False
    
    def new_node(self, image, x=0, y=0):
        s = self.image2sprite(image)
        self._nodes.append(node.Node(s, x, y))
        return self._nodes[-1]
    
    def new_button(self, image, image_hov, x=0, y=0):
        s = self.image2sprite(image)
        s_hov = self.image2sprite(image_hov)
        self._nodes.append(node.Button(s, s_hov, self, x, y))
        return self._nodes[-1]

    def new_multi_node(self, images, x=0, y=0):
        sprites = [self.image2sprite(img) for img in images]
        self._nodes.append(node.MultiNode(sprites, x, y))
        return self._nodes[-1]

    def remove_node(self, node):
        if node in self._nodes:
            self._nodes.pop(self._nodes.index(node))
        else:
            raise ValueError('Unknown Node')

    def image2sprite(self, image):
        mode = image.mode
        width, height = image.size
        rmask = gmask = bmask = amask = 0
        if mode in ("1", "L", "P"):
            # 1 = B/W, 1 bit per byte
            # "L" = greyscale, 8-bit
            # "P" = palette-based, 8-bit
            pitch = width
            depth = 8
        elif mode == "RGB":
            # 3x8-bit, 24bpp
            if endian.SDL_BYTEORDER == endian.SDL_LIL_ENDIAN:
                rmask = 0x0000FF
                gmask = 0x00FF00
                bmask = 0xFF0000
            else:
                rmask = 0xFF0000
                gmask = 0x00FF00
                bmask = 0x0000FF
            depth = 24
            pitch = width * 3
        elif mode in ("RGBA", "RGBX"):
            # RGBX: 4x8-bit, no alpha
            # RGBA: 4x8-bit, alpha
            if endian.SDL_BYTEORDER == endian.SDL_LIL_ENDIAN:
                rmask = 0x000000FF
                gmask = 0x0000FF00
                bmask = 0x00FF0000
                if mode == "RGBA":
                    amask = 0xFF000000
            else:
                rmask = 0xFF000000
                gmask = 0x00FF0000
                bmask = 0x0000FF00
                if mode == "RGBA":
                    amask = 0x000000FF
            depth = 32
            pitch = width * 4
        else:
            # We do not support CMYK or YCbCr for now
            raise TypeError("unsupported image format")

        pxbuf = image.tobytes()
        imgsurface = surface.SDL_CreateRGBSurfaceFrom(pxbuf, width, height,
                                                      depth, pitch, rmask,
                                                      gmask, bmask, amask)
        if not imgsurface:
            raise SDLError()
        imgsurface = imgsurface.contents
        # the pixel buffer must not be freed for the lifetime of the surface
        imgsurface._pxbuf = pxbuf

        if mode == "P":
            # Create a SDL_Palette for the SDL_Surface
            def _chunk(seq, size):
                for x in range(0, len(seq), size):
                    yield seq[x:x + size]

            rgbcolors = image.getpalette()
            sdlpalette = pixels.SDL_AllocPalette(len(rgbcolors) // 3)
            if not sdlpalette:
                raise SDLError()
            SDL_Color = pixels.SDL_Color
            for idx, (r, g, b) in enumerate(_chunk(rgbcolors, 3)):
                sdlpalette.contents.colors[idx] = SDL_Color(r, g, b)
            ret = surface.SDL_SetSurfacePalette(imgsurface, sdlpalette)
            # This will decrease the refcount on the palette, so it gets
            # freed properly on releasing the SDL_Surface.
            pixels.SDL_FreePalette(sdlpalette)
            if ret != 0:
                raise SDLError()

        return self.factory.from_surface(imgsurface, free=True)

    def run(self):
        self._window = sdl2.ext.Window('Fight of Life', size=self._resolution)
        self._window.show()

        self._renderer = HWRenderer(self._window)
        self._factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE,
            renderer=self._renderer
        )
        # self._world.add_system(self._renderer)
        self.setup_grid()
        self._running = True
        self.request('MainMenu')
        
        while self._running:
            self._update_mouse()
            self.event_handler()
            # self._renderer.render(self._active_sprites)
            if self._active_scene is not None:
                self._active_scene.process()
                self._render_visible()
            sdl2.timer.SDL_Delay(10)

        sdl2.ext.quit()

    def _render_visible(self):
        sprites = []
        for node in self._nodes:
            if node.visible:
                sprites.append(node.sprite)
        self.render(sprites)

    def _update_mouse(self):
        x, y = ctypes.c_int(0), ctypes.c_int(0)
        _ = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        self._mouse_pos = x.value, y.value

if __name__ == '__main__':
    Game().run()

