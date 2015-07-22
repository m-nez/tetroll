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
import pygame

class Window:
    def __init__(self, fullsc = False, size = [600, 600]):
        pygame.init()
        self.size = size
        self.title = "Tetroll"
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(self.size)
        self.logo = [
            [1,1,1,0,1,1,0,1,1,1,0,1,1,0,0,0,1,0,0,1,0,0,0,1,0,0],
            [0,1,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0],
            [0,1,0,0,1,1,0,0,1,0,0,1,1,0,0,1,0,1,0,1,0,0,0,1,0,0],
            [0,1,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0],
            [0,1,0,0,1,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,1],
                ]
        if fullsc:
            pygame.display.toggle_fullscreen()
    def resize(self, size):
        self.size[0], self.size[1] = size[0], size[1]
        self.screen = pygame.display.set_mode(self.size)
    def draw_matrix(self, matrix, pos, image):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    b_pos = (pos[0]+image.get_width()*j,pos[1]+image.get_height()*i)
                    self.screen.blit(image, b_pos)
