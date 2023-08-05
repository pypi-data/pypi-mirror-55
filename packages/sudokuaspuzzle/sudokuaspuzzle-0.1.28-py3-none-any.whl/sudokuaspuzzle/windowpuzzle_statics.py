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


TESTMARGIN = 2
try:
    import os
    import sys
    import math
    from copy import deepcopy
    import subprocess

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk, GdkPixbuf, Pango
    import cairo
    gi_require_version('PangoCairo', '1.0')
    from gi.repository import PangoCairo

    from constants import *

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

def create_board_pixbuf(pb, game_cells, dummyda):
    if pb == None: return

    one_size = min(dummyda.get_allocated_width(), dummyda.get_allocated_height())
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, one_size, one_size)
    cr = cairo.Context(surface)
    x0 = y0 = int((one_size-2) // 9)
    real_size = TESTMARGIN + 9 * x0
    selected = game_cells[0]
    if not dummyda.has_focus():
        selected = None

    for column in range(9):
        for row in range(9):
            number = (9 * row) + (column+1)
            shownum = game_cells[number][1]
            isconstant = game_cells[number][0]
            is_red = game_cells[number][2]
            cr.save() #save 1
            if (number == selected) and isconstant:
                cr.set_source_rgba(*pb.newcolors["RGBA_BG_CONSTANT_SELECTED"])
            elif (number == selected):
                cr.set_source_rgba(*pb.newcolors["RGBA_BG_SELECTED"])
            elif isconstant:
                cr.set_source_rgba(*pb.newcolors["RGBA_BG_CONSTANT"])
            else:
                cr.set_source_rgba(*pb.newcolors["RGBA_BG"])
            if is_red:
                thelist = pb.fitted_pixbufs_R
            else:
                thelist = pb.fitted_pixbufs
            if shownum:
                # first a square with selected color
                cr.save()#save 2
                cr.rectangle(x0*column,x0*row, x0, x0)
                cr.fill()
                cr.restore()
                #then print a scaled num (red or black)
                cr.save()
                apixbuf = thelist[shownum]
                Gdk.cairo_set_source_pixbuf(cr, apixbuf,x0*column,x0*row)
                cr.paint()
                cr.stroke()
                cr.restore() #save 2
                cr.restore() #save 1
            else:
                #an empty
                cr.save()
                cr.rectangle(x0*column,x0*row, x0, x0)
                cr.fill()
                cr.restore() #save 1
    cr.set_line_width(1)
    cr.set_source_rgba(0, 0, 0, 1)
    for acounter in range(9)[1:]:
        cr.save()
        if 0 == (acounter % 3) :
            cr.set_line_width(3)
        else:
            cr.set_line_width(1)
        x1 = y1 = x0 * acounter
        cr.move_to(x1, 0)
        cr.line_to(x1, real_size)
        cr.stroke()
        cr.move_to(0, x1)
        cr.line_to(real_size, x1)
        cr.stroke()
        cr.restore()
    w = h = real_size #- 4
    cr.set_line_width(3)
    cr.set_source_rgba(0, 0, 0, 1)
    cr.rectangle(1, 1, w-TESTMARGIN, h-TESTMARGIN)
    cr.stroke()
    board_pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, real_size, real_size)
    return board_pixbuf

# TODO: get it from qqwing's dynamic library.
def get_new_puzzle(difficulty = "easy"):
    """ Get a puzzle from qqwing.

    Return:
        - the puzzle as a string
        - the solution as a string
        - the difficulty (to show in case of "any")
    """
    while True:
        # print(difficulty)
        new_puzzle_output = subprocess.run(['qqwing', "--generate", "--difficulty",
                difficulty, "--one-line", "--solution",
                "--stats", "--count-solutions",
                "--symmetry", "random"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # print(new_puzzle_output)
        if "unique" in new_puzzle_output:
            new_puzzle_lines = new_puzzle_output.splitlines()
            puzzle_start = new_puzzle_lines[0]
            puzzle_solution = new_puzzle_lines[1]
            difficulty = new_puzzle_lines[-1].split()[-1].lower()
            # return b.split('\n')[0]
            return puzzle_start, puzzle_solution, difficulty

def get_real_positions(x, y, eb, pixbuf):
    cell_number = 0
    eb_w = eb.get_allocated_width()
    eb_h = eb.get_allocated_height()
    pb_one_size = pixbuf.get_width()
    pb_size_2 = pixbuf.get_height()

    start_x = int((eb_w - pb_one_size) / 2 )
    start_y = int((eb_h - pb_one_size) / 2 )
    cell_size = int(pb_one_size / 9)

    if x < start_x or x > start_x + pb_one_size-TESTMARGIN or y < start_y or y > start_y + pb_one_size -TESTMARGIN:
        return cell_number, start_x, start_y

    col = int((x - start_x) / cell_size)
    row = int((y - start_y) / cell_size)
    cell_number = int(row) * 9 + int(col+1)
    picker_x = start_x + col * cell_size
    picker_y = start_y + row * cell_size
    return cell_number, picker_x, picker_y

