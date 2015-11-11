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

"""
    Copyright (C) 2015 Michal Nieznanski
"""


import blocks
from sys import stdout
from random import randint
import pygame
from time import time
from copy import deepcopy
from tetai import AI
from networking import Connection

class board:
    def __init__(self):
        self.width = 11
        self.height = 24
        self.visible_height = 21
        self.guide_on = False
        self.dot_spawn_troll = False
        self.reset_matrix()
        self.win_functions = [
            self.win_func1
            ]
        self.loss_functions = [
            self.loss_func1
            ]
        self.win_conditions = [self.win_func1]
        self.loss_conditions = [self.loss_func1]
        self.forfeit = False
        self.send_multi = False
        self.multi_msg = ""

        self.active_block = blocks.block()
        self.pos = [5, 20]
        self.end_count = 0
        self.end_count_pos = [20, 380]
        self.end_count_matrix = [[]]
        self.levels_matrix = []

        self.last_game_step = time()
        self.curr_game_step = 0.0

        self.dot_meter = 0
        self.troll_meter = 0
        self.troll_meter_to_send = 0

        self.bo_pos = [200, 200]
        self.level = 0
        self.game_turn_time = 1.0
        self.end_time_increase = 0.5
        self.red_block_reward = 0.04
        self.turn_time_decrease = 0.83
        self.defill_time_decrease = True
        self.troll_time_decrease = False
        self.troll_time_modifier = 1.0
        self.troll_counter = 0 # Number of troll blocks spawned
        self.troll_time_counter = 0 # Number of time decreases

        self.init_images(1)

        self.scale = 1.0
        self.sp_level = 0

        self.last_landed = [5, 0]
        self.ai = AI(self)
    def send(self, b1, b2):
        """
        If multiplayer is enabled send two bytes to the other player.
        First byte is an unsigned integer, second byte is a signed integer.
        b1 <0, 255>
        b2 <-128, 127>
        If multiplayer is not enabled does nothing.
        """

        if self.send_multi:
            self.connection.send([b1, b2 + 128])
    def send_state(self):
        """
        Send elements necessary to recreate the board state.
        Pcket should be 512 bytes.
        """
        msg = []
        msg.append(self.level)
        msg.append(self.width) # Height doesn't change
        msg.append(self.active_block.identifier)
        msg.append(self.active_block.rotation)
        msg.append(self.active_block.colour)
        msg.append(self.pos[0])
        msg.append(self.pos[1])
        msg.append(self.forfeit)
        
        for l in self.matrix:
            msg.extend(l)
        msg.extend([0]*(512-len(msg)))

        self.connection.send(msg)
    def recreate_state(self, msg):
        """
        Recreate state from bytearry.
        """
        
        if (len(msg) - 8) % self.height != 0:
            print(msg)
        self.level = ord(msg[0]) # Python2 so msg is a string
        prev_width = self.width
        self.width = ord(msg[1])

        self.active_block.from_int(ord(msg[2]))
        self.active_block.rotation = ord(msg[3])
        self.active_block.colour = ord(msg[4])
        self.pos[0] = ord(msg[5])
        self.pos[1] = ord(msg[6])
        self.forfeit = ord(msg[7])
        
        mat = []
        for i in range(self.height):
            mat.append([ord(j) for j in msg[8 + i * self.width : 8 + (i+1) * self.width]])
        self.matrix = mat

    def try_recreate_state(self):
        """
        Receive 512 bytes encoding the board state
        """
        msg = self.connection.receive()
        if msg != 0:
            self.multi_msg += msg
            if len(msg) >= 512:
                index = (len(msg) // 512 - 1) * 512
                self.recreate_state(self.multi_msg[index:index+512])
                self.multi_msg = self.multi_msg[index+512:]
    def print_matrix(self):
        print(10*"*")
        self.add_block(self.pos, self.active_block.current_sqares())
        for i in reversed(range(self.visible_height)):
            for j in range(self.width):
                stdout.write(str(self.matrix[i][j]))
            print()
        self.erase_block(self.pos, self.active_block.current_sqares())
    def reset_matrix(self):
        self.matrix = []

        for i in range(self.height):
            self.matrix.append([])
            for j in range(self.width):
                self.matrix[i].append(0)

    def add_block(self, pos, sqares):
        for sq in sqares:
            self.matrix[pos[1]+sq[1]][pos[0]+sq[0]] = self.active_block.colour
    def check_block(self, pos, sqares):
        for sq in sqares:
            if (pos[0] + sq[0]) < 0 or (pos[0] + sq[0]) > self.width - 1:
                return 1
            if (pos[1] + sq[1]) < 0 or (pos[1] + sq[1]) > self.height - 1:
                return 1
            if self.matrix[pos[1]+sq[1]][pos[0]+sq[0]] >= 1:
                return 1
        return 0
    def erase_block(self, pos, sqares):
        for sq in sqares:
            self.matrix[pos[1]+sq[1]][pos[0]+sq[0]] = 0
    def spawn_block(self, seed=-1):
        self.pos = [5, 19]

        if seed != -1:
            self.active_block.from_int(seed)
        else:
            if self.dot_meter > 0:
                self.active_block.from_int(16)
                self.dot_meter -= 1
            elif self.troll_meter > 0:
                self.spawn_troll_block()
                self.troll_meter -= 1
            else:
                self.active_block.from_int(randint(0, 6))
        if self.check_block(self.pos, self.active_block.current_sqares()):
            self.end()
    def spawn_troll_block(self):
        self.troll_counter += 1
        if self.dot_spawn_troll:
            self.active_block.from_int(16)
        else:
            self.active_block.from_int(randint(7, 11))

    def advance_turn(self):
        if self.check_block([self.pos[0], self.pos[1] - 1], self.active_block.current_sqares()):
            self.last_landed = list(self.pos)
            self.add_block(self.pos, self.active_block.current_sqares())
            self.defill()
            self.spawn_block()
            self.last_game_step = time()
            return 1
        else:
            self.pos[1] -= 1
            return 0
    def dry_advance(self):
        if self.check_block([self.pos[0], self.pos[1] - 1], self.active_block.current_sqares()):
            self.add_block(self.pos, self.active_block.current_sqares())
            levels_cleared = self.dry_defill()
            self.erase_block(self.pos, self.active_block.current_sqares())
            return [True, levels_cleared]
        else:
            self.pos[1] -= 1
            return [False, 0]
    def dry_defill(self):
        counter = 0
        for i in range(self.height):
            counter += self.matrix[i].count(0) == 0
        return counter

    def try_move(self, x):
        if not self.check_block([self.pos[0] + x, self.pos[1]], self.active_block.current_sqares()):
            self.pos[0] += x
            return 1
        return 0
    def try_rotate(self, x):
        self.active_block.rotate(x)
        if self.check_block(self.pos, self.active_block.current_sqares()):
            self.active_block.rotate(-x)
            return 0
        return 1
    def defill(self):
        for i in reversed(range(self.height)):
            if self.matrix[i].count(0) == 0:
                if self.matrix[i].count(2) != 0:
                    self.dot_meter += 1
                    self.game_turn_time += self.red_block_reward
                self.bring_down(i)
                self.level += 1
                self.levels_matrix.append([1])
                if self.defill_time_decrease:
                    self.game_turn_time *= self.turn_time_decrease
                self.troll_meter_to_send += 1
                if self.troll_time_decrease:
                    self.troll_time_modifier *= self.turn_time_decrease
    def bring_down(self, line):
        for i in range(line + 1, self.height):
            self.matrix[i-1] = deepcopy(self.matrix[i])
    def advance_to_bottom(self):
        while not self.advance_turn():
            pass
    def draw(self, screen):
        self.add_block(self.pos, self.active_block.current_sqares())
        for i in range(self.visible_height):
            for j in range(self.width):
                b_pos = (
                    self.bo_pos[0] + self.block_image.get_width() * j,
                    self.bo_pos[1] + self.block_image.get_height() * (self.visible_height - i))
                if self.matrix[i][j] == 1:
                    if i < self.level:
                        screen.blit(self.green_block_image, b_pos)
                    else:
                        screen.blit(self.block_image, b_pos)
                elif self.matrix[i][j] == 2:
                    screen.blit(self.red_block_image, b_pos)
                elif self.matrix[i][j] == 0:
                    screen.blit(self.gray_grid_image, b_pos)
        self.erase_block(self.pos, self.active_block.current_sqares())
        #draw_border
        self.draw_border(screen)
        self.draw_end_count(screen)
        if self.guide_on:
            self.draw_guidelines(screen)

    def draw_border(self, screen):
        for i in range(-1, self.width + 1):
            b_pos = (self.bo_pos[0] + self.block_image.get_width()*i,self.bo_pos[1] + self.block_image.get_height()*(0))
            screen.blit(self.brown_block_image, b_pos)
            b_pos = (self.bo_pos[0] + self.block_image.get_width()*i,self.bo_pos[1] + self.block_image.get_height()*(self.visible_height+1))
            screen.blit(self.brown_block_image, b_pos)
        for i in range(self.visible_height+1):
            b_pos = (self.bo_pos[0] + self.block_image.get_width()*(-1),self.bo_pos[1] + self.block_image.get_height()*(i))
            screen.blit(self.brown_block_image, b_pos)
            b_pos = (self.bo_pos[0] + self.block_image.get_width()*(self.width),self.bo_pos[1] + self.block_image.get_height()*(i))
            screen.blit(self.brown_block_image, b_pos)
    def draw_matrix(self, screen, matrix, pos, image):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    b_pos = (pos[0]+image.get_width()*j,pos[1]+image.get_height()*i)
                    screen.blit(image, b_pos)
    def draw_end_count(self, screen):
        pos = [0,0]
        pos[0] = self.bo_pos[0] + self.end_count_pos[0]
        pos[1] = self.bo_pos[1] + self.end_count_pos[1]
        self.draw_matrix(screen, self.end_count_matrix, pos, self.green_block_image)
    def draw_guidelines(self, screen):
            guide_pos = deepcopy(self.pos)
            while not self.check_block(guide_pos, self.active_block.current_sqares()):
                guide_pos[1] -= 1
            guide_pos[1] += 1
            for sq in self.active_block.current_sqares():
                b_pos = (self.bo_pos[0] +self.blue_guidelines_image.get_width()*(guide_pos[0]+sq[0]),self.bo_pos[1] + self.blue_guidelines_image.get_height()*(self.visible_height - (guide_pos[1]+sq[1])))
                screen.blit(self.blue_guidelines_image, b_pos)

    def end(self):
        if self.matrix[self.visible_height-1].count(0) != self.width:
            self.end_count += 1
            self.end_count_matrix[0].append(1)
            self.width += 1
            self.reset_matrix()
            self.game_turn_time += self.end_time_increase
            self.spawn_block()
            return True
        else:
            return False
    def time_advance(self):
        self.curr_game_step = time()
        if self.curr_game_step - self.last_game_step >= self.game_turn_time:
            self.last_game_step = self.curr_game_step
            self.advance_turn()
            return True
        else:
            return False
    def change_enemy_board(self, enemy_board):
        self.send_troll(enemy_board)
    def send_troll(self, enemy_board):
        enemy_board.troll_meter = self.level - enemy_board.troll_counter
        if enemy_board.troll_time_decrease:
            power = max(0, self.level - enemy_board.troll_time_counter)
            enemy_board.game_turn_time *= self.turn_time_decrease**power
            enemy_board.troll_time_counter += power
    def init_images(self, scale):
        pos = int(16 * scale)
        pos = (pos, pos)
        self.block_image = pygame.transform.scale(pygame.image.load("images/block.png"), pos)
        self.red_block_image = pygame.transform.scale(pygame.image.load("images/red_block.png"), pos)
        self.green_block_image = pygame.transform.scale(pygame.image.load("images/green_block.png"), pos)
        self.yellow_block_image = pygame.transform.scale(pygame.image.load("images/yellow_block.png"), pos)
        self.brown_block_image = pygame.transform.scale(pygame.image.load("images/brown_block.png"), pos)
        self.blue_block_image = pygame.transform.scale(pygame.image.load("images/blue_block.png"), pos)
        self.purple_block_image = pygame.transform.scale(pygame.image.load("images/purple_block.png"), pos)
        self.blue_guidelines_image = pygame.transform.scale(pygame.image.load("images/blue_guidelines.png"), pos)
        self.gray_grid_image = pygame.transform.scale(pygame.image.load("images/gray_grid.png"), pos)


        self.scale = scale
    def draw_win(self, screen):
        win_mat = [
                [1,0,0,0,1,0,1,0,1,1,0,1,0,0],
                [1,0,1,0,1,0,1,0,1,0,1,1,0,0],
                [0,1,0,1,0,0,1,0,1,0,0,1,0,0],
                ]
        pos = [self.bo_pos[0], self.bo_pos[1] + 16*(self.visible_height/2)*self.scale]
        self.draw_matrix(screen, win_mat, pos, self.blue_block_image)
    def draw_level(self, screen):
        counter = str(self.level)
        numbers = [
                [
                [0,1,1,0],
                [1,0,0,1],
                [1,0,0,1],
                [1,0,0,1],
                [0,1,1,0],
                ],
                [
                [0,0,1,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,0],
                [0,0,1,0],
                ],

                [
                [0,1,1,0],
                [1,0,0,1],
                [0,0,1,0],
                [0,1,0,0],
                [1,1,1,1],
                ],

                [
                [1,1,1,0],
                [0,0,0,1],
                [1,1,1,0],
                [0,0,0,1],
                [1,1,1,0],
                ],

                [
                [1,0,1,0],
                [1,0,1,0],
                [1,1,1,1],
                [0,0,1,0],
                [0,0,1,0],
                ],

                [
                [1,1,1,1],
                [1,0,0,0],
                [1,1,1,0],
                [0,0,0,1],
                [1,1,1,0],
                ],
                [
                [0,0,1,0],
                [0,1,0,0],
                [1,1,1,0],
                [1,0,0,1],
                [0,1,1,0],
                ],
                [
                [1,1,1,1],
                [0,0,0,1],
                [0,0,1,0],
                [0,1,0,0],
                [1,0,0,0],
                ],
                [
                [0,1,1,0],
                [1,0,0,1],
                [0,1,1,0],
                [1,0,0,1],
                [0,1,1,0],
                ],
                [
                [0,1,1,0],
                [1,0,0,1],
                [1,1,1,1],
                [0,0,0,1],
                [1,1,1,0],
                ],
                ]
        mat = [[0],[0],[0],[0],[0]]
        for i in counter:
            i = int(i)
            for n, j in enumerate(numbers[i]):
                mat[n] += j + [0]


        pos = [self.bo_pos[0], self.bo_pos[1] + 16*(self.visible_height/2)*self.scale]
        self.draw_matrix(screen, mat, pos, self.blue_block_image)
    def sp_level_win(self):
        if self.level >= 10:
            self.width += 1
            self.reset_matrix()
            self.game_turn_time += self.end_time_increase
            self.sp_level += 1
            self.level = 0
            return True
        else:
            return False
    def sp_win(self):
        if self.sp_level == 5:
            return True
        else:
            return False
    def AI_move(self):
        choice = self.ai.move()
    def win_func1(self):
        return self.level >= self.visible_height
    def loss_func1(self):
        return self.end_count >= 3
    def outcome(self):
        for win_con in self.win_conditions:
            if win_con():
                return 1
        for loss_con in self.loss_conditions:
            if loss_con():
                return 2
        if self.forfeit:
            return 2
        return 0
    def set_win_cons(self, func_str):
        self.win_conditions = []
        for i, val in enumerate(func_str):
            if val != "0":
                self.win_conditions.append(self.win_functions[i])
    def set_loss_cons(self, func_str):
        self.loss_conditions = []
        for i, val in enumerate(func_str):
            if val != "0":
                self.loss_conditions.append(self.loss_functions[i])
    def set_game_cons(self, win_cons, loss_cons):
        self.set_win_cons(win_cons)
        self.set_loss_cons(loss_cons)
    def set_forfeit(self, value):
        self.forfeit = value
    def set_level(self, level):
        self.level = level
    def add_troll(self, value):
        self.troll_meter_to_send += value
    def add_wait_connection(self, ip):
        self.connection = Connection(self, ip, send=False)
    def add_send_connection(self, ip):
        self.connection = Connection(self, ip, send=True)
