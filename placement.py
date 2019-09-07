
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

import aabb
from scene import Scene
import graphics
from assets import TITLES
from assets import BUTTONS


class Placement(Scene):
    def __init__(self, root):
        super().__init__(root)
        self._nodes = {}
        self._data = None
        self._init = False

    def _init_nodes(self):
        rx, ry = self.root.resolution
        self._nodes['title'] = self.root.new_multi_node(
            [TITLES['p1_placement'], TITLES['p2_placement']],
            int(rx / 2 - TITLES['p1_placement'].size[0] / 2),
            int(ry / 20)
        )
        self._nodes['next'] = self.root.new_button(
            *BUTTONS['next'],
            int(rx / 2 - BUTTONS['next'][0].size[0] / 2),
            int(ry - 1.5 * BUTTONS['next'][0].size[1])
        )
        im_grid = graphics.build_grid(rx * 0.9, ry * 0.7, 46, 20)
        slen = int(im_grid.size[0] / 46 - 2)
        start_x = int(rx / 2 - im_grid.size[0] / 2)
        start_y = int(ry / 2 - im_grid.size[1] / 2)
        self._data['g_bb'] = aabb.AABB(
            start_x, 
            start_y,
            start_x + im_grid.size[0],
            start_y + im_grid.size[1]
        )
        self._data['slen'] = int(im_grid.size[0] / 46)
        self._nodes['grid'] = self.root.new_node(
            im_grid,
            start_x,
            start_y
        )
        
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
        if self._init:
            mx, my = self.root.mouse_pos
            rx, ry = self.root.resolution
            bb = self._data['g_bb']
            slen = self._data['slen']
            k = None
            if bb.inside(mx, my):
                if (self._data['p'] == 0 and mx < rx / 2) \
                    or (self._data['p'] and mx > rx / 2):
                    k = int((mx - bb.x1) / slen), int((my - bb.y1) / slen)
            else:
                if self._data['hover'] is not None:
                    self._nodes[self._data['hover']].set_active(
                        self._data['pstate']
                    )
                    self._data['hover'] = None
                    self._data['pstate'] = None
                    return

            if k is None or k[0] > 45 or k[1] > 19:
                return
            if (self._data['p'] == 0 and k[0] > 22) \
                    or (self._data['p'] and k[0] < 23):
                return
            if self._data['pstate'] is not None and self._data['hover'] != k:
                self._nodes[self._data['hover']].set_active(
                    self._data['pstate']
                )

            if k is not None and k != self._data['hover']:
                self._data['pstate'] = self._nodes[k].active
                self._data['hover'] = k
                self._nodes[k].set_active(self._data['p'] + 2)
                    

    def enter(self):
        if not self._init:
            self._data = self.root.scene_data
            self._data['p'] = 0
            self._data['sel'] = [{}, {}]
            self._data['hover'] = None
            self._data['pstate'] = None
            self._init_nodes()
            self._init = True
        elif self._data['p'] == 0:
            self._data['p'] = 1
        elif self._data['p'] == 1:
            self._data['p'] = 0
        self.clear()
        sa, sb = self.root.species_a, self.root.species_b
        self._data['species'] = sb if self._data['p'] else sa
        self._data['active'] = 0
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

    def clear(self):
        self._nodes['title'].set_active(self._data['p'])
        p1 = self._data['p'] == 0
        for x in range(46):
            for y in range(20):
                if (p1 and x < 23) or (not p1 and x >= 23):
                    a = 1
                elif (p1 and x >= 23) or (not p1 and x < 23):
                    a = 0
                self._nodes[(x, y)].set_active(a)

    def mouse_click(self):
        if self._nodes['next'].mouse_inside \
            and self._data['active'] == self._data['species'].population:
                if self._data['p'] == 0:
                    self.root.request('SpeciesSelection')
                else:
                    self.root.request('Simulation')
        if self._data['hover'] is not None:
            node = self._nodes[self._data['hover']]
            if self._data['species'].population > self._data['active'] \
                    and self._data['pstate'] < 2:
                self._data['active'] += 1
                node.set_active(self._data['p'] + 2)
                self._data['pstate'] = self._data['p'] + 2
            elif self._data['pstate'] > 1:
                self._data['active'] -= 1
                node.set_active(1)
                self._data['pstate'] = 1


