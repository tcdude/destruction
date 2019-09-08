
"""
Copyright (c) 2019 Tiziano Bettio
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

import os
from setuptools import setup
from setuptools import find_namespace_packages
from distutils.extension import Extension
from Cython.Build import cythonize


extensions = [
    Extension('*', ['destruction/*.pyx'],
              include_dirs=['.'])
]


setup(
    name='destruction',
    version='0.1',
    description='OLC CodeJam 2019 entry.',
    author='tcdude',
    packages=find_namespace_packages(include=['destruction']),
    package_data={'foolysh': [
        'LICENSE',
        'destruction/resources/437tt.ttf'
    ]},
    install_requires=['Pillow', 'PySDL2>=0.9.6'],
    setup_requires=['Cython'],
    ext_modules=cythonize(extensions,
                          compiler_directives={'language_level': 3},
                          annotate=False),
    include_package_data=True,
)
"""
from distutils.core import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize("fol.pyx"))
"""
