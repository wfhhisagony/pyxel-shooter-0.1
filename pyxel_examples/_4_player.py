#!/usr/bin/python3
# -*- coding: utf-8 -*-

from _8_skill import *


class Player:
    def __init__(self, x, y, default_skill, pb):         # defaultSkill标志了到底是哪一种飞机0、1、2
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.alive = True
        self.speed = PLAYER_SPEED
        self.bullet_delay = 0.25  # 子弹发射间隔为0.75秒
        self.last_bullet_time = 0  # 记录上次发射子弹的时间
        self.attack_mode = 0
        self.default_skill = default_skill
        self.status = [0,rtskill1(self),rtskill2(self),rtskill3(self)]
        # self.status[3].aliveTime=10
        self.pb = pb
        self.last_shoot_time = 0
        if self.default_skill == 0:
            self.status[0] = skill1(self)
        elif self.default_skill == 1:
            self.status[0] = skill2(self)
        elif self.default_skill == 2:
            self.status[0] = skill3(self)

    def update(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed

        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed

        if pyxel.btn(pyxel.KEY_W)or pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed

        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed

        if pyxel.btnp(pyxel.KEY_K):       # K 开启技能
            print(self.status[0])
            self.status[0].release()

        # 不能超出矩形框
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        if pyxel.btn(pyxel.KEY_J) and time.time() - self.last_shoot_time >= self.bullet_delay:
            self.last_shoot_time = time.time()
            print(self.attack_mode)
            if self.attack_mode < 10:
                if self.attack_mode == 0:
                    Bullet(
                        self.x + (PLAYER_WIDTH - BULLET_WIDTH) / 2, self.y - BULLET_HEIGHT / 2
                    )
                    # 播放声音
                    pyxel.play(0, 0)

                elif self.attack_mode == 1:
                    Bullet(
                        self.x + 1, self.y - BULLET_HEIGHT / 2
                    )
                    Bullet(
                        self.x + PLAYER_WIDTH - 3, self.y - BULLET_HEIGHT / 2
                    )
                    pyxel.play(0, 0)
            else:
                if self.attack_mode == 10:
                    Shrapnel(
                        self.x + (PLAYER_WIDTH - SHRAPNEL_RADIUS * 2) / 2, self.y - SHRAPNEL_RADIUS
                    )
                    # 播放声音
                    pyxel.play(0, 0)

                elif self.attack_mode == 11:
                    Shrapnel(
                        self.x - 3, self.y - SHRAPNEL_RADIUS
                    )
                    Shrapnel(
                        self.x + PLAYER_WIDTH - 3, self.y - SHRAPNEL_RADIUS
                    )
                    pyxel.play(0, 0)
                elif self.attack_mode == 20:
                    for i in range(0, randrange(8, 12)):
                        temp = uniform(-BULLET_SPEED * 1.5, BULLET_SPEED * 1.5)
                        s = uniform(0, 2)
                        if -0.5 < temp < 0.5:
                            s = 10
                        littleBullet(self.x, self.y, -s if temp > 0 else s,
                                     temp, LITTLE_BULLET_RADIUS_ALTER)
                        pyxel.play(0, 0)
                elif self.attack_mode == 21:
                    for i in range(0, randrange(16, 24)):
                        temp = uniform(-BULLET_SPEED * 1.5, BULLET_SPEED * 1.5)
                        s = uniform(0, 2)
                        if -0.5 < temp < 0.5:
                            s = 10
                        littleBullet(self.x, self.y, -s if temp > 0 else s,
                                     temp, LITTLE_BULLET_RADIUS_ALTER)
                        pyxel.play(0, 0)

            player_pos[0] = self.x + self.w / 2
            player_pos[1] = self.y + self.h / 2

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)