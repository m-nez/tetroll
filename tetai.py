#!/usr/bin/python2
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

import board
from copy import deepcopy
from random import randint


class AI:
    """
    2 Turn AI
    """
    def __init__(self, bo):
        self.sim_depth = 2
        self.turns_per_advance = 1
        self.advance_in = self.turns_per_advance
        self.bo = bo

        self.min_points = 0
        self.move_choice = []
        self.update()
        self.op2func = [
            self.mvp0rp0,
            self.mvm1rm1,
            self.mvm2rm2,
            self.mvp2rp2,
            self.mvp1rp1,
            self.mvm1rp1,
            self.mvp1rm1,
            self.mvm2rm1,
            self.mvp2rp1,
            self.mvm1rm2,
            self.mvp1rp2,
            self.mvm2rm0,
            self.mvp2rp0,
            self.mvm0rm2,
            self.mvp0rp2,
            self.mvm1rm0,
            self.mvp1rp0,
            self.mvm0rm1,
            self.mvp0rp1
                    ]

    #2 turn optimization
    def mvm1rm1(self):
        self.bo.try_move(-1)
        self.bo.try_rotate(-1)
    def mvm2rm2(self):
        self.bo.try_move(-1)
        self.bo.try_move(-1)
        self.bo.try_rotate(-1)
        self.bo.try_rotate(-1)
    def mvp2rp2(self):
        self.bo.try_move(1)
        self.bo.try_move(1)
        self.bo.try_rotate(1)
        self.bo.try_rotate(1)
    def mvp1rp1(self):
        self.bo.try_move(1)
        self.bo.try_rotate(1)
    def mvm1rp1(self):
        self.bo.try_move(-1)
        self.bo.try_rotate(1)
    def mvp1rm1(self):
        self.bo.try_move(1)
        self.bo.try_rotate(-1)
    def mvm2rm1(self):
        self.bo.try_move(-1)
        self.bo.try_move(-1)
        self.bo.try_rotate(-1)
    def mvp2rp1(self):
        self.bo.try_move(1)
        self.bo.try_move(1)
        self.bo.try_rotate(1)
    def mvm1rm2(self):
        self.bo.try_move(-1)
        self.bo.try_rotate(-1)
        self.bo.try_rotate(-1)
    def mvp1rp2(self):
        self.bo.try_move(1)
        self.bo.try_rotate(1)
        self.bo.try_rotate(1)
    def mvm2rm0(self):
        self.bo.try_move(-1)
        self.bo.try_move(-1)
    def mvp2rp0(self):
        self.bo.try_move(1)
        self.bo.try_move(1)
    def mvm0rm2(self):
        self.bo.try_rotate(-1)
        self.bo.try_rotate(-1)
    def mvp0rp2(self):
        self.bo.try_rotate(1)
        self.bo.try_rotate(1)
    def mvm1rm0(self):
        self.bo.try_move(-1)
    def mvp1rp0(self):
        self.bo.try_move(1)
    def mvm0rm1(self):
        self.bo.try_rotate(-1)
    def mvp0rp1(self):
        self.bo.try_rotate(1)
    def mvp0rp0(self):
        pass

    def set_sim_depth(self,d):
        self.sim_depth = d
    def set_turns_per_advance(self, t):
        self.turns_per_advance = t
    def update(self):
        self.block = deepcopy(self.bo.active_block)
        pass
    def move(self):
        block_backup = deepcopy(self.bo.active_block)
        pos_backup = deepcopy(self.bo.pos)
        block = deepcopy(self.bo.active_block)
        self.bo.active_block = block
        #mv = self.simulate2turn(1, self.advance_in)
        mv = self.simulate2turn_check_space(1, self.advance_in)
        self.bo.active_block = block_backup
        self.bo.pos = pos_backup

        self.op2func[mv]()

        self.advance_in -= 1
        if self.advance_in == 0:
            self.bo.advance_turn()
            self.advance_in = self.turns_per_advance

    def simulate2(self, depth, adv_in):
        rotation = self.bo.active_block.rotation
        pos = deepcopy(self.bo.pos)
        c_sq = deepcopy(self.bo.active_block.cur_sqares)
        pre_adv_in = adv_in
        turn_vals = []

        for func in [self.bo.try_move, self.bo.try_rotate]:
            for val in [-1, 0, 1]:
                self.bo.active_block.rotation = rotation
                self.bo.pos = deepcopy(pos)
                self.bo.active_block.cur_sqares = deepcopy(c_sq)
                func(val)
                landed = False
                adv_in = pre_adv_in
                levels_cleared = 0
                adv_in -= 1
                if adv_in == 0:
                    adv_in = self.turns_per_advance
                    landed, levels_cleared = self.bo.dry_advance()
                if landed:
                    points = self.evaluate(self.bo.pos, self.bo.active_block.cur_sqares, levels_cleared)
                    turn_vals.append(points)
                elif depth == self.sim_depth:
                    points = self.evaluate(self.bo.pos, self.bo.active_block.cur_sqares, levels_cleared)
                    turn_vals.append(points)
                else:
                    turn_vals.append(self.simulate2(depth + 1, adv_in))
        if depth == 1:
            return turn_vals.index(min(turn_vals))
        else:
            return min(turn_vals)


    def simulate2turn(self, depth, adv_in):
        rotation = self.bo.active_block.rotation
        pos = deepcopy(self.bo.pos)
        c_sq = deepcopy(self.bo.active_block.cur_sqares)
        pre_adv_in = adv_in
        turn_vals = []

        for func in self.op2func:
            self.bo.active_block.rotation = rotation
            self.bo.pos = deepcopy(pos)
            self.bo.active_block.cur_sqares = deepcopy(c_sq)
            func()
            landed = False
            adv_in = pre_adv_in
            levels_cleared = 0
            adv_in -= 1
            if adv_in == 0:
                adv_in = self.turns_per_advance
                landed, levels_cleared = self.bo.dry_advance()
            if landed:
                points = self.evaluate(self.bo.pos, self.bo.active_block.cur_sqares, levels_cleared)
                turn_vals.append(points)
            elif depth == self.sim_depth:
                points = self.evaluate(self.bo.pos, self.bo.active_block.cur_sqares, levels_cleared)
                turn_vals.append(points)
            else:
                turn_vals.append(self.simulate2turn(depth + 1, adv_in))
        if depth == 1:
            m = min(turn_vals)
            return turn_vals.index(m)
        else:
            return min(turn_vals)


    def simulate2turn_check_space(self, depth, adv_in):
        rotation = self.bo.active_block.rotation
        pos = deepcopy(self.bo.pos)
        c_sq = deepcopy(self.bo.active_block.cur_sqares)
        pre_adv_in = adv_in
        turn_vals = []

        for func in self.op2func:
            self.bo.active_block.rotation = rotation
            self.bo.pos = deepcopy(pos)
            self.bo.active_block.cur_sqares = deepcopy(c_sq)
            func()
            landed = False
            adv_in = pre_adv_in
            levels_cleared = 0
            adv_in -= 1
            if adv_in == 0:
                adv_in = self.turns_per_advance
                landed, levels_cleared = self.bo.dry_advance()
            if landed or depth == self.sim_depth:
                self.bo.add_block(self.bo.pos, self.bo.active_block.cur_sqares)
                points = self.evaluate_check_space(self.bo.pos, self.bo.active_block.cur_sqares, levels_cleared, self.bo.matrix)
                self.bo.erase_block(self.bo.pos, self.bo.active_block.cur_sqares)
                turn_vals.append(points)
            else:
                turn_vals.append(self.simulate2turn_check_space(depth + 1, adv_in))
        if depth == 1:
            m = min(turn_vals)
            return turn_vals.index(m)
        else:
            return min(turn_vals)

    def evaluate(self, pos, sqares, levels):
        points = 4 * pos[1]
        for sq in sqares:
            points += sq[1]
        points -= 20 * levels
        return points

    def evaluate_check_space(self, pos, sqares, levels, mat):
        #Space to check
        space_to_check = [
                [0, -1], [-1, 0]
                ]

        height = self.bo.height
        width = self.bo.width

        self.bo.add_block(pos, sqares)

        pos1 = pos[1]
        pos0 = pos[0]

        points = 32 * (pos1+2)
        points -= pos0
        for sq in sqares:
            sq1 = sq[1]
            sq0 = sq[0]
            for sp in space_to_check:
                space_sq = [sq0 + sp[0] + pos0, sq1 + sp[1] + pos1]
                if (width > space_sq[0] >= 0) and (height > space_sq[1] >= 0):
                    if mat[space_sq[1]][space_sq[0]] == 0:
                        points += 6 + 2*sq1
        points -= 45 * levels
        self.bo.erase_block(pos, sqares)

        return points
