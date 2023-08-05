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

from copy import deepcopy

ROWS = []
COLS = []
SQUARES = []
for xcounter in range(3):
    col = xcounter * 3
    colindex = col * 9
    rowindex = col
    for ycounter in range(3):
        ROWS.append( [1+ colindex + (ycounter*9) + x for x in range(9)])
        COLS.append( [1+ rowindex + ycounter + 9 * x for x in range(9)])
        row = ycounter * 3
        square = col * 9 + row
        SQUARES.append( [square+1, square+2, square+3,
                10+square, 11+square, 12+square,
                19+square, 20+square, 21+square])

class APuzzle():
    def __init__(self,  puzzle_string=None,
                #thelist=None, history_as_string=None,
                #history_position=None,
                trigger_refresh=None,
                difficulty=None,
                last_game = None):
        self.solved = False

        self.numbers_shown = {}
        self.all_pieces = {}
        if trigger_refresh:
            self.trigger_refresh = trigger_refresh
        else:
            raise "Cannot continue." + \
            " No method for trigger_refresh provided."
            sys.exit(-1)
        for acounter in range(9):
            self.all_pieces[acounter+1] = 9
        self.all_pieces[0] = 81
        self.remaining = {}
        self.history = []
        self.history_position = 0
        self.solution = []
        self.difficulty = difficulty
        if last_game:
            self.puzzle_string = last_game['puzzle_string']
            self.history_position = last_game['history_position']
            self.history_string = last_game['history_string']
            # create last history
            self.poke_history(last_game['history_string'])
            self.difficulty = last_game['difficulty']

        else:
            self.puzzle_string = puzzle_string
            self.start_cells = self.init_cells()
            #keep a separate list for running game
            self.current_cells = deepcopy(self.start_cells)
        self.set_remaining()

    def dummy_method(self, *args):
        pass

    def init_cells(self):
        dummy = []
        for acounter in range(81):
            s = self.puzzle_string[acounter]
            is_constant = True if s != "." else False
            theint = int(s) if s != "." else 0
            dummy.append ([is_constant, theint, False])
        dummy.insert(0, 1)
        return dummy

    def poke_history(self, history_as_string):
        self.start_cells = self.init_cells()
        #keep a separate list for running game
        self.current_cells = deepcopy(self.start_cells)
        for amovestring in self.history_string.strip().split(","):
            themove = amovestring.split(":")
            new_cell = int(themove[0])
            previous_value = int(themove[1])
            new_value = int(themove[2])
            seconds_passed = int(themove[3])
            self.history.append([new_cell,
                    previous_value,
                    new_value,
                    seconds_passed])

        #play up to history position
        for acounter in range(self.history_position):
            amove = self.history[acounter]
            the_cell = amove[0]
            the_int = amove[2]
            self.current_cells[the_cell][1] = the_int

    def undo(self):
        _last = self.history[self.history_position-1]
        thecell = _last[0]
        theint = _last[1]
        self.current_cells[thecell][1] = theint
        self.current_cells[0] = thecell
        self.history_position -= 1
        self.check_puzzle()

    def redo(self):
        _next = self.history[self.history_position]
        thecell = _next[0]
        theint = _next[2]
        self.current_cells[thecell][1] = theint
        self.current_cells[0] = thecell
        self.history_position += 1
        self.check_puzzle()

    def set_cell(self, thecell, theint, secondspassed):
        """ Insert a number in a cell and append action to history. """
        previous = self.current_cells[thecell][1]
        self.current_cells[thecell][1] = theint
        if self.history_position < len(self.history):
            #remove rest of history
            self.history = self.history[:self.history_position]
        self.history.append([thecell, previous, theint, secondspassed])
        self.history_position = len(self.history)
        self.check_puzzle()

    def check_puzzle(self):
        """ Check if there are duplicates and if puzzle is solved. """

        self.set_remaining()
        self.dups = []
        for alist in ROWS:
            self.enlist_duplicates(alist)
        for alist in COLS:
            self.enlist_duplicates(alist)
        for alist in SQUARES:
            self.enlist_duplicates(alist)
        all_filled = True
        for acounter in range(81):
            #set "duplicate-ness" of any duplicate cell
            self.current_cells[acounter+1][2] = (acounter+1 in self.dups)
        #self.set_remaining()
        self.solved = ((self.remaining[0] == 0) and (len(self.dups) == 0 ))
        self.trigger_refresh()

    def enlist_duplicates(self, thelist):
        """ Create a list of cell numbers that are duplicate in a 9 array. """
        cell_nums = [self.current_cells[x][1] for x in thelist]
        for acounter in range(8):
            if cell_nums[acounter] and cell_nums[acounter] in cell_nums[acounter+1:]:
                adup1pos = acounter
                adup2pos = acounter + 1 + cell_nums[acounter+1:].index(cell_nums[acounter])
                adup1cell = thelist[adup1pos]
                adup2cell = thelist[adup2pos]
                if adup1cell not in self.dups:
                    self.dups.append(adup1cell)
                if adup2cell not in self.dups:
                    self.dups.append(adup2cell)

    def set_remaining(self):
        """ Fill the list of numbers not already poked in puzzle board. """
        self.remaining = self.all_pieces.copy()
        for acounter in range(1, 82):
            theint = self.current_cells[acounter][1]
            if theint:
                self.remaining[theint] -= 1
                self.remaining[0] -= 1


