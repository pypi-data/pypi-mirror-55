#!/usr/bin/env python3
"""
    Copyright (C) Ηλίας Ηλιάδης, 2019-09-24; Ηλίας Ηλιάδης <iliadis@kekbay.gr>

    This file is part of «Sudoku as puzzle».

    «Sudoku as puzzle» is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    «Sudoku as puzzle» is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with «Sudoku as puzzle».  If not, see <http://www.gnu.org/licenses/>.
"""

"""
        WARNING !!!

Since we are in python, any method here will override base class.
So do not declare here methods that exist also in the base class.
"""
#FIXME: correct the version
__version__ = '0.1.28'
VERSIONSTR = 'v. {}'.format(__version__)

try:
    import os
    import sys

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk, GdkPixbuf, Pango
    import cairo
    gi_require_version('PangoCairo', '1.0')
    from gi.repository import PangoCairo

    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig, MessageBox
    from constants import *

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

game_cells = []
for acounter in range(81):
    s = TMPDEFAULTPUZZLE[acounter]
    is_constant = True if s != "." else False
    theint = int(s) if s != "." else 0
    game_cells.append ([is_constant, theint, False])
game_cells.insert(0, 1)

def create_board_pixbuf_for_options(pb):
    if pb == None: return

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, OPTIONS_BOARD_SIZE, OPTIONS_BOARD_SIZE)
    cr = cairo.Context(surface)
    x0 = int(OPTIONS_BOARD_SIZE // 3)
    # x3 = int(x0 // 3)
    for column in range(3):
        for row in range(3):
            cell_number = 1 + row * 3 + column
            apixbuf = pb.picker_pixbufs[cell_number]

            cr.save()
            if cell_number == 1:
                cr.set_source_rgba(*pb.newcolors["RGBA_PICKER_BG"])
            elif (cell_number == 2) or (cell_number == 6):
                cr.set_source_rgba(*pb.newcolors["RGBA_BG"])
            elif (cell_number == 3 ) or (cell_number == 7):
                cr.set_source_rgba(*pb.newcolors["RGBA_BG_SELECTED"])
            elif (cell_number == 4 ) or (cell_number == 8):
                cr.set_source_rgba(*pb.newcolors["RGBA_BG_CONSTANT"])
            else:
                cr.set_source_rgba(*pb.newcolors["RGBA_BG_CONSTANT_SELECTED"])
            if (cell_number>5):
                apixbuf = pb.fitted_pixbufs_R[cell_number]
            else:
                apixbuf = pb.fitted_pixbufs[cell_number]

            # first a square with selected color
            cr.rectangle(x0*column,x0*row, x0, x0)
            cr.fill()
            #then print a scaled num (red or black)
            Gdk.cairo_set_source_pixbuf(cr, apixbuf,x0*column,x0*row)
            cr.paint()
            cr.stroke()
            cr.restore()

    cr.set_source_rgba(0, 0, 0, 1)
    for acounter in range(2):
        cr.save()
        cr.set_line_width(1)
        x1 = x0 * (acounter + 1)
        cr.move_to(x1, 0)
        cr.line_to(x1, OPTIONS_BOARD_SIZE)
        cr.stroke()
        cr.move_to(0, x1)
        cr.line_to(OPTIONS_BOARD_SIZE, x1)
        cr.stroke()
        cr.restore()


    w = h = OPTIONS_BOARD_SIZE #- 4
    cr.set_line_width(3)

    cr.rectangle(2, 2, w-4, h-4)
    cr.stroke()
    board_pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, OPTIONS_BOARD_SIZE, OPTIONS_BOARD_SIZE)
    return board_pixbuf
