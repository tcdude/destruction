#distutils: language = c++

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

from cython.operator cimport dereference as deref
from libcpp.memory cimport unique_ptr

print('test')

cimport cppfol

cdef class Species:
    cdef unique_ptr[cppfol.Species] thisptr

    def __init__(self):
        self.thisptr.reset(new cppfol.Species())

    @property
    def strength(self):
        return deref(self.thisptr).get_strength()

    @strength.setter
    def strength(self, int s):
        if 0 < s < 4:
            deref(self.thisptr).set_strength(s)
        else:
            raise ValueError('Must be between 1 and 3')
    @property
    def fertility(self):
        return deref(self.thisptr).get_fertility()

    @fertility.setter
    def fertility(self, int f):
        if 0 < f < 4:
            deref(self.thisptr).set_fertility(f)
        else:
            raise ValueError('Must be between 1 and 3')

    @property
    def nutrition(self):
        return deref(self.thisptr).get_nutrition()

    @property
    def population(self):
        return deref(self.thisptr).get_population()

    @property
    def is_initialized(self):
        return deref(self.thisptr).is_initialized()


cdef class World:
    cdef unique_ptr[cppfol.World] thisptr

    def __init__(self, width, height, s_a, s_b, max_food):
        cdef cppfol.Species a, b
        a.set_strength(s_a.strength)
        a.set_fertility(s_a.fertility)
        b.set_strength(s_b.strength)
        b.set_fertility(s_b.fertility)
        self.thisptr.reset(new cppfol.World())
        deref(self.thisptr).init(width, height, max_food, a, b)

    def simulate_step(self):
        deref(self.thisptr).simulate_step()

    @property
    def cells(self):
        return deref(self.thisptr).cells()

    @property 
    def food(self):
        return deref(self.thisptr).food()

