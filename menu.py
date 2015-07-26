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
#   Tetroll is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Tetroll.  If not, see <http://www.gnu.org/licenses/>.

import sys
import PyQt5
from PyQt5.QtWidgets import (QApplication, QWidget,
        QPushButton, QToolTip, QMessageBox, 
        QVBoxLayout, QComboBox, QLabel,
        QLineEdit, QCheckBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication
from os import system, listdir

class Resolution(QWidget):
    """
    Widget for setting the resolution
    """
    def __init__(self):
        super(Resolution, self).__init__()
        self.width = 0
        self.height = 0
        self.fullscreen = True
        self.initUI()
        self.hide()
    def initUI(self):
        vbox = QVBoxLayout(self)
        self.width_line = QLineEdit("0", self)
        self.width_line.setToolTip("Width (0 is your screen resolution)")
        self.height_line = QLineEdit("0", self)
        self.height_line.setToolTip("Height (0 is your screen resolution)")
        self.fullscreen_box = QCheckBox("Fullscreen", self)
        self.fullscreen_box.setTristate(False)
        self.fullscreen_box.setChecked(True)
        vbox.addWidget(self.width_line)
        vbox.addWidget(self.height_line)
        vbox.addWidget(self.fullscreen_box)
    def validate_lines(self):
        states = []
        for line in [self.width_line, self.height_line]:
            text = line.text()
            if text.isdigit():
                if int(text) >= 0:
                    line.setStyleSheet("QLineEdit {background: rgb(210, 255, 210)}")
                    states.append(0)
                else:
                    states.append(1)
                    line.setStyleSheet("QLineEdit {background: rgb(255, 210, 210)}")
            else:
                states.append(2)
                line.setStyleSheet("QLineEdit {background: rgb(255, 210, 210)}")
        if states.count(0) == len(states):
            return True
        else:
            return False

    def set_values(self):
        self.width = int(self.width_line.text())
        self.height = int(self.height_line.text())
        self.fullscreen = self.fullscreen_box.isChecked()
    def __call__(self):
        if self.isVisible():
            if self.validate_lines():
                self.set_values()
                self.hide()
        else:
            self.show()

class Controls(QWidget):
    """
    Widget for setting the controlls
    """
    def __init__(self):
        super(Controls, self).__init__()
        # 0 - key action
        # 1 - bool setting
        self.boards = [1, 2]
        self.next_setting = True
        self.settings = [
                ["ml", 0],
                ["mr", 0],
                ["rl", 0],
                ["rr", 0],
                ["at", 0],
                ["ab", 0],
                ["guide_on", 1],
                ]
        self.actions = []
        self.conversion = {
                65509:301,
                65505:304,
                65507:306,
                65513:308,
                65027:313,
                65508:305,
                65506:303,
                65293:13,
                65288:8,
                65361:276,
                65363:275,
                65362:273,
                65364:274,
                }
        self.current_board = 0
        self.current_setting = 0
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        self.line = QLineEdit("HUQ", self)
        self.line.setToolTip("Press a key to assign to an action\nor (y/n) in case of a boolean.")
        self.one_more = QPushButton("ONE MORE", self)
        self.one_more.setToolTip("Set the current setting once again.")
        self.one_more.clicked.connect(self.stop_settings)
        self.input_prompt()
        self.line.keyPressEvent = self.keyPressEvent
        vbox.addWidget(self.line)
        vbox.addWidget(self.one_more)
        self.hide()


    def __call__(self):
        self.hide() if self.isVisible() else self.show()

    def keyPressEvent(self, e):
        key = e.nativeVirtualKey()
        if key in self.conversion:
            key = self.conversion[key]
        self.actions.append([
            self.boards[self.current_board],
            self.settings[self.current_setting][0],
            self.settings[self.current_setting][1],
            key])

        if self.next_setting:
            self.current_setting += 1
            if self.current_setting >= len(self.settings):
                self.current_setting = 0
                self.current_board += 1
                if self.current_board >= len(self.boards):
                    self.current_board = 0
                    self.finalize()
            self.input_prompt()
        else:
            self.restart_settings()

    def finalize(self):
        f = open("config/tmp_config.conf", "w")
        for board, action, t, key in self.actions:
            if t == 0:
                f.write("".join([str(key), ":", str(board), ":", action, "\n"]))
            elif key == 121:
                f.write("".join([str(board), ":", action, "\n"]))
        f.close()
        self.actions = []
        self.hide()

    def input_prompt(self):
        hint = "key"
        if self.settings[self.current_setting][1] == 1:
            hint = "y/n"
        self.line.setText("Board %i %s (%s)" % (
                self.boards[self.current_board],
                self.settings[self.current_setting][0],
                hint))

    def stop_settings(self):
        self.next_setting = False
        self.line.setStyleSheet("QLineEdit {background: rgb(200, 200, 255)}")

    def restart_settings(self):
        self.next_setting = True
        self.line.setStyleSheet("QLineEdit {background: white}")

class Menu(QWidget):
    """
    Tetroll Menu
    """
    def __init__(self):
        super(Menu, self).__init__()

        self.joy = 1
        self.mod = "20levels.mods"
        self.ai = "0"

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont("SansSerif", 10))
        vbox = QVBoxLayout(self)
        self.configbox = QComboBox(self)
        self.configbox.setToolTip("Configuration file")

        for f in listdir("./config"):
            if f[-4:] == "conf":
                self.configbox.addItem(f)
        self.ai_delay = QComboBox(self)
        for i in range(1,4):
            self.ai_delay.addItem(str(i))
        self.ai_delay.setToolTip("AI Delay")


        btn_pl_vs_pl = QPushButton("PL VS PL", self)
        btn_pl_vs_pl.clicked.connect(self.pl_vs_pl)
        btn_pl_vs_pl.setToolTip("-get 21 levels\n-don't fill up 3 times\n-speed raises when you clear a level")

        btn_pl_vs_pl_mod = QPushButton("PL VS PL MOD", self)
        btn_pl_vs_pl_mod.clicked.connect(self.pl_vs_pl_mod)
        btn_pl_vs_pl_mod.setToolTip("-don't fill up 3 times\n-enemy speed raises when you clear a level")

        btn_vs_ai = QPushButton("PL VS AI", self)
        btn_vs_ai.clicked.connect(self.vs_ai)
        btn_vs_ai.setToolTip("-play against an AI\n-get 21 levels\n-don't fill up 3 times\n-speed raises when you clear a level")

        btn_vs_ai_mod = QPushButton("PL VS AI MOD", self)
        btn_vs_ai_mod.clicked.connect(self.vs_ai)
        btn_vs_ai_mod.setToolTip("-play against an AI\n-get 21 levels\n-don't fill up 3 times\n-speed raises when enemy clears a level")

        btn_ai_vs_ai = QPushButton("AI VS AI", self)
        btn_ai_vs_ai.clicked.connect(self.ai_vs_ai)
        btn_ai_vs_ai.setToolTip("-watch an AI vs AI match\n-get 21 levels\n-don't fill up 3 times")


        controls = Controls()
        btn_toggle_controls = QPushButton("SET CONTROLS", self)
        btn_toggle_controls.setToolTip("-fill all settings\n-new config is available at tmp_config.conf")
        btn_toggle_controls.clicked.connect(controls)

        self.resolution = Resolution()
        btn_toggle_resolution = QPushButton("SET RESOLUTION", self)
        btn_toggle_resolution.setToolTip("-set the game resolution")
        btn_toggle_resolution.clicked.connect(self.resolution)

        vbox.addWidget(btn_pl_vs_pl)
        vbox.addWidget(btn_pl_vs_pl_mod)
        vbox.addWidget(btn_vs_ai)
        vbox.addWidget(btn_vs_ai_mod)
        vbox.addWidget(btn_ai_vs_ai)
        vbox.addWidget(btn_toggle_controls)
        vbox.addWidget(controls)
        vbox.addWidget(self.configbox)
        vbox.addWidget(self.ai_delay)
        vbox.addWidget(btn_toggle_resolution)
        vbox.addWidget(self.resolution)

        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle("Menu")
        self.setWindowIcon(QIcon("green_block.png"))



        self.show()
    def vs_ai_mod(self):
        self.mod = "20levels_trolltime.mods"
        self.ai = "1"
        system("./tetroll.py" + self.option_str())
    def vs_ai(self):
        self.mod = "20levels.mods"
        self.ai = "1"
        system("./tetroll.py" + self.option_str())
    def ai_vs_ai(self):
        self.mod = "20levels.mods"
        self.ai = "2"
        system("./tetroll.py" + self.option_str())
    def pl_vs_pl(self):
        self.mod = "20levels.mods"
        self.ai = "0"
        system("./tetroll.py" + self.option_str())
    def pl_vs_pl_mod(self):
        self.mod = "3fill.mods"
        self.ai = "0"
        system("./tetroll.py" + self.option_str())
    def option_str(self):
        print(self.configbox.currentText())
        opt = ""
        optlist = [self.joy, int(self.resolution.fullscreen),
                    self.resolution.width, self.resolution.height,
                    self.configbox.currentText(), self.mod, self.ai,
                    self.ai_delay.currentText()]
        for i in optlist:
            opt += " "
            opt += str(i)
        return opt

app = QApplication(sys.argv)

menu = Menu()

sys.exit(app.exec_())
