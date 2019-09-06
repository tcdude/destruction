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
import aabb


EXT = '.png'
BUTTONS = {
    'vs': {
        'text': '2 Players VS',
        'path': 'resources/2player',
    },
    'train': {
        'text': 'Train AI',
        'path': 'resources/train_ai',
    },
    'quit': {
        'text': 'Quit',
        'path': 'resources/quit',
    },
}


class MainMenu(Scene):
    def __init__(self, root):
        super().__init__(root)
        self._sprites = {}
        self._bb = {}
        self._title_bb = None

    def init_sprites(self):
        im_title = graphics.build_text(
            'Fight of Life', 
            fg=graphics.RED, 
            font=graphics.FONT_LARGE
        )
        im_title.save('resources/title.png')
        rx, ry = self.root.resolution
        s = self.factory.from_image('resources/title.png')
        s.position = (
            int(rx / 2 - im_title.size[0] / 2),
            int(ry / 15)
        )
        self._title_bb = aabb.AABB(
            *s.position,
            s.x + im_title.size[0], 
            s.y + im_title.size[1]
        ) 
        self._sprites['title'] = s
        for i, k in enumerate(BUTTONS):
            im, im_hov = graphics.build_button(BUTTONS[k]['text'])
            im_name = BUTTONS[k]['path'] + EXT
            im_hov_name = BUTTONS[k]['path'] + '_hov' + EXT
            im.save(im_name)
            im_hov.save(im_hov_name)
            s1 = self.factory.from_image(im_name)
            x = int(self.root.resolution[0] / 2 - im.size[0] / 2)
            y_spacing = im.size[1] / 4
            y_tot = im.size[1] * len(BUTTONS) 
            y_tot += y_spacing * (len(BUTTONS) - 1)
            y = int(
                self.root.resolution[1] / 2 - y_tot 
                / 2 + i * im.size[1] + i * y_spacing
            )
            self._bb[k] = aabb.AABB(x, y, x + im.size[0], y + im.size[1])
            s1.position = x, y
            s1.depth = 1
            self._sprites[k] = s1
            s2 = self.factory.from_image(im_hov_name)
            s2.position = -x, -y
            s2.depth = 0
            self._sprites[k + '_hov'] = s2

    def process(self):
        mx, my = self.root.mouse_pos
        for k in self._bb:
            if self._bb[k].inside(mx, my):
                self._sprites[k].depth = 0
                self._sprites[k].position = -self._bb[k].x1, -self._bb[k].y1 
                self._sprites[k + '_hov'].depth = 1
                self._sprites[k + '_hov'].position = self._bb[k].x1, self._bb[k].y1
            else:
                self._sprites[k].depth = 1
                self._sprites[k].position = self._bb[k].x1, self._bb[k].y1
                self._sprites[k + '_hov'].depth = 0
                self._sprites[k + '_hov'].position = -self._bb[k].x1, -self._bb[k].y1
        self.root.render(list(self._sprites.values()))

    def enter(self):
        self._sprites = {}
        self.root.event_handler.reset()
        self.root.event_handler.register(
            sdl2.SDL_MOUSEBUTTONUP,
            self.mouse_click,
            button=sdl2.SDL_BUTTON_LEFT
        )
        self.init_sprites()

    def exit(self):
        pass

    def mouse_click(self):
        mx, my = self.root.mouse_pos
        for k in self._bb:
            if self._bb[k].inside(mx, my):
                print(f'clicked "{k}"')
                break

