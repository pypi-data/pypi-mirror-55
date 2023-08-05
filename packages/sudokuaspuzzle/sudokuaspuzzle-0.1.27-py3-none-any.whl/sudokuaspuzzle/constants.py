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
    import re
    # Localization
    import locale
    import gettext

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk
    from gi.repository import GObject
    from gi.repository import GdkPixbuf
    # space for extra Gtk imports

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

#avoiding unsecure eval
RGBA_re = 'Gdk.RGBA\(red=(?P<RED>.*?), green=(?P<GREEN>.*?), blue=(?P<BLUE>.*?), alpha=(?P<ALPHA>.*?)\)'

def eval_rgba(rgba_str):
    """ Securely avaluate a Gdk.RGBA string. """
    amatch = re.match(RGBA_re, rgba_str.strip())
    if amatch:
        return eval(rgba_str.strip())
        # #print(amatch.groupdict())
        # thedict = amatch.groupdict()
        return Gdk.RGBA(red = float(thedict['RED']),
            green=float(thedict['GREEN']),
            blue=float(thedict['BLUE']),
            alpha=float(thedict['ALPHA']))
    return None

def RGBAARRAY2int(an_RGBA_AS_ARRAY):
    return int('%02x%02x%02x%02x' % (
                int(an_RGBA_AS_ARRAY[0]*255),
                int(an_RGBA_AS_ARRAY[1]*255),
                int(an_RGBA_AS_ARRAY[2]*255),
                int(an_RGBA_AS_ARRAY[3]*255)),
                16)
def rgba_int(an_rgba):
    return int('%02x%02x%02x%02x' % (
                int(an_rgba.red*255),
                int(an_rgba.green*255),
                int(an_rgba.blue*255),
                int(an_rgba.alpha*255)),
                16)

CLEAR_AS_NUMBER_PICKED = -7

DEFAULT_RGBA = {}
DEFAULT_RGBA['BG'] = Gdk.RGBA(red=1., green=1., blue=1., alpha=1.0)
DEFAULT_RGBA['FG'] = Gdk.RGBA(red=0., green=0., blue=0., alpha=1.0)
DEFAULT_RGBA['FG_RED'] = Gdk.RGBA(red=1., green=0., blue=0., alpha=1.0)
DEFAULT_RGBA['BG_CONSTANT'] = Gdk.RGBA(red=0.85, green=0.85, blue=0.85, alpha=1.0)
DEFAULT_RGBA['BG_SELECTED'] = Gdk.RGBA(red=0.6, green=0.8, blue=0.9, alpha=1.0)
DEFAULT_RGBA['BG_CONSTANT_SELECTED'] = Gdk.RGBA(red=0.6, green=0.7, blue=0.9, alpha=1.0)
DEFAULT_RGBA['PICKER_BG'] = Gdk.RGBA(red=0., green=1., blue=0., alpha=1.0)
DEFAULT_RGBA['BG_TRANSP'] = Gdk.RGBA(red=1., green=1., blue=1., alpha=0.0)

OPTIONS_BOARD_SIZE = 150

TMPDEFAULTPUZZLE = '83....5....29..6....7..8.39..8....2..4.....569............3...8.83.2..6.7.5...29.'

#Create localized constant strings
#WARNING!!! This must be the same as in the APP main
APPID = "org.kekbay.sudokuaspuzzleocp"
APPNAME = "Sudoku as puzzle"
WHERE_AM_I = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
LOCALE_DIR = os.path.join(WHERE_AM_I, 'localedir')

locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain(APPID, LOCALE_DIR)
gettext.install(APPID, LOCALE_DIR)

CLEAR_ICON = GdkPixbuf.Pixbuf.new_from_file(os.path.abspath(os.path.join(WHERE_AM_I, "icons","edit-clear.png")))
CLEAR_ICON_NO_DROP = GdkPixbuf.Pixbuf.new_from_file(os.path.abspath(os.path.join(WHERE_AM_I, "icons","edit-delete.png")))

#make them available to translators
dummy = _('standard')
dummy = _('arabic')
dummy = _('greek')
dummy = _('chinese')
dummy = _('persian')
dummy = _('tibetan')
dummy = _('custom')

DICTSLIST = ['standard', 'arabic', 'greek', 'chinese',
        'persian', 'tibetan', 'custom']
THEDICTS = {}
THEDICTS['standard'] = [' ','1','2','3','4','5','6','7','8','9']
THEDICTS['arabic'] = [' ','١','٢','٣','٤','٥','٦','٧','٨','٩']
THEDICTS['greek'] = [' ','α','β','γ','δ','ε','ς','ζ','η','θ']
THEDICTS['chinese'] = [' ','一','二','三','四','五','六','七','八','九']
THEDICTS['persian'] = [' ','۱','۲','۳','۴','۵','۶','۷','۸','۹']
THEDICTS['tibetan'] = [ ' ','༡','༢','༣','༤','༥','༦','༧','༨','༩']
THEDICTS['custom'] = THEDICTS['standard'].copy()


ALL_PLACED_TEXT = _("You have placed all «{}».")
PLACE_NUMBER_TEXT = _("Drag «{}» to the board...")
