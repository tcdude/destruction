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

from .scene import Scene
from . import graphics
from . import aabb
from .assets import BUTTONS
from .assets import TITLES


class MainMenu(Scene):
    def __init__(self, root):
        super().__init__(root)
        self._nodes = {}
        self._init = False

    def _init_sprites(self):
        im_title = TITLES['fol']
        self._nodes['title'] = self.root.new_node(im_title)
        rx, ry = self.root.resolution
        self._nodes['title'].position = (
            int(rx / 2 - im_title.size[0] / 2),
            int(ry / 18)
        )
        buttons = (BUTTONS['vs'], BUTTONS['ai'], BUTTONS['quit'])
        x = int(rx / 2 - buttons[0][0].size[0] / 2)
        y_start = self._nodes['title'].y + self._nodes['title'].size[1]
        y_start += BUTTONS['vs'][0].size[1]
        for i, (im, im_hov) in enumerate(buttons):
            self._nodes[i] = self.root.new_button(im, im_hov)
            y = int(y_start + i * BUTTONS['vs'][0].size[1] * 1.3)
            self._nodes[i].position = x, y

    def process(self):
        pass

    def enter(self):
        if not self._init:
            self._init_sprites()
            self._init = True
        self.root.event_handler.register(
            sdl2.SDL_MOUSEBUTTONUP,
            self.mouse_click,
            button=sdl2.SDL_BUTTON_LEFT
        )
        for node in self._nodes:
            self._nodes[node].show()

    def exit(self):
        self.root.event_handler.reset()
        for node in self._nodes:
            self._nodes[node].hide()

    def mouse_click(self):
        mx, my = self.root.mouse_pos
        for i in range(3):
            if self._nodes[i].aabb.inside(mx, my):
                if i == 0:
                    self.root.request('SpeciesSelection')
                elif i == 1:
                    print('you wish...')
                elif i == 2:
                    self.root.quit()
                break

