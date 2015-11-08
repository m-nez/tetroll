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

class block:
    def __init__(self):
        self.sqares = []
        self.cur_sqares = [[0,0],[0,0],[0,0],[0,0]]

        self.rotation = 0
        self.colour = 1
        self.identifier = 0
    def I(self):
        self.sqares = [
                [[0, 0], [0, 1], [0, 2], [0, 3]],
                [[0,1], [-1, 1], [1, 1], [2, 1]] 
        ]
        self.init_cur_sqares()
        self.colour = 1
        self.identifier = 0
    def T(self):
        self.sqares = [
                [[-1, 0], [0, 0], [1, 0], [0, 1]],
                [[0, -1], [0, 0], [1, 0], [0, 1]],
                [[-1, 0], [0, 0], [1, 0], [0, -1]],
                [[-1, 0], [0, 0], [0, -1], [0, 1]]
                ]
        self.init_cur_sqares()
        self.colour = 1
        self.identifier = 1
    def O(self):
        self.sqares = [
                [[0,0], [1, 0], [0, 1], [1 , 1]]
                ]
        self.init_cur_sqares()
        self.colour = 1
        self.identifier = 2
    def S(self):
        self.sqares = [
                [[-1, 0], [0, 0], [0, 1], [1, 1]],
                [[-1, 1], [0, 1], [-1, 2], [0, 0]]
                ]
        self.init_cur_sqares()
        self.colour = 1
        self.identifier = 3
    def Z(self):
        self.sqares = [
                [[0, 0], [1, 0], [-1, 1], [0, 1]],
                [[0, 0], [1, 1], [1, 2], [0, 1]]
                ]
        self.init_cur_sqares()
        self.colour = 1
        self.identifier = 4
    def L(self):
        self.sqares = [
                [[0, 0], [1, 0], [0, 1], [0, 2]],
                [[0, 0], [0, 1], [1, 1], [2, 1]],
                [[0, 2], [1, 0], [1, 1], [1, 2]],
                [[0, 0], [1, 0], [1, 1], [-1,0]]
                ]
        self.init_cur_sqares()
        self.colour = 1
        self.identifier = 5
    def J(self):
        self.sqares = [
                [[0, 0], [1, 0], [1, 1], [1, 2]],
                [[0, 0], [0, 1], [2, 0], [1, 0]],
                [[0, 0], [0, 1], [0, 2], [1, 2]],
                [[0, 1], [1, 1], [2, 1], [2, 0]],
                ]
        self.init_cur_sqares()
        self.colour = 1
        self.identifier = 6
    def X(self):
        self.sqares = [
                [[-1, 0], [1, 0], [0, 1], [-1, 2], [1,2]]
                ]
        self.init_cur_sqares()
        self.colour = 2
        self.identifier = 7
    def H(self):
        self.sqares = [
                [[-1, 0], [1, 0], [0, 1], [-1, 2], [1,2], [-1,1], [1,1]]
                ]
        self.init_cur_sqares()
        self.colour = 2
        self.identifier = 8
    def U(self):
        self.sqares = [
                [[0, 0], [-1, 2], [1,2], [-1,1], [1,1]]
                ]
        self.init_cur_sqares()
        self.colour = 2
        self.identifier = 9
    def Tbig(self):
        self.sqares = [
                [[0, 0], [-1, 2], [1,2], [0,1], [0,2]]
                ]
        self.init_cur_sqares()
        self.colour = 2
        self.identifier = 10
    def t(self):
        self.sqares = [
                [[0, 0], [-1, 1], [1,1], [0,1], [0,2]]
                ]
        self.init_cur_sqares()
        self.colour = 2
        self.identifier = 11
    def dot(self):
        self.sqares = [
                [[0, 0]]
                ]
        self.init_cur_sqares()
        self.colour = 1
        self.identifier = 16
    def from_int(self, x):
        if x == 0:
            self.I();
        elif x == 1:
            self.T()
        elif x == 2:
            self.O()
        elif x == 3:
            self.S()
        elif x == 4:
            self.Z()
        elif x == 5:
            self.L()
        elif x == 6:
            self.J()
        elif x == 7:
            self.X()
        elif x == 8:
            self.H()
        elif x == 9:
            self.U()
        elif x == 10:
            self.Tbig()
        elif x == 11:
            self.t()
        elif x == 16:
            self.dot()
    def rotate(self, r_amount):
        self.rotation = (self.rotation + r_amount) % len(self.sqares)
        self.cur_sqares = self.sqares[self.rotation]
    def current_sqares(self):
        return self.sqares[self.rotation]
    def init_cur_sqares(self):
        self.cur_sqares = []
        for i in self.sqares[0]:
            self.cur_sqares.append(i)
        self.rotation = 0
