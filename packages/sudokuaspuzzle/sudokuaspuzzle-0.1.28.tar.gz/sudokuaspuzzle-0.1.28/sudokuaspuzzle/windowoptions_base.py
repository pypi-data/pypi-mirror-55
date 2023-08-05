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

Since we are in python, any subclass of this class
will take over any method with the same name.
So do not declare here methods that exist also in the subclass.
(subclass is the class that uses the class here as Base.
Imagine the subclass as a super-duper class,
although in computing superclass is the base class)
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
    from gi.repository import Gdk
    from gi.repository import GObject
    # space for extra Gtk imports

    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox
    from constants import *

    # Load static methods
    from windowoptions_statics import *

    from puzzle import *
    from gamepixbufs import *

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

class WindowOptionsBase(object):
    #FIXME: fix the docstring.
    """ Main window with all components. """

    def __init__(self, *args, **kwargs):
        # Set the app
        self.myparent = None
        self.custom_args = kwargs['custom_args']

        # bind settings,options to a class variable
        global settings
        settings = self.settings
        global options
        options = self.options

        # Before builder.
        self._run_before_builder()

        # Read GUI from file and retrieve objects from Gtk.Builder
        thebuilder = Gtk.Builder()
        thebuilder.set_translation_domain(self.Application.id)
        try:
            thebuilder.add_from_file(os.path.join(self.Application.custom_args.APP_DIR,
                'ui',
                'windowoptions.glade')
                )
        except GObject.GError:
            print("Error reading GUI file")
            raise

        # Fire up the main window
        #We must get the object from builder to set the Application
        #before loading the objects, so that the rest will be loaded
        #using locale
        self.WindowOptions = thebuilder.get_object("WindowOptions")
        self.WindowOptions.set_application(self.Application)
        self._get_from_builder(thebuilder)
        self.mywindow = self.WindowOptions
        self._post_initialisations()
        self.mywindow.show()

