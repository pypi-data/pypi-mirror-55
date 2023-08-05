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
__version__ = '0.1.21'
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

    # Configuration and message boxes
    from auxiliary import *
    from constants import *

    # Load base window class and static methods
    from windowmain_base import WindowMainBase
    from windowmain_statics import *

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

class WindowMainClass(WindowMainBase):
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

        super().__init__(self,  *args, **kwargs)

        #place here initilisations after loading the ui
        self.show_defaults()
