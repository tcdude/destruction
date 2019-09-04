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

import time

import sdl2.ext


class HWRenderer(sdl2.ext.TextureSpriteRenderSystem):
    def __init__(self, window):
        super(HWRenderer, self).__init__(window)
        self.renderer = self.sdlrenderer

    def render(self, components, **kwargs):
        self._renderer.clear()
        super(HWRenderer, self).render(components, **kwargs)


class Game(object):
    def __init__(self, resolution=(1280, 720), grid=(100, 100), max_food=100):
        self._resolution = resolution
        self._grid = grid
        self._max_food = max_food
        
        self._world = sdl2.ext.World()
        sdl2.ext.init()
        self._window = sdl2.ext.Window('Fight of Life', size=self._resolution)
        self._window.show()

        self._renderer = HWRenderer(self._window)
        self._factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE,
            renderer=self._renderer
        )
        self._world.add_system(self._renderer)

        time.sleep(2)
        sdl2.ext.quit()
