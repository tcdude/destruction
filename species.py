
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
from assets import BUTTONS
from assets import TITLES
from assets import TEXTS


class SpeciesSelection(Scene):
    def __init__(self, root):
        super().__init__(root)
        self._init = False
        self._data = None

    def _init_assets(self):
        # Screen 0, Species A
        rx, ry = self.root.resolution
        tot_y = 2 * TITLES['p1_species'].size[1] + TEXTS['species0'].size[1]
        k = 0, 0
        self._data['nodes'][k] = {
            0: self.root.new_node(
                TITLES['p1_species'],
                int(rx / 2 - TITLES['p1_species'].size[0] / 2),
                int(ry / 2 - tot_y / 2)
            ),
            1: self.root.new_node(
                TEXTS['species0'],
                int(rx / 2 - TEXTS['species0'].size[0] / 2),
                int(ry / 2 - tot_y / 2 + 2 * TITLES['p1_species'].size[1])
            )
        }

        # Screen 1, Species A
        tot_y -= TEXTS['species0'].size[1]
        tot_y += TEXTS['str'].size[1] * 5 + BUTTONS['next'][0].size[1] * 2
        tot_y += TEXTS['str_info'].size[1] * 2
        tot_x = max(TEXTS['str_info'].size[0], TEXTS['fer_info'].size[0])
        y_str = int(ry / 2 - tot_y / 2 + 2 * TITLES['p1_species'].size[1])
        y_str_i = int(y_str + TEXTS['str'].size[1])
        y_fer = int(y_str_i + TEXTS['str_info'].size[1] + TEXTS['str'].size[1] / 3)
        y_fer_i = int(y_fer + TEXTS['str'].size[1])
        y_nut = int(y_fer_i + TEXTS['str_info'].size[1] + TEXTS['str'].size[1] / 3)
        y_pop = int(y_nut + TEXTS['str'].size[1] * 4 / 3)
        x_left = int(rx / 2 - tot_x / 2)
        x_dec = int(x_left + TEXTS['pop'].size[0] * 1.2)
        x_num = int(x_dec + BUTTONS['dec'][0].size[0] * 1.3)
        x_inc = int(x_num + TEXTS[9].size[0] * 1.3)
        y_but_offset = -int(BUTTONS['inc'][0].size[1] * 0.15)
        x_num0 = x_num - TEXTS[9].size[0]
        k = 1, 0
        self._data['nodes'][k] = {
            0: self.root.new_node(
                TITLES['p1_species'],
                int(rx / 2 - TITLES['p1_species'].size[0] / 2),
                int(ry / 2 - tot_y / 2)
            ),
            1: self.root.new_node(
                TEXTS['str'],
                x_left,
                y_str
            ),
            2: self.root.new_node(
                TEXTS['str_info'],
                x_left, 
                y_str_i
            ),
            3: self.root.new_node(
                TEXTS['fer'],
                x_left, 
                y_fer
            ),
            4: self.root.new_node(
                TEXTS['fer_info'],
                x_left, 
                y_fer_i
            ),
            5: self.root.new_node(
                TEXTS['nut'],
                x_left, 
                y_nut
            ),
            6: self.root.new_node(
                TEXTS['pop'],
                x_left, 
                y_pop
            ),
            7: self.root.new_node(
                TEXTS['gen_info'],
                int(rx / 2 - TEXTS['gen_info'].size[0] / 2),
                int(ry - TEXTS['gen_info'].size[1] * 1.3)
            ),
            'next': self.root.new_button(
                *BUTTONS['next'],
                int(rx / 2 - BUTTONS['next'][0].size[0] / 2),
                y_pop + BUTTONS['next'][0].size[1]
            ),
            'str_dec': self.root.new_button(
                *BUTTONS['dec'],
                x_dec,
                y_str + y_but_offset
            ),
            'str': self.root.new_multi_node(
                [TEXTS[i] for i in range(1, 4)],
                x_num,
                y_str
            ),
            'str_inc': self.root.new_button(
                *BUTTONS['inc'],
                x_inc,
                y_str + y_but_offset
            ),
            'fer_dec': self.root.new_button(
                *BUTTONS['dec'],
                x_dec,
                y_fer + y_but_offset
            ),
            'fer': self.root.new_multi_node(
                [TEXTS[i] for i in range(1, 4)],
                x_num,
                y_fer
            ),
            'fer_inc': self.root.new_button(
                *BUTTONS['inc'],
                x_inc,
                y_fer + y_but_offset
            ),
            'nut0': self.root.new_multi_node(
                [TEXTS[i] for i in range(10)],
                x_num0,
                y_nut
            ),
            'nut1': self.root.new_multi_node(
                [TEXTS[i] for i in range(10)],
                x_num,
                y_nut
            ),
            'pop0': self.root.new_multi_node(
                [TEXTS[i] for i in range(10)],
                x_num0,
                y_pop
            ),
            'pop1': self.root.new_multi_node(
                [TEXTS[i] for i in range(10)],
                x_num,
                y_pop
            ),
            
        }
        for node in self._data['nodes'][k].values():
            node.hide()

    def process(self):
        pass

    @property
    def key(self):
        return (
            self._data['screen'], 
            0 if self.root.species_a == self._data['species'] else 1
        )

    def enter(self):
        sa, sb = self.root.species_a, self.root.species_b
        if not self._init:
            self._data = self.root.scene_data
            self._data['species'] = sa
            self._data['screen'] = 0
            self._data['first'] = True
            self._data['nodes'] = {}
            self._init_assets()
            self._init = True
        if self._data['first']:
            self._data['first'] = False
        elif self._data['screen'] == 0:
            self._data['screen'] = 1
            self._update_stats()
        elif self._data['screen'] == 1:
            self._data['species'] = sb if self._data['species'] == sa else sa
            self._data['screen'] = 0
            self._data['species'].strength = 1
            self._data['species'].fertility = 3
            self._update_stats()
        
        for node in self._data['nodes'][self.key].values():
            node.show()

        self.root.event_handler.reset()
        self.root.event_handler.register(
            sdl2.SDL_MOUSEBUTTONUP,
            self.mouse_click,
            button=sdl2.SDL_BUTTON_LEFT
        )

    def exit(self):
        for node in self._data['nodes'][self.key].values():
            node.hide()

    def mouse_click(self):
        if self._data['screen'] == 0:
            self.exit()
            self.enter()
        elif self._data['screen'] == 1:
            nodes = self._data['nodes'][self.key]
            if nodes['str_dec'].mouse_inside:
                if self._data['species'].strength > 1:
                    self._data['species'].strength -= 1
                    self._update_stats()
            elif nodes['str_inc'].mouse_inside:
                if self._data['species'].strength < 3:
                    self._data['species'].strength += 1
                    self._update_stats()
            elif nodes['fer_dec'].mouse_inside:
                if self._data['species'].fertility > 1:
                    self._data['species'].fertility -= 1
                    self._update_stats()
            elif nodes['fer_inc'].mouse_inside:
                if self._data['species'].fertility < 3:
                    self._data['species'].fertility += 1
                    self._update_stats()
                   
    def _update_stats(self):
        nodes = self._data['nodes'][self.key]
        nodes['str'].set_active(self._data['species'].strength - 1)
        nodes['fer'].set_active(self._data['species'].fertility - 1)
        n = f'{self._data["species"].nutrition:02}'
        p = f'{self._data["species"].population:02}'
        nodes['nut0'].set_active(int(n[0]))
        nodes['nut1'].set_active(int(n[1]))
        nodes['pop0'].set_active(int(p[0]))
        nodes['pop1'].set_active(int(p[1]))

