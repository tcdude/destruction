
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

import sdl2

from scene import Scene
import graphics


class Placement(Scene):
    def __init__(self, root):
        super().__init__(root)
        self._nodes = {}
        self._data = None
        self._init = False

    def _init_nodes(self):
        rx, ry = self.root.resolution
        
        im_grid = graphics.build_grid(rx * 0.9, ry * 0.7, 46, 20)
        slen = int(im_grid.size[0] / 46 - 2)
        start_x = int(rx / 2 - im_grid.size[0] / 2)
        start_y = int(ry / 2 - im_grid.size[1] / 2)
        self._nodes = {
            'grid': self.root.new_node(
                im_grid,
                start_x,
                start_y
            )
        }
        im_rects = [
            graphics.build_rect(slen),
            graphics.build_rect(slen, color=graphics.BLACK),
            graphics.build_rect(slen, color=graphics.RED),
            graphics.build_rect(slen, color=graphics.BLUE),
            graphics.build_rect(slen, color=graphics.GREEN),
        ]
        for x in range(46):
            for y in range(20):
                self._nodes[(x, y)] = self.root.new_multi_node(
                    im_rects,
                    start_x + (x + 1) * 2 + x * slen,
                    start_y + (y + 1) * 2 + y * slen
                )

    def process(self):
        pass

    def enter(self):
        if not self._init:
            self._data = self.root.scene_data
            self._data['p'] = 0
            self._data['nodes'] = [{}, {}]

            self._init_nodes()
            self._init = True
        self.root.event_handler.reset()
        self.root.event_handler.register(
            sdl2.SDL_MOUSEBUTTONUP,
            self.mouse_click,
            button=sdl2.SDL_BUTTON_LEFT
        )

        for node in self._nodes.values():
            node.show()

    def exit(self):
        for node in self._nodes.values():
            node.hide()

    def mouse_click(self):
        self.root.request('SpeciesSelection')

