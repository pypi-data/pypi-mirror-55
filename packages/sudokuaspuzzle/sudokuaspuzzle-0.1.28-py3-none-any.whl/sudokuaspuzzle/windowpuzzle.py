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
    import datetime
    import random

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk
    from gi.repository import GObject

    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox
    from constants import *

    # Load base window class and static methods
    from windowpuzzle_base import WindowPuzzleBase
    from windowpuzzle_statics import *

    from picker import *
    from gamepixbufs import *

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

class WindowPuzzleClass(WindowPuzzleBase):
    #FIXME: fix the docstring.
    """ Main window with all components. """

    def __init__(self, application, *args, **kwargs):
        self.Application = application
        # define and bind settings, options to a class variable
        global settings
        global options
        settings = SectionConfig(self.Application.id, self.__class__.__name__)
        options = OptionConfig(self.Application.id)
        self.settings = settings
        self.options = options

        #Place here any initilizations before loading the ui
        #Passed custom_args will be evaluated while loading the ui
        self.targets = None # Gtk.TargetList.new([])
        self.number_picked = None
        self.remaining_ebs = {}
        self.show_picker_at = None

        super().__init__(self,  *args, **kwargs)

        #place here initilisations after loading the ui
        self.one_size = 0
        self.mouse_over = 0

        self.pb = GamePixBufs(self.mywindow, self.strings_to_use,
                self.font_name, self.new_colors,
                font_ratio = self.font_ratio)

        if self.SHOW_ONLY_BOARD:
            self.SHOW_PIECES = False
            self.SHOW_TIMER = False
            self.BoxOnTop.set_visible(False)
        if self.SHOW_PIECES:
            self.init_remaining()
        else:
            self.ListBoxForPieces.set_visible(False)
        self.set_show_timer(self.SHOW_TIMER)

        self.check_board_resize()
        self._create_picker()

        self.trigger_from_puzzle()
        self.EventBoxForPuzzle.grab_focus()
        self.start_time = datetime.datetime.utcnow()
        if 'continue' in self.custom_args:
            self.start_time = datetime.datetime.utcnow() - \
                    datetime.timedelta(seconds = int(self.last_game['last_seconds_passed']))

        self.timer_id = GObject.timeout_add(interval=500, function=self.show_new_time)

    def _create_picker(self):
        """ Create the picker window.

        Must be called only once!"""
        some_custom_args = {}
        some_custom_args['response_from_picker'] = self.response_from_picker
        some_custom_args['parent'] = self.mywindow
        some_custom_args['pixbufs'] = self.pb.picker_pixbufs
        some_custom_args['strings_to_use'] = self.strings_to_use
        some_custom_args['RGBA_PICKER_BG'] = self.new_colors['RGBA_PICKER_BG']
        self.picker = NumberPicker(args_to_pass=some_custom_args)
        self.picker.mywindow.hide()

    def on_remaining_pressed(self, widget, event, *args):
        """ Handler for any "remaining pieces label" button-press-event.

        Triggered if label with remaining pieces is pressed. """
        if self.puzzle.remaining[args[0]]>0:
            self.remaining_Image.set_from_pixbuf(self.pb.fitted_pixbufs[args[0]])
        else:
            self.remaining_Image.set_from_pixbuf(CLEAR_ICON)

    def _clear_icon_drag_begin(self, widget, context):
        self.number_picked = CLEAR_AS_NUMBER_PICKED
        Gtk.drag_set_icon_pixbuf(context, CLEAR_ICON, 0, CLEAR_ICON.get_height())

    def _clear_icon_drag_end(self, widget, context):
        self.number_picked = None

    def _eb_drag_begin(self, widget, context):
        #set here the drag icon, this is a connect_after event
        #will override the default dragicon
        if len(widget.get_children()[0].get_label().strip()):
            self.number_picked = widget.my_tag
            Gtk.drag_set_icon_pixbuf(context,
                    self.pb.picker_pixbufs[int(self.number_picked)],
                    self.pb.picker_pixbufs[int(self.number_picked)].get_width(),
                    self.pb.picker_pixbufs[int(self.number_picked)].get_height())
        else:
            self.number_picked = None

    def _eb_drag_end(self, widget, context):
        self.number_picked = None
        self.remaining_Image.set_from_pixbuf(CLEAR_ICON)

    def init_remaining(self):
        self.labels_remaining = {}
        self.ebs_remaining = {}
        thelistbox = self.ListBoxForPieces
        allchildren = thelistbox.get_children()
        for achild in allchildren[:]:
            achild.destroy()
        labeltext = _('Remaining numbers:')
        label = Gtk.Label(labeltext)
        #prevent resize of right listbox
        if len(labeltext) < 12:
            label.set_label(labeltext + " " * 2 * (12-len(labeltext)))
        label.set_visible(True)
        label.set_can_focus (False)
        thelistbox.add(label)
        for number_counter in range(9):
            number_to_show = self.strings_to_use[number_counter+1]
            remaining = 9
            label = Gtk.Label(number_to_show * remaining)
            label.set_xalign(0)
            label.set_can_focus (False)
            eb = Gtk.EventBox()
            eb.add(label)
            self.labels_remaining[number_counter+1] = label
            eb.connect('button-press-event', self.on_remaining_pressed, number_counter+1)
            label.set_tooltip_text(PLACE_NUMBER_TEXT.format(number_to_show))
            thelistbox.add(eb)
            eb.set_visible(True)
            eb.my_tag = str(number_counter+1)
            label.set_visible(True)
            eb_data = {'widget':eb,
                'handler1':None,
                'handler2':None}
            self.remaining_ebs[number_counter] = eb_data
        label = Gtk.Label("81")
        label.set_xalign (0.5)
        label.set_can_focus (False)
        self.LabelRemaining = label
        eb = Gtk.EventBox()
        eb.add(label)
        thelistbox.insert(eb,1)
        eb.set_visible(True)
        label.set_visible(True)
        theimage = Gtk.Image.new_from_pixbuf(CLEAR_ICON)
        theimage.set_visible(True)
        self.remaining_Image = theimage
        eb = Gtk.EventBox()
        eb.add(theimage)
        thelistbox.add(eb)
        eb.drag_source_set(Gdk.ModifierType.BUTTON1_MASK,
            self.targets,
            Gdk.DragAction.COPY)
        eb.connect_after("drag-begin", self._clear_icon_drag_begin)
        eb.connect("drag-end", self._clear_icon_drag_end)
        eb.drag_source_add_text_targets()
        self.ListBoxForPieces.show_all()
        self.show_remaining()

    def response_from_picker(self, *args, **kwargs):
        self.picker.mywindow.hide()
        if 'thenumbertupple' not in kwargs:
            if 'number' not in kwargs:
                return
        if self.clicked_on:
            self.clicked_on = None
            if kwargs['number'] == -1:return
            self.set_selected_cell(kwargs['number'])

    def check_board_resize(self):
        one_size = min(self.EventBoxForPuzzle.get_allocated_height(), self.EventBoxForPuzzle.get_allocated_width())
        if one_size != self.previous_size:
            ameasure = 3 * int(int(one_size/9)/3)
            self.pb.fit_pixbufs(ameasure)
            self.board_pixbuf = create_board_pixbuf(self.pb,
                    self.puzzle.current_cells,
                    self.EventBoxForPuzzle)
            self.previous_size = self.board_pixbuf.get_width()
            #print("check_board_resize", self.picker)
            if self.picker:
                self.picker.change_for_pixbufs(self.pb.picker_pixbufs)
            self.DrawingAreaForPuzzle.queue_draw()

    def show_new_time(self):
        secondspassed = self.seconds_passed()
        minutes, seconds = divmod(secondspassed, 60)
        if minutes>59:
            hours, minutes = divmod(minutes, 60)
            thestr = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
        else:
            thestr = '{:02}:{:02}'.format( minutes, seconds)
        if self.SHOW_TIMER:
            self.LabelTimePassed.set_label(thestr)
        return True

    def move_selection_by_arrow(self, arrowtxt):
        if not self.EventBoxForPuzzle.is_focus():
            self.EventBoxForPuzzle.grab_focus()
        row, column = divmod(self.puzzle.current_cells[0]-1, 9)
        if arrowtxt == "Up":
            row = (row-1) if (row>0) else 8
        elif arrowtxt == "Down":
            row = (row+1) if (row<8) else 0
        elif arrowtxt == "Left":
            column = (column-1) if (column>0) else 8
        elif arrowtxt == "Right":
            column = (column+1) if (column<8) else 0
        self.puzzle.current_cells[0] = (9 * row) + (column+1)
        self.create_board()
        return True

    def set_selected_cell(self, anint):
        if not self.EventBoxForPuzzle.is_focus():
            self.EventBoxForPuzzle.grab_focus()
        # do not append to history if same
        if self.puzzle.current_cells[self.puzzle.current_cells[0]][1] != \
                    anint:
            self.puzzle.set_cell(self.puzzle.current_cells[0], anint, self.seconds_passed())
        self.create_board()
        if self.puzzle.solved:
            if self.timer_id:
                GObject.source_remove(self.timer_id)
                self.timer_id = 0
            ok = self.msg(_("Bravo. Puzzle solved."))
            self.exit_requested()
        return True

    def seconds_passed(self):
        """ Return real time seconds passed."""
        new_time = datetime.datetime.utcnow()
        return int( (new_time - self.start_time).total_seconds())

    def show_remaining(self):
        if not self.SHOW_PIECES:return
        self.LabelRemaining.set_label( str(self.puzzle.remaining[0]))
        for acounter in range(9):
            label = self.labels_remaining[acounter+1]
            thestr1 = self.strings_to_use[acounter+1]
            if self.puzzle.remaining[acounter+1]:
                self.labels_remaining[acounter+1].set_label(
                        self.puzzle.remaining[acounter+1] *
                        self.strings_to_use[acounter+1])
            else:
                self.labels_remaining[acounter+1].set_label("")
            #if there are remaining
            no_remainings = (self.puzzle.remaining[acounter+1] < 1)
            thehandler = self.remaining_ebs[acounter]['handler1']
            if no_remainings:
                self.labels_remaining[acounter+1].set_tooltip_text(ALL_PLACED_TEXT.format(thestr1))
                if thehandler: self.unset_the_drag_for(acounter)
            else:
                self.labels_remaining[acounter+1].set_tooltip_text(PLACE_NUMBER_TEXT.format(thestr1))
                if thehandler == None: self.set_the_drag_for(acounter)

    def set_the_drag_for(self, acounter):
        """ Set the EventBox for «acounter» as drag source.

        Caller must check if not already set
        by examining if «handler1» is not None."""
        self.remaining_ebs[acounter]['widget'].drag_source_set(Gdk.ModifierType.BUTTON1_MASK,
            self.targets,
            Gdk.DragAction.COPY)
        eb_h = self.remaining_ebs[acounter]['widget'].connect_after("drag-begin", self._eb_drag_begin)
        self.remaining_ebs[acounter]['handler1'] = eb_h
        eb_h = self.remaining_ebs[acounter]['widget'].connect("drag-end", self._eb_drag_end)
        self.remaining_ebs[acounter]['handler2'] = eb_h
        self.remaining_ebs[acounter]['widget'].drag_source_add_text_targets()

    def unset_the_drag_for(self, acounter):
        """ Unset the EventBox for «acounter» as drag source.

        Caller must check if not already has been unset
        by examining if «handler1» is None."""
        self.remaining_ebs[acounter]['widget'].drag_source_unset()
        self.remaining_ebs[acounter]['widget'].disconnect(self.remaining_ebs[acounter]['handler1'])
        self.remaining_ebs[acounter]['handler1'] = None
        self.remaining_ebs[acounter]['widget'].disconnect(self.remaining_ebs[acounter]['handler2'])
        self.remaining_ebs[acounter]['handler2'] = None

    def show_undo_redo(self):
        self.ButtonUndo.set_sensitive((len(self.puzzle.history) > 0) and (self.puzzle.history_position > 0))
        self.ButtonRedo.set_sensitive(self.puzzle.history_position < len(self.puzzle.history))

    def set_show_timer(self, avalue):
        """ Hide or show the label for time based on preferences."""
        if self.SHOW_ONLY_BOARD:
            self.SHOW_TIMER  = False
        else:
            self.SHOW_TIMER = avalue
        if self.SHOW_TIMER:
            self.LabelTimePassed.show()
            self.ImageClock.show()
        else:
            self.LabelTimePassed.hide()
            self.ImageClock.hide()

    def trigger_from_puzzle(self, *args):
        """ Show remaining pieces and set the sensitivity
        of undo and redo buttons.

        Triggered when a move is done in the puzzle class."""
        self.show_remaining()
        self.show_undo_redo()

