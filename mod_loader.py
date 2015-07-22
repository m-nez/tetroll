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
#   Tetroll is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Tetroll.  If not, see <http://www.gnu.org/licenses/>.
import os.path

class ModLoader:
    def __init__(self, bo, bo2, f):
        """
        Convert config file to a dictionary of actions
        """
        self.actions = {}
        self.boards = [bo, bo2]
        conf = open(os.path.join("./mods", f), "r")
        for lnum, line in enumerate(conf):
            if line[:1] != "#":
                line = line.strip().split(":")
                if len(line) == 2:
                    setting = line[0]
                    value = line[1]
                    if setting == "game_turn_time":
                        value = float(value)
                        for bo in self.boards:
                            bo.game_turn_time = value
                    elif setting == "end_time_increase":
                        value = float(value)
                        for bo in self.boards:
                            bo.end_time_increase = value
                    elif setting == "red_block_reward":
                        value = float(value)
                        for bo in self.boards:
                            bo.red_block_reward = value
                    elif setting == "turn_time_decrease":
                        value = float(value)
                        for bo in self.boards:
                            bo.turn_time_decrease = value
                    elif setting == "defill_time_decrease":
                        value = bool(int(value))
                        for bo in self.boards:
                            bo.defill_time_decrease = value
                    elif setting == "troll_time_decrease":
                        value = bool(int(value))
                        for bo in self.boards:
                            bo.troll_time_decrease = value
                    elif setting == "win_functions":
                        for bo in self.boards:
                            bo.set_win_cons(value)
                    elif setting == "loss_functions":
                        for bo in self.boards:
                            bo.set_loss_cons(value)
                    else:
                        raise ValueError("Invalid setting", setting, "on line", lnum, "in file: ", f)
