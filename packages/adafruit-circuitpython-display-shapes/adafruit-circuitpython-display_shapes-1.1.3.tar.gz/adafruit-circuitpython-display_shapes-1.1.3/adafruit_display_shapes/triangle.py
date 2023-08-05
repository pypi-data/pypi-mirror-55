# The MIT License (MIT)
#
# Copyright (c) 2019 Limor Fried for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`triangle`
================================================================================

Various common shapes for use with displayio - Triangle shape!


* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes.git"


class Triangle(displayio.TileGrid):
    # pylint: disable=too-many-arguments,invalid-name
    """A triangle.

    :param x0: The x-position of the first vertex.
    :param y0: The y-position of the first vertex.
    :param x1: The x-position of the second vertex.
    :param y1: The y-position of the second vertex.
    :param x2: The x-position of the third vertex.
    :param y2: The y-position of the third vertex.
    :param fill: The color to fill the triangle. Can be a hex value for a color or
                 ``None`` for transparent.
    :param outline: The outline of the triangle. Can be a hex value for a color or
                    ``None`` for no outline.
    """
    def __init__(self, x0, y0, x1, y1, x2, y2, *, fill=None, outline=None):
        # Sort coordinates by Y order (y2 >= y1 >= y0)
        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0

        if y1 > y2:
            y1, y2 = y2, y1
            x1, x2 = x2, x1

        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0

        # Find the largest and smallest X values to figure out width for bitmap
        xs = [x0, x1, x2]
        width = max(xs) - min(xs) + 1
        height = y2 - y0 + 1

        self._palette = displayio.Palette(3)
        self._palette.make_transparent(0)
        self._bitmap = displayio.Bitmap(width, height, 3)

        if fill is not None:
            self._draw_filled(x0 - min(xs), 0, x1 - min(xs), y1 - y0, x2 - min(xs), y2 - y0)
            self._palette[2] = fill
        else:
            self._palette.make_transparent(2)

        if outline is not None:
            # print("outline")
            self._palette[1] = outline
            self._line(x0 - min(xs), 0, x1 - min(xs), y1 - y0, 1)
            self._line(x1 - min(xs), y1 - y0, x2 - min(xs), y2 - y0, 1)
            self._line(x2 - min(xs), y2 - y0, x0 - min(xs), 0, 1)

        super().__init__(self._bitmap, pixel_shader=self._palette, x=min(xs), y=y0)

    # pylint: disable=invalid-name, too-many-locals, too-many-branches
    def _draw_filled(self, x0, y0, x1, y1, x2, y2):
        if y0 == y2: # Handle awkward all-on-same-line case as its own thing
            a = x0
            b = x0
            if x1 < a:
                a = x1
            elif x1 > b:
                b = x1

            if x2 < a:
                a = x2
            elif x2 > b:
                b = x2
            self._line(a, y0, b, y0, 2)
            return

        if y1 == y2:
            last = y1   # Include y1 scanline
        else:
            last = y1 - 1 # Skip it

        # Upper Triangle
        for y in range(y0, last + 1):
            a = round(x0 + (x1 - x0) * (y - y0) / (y1 - y0))
            b = round(x0 + (x2 - x0) * (y - y0) / (y2 - y0))
            if a > b:
                a, b = b, a
            self._line(a, y, b, y, 2)
        # Lower Triangle
        for y in range(last + 1, y2 + 1):
            a = round(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
            b = round(x0 + (x2 - x0) * (y - y0) / (y2 - y0))

            if a > b:
                a, b = b, a
            self._line(a, y, b, y, 2)

    def _line(self, x0, y0, x1, y1, color):
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for _h in range(y0, y1):
                self._bitmap[x0, _h] = color
        elif y0 == y1:
            if x0 > x1:
                x0, x1 = x1, x0
            for _w in range(x0, x1):
                self._bitmap[_w, y0] = color
        else:
            steep = abs(y1 - y0) > abs(x1 - x0)
            if steep:
                x0, y0 = y0, x0
                x1, y1 = y1, x1

            if x0 > x1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            dx = x1 - x0
            dy = abs(y1 - y0)

            err = dx / 2

            if y0 < y1:
                ystep = 1
            else:
                ystep = -1

            for x in range(x0, x1):
                if steep:
                    self._bitmap[y0, x] = color
                else:
                    self._bitmap[x, y0] = color
                err -= dy
                if err < 0:
                    y0 += ystep
                    err += dx
    # pylint: enable=invalid-name, too-many-locals, too-many-branches

    @property
    def fill(self):
        """The fill of the triangle. Can be a hex value for a color or
        ``None`` for transparent."""
        return self._palette[2]

    @fill.setter
    def fill(self, color):
        if color is None:
            self._palette[2] = 0
            self._palette.make_transparent(2)
        else:
            self._palette[2] = color
            self._palette.make_opaque(2)

    @property
    def outline(self):
        """The outline of the triangle. Can be a hex value for a color or
        ``None`` for no outline."""
        return self._palette[1]

    @outline.setter
    def outline(self, color):
        if color is None:
            self._palette[1] = 0
            self._palette.make_transparent(1)
        else:
            self._palette[1] = color
            self._palette.make_opaque(1)
