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


class MainMenu(Scene):
    def __init__(self, root):
        super().__init__(root)
        self._sprites = {}
        self._bb = {}

    def process(self):
        if self._bb['vs'][0] <= self.root.mouse_pos[0] <= self._bb['vs'][2] \
                and self._bb['vs'][1] <= self.root.mouse_pos[1] <= self._bb['vs'][3]:
            self._sprites['vs'].depth = 0
            self._sprites['vs'].position = -self._bb['vs'][0], -self._bb['vs'][1] 
            self._sprites['vs_hov'].depth = 1
            self._sprites['vs_hov'].position = self._bb['vs'][:2]
        else:
            self._sprites['vs'].depth = 1
            self._sprites['vs'].position = self._bb['vs'][:2] 
            self._sprites['vs_hov'].depth = 0
            self._sprites['vs_hov'].position = -self._bb['vs'][0], -self._bb['vs'][1] 

        self.root.render(list(self._sprites.values()))

    def enter(self):
        self._sprites = {}
        self.root.event_handler.reset()
        self.root.event_handler.register(
            sdl2.SDL_MOUSEBUTTONUP,
            self.mouse_click,
            button=sdl2.SDL_BUTTON_LEFT
        )

        i, i_hov = graphics.build_button('2 Players VS')
        i.save('resources/2player.png')
        i_hov.save('resources/2player_hov.png')
        s1 = self.factory.from_image('resources/2player.png')
        pos = (
            int(self.root.resolution[0] / 2 - i.size[0] / 2), 
            int(self.root.resolution[1] / 2 - i.size[1] * 1.5)
        )
        self._bb['vs'] = pos + (pos[0] + i.size[0], pos[1] + i.size[1])
        s1.position = pos
        s1.depth = 1
        self._sprites['vs'] = s1
        s2 = self.factory.from_image('resources/2player_hov.png')
        s2.position = -pos[0], -pos[1]
        s2.depth = 0
        self._sprites['vs_hov'] = s2

    def exit(self):
        pass

    def mouse_click(self):
        print('click')