#********* Auto created "class defs" START ************************************************************
    def _run_before_builder(self):
        self.board_pixbuf = None
        #self.new_colors["RGBA_BG_TRANSP"] = Gdk.RGBA(red=1., green=1., blue=1., alpha=0.0)
        self.dicts_widgets = {}
        self.custom_chars_widgets = {}
        THEDICTS["custom"] = THEDICTS["standard"].copy()

    def _get_from_builder(self, builder):
        """ Create self names for easy access. """
        self.AdjustmentForRatio = builder.get_object('AdjustmentForRatio')
        self.BoxForBottom = builder.get_object('BoxForBottom')
        self.BoxForDifficulty = builder.get_object('BoxForDifficulty')
        self.BoxForDrawingArea = builder.get_object('BoxForDrawingArea')
        self.BoxForLegend = builder.get_object('BoxForLegend')
        self.BoxMain = builder.get_object('BoxMain')
        self.BoxOnButtonCheck = builder.get_object('BoxOnButtonCheck')
        self.BoxOnTop = builder.get_object('BoxOnTop')
        self.ButtonBgColorConstant = builder.get_object('ButtonBgColorConstant')
        self.ButtonBgColorConstantSelected = builder.get_object('ButtonBgColorConstantSelected')
        self.ButtonBgColorEmpty = builder.get_object('ButtonBgColorEmpty')
        self.ButtonBgColorSelected = builder.get_object('ButtonBgColorSelected')
        self.ButtonDefaults = builder.get_object('ButtonDefaults')
        self.ButtonExit = builder.get_object('ButtonExit')
        self.ButtonFgColorRed = builder.get_object('ButtonFgColorRed')
        self.ButtonFontName = builder.get_object('ButtonFontName')
        self.ButtonForeColor = builder.get_object('ButtonForeColor')
        self.ButtonPickerBgColor = builder.get_object('ButtonPickerBgColor')
        self.ButtonRefresh = builder.get_object('ButtonRefresh')
        self.ButtonSave = builder.get_object('ButtonSave')
        self.CheckOnlyBoard = builder.get_object('CheckOnlyBoard')
        self.CheckShowRemaining = builder.get_object('CheckShowRemaining')
        self.CheckShowTimer = builder.get_object('CheckShowTimer')
        self.DrawingAreaForDemo = builder.get_object('DrawingAreaForDemo')
        self.DummyLabelColors = builder.get_object('DummyLabelColors')
        self.DummyLabelFont = builder.get_object('DummyLabelFont')
        self.Eb1_1 = builder.get_object('Eb1_1')
        self.Eb1_2 = builder.get_object('Eb1_2')
        self.Eb1_3 = builder.get_object('Eb1_3')
        self.Eb1_4 = builder.get_object('Eb1_4')
        self.Eb1_5 = builder.get_object('Eb1_5')
        self.Eb1_6 = builder.get_object('Eb1_6')
        self.Eb1_7 = builder.get_object('Eb1_7')
        self.Eb1_8 = builder.get_object('Eb1_8')
        self.Eb1_9 = builder.get_object('Eb1_9')
        self.GridForDictionaries = builder.get_object('GridForDictionaries')
        self.GridForFontAndColors = builder.get_object('GridForFontAndColors')
        self.GridForLegend = builder.get_object('GridForLegend')
        self.GridPresentOptions = builder.get_object('GridPresentOptions')
        self.ImageOnButtonRefresh = builder.get_object('ImageOnButtonRefresh')
        self.LabelAppearance = builder.get_object('LabelAppearance')
        self.LabelDifficulty = builder.get_object('LabelDifficulty')
        self.LabelLegend = builder.get_object('LabelLegend')
        self.LabelLegend1 = builder.get_object('LabelLegend1')
        self.LabelLegend2 = builder.get_object('LabelLegend2')
        self.LabelLegend3 = builder.get_object('LabelLegend3')
        self.LabelLegend4 = builder.get_object('LabelLegend4')
        self.LabelLegend5 = builder.get_object('LabelLegend5')
        self.LabelLegend6 = builder.get_object('LabelLegend6')
        self.LabelLegend7 = builder.get_object('LabelLegend7')
        self.LabelLegend8 = builder.get_object('LabelLegend8')
        self.LabelLegend9 = builder.get_object('LabelLegend9')
        self.LabelLegendDescription = builder.get_object('LabelLegendDescription')
        self.LabelLetter1_1 = builder.get_object('LabelLetter1_1')
        self.LabelLetter1_2 = builder.get_object('LabelLetter1_2')
        self.LabelLetter1_3 = builder.get_object('LabelLetter1_3')
        self.LabelLetter1_4 = builder.get_object('LabelLetter1_4')
        self.LabelLetter1_5 = builder.get_object('LabelLetter1_5')
        self.LabelLetter1_6 = builder.get_object('LabelLetter1_6')
        self.LabelLetter1_7 = builder.get_object('LabelLetter1_7')
        self.LabelLetter1_8 = builder.get_object('LabelLetter1_8')
        self.LabelLetter1_9 = builder.get_object('LabelLetter1_9')
        self.LabelNumberingSystem = builder.get_object('LabelNumberingSystem')
        self.LabelOnButtonRefresh = builder.get_object('LabelOnButtonRefresh')
        self.RadioButtonAny = builder.get_object('RadioButtonAny')
        self.RadioButtonForLetters = builder.get_object('RadioButtonForLetters')
        self.RadioButtoneasy = builder.get_object('RadioButtoneasy')
        self.RadioButtonexpert = builder.get_object('RadioButtonexpert')
        self.RadioButtonintermediate = builder.get_object('RadioButtonintermediate')
        self.RadioButtonsimple = builder.get_object('RadioButtonsimple')
        self.ScaleForRatio = builder.get_object('ScaleForRatio')
        self.WindowOptions = builder.get_object('WindowOptions')

        # Connect signals existing in the Glade file.
        builder.connect_signals(self)

        # Connect generated by OCPgenerator signals:
        # to builder's main window
        # first are the defaults for window
        self.WindowOptions.connect('delete-event', self.on_WindowOptions_delete_event)
        self.WindowOptions.connect('destroy', self.on_WindowOptions_destroy)
        self.WindowOptions.connect('size-allocate', self.on_WindowOptions_size_allocate)
        self.WindowOptions.connect('window-state-event', self.on_WindowOptions_window_state_event)
        self.ButtonDefaults.connect('clicked', self.on_ButtonDefaults_clicked)
        self.ButtonExit.connect('clicked', self.on_ButtonExit_clicked)
        self.ButtonRefresh.connect('clicked', self.on_ButtonRefresh_clicked)
        self.ButtonSave.connect('clicked', self.on_ButtonSave_clicked)
        self.CheckOnlyBoard.connect('toggled', self.on_CheckOnlyBoard_toggled)
        self.CheckShowRemaining.connect('toggled', self.on_CheckShowRemaining_toggled)
        self.CheckShowTimer.connect('toggled', self.on_CheckShowTimer_toggled)

    def _post_initialisations(self):
        """ Do some extra initializations.

        Display the version if a labelVersion is found.
        Set defaults (try to load them from a configuration file):
            - Window size and state (width, height and if maximized)
        Load any custom settings from a configuration file.
        """
        if 'parent' in self.custom_args:#Is a child window, get the parent window
            self.myparent = self.custom_args['parent']
            #if has parent check for transient
            # modality can be false, and parent may not be present
            if 'transient' in self.custom_args:
                self.mywindow.set_transient_for(self.myparent)
                if 'modal' in self.custom_args:
                    self.mywindow.set_modal(True)

        if 'trigger_before_exit' in self.custom_args:
            # must be a function on calling class
            self.trigger_before_exit = self.custom_args['trigger_before_exit']
            self.return_parameters = None

        # Bind message boxes.
        self.MessageBox = MessageBox(self.WindowOptions, self.Application)
        self.msg = self.MessageBox.Message
        self.are_you_sure = self.MessageBox.are_you_sure

        # Reset MainWindow to a default or previous size and state.
        width = settings.get('width', 350)
        height = settings.get('height', 350)
        self.WindowOptions.set_title(_("Options") + " - " + self.Application.custom_args.localizedname)
        self.WindowOptions.resize(width, height)
        self.WindowOptions.set_icon(self.Application.icon)
        if settings.get_bool('maximized', False):
            self.WindowOptions.maximize()

        # Load any other settings here.
        self.pb = None
        self.picker = None
        self.previous_size = 0

        self.init_defaults()
        self.GridForLegend.override_background_color(Gtk.StateFlags.NORMAL, DEFAULT_RGBA['BG'])

