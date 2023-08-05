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

import os
import sys

WHERE_AM_I = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
#mypackagefolder = os.path.abspath(os.path.join(WHERE_AM_I,".."))
sys.path.insert(0, WHERE_AM_I)

#FIXME: change package name
from myapplication import MyApplication

def main(*args, **kwargs):
    START_DIR = os.path.dirname(os.path.abspath('.'))
    myapp = MyApplication(START_DIR=START_DIR)
    myapp.run(**kwargs)

if __name__ == '__main__':
    """ Main entry for the entire application. """
    main(sys.argv)
