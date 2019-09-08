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

import sdl2.ext


class EventHandler(object):
    def __init__(self, on_quit):
        self._events = {}
        self._on_quit = on_quit

    def register(self, event_type, callback, key=None, button=None, args=()):
        if (key is None and button is None) \
                or (key is not None and button is not None):
            raise ValueError('Either key or button needed')
        if event_type not in self._events:
            self._events[event_type] = {}
        if key is not None:
            self._events[event_type][key] = callback, args
        else:
            self._events[event_type][button] = callback, args

    def reset(self):
        self._events = {}

    def __call__(self, *args, **kwargs):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT or event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == 27:
                self._on_quit()
            elif event.type in self._events:
                ecb = self._events[event.type]
                if hasattr(event, 'button') and event.button.button in ecb:
                    f, a = ecb[event.button.button]
                elif hasattr(event, 'key') and event.key.keysym.sym in ecb:
                    f, a = ecb[event.key.keysym.sym]
                else:
                    continue
                f(*a)