#********* Auto created handlers START *********************************
    def on_ButtonColor_color_set(self, widget, *args):
        """ Handler for any ButtonColor.color-set. """
        rbga = widget.get_rgba()
        if widget == self.ButtonBgColorEmpty:
            self.all_colors['RGBA_BG'] = rbga
        elif widget == self.ButtonForeColor:
            self.all_colors['RGBA_FG'] = rbga
        elif widget == self.ButtonFgColorRed:
            self.all_colors['RGBA_FG_RED'] = rbga
        elif widget == self.ButtonBgColorConstant:
            self.all_colors['RGBA_BG_CONSTANT'] = rbga
        elif widget == self.ButtonBgColorSelected:
            self.all_colors['RGBA_BG_SELECTED'] = rbga
        elif widget == self.ButtonBgColorConstantSelected:
            self.all_colors['RGBA_BG_CONSTANT_SELECTED'] = rbga
        elif widget == self.ButtonPickerBgColor:
            self.all_colors['RGBA_PICKER_BG'] = rbga

    def on_ButtonDefaults_clicked(self, widget, *args):
        """ Handler for ButtonDefaults.clicked. """
        self.set_defaults()

    def on_ButtonExit_clicked(self, widget, *args):
        """ Handler for ButtonExit.clicked. """
        self.exit_requested()
        return True

    def on_ButtonFontName_font_set(self, widget, *args):
        """ Handler for ButtonFontName.font-set. """
        self.font_name = widget.get_font_name()
        self.fix_font_size()

    def on_ButtonRefresh_clicked(self, widget, *args):
        """ Handler for ButtonRefresh.clicked. """
        self.create_board()
        return True

    def on_ButtonSave_clicked(self, widget, *args):
        """ Handler for ButtonSave.clicked. """
        self.save_new_options()
        self.exit_requested()
        return True

    def on_CheckOnlyBoard_toggled(self, widget, *args):
        """ Handler for CheckOnlyBoard.toggled. """
        self.SHOW_ONLY_BOARD = self.CheckOnlyBoard.get_active()
        self.CheckShowRemaining.set_sensitive(not self.SHOW_ONLY_BOARD)
        self.CheckShowTimer.set_sensitive(not self.SHOW_ONLY_BOARD)

    def on_CheckShowRemaining_toggled(self, widget, *args):
        """ Handler for CheckShowRemaining.toggled. """
        self.SHOW_PIECES = self.CheckShowRemaining.get_active()

    def on_CheckShowTimer_toggled(self, widget, *args):
        """ Handler for CheckShowTimer.toggled. """
        self.SHOW_TIMER = self.CheckShowTimer.get_active()

    def on_DrawingAreaForDemo_draw(self, widget, cr, *args):
        """ Handler for DrawingAreaForDemo.draw. """
        if self.board_pixbuf:
            cr.save()
            Gdk.cairo_set_source_pixbuf(cr, self.board_pixbuf, 0, 0)
            cr.paint()
            cr.restore()

    def on_RadioButtonDifficulty_toggled(self, widget, *args):
        """ Handler for any RadioButton for difficulty toggled. """
        if widget.get_active():
            self.DIFFICULTY = widget.get_name()

    def on_ScaleForRatio_change_value(self, widget, scroll, new_value, *args):
        """ Handler for ScaleForRatio.change-value. """
        if new_value <= 1 and new_value >=0.4:
            self.font_ratio = new_value

    def on_WindowOptions_key_release_event(self, widget, event, *args):
        """ Handler for WindowOptions.key-release-event. """
        txt = Gdk.keyval_name(event.keyval)
        if type(txt) == type(None):
            return False

        unichar = chr(Gdk.keyval_to_unicode(event.keyval))
        txt = txt.replace('KP_', '')
        if event.get_state() & Gdk.ModifierType.CONTROL_MASK:
            if txt.lower() == "s":
                self.save_new_options()
                self.exit_requested()
                return True
            elif txt.lower() == "p":
                self.create_board()
                return True
            elif txt.lower() == "h":
                self.exit_requested()
                return True
            elif txt.lower() == "q":
                self.exit_requested()
                return True
            elif txt.lower() == "a":
                self.MessageBox.AboutBox()
                return True
