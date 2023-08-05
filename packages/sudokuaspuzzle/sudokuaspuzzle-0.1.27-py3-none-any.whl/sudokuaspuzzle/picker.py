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

# No need to check imports.
# They must be already imported by main window class.
import os
import sys
# Gtk and related
from gi import require_version as gi_require_version
gi_require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
import cairo

class NumberPicker(object):
    def __init__(self, *args, **kwargs):
        self.passed_args = kwargs['args_to_pass']
        self.pixbufs = self.passed_args['pixbufs']
        self.myparent = self.passed_args['parent']
        self.strings_to_use = self.passed_args['strings_to_use']
        self.response_from_picker = self.passed_args['response_from_picker']

        self.bg_color = self.passed_args['RGBA_PICKER_BG'] #self.pixbufs.newcolors['RGBA_PICKER_BG']

        #dummy initilisation
        self.cell_size = 15

        self.mywindow = Gtk.Window()
        self.mywindow.set_transient_for(self.myparent)
        self.mywindow.set_modal(False)
        self.mywindow.set_decorated(False)
        self.mywindow.set_size_request(1,1)

        self.mywindow.connect('destroy', self.on_Me_destroy)
        self.mywindow.connect('hide', self.on_Me_hide)
        self.mywindow.connect('key-release-event', self.picker_key_release_event)
        self.mywindow.connect('button-press-event', self.on_Me_clicked)

        self.init_for_hide = True

        box = Gtk.Box()
        da = Gtk.DrawingArea()
        da.set_visible(True)
        da.set_hexpand(True)
        da.set_vexpand(True)
        da.connect('draw', self.draw_da)
        da.show()
        box.add(da)
        self.da = da
        box.set_visible(True)
        self.mywindow.add(box)
        box.show()

        self.board_pixbuf = self.create_pixbuf()

    def draw_da(self, widget, cr, *args):
        if self.board_pixbuf:
            box_size = 3 * self.cell_size
            Gdk.cairo_set_source_pixbuf(cr, self.board_pixbuf, 0, 0)
            cr.paint()

    def on_Me_clicked(self, widget, event, *args):
        if event.button == 3:
            self.response_from_picker(number = 0)
        elif event.button == 1:
            x = event.x
            y=event.y
            col, dummy = divmod(x,self.cell_size)
            row, dummy = divmod(y,self.cell_size)
            number = int((3 * row) + col+1)
            self.response_from_picker(number = number)
        return True

    def on_Me_leave_event(self, widget, *args):
        self.response_from_picker(number = -1)
        return True

    def on_Me_hide(self, widget, *args):
        pass

    def on_Me_destroy(self, widget, *args):
        pass

    def picker_key_release_event(self, widget, event, *args):
        """ Handler for mywindow.key-release-event. """
        txt = Gdk.keyval_name(event.keyval)
        if type(txt) == type(None):
            return False
        unichar = chr(Gdk.keyval_to_unicode(event.keyval))
        txt = txt.replace('KP_', '')
        if txt in ['BackSpace','Delete',]:
            self.response_from_picker(number = 0)
            return True
        if txt == 'Escape':
            self.response_from_picker(number = -1)
            return True
        if unichar in self.strings_to_use[1:]:
            theint = self.strings_to_use.index(unichar)
            self.response_from_picker(number = theint)
            return True

    def picker_button_press_event(self, widget, event, *args):
        if event.button == 3:
            self.response_from_picker(number = 0)
        elif event.button == 1:
            number = (3 * args[1]) + (args[0]+1)
            self.response_from_picker(number = number)
        return True

    def create_pixbuf(self):
        one_size = 3 * self.cell_size
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, one_size, one_size)
        cr = cairo.Context(surface)
        w0 = self.cell_size

        number = 0

        for column in range(3):
            for row in range(3):
                number = (3 * row) + (column+1)
                apixbuf = self.pixbufs[number]
                cr.save()
                cr.set_source_rgba(*self.bg_color)
                cr.rectangle(w0*column  ,w0*row , w0, w0)
                cr.fill()
                cr.restore()
                cr.save()
                Gdk.cairo_set_source_pixbuf(cr, apixbuf,w0*column,w0*row)
                cr.paint()
                cr.stroke()
                cr.restore()
        cr.set_line_width(1)
        cr.set_source_rgba(0, 0, 0, 1)
        for acounter in range(3):
            cr.save()
            x1 = y1 = w0 * acounter
            cr.move_to(x1, 0)
            cr.line_to(x1, one_size)
            cr.stroke()
            cr.move_to(0, x1)
            cr.line_to(one_size, x1)
            cr.stroke()
            cr.restore()

        board_pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, one_size, one_size)
        return board_pixbuf

    def change_for_pixbufs(self, pixbufs):
        self.pixbufs = pixbufs
        self.cell_size = 2 + self.pixbufs[1].get_width()
        self.board_pixbuf = self.create_pixbuf()

        self.mywindow.set_size_request(3*self.cell_size - 2 , 3*self.cell_size-2)
        self.mywindow.resize(3*self.cell_size - 2 , 3*self.cell_size -2)

