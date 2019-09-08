#distutils: language = c++
# cython: language_level=3

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

from libcpp.vector cimport vector


cdef extern from "ext/fol.cpp":
    pass


cdef extern from "ext/fol.hpp":
    cdef cppclass Species:
        Species() except +
        void set_strength(const int)
        void set_fertility(const int)
        int get_strength()
        int get_fertility()
        int get_nutrition()
        int get_population()
        bint is_initialized()

    cdef cppclass World:
        World() except +
        void init(int, int, int, Species&, Species&)
        bint toggle(int, int, int)
        void simulate_step()
        vector[int] cells()
        vector[int] food()
        int count_a()
        int count_b()