#********* Auto created handlers END ***********************************

#********* Standard handlers START *************************************
    def msg_not_yet(self):
        """ Standarized message for not implemented functionality. """
        self.msg(_('Not yet implemented'))

    def on_WindowOptions_delete_event(self, widget, event, *args):
        """ Handler for our main window: delete-event. """
        return (self.exit_requested())

    def on_WindowOptions_destroy(self, widget, *args):
        """ Handler for our main window: destroy. """
        return (self.exit_requested('from_destroy'))

    def on_WindowOptions_size_allocate(self, widget, allocation, *args):
        """ Handler for our main window: size-allocate. """
        self.save_my_size()

    def on_WindowOptions_window_state_event(self, widget, event, *args):
        """ Handler for our main window: window-state-event. """
        settings.set('maximized',
            ((int(event.new_window_state) & Gdk.WindowState.ICONIFIED) != Gdk.WindowState.ICONIFIED) and
            ((int(event.new_window_state) & Gdk.WindowState.MAXIMIZED) == Gdk.WindowState.MAXIMIZED)
            )
        self.save_my_size()

#********* Standard handlers END ***************************************
#********* Standard exit defs START *********************************************************
    def exit_requested(self, *args, **kwargs):
        """ Final work before exit. """
        self.WindowOptions.set_transient_for()
        self.WindowOptions.set_modal(False)
        self.set_unhandled_settings()# also saves all settings
        if 'from_destroy' in args:
            return True
        else:
            # Check if we should provide info to caller
            if 'trigger_before_exit' in self.custom_args:
                self.trigger_before_exit(exiting = True,
                    return_parameters = self.return_parameters)
            self.WindowOptions.destroy()

    def present(self):
        """ Show the window. """
        pass

    def save_my_size(self):
        """ Save the window size into settings, if not maximized. """
        if not settings.get_bool('maximized', False):
            width, height = self.WindowOptions.get_size()
            settings.set('width', width)
            settings.set('height', height)

    def set_unhandled_settings(self):
        """ Set, before exit, any settings not applied during the session.

        Additionally, flush all settings to .conf file.
        """
        # Set any custom settings
        # which where not setted (ex. on some widget's state changed)
        # Save all settings
        settings.save()
