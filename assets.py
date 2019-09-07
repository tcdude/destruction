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

import graphics


BUTTONS = {
    'vs': graphics.build_button(chr(0xf18e) + ' 2 Player VS', line_width=0),
    'ai': graphics.build_button(chr(0xe28c) + ' Train AI', line_width=0),
    'quit': graphics.build_button(chr(0xf659) + ' Quit', line_width=0),
    'inc': graphics.build_button(chr(0xf055), line_width=0),
    'dec': graphics.build_button(chr(0xf056), line_width=0),
    'next': graphics.build_button('Next', line_width=1),
}

TITLES = {
    'fol': graphics.build_text(
        chr(0xe76b) + ' Fight of Life ' + chr(0xe76b), 
        fg=graphics.RED, 
        font=graphics.FONT_LARGE
    ),
    'p1_species': graphics.build_text(
        'Player One - Setup Species', 
        fg=graphics.RED, 
        font=graphics.FONT_LARGE
    ),
    'p2_species': graphics.build_text(
        'Player Two - Setup Species', 
        fg=graphics.BLUE
    ),
    'p1_placement': graphics.build_text(
        'Player One - Place initial Population', 
        fg=graphics.RED
    ),
    'p2_placement': graphics.build_text(
        'Player Two - Place initial Population', 
        fg=graphics.BLUE
    ),
    'sim': graphics.build_text(
        'Ordered chaos in progress...',
        fg=graphics.RED
    ),
}

TEXTS = {
    'species0': graphics.build_text(
        'Adjust the stats of your species to your liking and click "Next" '
        'when done.\nWhile Player One is setting up their species, Player '
        'Two: "No peeking!"...\n\n*...this really needs networking support '
        'or something...*\n\n\n    Left click to continue',
        font=graphics.FONT_SMALL
    ),
    'species1': graphics.build_text(
        'Now while Player one tries to not peek, Player Two, please adjust '
        'the stats of your Species.\n\n...this is really awkward, two '
        'people in front of one PC???\nare we accidentally back in the 90s???'
        '\n\n\n    Left click to continue',
        font=graphics.FONT_SMALL
    ),
    'str': graphics.build_text(
        'Strength:',
    ),
    'fer': graphics.build_text(
        'Fertility:',
    ),
    'nut': graphics.build_text(
        'Hunger:',
        graphics.GREEN
    ),
    'pop': graphics.build_text(
        'Population:',
        graphics.BLUE
    ),
    'str_info': graphics.build_text(
        'Multiplier used during fighting, high strength makes hungry...',
        font=graphics.FONT_SMALL
    ),
    'fer_info': graphics.build_text(
        'Number of cells needed to reproduce, division of "labour" leaves '
        'more time to chill...',
        font=graphics.FONT_SMALL
    ),
    'gen_info': graphics.build_text(
        chr(0xf05a) + 
        ' The combination of strength and fertility affect the initial '
        'population',
        font=graphics.FONT_SMALL
    )

}

for i in range(10):
    TEXTS[i] = graphics.build_text(str(i))
