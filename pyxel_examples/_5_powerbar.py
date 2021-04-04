#!/usr/bin/python3
# -*- coding: utf-8 -*-

powerBar_width = 20
powerBar_height = 5
powerBar_totalColor = 1
powerBar_currentColor = 10

import pyxel
class powerBar:
    def __init__(self, total):
        # if curren 等于 total 才能释放技能
        self.total = total
        self.current = total
        self.w = powerBar_width
        self.h = powerBar_height
        # self.parent = parent
        self.cw = self.w
        self.skillbar = True

    def set(self, t, c):
        self.total = t
        self.current = c

    def update(self):
        self.cw = int(self.w * self.current / self.total)

        # 稍微检错
        if self.current < 0:
            self.current = 0
        if self.current > self.total:
            self.current = self.total

    def draw(self):
        pyxel.rect(3, 3, self.w, self.h, powerBar_totalColor)
        pyxel.rect(3, 3, self.cw, self.h, powerBar_currentColor-1 if self.current == self.total and pyxel.frame_count % 72 > 36 else powerBar_currentColor)