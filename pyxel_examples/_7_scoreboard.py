#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pyxel

class ScoreBoard:
    def __init__(self):
        self.current = 0
        self.parent = 0
        # self.addType = [10, 30, 15, 2000]

    def setParent(self, parent):
        self.parent = parent

    # 要先调用setParent才能调用update
    def update(self):
        self.current = self.parent.score

    def draw(self):
        # :8是指8个空格
        pyxel.text(120 - 45, 4, "SCORE {0}".format(self.current), 7)
