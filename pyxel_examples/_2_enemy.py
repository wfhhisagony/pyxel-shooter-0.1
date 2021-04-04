#!/usr/bin/python3
# -*- coding: utf-8 -*-

from _0_global import *

class GenralEnemy:
    def __init__(self):
        pass

class Octopus(GenralEnemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)
        enemy_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += ENEMY_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY_SPEED
            self.dir = -1

        self.y += ENEMY_SPEED

        if self.y > pyxel.height - 1:
            self.alive = False
    # 这个画应该是不停的画,传入坐标和框框大小
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w * self.dir, self.h, 0)

# 先不考虑圆盘发射子弹
class Enemy(GenralEnemy):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.speed = speed
        self.alive = True
        self.shoot = False
        self.shoot_time = -1

        enemy_list.append(self)

    def update(self):
        self.y += self.speed
        if self.y > pyxel.height - 1:
            self.alive = False

        if self.shoot is False:
            self.shoot = True if randrange(0, 1000) < 5 else False

        if self.shoot is True and self.shoot_time == -1:
            EnemyCircle(self.x+self.w/2, self.y+self.h, ENEMY_SPEED-1)
            self.shoot_time = pyxel.frame_count % 25

        elif self.shoot_time > 0 and self.shoot_time ==pyxel.frame_count % 25 and self.shoot is True:
            self.shoot_time = -1
            self.shoot = False

    # 这个画应该是不停的画,传入坐标和框框大小
    def draw(self):
        if self.shoot is False:
            pyxel.blt(self.x, self.y, 1, 8, 48, self.w, self.h, 0)
        else:
            pyxel.blt(self.x, self.y, 1, 0, 48, self.w, self.h, 0)


class EnemyCircle(GenralEnemy):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.speed = speed
        self.dir = player_pos
        self.xspeed = self.speed if player_pos[0]-self.x > 0 else -self.speed
        self.yspeed = -self.xspeed * (player_pos[1] - self.y) / (player_pos[0] - self.x) if abs(player_pos[0] - self.x) > 1.5 else 0
        self.alive = True

        enemy_list.append(self)

    def update(self):
        self.y -= self.yspeed
        self.x += self.xspeed

        if self.y > pyxel.height - 1:
            self.alive = False

    # 这个画应该是不停的画,传入坐标和框框大小
    def draw(self):
        pyxel.blt(self.x, self.y, 1, 40, 32, self.w, self.h, 0)


# 移动先算了
class Boss(GenralEnemy):  # 150发子弹的血量
    def __init__(self):
        self.blood = BOSS_BLOOD
        self.x = 46
        self.y = 0
        self.w = BOSS_WIDTH
        self.h = BOSS_HEIGHT
        self.alive = True
        self.pic_pos = [[0, 128], [28, 128], [56, 128]]
        self.index = 0
        self.anger = BOSS_ANGER
        self.angry = False
        self.duration_start = 0
        self.draw_flag = False

        boss_list.append(self)

    def update(self):
        if self.blood <= 0:
            self.alive = False
        if pyxel.frame_count % 20 == 0:
            if randrange(0, 3) > 0:     # 2/3 几率出怪
                self.index = (self.index + 1) % 3
                for i in range(randrange(4, 7)):
                    Octopus(self.x + self.w / 2+(i-3)*8,self.y+self.h+1)

        # 血量小于 150 愤怒模式
        if 0 < self.blood <= BOSS_ANGER and self.draw_flag is False and self.duration_start == 0:
            self.angry = True
            self.duration_start = time.time()
            self.draw_flag = True

        if self.angry is True:
            if pyxel.frame_count % 30 == 0:
                if randrange(0, 3) > 0:
                    EnemyCircle(self.x + self.w / 2,self.y, BULLET_SPEED)

        if time.time() - self.duration_start >= 10:
            self.draw_flag = False

    def draw(self):
        # 只要想办法改变这其中的参数就能实现图片的切换，也就能实现动画
        # 总之下面的是画出boss来
        pyxel.blt(self.x, self.y, 1, self.pic_pos[self.index][0], self.pic_pos[self.index][1], self.w, self.h, 0)
        if self.draw_flag:
            pyxel.text(self.x + self.w / 2 + randrange(-1, 2), self.y + self.h/4, "Angery", 8)