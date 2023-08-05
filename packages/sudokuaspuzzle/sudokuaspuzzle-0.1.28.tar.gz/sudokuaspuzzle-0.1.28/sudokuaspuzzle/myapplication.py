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

#FIXME: correct the version
APPID = "org.kekbay.sudokuaspuzzleocp"
APPNAME = "Sudoku as puzzle"
__version__ = '0.1.28'

ERROR_IMPORT_LIBRARIES_FAIL = -1

try:
    import os
    import sys

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk, GdkPixbuf, GObject, Gio, GLib

    # Localization
    import locale
    import gettext

    #from locale import gettext

    # Configuration and message boxes
    from auxiliary import *
    from constants import *

    #At least a starting window must exist
    from windowmain import WindowMainClass

except ImportError as eximp:
    print("eximp1", eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

WHERE_AM_I = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))

settings = None # Will keep window related options
options = None # Will keep application wide options in a 'General Options' section

class CustomAppArgs:
    pass

class MyApplication(Gtk.Application):
    #FIXME: fix the docstring.
    """ Main entry of the application. """

    def __init__(self, *args, **kwargs):
        self.custom_args = CustomAppArgs()
        self.custom_args.START_DIR = kwargs['START_DIR']
        self.custom_args.APP_DIR = WHERE_AM_I
        self.id = APPID
        self.custom_args.version = __version__
        self.custom_args.windowmain = None
        self.init_locale()
        self.custom_args.name = APPNAME
        self.custom_args.localizedname = _("Sudoku as puzzle")

        Gtk.Application.__init__(self,
                application_id=self.id,
                flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)

        # Load the icon file.
        icon_file = os.path.join(self.custom_args.APP_DIR, "icons", "logo.png")
        self.icon = None
        if os.path.exists(icon_file):
            try:
                self.icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)
            except Exception:
                pass

        # Init the modules for settings (globally).
        self.set_config_file()

        self.connect("activate", self.my_activate)

    def init_locale(self):
        LOCALE_DIR = os.path.join(self.custom_args.APP_DIR, 'localedir')
        locale.setlocale(locale.LC_ALL, '')
        locale.bindtextdomain(self.id , LOCALE_DIR)
        #bind locale application wide
        gettext.install(self.id, LOCALE_DIR)

    def set_config_file(self):
        global settings
        settings = SectionConfig(self.id , self.__class__.__name__)
        global options
        options = OptionConfig(self.id)

    def my_activate(self, *args, **kwargs):
        # We only allow a single window and raise any existing ones
        if not self.custom_args.windowmain:
            self.open_windowmain()
        else:
            #probably unnecessary since it prints out in the first open
            #not in the second... so a second open will simply aborts.
            #logging is disk space consuming, so no log provided.
            print("WARNING! Application main window already exists")
        self.custom_args.windowmain.present()

    #FIXME: remove if not needed
    def custom_return_function(self, *args, **kwargs):
        """ Custom function to be triggered before opened window exit.

        Opened "startwindow" can use it to:
        - Return to this class a value.
        - Get from this class a processed value before exit.

        Notes
        -----
        This function will run BEFORE the opened window is destroyed.
        If you want to do something AFTER the window is destroyed,
        you should find other way or trigger.
        """
        # dummy printout
        # print("Game exited")
        # dummy return of my class name
        return self.__class__.__name__

    def do_command_line(self, command_line):
        """ Parse command line and activate the application. """
        start_options = command_line.get_options_dict()
        if start_options.contains("test"):
            # This is printed on the main instance
            # dummy printout
            print("Test argument recieved")
        self.activate()
        return 0

    def open_windowmain(self):
        #create args to send
        some_custom_args = {}
        some_custom_args['a text arg'] = "some text to pass as arg"

        # provide a local function to be triggered on exit
        some_custom_args['trigger_before_exit'] = self.trigger_from_windowmain
        #import the class
        #this is the app file. one window imported already

        #create an instance and add it to self.Application.MyArgs
        #as property
        self.custom_args.windowmain = WindowMainClass(application = self,
            custom_args = some_custom_args)
        self.custom_args.windowmain.mywindow.connect("destroy", self.windowmain_destroyed)
        #open the window
        self.custom_args.windowmain.present()

    def windowmain_destroyed(self, *args, **kwargs):
        """ Custom function to be triggered after opened window is destroyed.

        """
        #self.exit_requested()
        #nullify window as property of self.Application.MyArgs
        self.custom_args.windowmain = None

    def trigger_from_windowmain(self, *args, **kwargs):
        """ Custom function to be triggered before opened window exit.

        Opened "windowmain" can use it to:
        - Return to this class a value.
        - Get from this class a processed value before exit.

        Notes
        -----
        This function will run BEFORE the opened window is destroyed.
        If you want to do something AFTER the window is destroyed,
        you must use windowmain_destroyed.
        """

        # dummy return of my class name
        return self.__class__.__name__
