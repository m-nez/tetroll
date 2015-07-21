# -*- coding: utf-8 -*-
#	Copyright 2015 Michał Nieznański
#
#   This file is part of Tetroll.
#
#   Tetroll is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Foobar is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Tetroll.  If not, see <http://www.gnu.org/licenses/>.
import os.path

class ConfigLoader:
    def __init__(self, bo, bo2, f):
        """
        Convert config file to a dictionary of actions
        """
        self.actions = {}
        self.boards = [bo, bo2]
        conf = open(os.path.join("./config", f), "r")
        for lnum, line in enumerate(conf):
            if line[:1] != "#":
                line = line.strip().split(":")
                if len(line) == 2:
                    board = int(line[0])
                    if board != 1 and board != 2:
                        raise ValueError("Invalid board number", board, "on line", lnum, "in file:", f)
                    board -= 1
                    ac = line[1]
                    if ac == "guide_on":
                            self.boards[board].guide_on = True
                    elif ac == "dot_troll":
                            self.boards[board].dot_spawn_troll = True

                    else:
                        raise ValueError("Invalid action", ac, "on line", lnum, "in file: ", f)
                else:
                    if line[0].isalpha():
                        key = ord(line[0])
                    elif line[0].isdigit():
                        key = int(line[0])
                    else:
                        raise ValueError("No key specified on line", lnum, "in file:", f)

                    board = int(line[1])
                    if board != 1 and board != 2:
                        raise ValueError("Invalid board number", board, "on line", lnum, "in file:", f)
                    board -= 1

                    ac = line[2]
                    if ac == "ml":
                        action = self.boards[board].try_move
                        args = [-1]
                    elif ac == "mr":
                        action = self.boards[board].try_move
                        args = [1]
                    elif ac == "rl":
                        action = self.boards[board].try_rotate
                        args = [-1]
                    elif ac == "rr":
                        action = self.boards[board].try_rotate
                        args = [1]
                    elif ac == "at":
                        action = self.boards[board].advance_turn
                        args = []
                    elif ac == "ab":
                        action = self.boards[board].advance_to_bottom
                        args = []
                    else:
                        raise ValueError("Invalid action", ac, "on line", lnum, "in file: ", f)

                    self.actions[key] = (action, args)
    def action(self, key):
        self.actions[key][0](*self.actions[key][1])
