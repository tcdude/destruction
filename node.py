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

import aabb


class Node(object):
    def __init__(self, sprite, x=0, y=0):
        self._sprite = sprite
        self._sprite.position = x, y
        self._x = x
        self._y = y
        self._visible = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, v):
        if self._visible:
            self._sprite.x = v
        self._x = v
        self._on_pos_change()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, v):
        if self._visible:
            self._sprite.y = v
        self._y = v
        self._on_pos_change()

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, v):
        if self._visible:
            self._sprite.position = v
        self._x, self._y = v
        self._on_pos_change()

    @property
    def sprite(self):
        return self._sprite

    @property
    def visible(self):
        return self._visible

    @property
    def aabb(self):
        return aabb.AABB(
            *self.position, 
            self.x + self._sprite.size[0],
            self.y + self._sprite.size[1]
        )

    def hide(self):
        self._visible = False
        self._sprite.position = (int(-10e6), ) * 2

    def show(self):
        self._visible = True
        self._sprite.position = self._x, self._y

    def _on_pos_change(self):
        pass


class Button(Node):
    def __init__(self, sprite, sprite_hover, root, x=0, y=0):
        super().__init__(sprite, x, y)
        self._sprite_normal = sprite
        self._sprite_hover = sprite_hover
        self._sprite_normal.position = x, y
        self._sprite_hover.position = x, y 
        self._root = root
        self._mouse_inside = False

    @property
    def sprite(self):
        if self.aabb.inside(*self._root.mouse_pos):
            self._mouse_inside = True
            return self._sprite_hover
        else:
            self._mouse_inside = False
            return self._sprite_normal

    @property
    def mouse_inside(self):
        return self._mouse_inside

    def _on_pos_change(self):
        self._sprite_normal.position = super().position
        self._sprite_hover.position = super().position


class MultiNode(Node):
    """Node with multiple sprites. Use `set_active()` to change visible node."""
    def __init__(self, sprites, x, y):
        super().__init__(sprites[0], x, y)
        self._sprites = sprites
        self._active = 0
        for s in sprites:
            s.position = x, y

    @property
    def sprite(self):
        return self._sprites[self._active]

    def set_active(self, idx):
        if -1 < idx < len(self._sprites):
            self._active = idx
        else:
            raise IndexError()
    
    @property
    def aabb(self):
        return aabb.AABB(
            *self.position, 
            self.x + self._sprites[self._active].size[0],
            self.y + self._sprites[self._active].size[1]
        )

    def _on_pos_change(self):
        for s in self._sprites:
            s.position = self.position

