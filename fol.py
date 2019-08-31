
"""MIT License

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
SOFTWARE."""
import random


class World(object):
    def __init__(self, width, height, num_spec):
        self._num_spec = num_spec
        self._dim = width, height
        self._world = [[0 for _ in range(height)] for _ in range(width)]
        self._turn = 0

    def seed(self, s=None):
        random.seed(s)
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                self._world[x][y] = random.randint(self._num_spec)

    def sim(self):
        tmp_world = [] + self._world
        for x in range(self._dim[0]):
            for y in range(self._dim[1]):
                tmp_world[x][y] = self._check(x, y, self._world[x][y])
        self._world = tmp_world
        self._turn += 1

    def check(self, x, y, val):
        cnt = [0 for _ in range(self._num_spec + 1)]
        for xo in (-1, 0, 1):
            for yo in (-1, 0, 1):
                if xo == yo == 0:
                    continue
                xc = x + xo
                yc = y + yo
                if -1 < xc < self._dim[0] and -1 < yc < self._dim[1]:
                    cnt[self._world[xc][yc]] += 1
        cntmax = max(cnt[1:])
        if val == 0:
            if cntmax == 0:
                return 0
            if cnt[1:].count(cntmax) > 1:
                return 0
            return cnt[1:].index(cntmax) + 1
        if cnt[1:].count(cntmax) == 1:
            idx = cnt[1:].index(cntmax) + 1
            if cnt[val] + 1 >= cntmax:
                return val
            return idx
        return val

    @property
    def world(self):
        return self._world

    @property
    def turn(self):
        return self._turn

