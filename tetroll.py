#!/usr/bin/env python
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

import blocks
import board
from random import randint
from time import time, sleep
import window
import pygame

from sys import argv
from config_loader import ConfigLoader
from mod_loader import ModLoader
from strmat import str_to_matrix

pygame.init()

#Handle Command line arguments
fullsc = False
if len(argv) > 2:
    fullsc = int(argv[2])

size = [600, 600]
if len(argv) > 4:
    size = [int(argv[3]), int(argv[4])]

#Load config
configfile = "config0.conf"
if len(argv) > 5:
    configfile = argv[5]

modfile = "20levels.mods"
if len(argv) > 6:
    modfile = argv[6]

ai = "0"
if len(argv) > 7:
    ai = argv[7]

ai_delay = 1
if len(argv) > 8:
    ai_delay = int(argv[8])

opponent_ip = None
if len(argv) > 9:
    opponent_ip = argv[9]

if size[0] == 0 or size[1] == 0:
    size = pygame.display.list_modes()[0]

win = window.Window(fullsc, size)

scale = float(min(win.size))/(16*34)#max size in any dimension

bo = board.board()
bo.spawn_block()
#bo.bo_pos=[16*scale, 16*scale] #Legacy position
bo.bo_pos=[3*16*scale, 8*16*scale] #New position
bo.end_count_pos = [16*scale, (bo.visible_height+3)*16*scale]
bo.init_images(scale)

bo2 = board.board()
bo2.spawn_block()
#bo2.bo_pos=[16*17*scale, 16*scale] #Legacy position
bo2.bo_pos=[20*16*scale, 8*16*scale] #New position
bo2.end_count_pos = [16*scale, (bo2.visible_height+3)*16*scale]
bo2.init_images(scale)

#Configure keybindings
if ai == "1":
    cfg = ConfigLoader(bo, bo, configfile)
elif ai == "2":
    cfg = ConfigLoader(bo, bo2, configfile)
    cfg.actions = {}
elif ai == "3" or ai == "4":
    cfg = ConfigLoader(bo, bo, configfile)
    if opponent_ip == None:
        print("Opponent ip not specified")
        exit(1)
    if ai == "3":
        bo2.add_send_connection(opponent_ip)
    else:
        bo.draw_matrix(win.screen, str_to_matrix("please\nwait\nfor the\nsecond\nplayer"),
                [1*16*scale, 1*16*scale], bo.purple_block_image)
        pygame.display.flip()
        bo2.add_wait_connection(opponent_ip)
    bo.connection = bo2.connection
    bo.send_multi = True
else:
    cfg = ConfigLoader(bo, bo2, configfile)


#Load mod settings
mods = ModLoader(bo, bo2, modfile)

dt = 1.0/30.0
last_draw = time()
curr_draw = 0.0
game_step = 1.0
last_game_step = time()
curr_game_step = 0.0

winner = 0

done = False
time_advanced_lately = False

#Joystick support
#Too complicated to put in the config
joystick_support = pygame.joystick.get_count() > 0
joystick = 0
last_x_axis_val = 0.0
last_y_axis_val = 0.0
joy_min_val = 0.0
joy_max_val = 0.0
joy_y_min_val = 0.0
movement_buffer = 0.2
y_movement_buffer = 0.16
joy_bo = bo
if len(argv) > 1:
    if argv[1] == '1':
        joy_bo = bo
    elif argv[1] == '2':
        joy_bo = bo2
    else:
        joystick_support = False
else:
    joystick_support = False
if joystick_support:
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


while(not done):
    #handle input for dt
    #check if game_step
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bo.set_forfeit(True)
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                bo.set_forfeit(True)
                done = True
            #Use config
            elif event.key in cfg.actions:
                cfg.action(event.key)
        elif joystick_support:
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value > last_x_axis_val:
                        if event.value > 0.9:
                            if event.value - joy_min_val > movement_buffer:
                                joy_bo.try_move(1)
                                joy_min_val = event.value
                        joy_max_val = max(event.value, joy_max_val)

                    elif event.value < last_x_axis_val:
                        if event.value < -0.9:
                            if event.value - joy_max_val < -movement_buffer: 
                                joy_bo.try_move(-1)
                                joy_max_val = event.value
                        joy_min_val = min(event.value, joy_min_val)
                            
                            
                    last_x_axis_val = event.value
                elif event.axis == 1:
                    if event.value > last_y_axis_val:
                        if event.value > 0.75:
                            if event.value - joy_y_min_val > y_movement_buffer:
                                joy_bo.advance_turn()
                                joy_y_min_val = event.value
                    else:
                        joy_y_min_val = min(event.value, joy_y_min_val)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 4:
                    joy_bo.try_rotate(1)
                elif event.button == 3:
                    joy_bo.try_rotate(-1)
                elif event.button == 0:
                    joy_bo.advance_to_bottom()

    if ai == "1":
        if time_advanced_lately >= ai_delay:
            time_advanced_lately = 0
            bo2.ai.move()
            bo.time_advance()
            time_advanced_lately = False
    elif ai == "2":
        if time_advanced_lately:
            bo.ai.move()
            bo2.ai.move()
            time_advanced_lately = False
    elif ai == "3" or ai == "4":
        # Networked player
        bo.time_advance()
        bo2.try_recreate_state()
    else:
        bo.time_advance()
        bo2.time_advance()

    bo.change_enemy_board(bo2)
    bo2.change_enemy_board(bo)

    bo.end()
    bo2.end()

    outcome1 = bo.outcome()
    outcome2 = bo2.outcome()
    if outcome1 or outcome2:
        done = True


    #Send state after all the calculation
    if ai == "3" or ai == "4":
        bo.send_state()

    curr_draw = time()
    draw_time_diff = curr_draw - last_draw
    if draw_time_diff >= dt:
        time_advanced_lately += 1
        last_draw = curr_draw
        win.screen.fill((0,0,0))
        #Draw logo
        bo.draw_matrix(win.screen, win.logo,
                [4*16*scale, 16*scale], bo.purple_block_image)
        bo.draw(win.screen)
        bo2.draw(win.screen)
        pygame.display.flip()
    else:
        sleep(draw_time_diff)
    

if outcome1 == 1 or outcome2 == 2:
    winner = 1
elif outcome1 == 2 or outcome2 == 1:
    winner = 2

if winner == 2:
    bo2.draw_win(win.screen)
    bo.draw_level(win.screen)
elif winner == 1:
    bo.draw_win(win.screen)
    bo2.draw_level(win.screen)

if winner != 0:
    pygame.display.flip()
    sleep(2)
pygame.quit()
