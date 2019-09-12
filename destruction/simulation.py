
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

import sdl2

from .scene import Scene
from .assets import BUTTONS
from .assets import TEXTS
from .assets import TITLES
from . import fol

MAX_FOOD = 500
STEP_TIME = 1 / 15


class Simulation(Scene):
    def __init__(self, root):
        super().__init__(root)
        self._nodes = {}
        self._init = False
        self._world = None
        self._running = False
        self._finished = False
        self._last_time = 0.0

    def _init_nodes(self):
        rx, ry = self.root.resolution
        self._nodes['title'] = self.root.new_node(
            TITLES['sim'],
            int(rx / 2 - TITLES['sim'].size[0] / 2),
            int(ry / 20)
        )
        self._nodes['grid'] = self.root.grid
        self._nodes.update(self.root.cells)
        self._nodes.update(self.root.food)
        self._nodes['start'] = self.root.new_button(
            *BUTTONS['start'],
            int(rx / 2 - BUTTONS['start'][0].size[0] / 2),
            int(ry - 1.5 * BUTTONS['start'][0].size[1])
        )
        rsx = BUTTONS['replay'][0].size[0] + TEXTS[9].size[0]
        msx = BUTTONS['menu'][0].size[0]
        replay_x = int(rx / 2 - (rsx + msx) / 2)
        menu_x = replay_x + rsx
        self._nodes['replay'] = self.root.new_button(
            *BUTTONS['replay'],
            replay_x,
            int(ry - 1.5 * BUTTONS['replay'][0].size[1])
        )
        self._nodes['menu'] = self.root.new_button(
            *BUTTONS['menu'],
            menu_x,
            int(ry - 1.5 * BUTTONS['replay'][0].size[1])
        )
        p_y = self._nodes['grid'].size[1] + self._nodes['grid'].y
        a_x = self._nodes['grid'].x
        b_x = a_x + self._nodes['grid'].size[0] - 4 * TEXTS[9].size[0]
        n_sp = TEXTS[9].size[0]
        self._nodes['popa1'] = self.root.new_multi_node(
            [TEXTS[i] for i in range(10)],
            a_x,
            p_y
        )
        self._nodes['popa2'] = self.root.new_multi_node(
            [TEXTS[i] for i in range(10)],
            a_x + n_sp,
            p_y
        )
        self._nodes['popa3'] = self.root.new_multi_node(
            [TEXTS[i] for i in range(10)],
            a_x + 2 * n_sp,
            p_y
        )
        self._nodes['popa4'] = self.root.new_multi_node(
            [TEXTS[i] for i in range(10)],
            a_x + 3 * n_sp,
            p_y
        )
        self._nodes['popb1'] = self.root.new_multi_node(
            [TEXTS[i] for i in range(10)],
            b_x,
            p_y
        )
        self._nodes['popb2'] = self.root.new_multi_node(
            [TEXTS[i] for i in range(10)],
            b_x + n_sp,
            p_y
        )
        self._nodes['popb3'] = self.root.new_multi_node(
            [TEXTS[i] for i in range(10)],
            b_x + 2 * n_sp,
            p_y
        )
        self._nodes['popb4'] = self.root.new_multi_node(
            [TEXTS[i] for i in range(10)],
            b_x + 3 * n_sp,
            p_y
        )

    def process(self):
        ft = time.perf_counter()
        if self._running and ft - self._last_time >= STEP_TIME:
            self.simulate()
            self._last_time = ft

    def enter(self):
        if not self._init:
            self._init_nodes()
            self._init = True
        self._world = fol.World(
            48, 
            21, 
            self.root.species_a, 
            self.root.species_b, 
            MAX_FOOD
        )
        for s, p in enumerate(self.root.placement):
            for x, y in p:
                self._world.toggle(s + 1, x, y)
        self._running = False
        self._finished = False
        for node in self._nodes.values():
            node.show()
        self.clear()
        self._nodes['replay'].hide()
        self._nodes['menu'].hide()
        self.root.event_handler.reset()
        self.root.event_handler.register(
            sdl2.SDL_MOUSEBUTTONUP,
            self.mouse_click,
            button=sdl2.SDL_BUTTON_LEFT
        )

    def exit(self):
        for node in self._nodes.values():
            node.hide()

    def clear(self):
        self.update_pop_count()
        for x in range(48):
            for y in range(21):
                k = x, y
                if k in self.root.placement[0]:
                    a = 2
                elif k in self.root.placement[1]:
                    a = 3
                else:
                    a = 1
                if a > 1:
                    self._nodes[k].set_active(a)
                    self._nodes[k].depth = 1
                    self._nodes[(0, ) + k].depth = 0
                else:
                    self._nodes[(0, ) + k].set_active(9)
                    self._nodes[k].depth = 0
                    self._nodes[(0, ) + k].depth = 1

    def simulate(self):
        if not self._running:
            return
        self._world.simulate_step()
        cells = self._world.cells
        food = self._world.food
        for x in range(48):
            for y in range(21):
                c = cells[x + y * 48]
                if c:
                    self._nodes[(x, y)].set_active(c + 1)
                    self._nodes[(x, y)].depth = 1
                    self._nodes[(0, x, y)].depth = 0
                else:    
                    food_idx = min(9, int(food[x + y * 48] / MAX_FOOD * 10))
                    self._nodes[(0, x, y)].set_active(food_idx)
                    self._nodes[(0, x, y)].depth = 1
                    self._nodes[(x, y)].depth = 0
        if self._world.count_a == 0 or self._world.count_b == 0:
            self._running = False
            self._finished = True
            self._nodes['replay'].show()
            self._nodes['menu'].show()
        self.update_pop_count()

    def update_pop_count(self):
        pa1, pa2, pa3, pa4 = f'{self._world.count_a:04}'
        pb1, pb2, pb3, pb4 = f'{self._world.count_b:04}'
        self._nodes['popa1'].set_active(int(pa1))
        self._nodes['popa2'].set_active(int(pa2))
        self._nodes['popa3'].set_active(int(pa3))
        self._nodes['popa4'].set_active(int(pa4))
        self._nodes['popb1'].set_active(int(pb1))
        self._nodes['popb2'].set_active(int(pb2))
        self._nodes['popb3'].set_active(int(pb3))
        self._nodes['popb4'].set_active(int(pb4))

    def mouse_click(self):
        if self._nodes['start'].visible and self._nodes['start'].mouse_inside:
            self._nodes['start'].hide()
            self._running = True
            self._last_time = time.perf_counter() - STEP_TIME
        elif self._nodes['replay'].mouse_inside and self._finished:
            self.enter()
        elif self._nodes['menu'].mouse_inside and self._finished:
            self.root.request('MainMenu')

