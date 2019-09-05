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

import graphics
from event_handler import EventHandler
from render import HWRenderer
from menu import MainMenu
from species import SpeciesSelection
from placement import Placement
from simulation import Simulation


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
        
        self._world = sdl2.ext.World()
        self._window = None
        self._factory = None
        self._renderer = None

        self._clean_exit = False
        self._running = False
        self._active_sprites = []
        self._mouse_pos = 0, 0

        self._event_handler = EventHandler(self.quit)

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

    def run(self):
        self._window = sdl2.ext.Window('Fight of Life', size=self._resolution)
        self._window.show()

        self._renderer = HWRenderer(self._window)
        self._factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE,
            renderer=self._renderer
        )
        self._world.add_system(self._renderer)
        
        self._running = True
        self.request('MainMenu')
        
        while self._running:
            self._update_mouse()
            self.event_handler()
            # self._renderer.render(self._active_sprites)
            if self._active_scene is not None:
                self._active_scene.process()
            sdl2.timer.SDL_Delay(10)


        sdl2.ext.quit()

    def _update_mouse(self):
        x, y = ctypes.c_int(0), ctypes.c_int(0)
        _ = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        self._mouse_pos = x.value, y.value

if __name__ == '__main__':
    Game().run()

