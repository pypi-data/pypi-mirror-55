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

try:
    import os
    import sys
    import math
    from copy import deepcopy

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


class GamePixBufs:
    def __init__(self, window, stringslist, fontstring, newcolors, font_ratio = 1):
        self.fontstring = fontstring
        self.fix_font_size()
        self.font_ratio = font_ratio
        self.newcolors = newcolors

        self.fgcolor_cairo = self.newcolors["RGBA_FG"]
        self.fgRcolor_cairo = self.newcolors["RGBA_FG_RED"]

        #create a dummy cairo context da
        cr = window.get_window().cairo_create()
        self.bigpixbufs = []
        self.bigpixbufs_R = []
        # self.bigpixbufs_P = []

        self.picker_pixbufs = []

        wh = 0
        pixbufs1 = []
        pixbufs_R = []
        for aletter in stringslist[1:]:
            try:
                apixbuf = self.create_digit(aletter)
                apixbuf_R = self.create_digit(aletter, True)
            except Exception as e:
                print("apixbuf Exception", e)
            wh = max(wh, apixbuf.get_width(), apixbuf.get_height())
            pixbufs1.append(apixbuf)
            pixbufs_R.append(apixbuf_R)
        #insert an empty pixbuf
        theempty = self.anempty_big(pixbufs1[0], wh)
        pixbufs1.insert(0, theempty)
        pixbufs_R.insert(0, theempty)
        for apixbuf in pixbufs1:
            self.bigpixbufs.append(self.resize_bg(apixbuf, wh))
            # self.bigpixbufs_P.append(self.resize_bg(apixbuf, wh, for_picker = True))

        for apixbuf in pixbufs_R:
            self.bigpixbufs_R.append(self.resize_bg(apixbuf, wh))

        # TODO try to set a minimu picker pibuf

    def fix_font_size(self):
        self.fontstring = self.fontstring.split(" ",-1)[0] + " 300"

    def fit_pixbufs(self, ameasure):
        self.fitted_pixbufs = []
        self.fitted_pixbufs_R = []
        self.picker_pixbufs = []
        one_third = int(ameasure / 3) - 2
        for apixbuf in self.bigpixbufs:
            scaled = apixbuf.scale_simple(ameasure,
                    ameasure,
                    GdkPixbuf.InterpType.BILINEAR)
            self.fitted_pixbufs.append(scaled)
        # for apixbuf in self.bigpixbufs_P:
            picker_pixbuf = apixbuf.scale_simple(one_third,
                    one_third,
                    GdkPixbuf.InterpType.BILINEAR)
            self.picker_pixbufs.append(picker_pixbuf)
        for apixbuf in self.bigpixbufs_R:
            scaled = apixbuf.scale_simple(ameasure,
                    ameasure,
                    GdkPixbuf.InterpType.BILINEAR)
            self.fitted_pixbufs_R.append(scaled)

    def create_digit(self, letter, red = False, white = False):
        #pixbuf will be unscaled
        #just a big pixbuf
        fontname = self.fontstring
        left = 20
        top = 0
        #create a temporary pixbuf
        #to find the extends
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 600)
        cr = cairo.Context(surface)

        layout = PangoCairo.create_layout(cr)
        thefontdescr = Pango.font_description_from_string(fontname)

        layout.set_font_description(Pango.font_description_from_string(fontname))
        crcr = layout.get_context()

        amap = crcr.get_font_map()
        afont = amap.load_font (crcr, thefontdescr)

        cr.move_to(left,top)

        if red:
            cr.set_source_rgba(*self.fgRcolor_cairo)
        else:
            cr.set_source_rgba(*self.fgcolor_cairo)
        #avoid problems with left bearing going out of surface
        layout.set_text(" " + letter, -1)

        PangoCairo.update_layout(cr, layout)

        ink_pixel_extends, logical_pixel_extends = layout.get_pixel_extents ()
        PangoCairo.show_layout(cr, layout)

        surface.flush()

        surface2  = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                ink_pixel_extends.width,
                logical_pixel_extends.height)
        cr2 = cairo.Context(surface2)
        cr2.set_source_surface(surface, -(left + ink_pixel_extends.x), -top)
        cr2.rectangle(0, 0, ink_pixel_extends.width, logical_pixel_extends.height)
        cr2.fill()

        digit_pixbuf = Gdk.pixbuf_get_from_surface (surface2,
                0,
                0,
                ink_pixel_extends.width,
                logical_pixel_extends.height)

        return digit_pixbuf

    def resize_bg(self, pixbuf, full_W, for_picker = False):
        font_ratio = self.font_ratio
        if for_picker:
            font_ratio = 1

        old_W = pixbuf.get_width() * font_ratio
        old_H = pixbuf.get_height() * font_ratio
        diff_W = full_W - old_W
        diff_H = full_W - old_H
        dest_x = diff_W // 2
        dest_y = diff_H // 2
        colorspace = pixbuf.get_colorspace()
        bitspersample = pixbuf.get_bits_per_sample()
        new_pixbuf = GdkPixbuf.Pixbuf.new(colorspace, True, bitspersample, full_W, full_W)
        # new_pixbuf.fill(self.all_colors["TRANS_BG_ΙΝΤ"])
        new_pixbuf.fill(rgba_int(self.newcolors["RGBA_BG_TRANSP"]))
        pixbuf.composite(new_pixbuf,dest_x,dest_y,old_W,old_H,dest_x,dest_y,font_ratio,font_ratio,GdkPixbuf.InterpType.BILINEAR , 255)
        return new_pixbuf

    def anempty_big(self, otherpixbuf, wh):
        colorspace = otherpixbuf.get_colorspace()
        bitspersample = otherpixbuf.get_bits_per_sample()
        new_pixbuf = GdkPixbuf.Pixbuf.new(colorspace, True, bitspersample, wh, wh)
        new_pixbuf.fill(rgba_int(self.newcolors["RGBA_BG"]))
        return new_pixbuf

    def resize_letters(self, one_size):
        pass
