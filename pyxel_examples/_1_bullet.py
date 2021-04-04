#!/usr/bin/python3
# -*- coding: utf-8 -*-

from _0_global import *

# 普通子弹类
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.alive = True

        bullet_list.append(self)

    def update(self):
        self.y -= BULLET_SPEED

        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)


# littelBullet类
class littleBullet:
    def __init__(self, x, y, direction, speed, radius):  # direction是纵速比横速，speed是横向速度,纵向速度 = speed * direction
        self.x = x
        self.y = y
        self.xspeed = speed
        self.yspeed = self.xspeed * direction
        self.radius = radius
        self.w = self.h = self.radius * 2
        self.alive = True

        bullet_list.append(self)

    def update(self):
        self.y += self.yspeed
        self.x += self.xspeed

        # 超出范围后死亡
        if self.y + 2 * self.radius - 1 < 0:
            self.alive = False
        if self.x + 2 * self.radius - 1 < 0 or self.x - 2 * self.radius + 1 > 120:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x+self.radius, self.y+self.radius, self.radius, randrange(7, 12))

# Sharpnel类
class Shrapnel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = SHRAPNEL_RADIUS
        self.w = self.h = self.radius * 2
        self.alive = True

        bullet_list.append(self)

    def update(self):
        self.y -= BULLET_SPEED

        # 超出范围后死亡
        if self.y - 1 < 0:
            self.alive = False

        if self.alive is False and self.y -1 < 0:
            for i in range(0, randrange(5, 8)):
                # print(1)
                temp = uniform(-BULLET_SPEED * 1.5, BULLET_SPEED * 1.5)
                littleBullet(self.x, self.y, uniform(0, 2) if temp > 0 else -uniform(0, 2),
                                                        temp, LITTLE_BULLET_RADIUS)
        elif self.alive is False:
            for i in range(0, randrange(5, 8)):
                littleBullet(self.x, self.y, uniform(-0.8, 0.8),
                                                        uniform(-BULLET_SPEED * 1.5, BULLET_SPEED * 1.5), LITTLE_BULLET_RADIUS)

    def draw(self):
        pyxel.circ(self.x+self.radius, self.y+self.radius, self.radius, SHRAPNEL_COLOR)


