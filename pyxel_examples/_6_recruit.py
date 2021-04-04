#!/usr/bin/python3
# -*- coding: utf-8 -*-

from _0_global import *
from _9_utils import *

class Recruit:
    def __init__(self, x, number, direction, speed): # speed 是 y的speed
        self.x = x
        self.y = 0
        self.alive = True
        self.yspeed = speed
        self.xspeed = speed * direction
        self.collisionsNum = 5              # 碰撞5次消失
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.number = number
        if self.number == 0:
            self.str = "A"
        elif self.number == 1:
            self.str = "B"
        else:
            self.str = "C"
        recruit_list.append(self)

    def update(self):
        self.y += self.yspeed
        self.x += self.xspeed
        if self.collisionsNum != 0:
            if edgeCheck(120, 160, self, 1):
                self.collisionsNum -= 1
            if self.x + 0.5 < 0 or self.x + self.w - 0.5 > 120:
                self.xspeed = - self.xspeed
            if self.y + 0.5 < 0 or self.y - 0.5 + self.h > 160:
                self.yspeed = - self.yspeed
        if self.collisionsNum == 0:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 0)
        pyxel.text(self.x + 3, self.y + 3, self.str, 3 if pyxel.frame_count % 72 > 36 else 4)