#********* Standard exit defs END **************************************
#********* Auto created "class defs" END **************************************************************

    def fill_dicts(self):
        thegrid = self.GridForDictionaries
        self.RadioButtonForLetters.tag = 'standard'
        self.dicts_widgets['standard'] = self.RadioButtonForLetters
        self.RadioButtonForLetters.connect('toggled', self.on_RadioButtonDict_toggled, self.dicts_widgets['standard'])
        for rowcounter in range(len(DICTSLIST))[1:-1]:
            dict_name = DICTSLIST[rowcounter]
            thedict = THEDICTS[dict_name]
            theoption = Gtk.RadioButton(_(dict_name).title())
            theoption.join_group(self.RadioButtonForLetters)
            theoption.connect('toggled', self.on_RadioButtonDict_toggled, theoption)
            theoption.tag = dict_name
            thegrid.attach(theoption,0,rowcounter,1,1)
            self.dicts_widgets[dict_name] = theoption
            for x in range(9):
                label = Gtk.Label(thedict[x+1])
                thegrid.attach(label,x+1,rowcounter,1,1)
        rowcounter = len(DICTSLIST)-1
        dict_name = DICTSLIST[rowcounter]
        thedict = THEDICTS[dict_name]
        theoption = Gtk.RadioButton(_(dict_name).title())
        theoption.join_group(self.RadioButtonForLetters)
        theoption.connect('toggled', self.on_RadioButtonDict_toggled, theoption)
        theoption.tag = dict_name
        thegrid.attach(theoption,0,rowcounter,1,1)
        for lettercounter in range(9):
            entry = Gtk.Entry()
            entry.set_text(thedict[lettercounter+1])
            entry.set_width_chars(2)#fixing the stupid GtkEnonEntryButEntryWithGarbageandmore
            entry.set_has_frame (False)
            entry.set_max_width_chars(1)
            entry.entry_tag = lettercounter+1
            entry.connect('changed', self.on_any_custom_char_changed, lettercounter+1)
            entry.connect('button-release-event', self.on_any_custom_char_clicked)
            entry.set_sensitive(False)
            thegrid.attach(entry,lettercounter+1,rowcounter,1,1)
            self.custom_chars_widgets[lettercounter] = entry
        self.dicts_widgets[dict_name] = theoption
        thegrid.show_all()
        #self.dicts_widgets[self.use_dict].set_active(True)

    def on_RadioButtonDict_toggled(self, widget, *args):
        #self.use_dict = args[0].tag
        if widget.get_active():
            self.use_dict = widget.tag
            is_the_custom = (widget.tag == 'custom')
            for anentry in self.custom_chars_widgets:
                self.custom_chars_widgets[anentry].set_sensitive(is_the_custom)

    def on_any_custom_char_changed(self, widget, *args):
        THEDICTS['custom'][args[0]] = widget.get_text()

    def on_any_custom_char_clicked(self, widget, *args):
        widget.select_region(0,-1)

    def init_defaults(self):
        self.DIFFICULTY = 'easy' #simple, easy, intermediate, expert
        self.SHOW_ONLY_BOARD = False
        self.SHOW_PIECES = True
        self.SHOW_TIMER = True
        self.font_name = "Arial 400"
        self.font_ratio = float(0.95)
        self.use_dict = "standard"
        self.all_colors = {}#ALL_COLORS.copy()
        self.all_colors['RGBA_BG'] = DEFAULT_RGBA['BG']
        self.all_colors['RGBA_FG'] = DEFAULT_RGBA['FG']
        self.all_colors['RGBA_FG_RED'] = DEFAULT_RGBA['FG_RED']
        self.all_colors['RGBA_BG_CONSTANT'] = DEFAULT_RGBA['BG_CONSTANT']
        self.all_colors['RGBA_BG_SELECTED'] = DEFAULT_RGBA['BG_SELECTED']
        self.all_colors['RGBA_BG_CONSTANT_SELECTED'] = DEFAULT_RGBA['BG_CONSTANT_SELECTED']
        self.all_colors["RGBA_BG_TRANSP"] = DEFAULT_RGBA['BG_TRANSP']
        self.all_colors["RGBA_PICKER_BG"] = DEFAULT_RGBA['PICKER_BG']

    def set_defaults(self):
        self.init_defaults()
        self.show_current_options()

    def load_options(self):
        """ Load options.

        First will set the defaults.
        Then will load them from a user configuration file.
        """
        self.init_defaults()
        self.DIFFICULTY = options.get("DIFFICULTY", self.DIFFICULTY)
        if self.DIFFICULTY not in ["simple", "easy", "intermediate", "expert", "any"]:
            self.DIFFICULTY = 'easy'
        self.SHOW_ONLY_BOARD = options.get_bool("show_only_board", self.SHOW_ONLY_BOARD)
        self.SHOW_PIECES = options.get_bool("show_pieces", self.SHOW_PIECES)
        self.SHOW_TIMER = options.get_bool("show_timer", self.SHOW_TIMER)

        self.font_name = options.get("font_name", self.font_name)
        self.fix_font_size()
        self.ButtonFontName.set_font_name(self.font_name)
        font_ratio = options.get("font_ratio",str(self.font_ratio))
        self.font_ratio = float(font_ratio)
        strings = options.get("custom_dict","")
        strings_list = [x.strip() for x in strings.split(",")]
        if len(strings_list) == 9:
            strings_list.insert(0, ' ')
            THEDICTS['custom'] = strings_list
        self.use_dict = options.get("use_dict", self.use_dict)
        self.all_colors["RGBA_BG"] = eval_rgba(
                options.get('RGBA_BG', str(self.all_colors['RGBA_BG'])))
        self.all_colors["RGBA_FG"] = eval_rgba(
                options.get('RGBA_FG', str(self.all_colors['RGBA_FG'])))
        self.all_colors["RGBA_FG_RED"] = eval_rgba(
                options.get('RGBA_FG_RED', str(self.all_colors['RGBA_FG_RED'])))
        self.all_colors["RGBA_BG_CONSTANT"] = eval_rgba(
                options.get('RGBA_BG_CONSTANT', str(self.all_colors['RGBA_BG_CONSTANT'])))
        self.all_colors["RGBA_BG_SELECTED"] = eval_rgba(
                options.get('RGBA_BG_SELECTED', str(self.all_colors['RGBA_BG_SELECTED'])))
        self.all_colors["RGBA_BG_CONSTANT_SELECTED"] = eval_rgba(
                options.get('RGBA_BG_CONSTANT_SELECTED', str(self.all_colors['RGBA_BG_CONSTANT_SELECTED'])))
        self.all_colors["RGBA_PICKER_BG"] = eval_rgba(
                options.get('RGBA_PICKER_BG', str(self.all_colors['RGBA_PICKER_BG'])))
        self.show_current_options()

    def show_current_options(self):
        """ Show active options.

        Forces update of any changes.
        Calls set_rgba_in_buttons for updating the colors
        in buttons.
        """
        self.CheckOnlyBoard.set_active(self.SHOW_ONLY_BOARD)
        self.CheckShowRemaining.set_active(self.SHOW_PIECES)
        self.CheckShowTimer.set_active(self.SHOW_TIMER)
        self.ScaleForRatio.set_value(self.font_ratio)
        self.set_rgba_in_buttons()
        if not (self.use_dict in self.dicts_widgets):
            #show a delayed message
            GObject.timeout_add(interval=50, function=self.stupid_timer_1)
            self.use_dict = "standard"
        self.dicts_widgets[self.use_dict].set_active(True)
        for anumber in range(9):
            self.custom_chars_widgets[anumber].set_text(THEDICTS["custom"][anumber+1])
        self.create_board()
        for anwidget in self.BoxForDifficulty.get_children():
            if anwidget.get_name() == self.DIFFICULTY:
                anwidget.set_active(True)
                break

    def stupid_timer_1(self):
        self.msg(_("Dictionary {0} not found!\nUsing standard.").format(self.use_dict,),
            boxtype = 'ERROR')
        return False

    def set_rgba_in_buttons(self):
        self.ButtonBgColorEmpty.set_rgba(self.all_colors['RGBA_BG'])
        self.ButtonForeColor.set_rgba(self.all_colors['RGBA_FG'])
        self.ButtonFgColorRed.set_rgba(self.all_colors['RGBA_FG_RED'])
        self.ButtonBgColorConstant.set_rgba(self.all_colors['RGBA_BG_CONSTANT'])
        self.ButtonBgColorSelected.set_rgba(self.all_colors['RGBA_BG_SELECTED'])
        self.ButtonBgColorConstantSelected.set_rgba(self.all_colors['RGBA_BG_CONSTANT_SELECTED'])
        self.ButtonPickerBgColor.set_rgba(self.all_colors['RGBA_PICKER_BG'])

    def save_new_options(self):
        try:
            options.set("show_only_board", self.SHOW_ONLY_BOARD)
            options.set("show_pieces", self.SHOW_PIECES)
            options.set("show_timer", self.SHOW_TIMER)
            options.set("DIFFICULTY", self.DIFFICULTY)
            options.set("font_name", self.font_name)
            options.set("font_ratio",str(self.font_ratio))
            options.set("custom_dict",','.join([str(x) for x in THEDICTS["custom"][1:]]))
            options.set("use_dict", self.use_dict)
            options.set("RGBA_BG", str(self.all_colors['RGBA_BG']))
            options.set("RGBA_FG", str(self.all_colors['RGBA_FG']))
            options.set("RGBA_FG_RED", str(self.all_colors['RGBA_FG_RED']))
            options.set("RGBA_BG_CONSTANT", str(self.all_colors['RGBA_BG_CONSTANT']))
            options.set("RGBA_BG_SELECTED", str(self.all_colors['RGBA_BG_SELECTED']))
            options.set("RGBA_BG_CONSTANT_SELECTED", str(self.all_colors['RGBA_BG_CONSTANT_SELECTED']))
            options.set("RGBA_PICKER_BG", str(self.all_colors['RGBA_PICKER_BG']))
            self.msg(_("Options saved!"), boxtype = 'INFO')
            return
        except Exception as e:
            print(e)
        self.msg(_("Options NOT saved!"), boxtype = 'ERROR')

    def create_board(self):
        self.pb = GamePixBufs(self.mywindow, THEDICTS[self.use_dict], self.font_name, self.all_colors, self.font_ratio)
        self.pb.fit_pixbufs(OPTIONS_BOARD_SIZE // 3)
        self.board_pixbuf = create_board_pixbuf_for_options(self.pb)
        self.DrawingAreaForDemo.queue_draw()

    def fix_font_size(self):
        self.font_name = self.font_name.split(" ",-1)[0] + " 10"

#********* Window class  END***************************************************************************
