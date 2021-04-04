#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 1、释放
# 2、和powerBar拉钩
# 3、和玩家有关(玩家的形态改变、属性改变)

from _0_global import *
from _1_bullet import Bullet, Shrapnel, littleBullet

# 幻影
class skill1:
    def __init__(self, parent):
        self.limitTime = 10
        self.aliveTime = 0  # 技能好了要重置
        self.flag = False                # 技能开关,只有开了才会减
        self.parent = parent
        self.p1 = 0
        self.p2 = 0
        self.start_time = -1

    def release(self):
        if self.parent.pb.current == self.parent.pb.total:
            self.aliveTime = self.limitTime
            self.parent.pb.skillbar = True

    def update(self):
        if self.aliveTime == self.limitTime and self.flag is False: #表示第一次启动
            print(1)
            self.flag = True
            self.p1 = PlayerCopy(-self.parent.w - 2, self.parent)  # 左边的
            self.p2 = PlayerCopy(self.parent.w + 2, self.parent)  # 右边的
            self.start_time = time.time()

        if self.aliveTime > 0 and self.flag is True:
            self.p1.update()
            self.p2.update()
            self.aliveTime = self.limitTime - (time.time() - self.start_time)
            self.parent.pb.current = self.aliveTime

        # 小于是一种粗略的错误检验
        if self.aliveTime <= 0 and self.flag is True:     # 通过main函数让aliveTime减小的
            self.aliveTime = 0
            self.flag = False
            self.parent.pb.skillbar = False
            del self.p1
            del self.p2

    def draw(self):
        if self.aliveTime > 0 and self.flag is True:
            self.p1.draw()
            self.p2.draw()

# 激光类
class Laser:
    def __init__(self, parent):
        self.parent = parent
        self.alive = False
        self.w = self.parent.parent.w
        self.h = self.parent.parent.y - 3
        self.x = self.parent.parent.x
        self.y = 0
        self.flag = False

    def update(self):
        if self.parent.aliveTime > 0 and self.flag is False:
            self.alive = True
            self.flag = True
            bullet_list.append(self)

        if self.parent.aliveTime > 0 and self.flag is True:
            self.x = self.parent.parent.x
            self.y = 0

        if self.parent.aliveTime <= 0:
            self.parent.aliveTime = 0
            self.alive = False
            self.flag = False

    def draw(self):
        if self.parent.aliveTime > 0 and self.alive is True:
            if self.parent.parent.y - 3 > 0:
                pyxel.rect(self.parent.parent.x-randrange(0, 2), 0, self.parent.parent.w-randrange(0, 2), self.parent.parent.y - 3,
                           LASER_COLOR)
# 激光
# 发射激光时捡了暴走无效
class skill2:
    def __init__(self, parent):
        self.limitTime = 1
        self.aliveTime = 0  # 技能好了要重置
        self.flag = False  # 技能开关,只有开了才会减
        self.parent = parent
        # self.temp = 0
        self.Laser = Laser(self)
        self.start_time = -1

    def release(self):
        if self.parent.pb.current == self.parent.pb.total:
            self.aliveTime = self.limitTime
            self.parent.pb.skillbar = True
            self.flag = True
            self.parent.pb.current = self.aliveTime / self.limitTime * 20
            self.start_time = time.time()
            # self.parent.speed, self.temp = self.temp, self.parent.speed

    def update(self):
        if self.aliveTime > 0 and self.flag is True:
            self.aliveTime = self.limitTime - (time.time() - self.start_time)
            self.parent.pb.current = self.aliveTime / self.limitTime * 20
            self.Laser.update()

        # 小于是一种粗略的错误检验
        if self.aliveTime <= 0 and self.flag is True:     # 通过main函数让aliveTime减小的
            self.aliveTime = 0
            self.flag = False
            self.start_time = -1
            # self.parent.speed, self.temp = self.temp, self.parent.speed
            self.parent.pb.skillbar = False

    def draw(self):
        self.Laser.draw()

# 敏捷
class skill3:
    def __init__(self, parent):
        self.limitTime = 3
        self.aliveTime = 0  # 技能好了要重置
        self.flag = False                # 技能开关,只有开了才会减
        self.parent = parent
        self.temp = [0, 0]
        self.start_time = -1
        self.now_pic = 0

    def release(self):
        if self.parent.pb.current == self.parent.pb.total:
            self.aliveTime = self.limitTime
            self.parent.pb.skillbar = True
            self.flag = True
            self.parent.pb.current = self.aliveTime
            self.start_time = time.time()

            self.temp[0] = self.parent.speed
            self.temp[1] = self.parent.bullet_delay
            self.parent.speed = self.temp[0] * 2.5
            self.parent.bullet_delay = self.temp[1] * 0.1

    def update(self):
        if self.aliveTime > 0 and self.flag is True:
            self.aliveTime = self.limitTime - (time.time() - self.start_time)
            self.parent.pb.current = self.aliveTime
            self.temp[0] = self.parent.speed / 2.5       #  与暴走保持一致

        # 小于是一种粗略的错误检验
        if self.aliveTime <= 0 and self.flag is True:     # 通过main函数让aliveTime减小的
            self.aliveTime = 0
            self.flag = False
            self.start_time = -1
            self.parent.speed = self.temp[0]
            self.parent.bullet_delay = self.temp[1]
            self.parent.pb.skillbar = False

    def draw(self):
        if self.aliveTime > 0:
            if pyxel.frame_count % 24 < 8:
                self.now_pic = 84
            elif 8<=pyxel.frame_count % 24<16:
                self.now_pic = 86
            else:
                self.now_pic = 88
            pyxel.blt(self.parent.x + self.parent.w-2, self.parent.y+self.parent.h, 1,self.now_pic, 128, 2, 8)
            pyxel.blt(self.parent.x , self.parent.y+self.parent.h, 1,self.now_pic, 128, 2, 8)

# 子弹数加1
class rtskill1:
    def __init__(self, parent):
        self.limitTime = 15
        self.aliveTime = 0              # 技能好了要重置
        self.flag = False                # 技能开关,只有开了才会减
        self.parent = parent            # 想要改变parent中的mode
        self.start_time = 0
        self.total_time = 0             # 之前的limitTime就相当于时total_time

    def release(self):
        if self.parent.attack_mode % 10 < 1:  # 0、1两种种模式。(第一次捡)
            self.start_time = time.time()
            self.parent.attack_mode += 1
            self.aliveTime += self.limitTime
        else:
            self.aliveTime += self.limitTime
            self.start_time = time.time()

        self.flag = True
        self.total_time = self.aliveTime

    def update(self):
        # 开启之前
        if self.flag and self.aliveTime > 0:
            self.aliveTime = self.total_time - (time.time() - self.start_time)

        # 小于是一种粗略的错误检验
        if self.aliveTime <= 0 and self.flag is True:
            self.aliveTime = 0
            self.flag = False
            self.total_time = 0
            self.parent.attack_mode -= 1            # 回归0
            if self.parent.attack_mode < 0:
                self.parent.attack_mode = 0

    def draw(self):
        pass
# 暴走
class rtskill2:
    def __init__(self, parent):
        self.limitTime = 15
        self.aliveTime = 0  # 技能好了要重置
        self.flag = False  # 技能开关,只有开了才会减
        self.turnon = False
        self.parent = parent  # 想要改变parent中的mode
        self.temp = [0]
        self.total_time = 0
        self.start_time = 0

    def release(self):
        if self.turnon is False:  # (第一次捡)
            self.turnon = True
            self.start_time = time.time()
            self.aliveTime += self.limitTime
            self.temp[0] = self.parent.speed
            self.parent.speed = self.temp[0] * 2
            print(self.parent.speed)
        else:
            self.aliveTime += self.limitTime
            self.start_time = time.time()

        self.flag = True
        self.total_time = self.aliveTime

    def update(self):
        if self.flag and self.turnon and self.aliveTime > 0:
            self.temp[0] = self.parent.speed / 2  # 与其保持一致,防止暴走与敏捷冲突
            self.aliveTime = self.total_time - (time.time() - self.start_time)
            print(self.temp[0], self.parent.speed)

        # 小于是一种粗略的错误检验
        if self.aliveTime <= 0 and self.flag:
            self.aliveTime = 0
            self.flag = False
            self.turnon = False
            self.parent.speed = self.temp[0]
            print(self.parent.speed)
            self.total_time = 0

    def draw(self):
        pass
#榴弹
class rtskill3:
    def __init__(self, parent):
        self.limitTime = 10
        self.aliveTime = 0  # 技能好了要重置
        self.flag = False  # 技能开关,只有开了才会减
        self.parent = parent  # 想要改变parent中的mode
        self.start_time = 0
        self.total_time = 0

    def release(self):
        if (self.parent.attack_mode / 10) % 10 < 2:  # 0、1两种种模式。(第一次捡)
            self.parent.attack_mode += 10
            self.aliveTime += self.limitTime
            self.start_time = time.time()
        else:
            self.aliveTime += self.limitTime
            self.start_time = time.time()
        self.flag = True
        self.total_time = self.aliveTime

    def update(self):
        # 中间过程
        if self.flag and self.aliveTime > 0:
            self.aliveTime = self.total_time - (time.time() - self.start_time)
            print(self.aliveTime)

        # 小于是一种粗略的错误检验
        if self.aliveTime <= 0 and self.flag:
            self.aliveTime = 0
            self.total_time = 0
            self.flag = False
            self.parent.attack_mode -= (10 * ((self.parent.attack_mode / 10) % 10))
            if self.parent.attack_mode < 0:
                self.parent.attack_mode = 0
            print(self.parent.attack_mode)

    def draw(self):
        pass

class PlayerCopy:
    def __init__(self, shift, parent):         # shift相对偏移量
        self.parent = parent
        self.x = self.parent.x + shift              # 使用偏移量
        self.y = self.parent.y
        self.w = self.parent.w
        self.h = self.parent.h / 2
        self.alive = self.parent.alive
        self.speed = self.parent.speed
        self.bullet_delay = self.parent.bullet_delay  # 子弹发射间隔为0.75秒
        self.last_bullet_time = self.parent.last_bullet_time  # 记录上次发射子弹的时间
        self.attack_mode = self.parent.attack_mode
        self.status = self.parent.status  # 本体
        self.shift = shift          # 偏移
        self.last_shoot_time = self.parent.last_shoot_time

    def update(self):
        self.x = self.parent.x + self.shift
        self.y = self.parent.y
        self.alive = self.parent.alive
        self.speed = self.parent.speed
        self.bullet_delay = self.parent.bullet_delay  # 子弹发射间隔为0.25秒
        self.last_bullet_time = self.parent.last_bullet_time  # 记录上次发射子弹的时间
        self.attack_mode = self.parent.attack_mode
        self.status = self.parent.status

        if pyxel.btn(pyxel.KEY_J) and time.time() - self.last_shoot_time >= self.bullet_delay:
            self.last_shoot_time = time.time()
            if self.attack_mode < 10:
                if self.attack_mode == 0:
                    Bullet(
                        self.x + (PLAYER_WIDTH - BULLET_WIDTH) / 2, self.y - BULLET_HEIGHT / 2
                    )

                elif self.attack_mode == 1:
                    Bullet(
                        self.x + 1, self.y - BULLET_HEIGHT / 2
                    )
                    Bullet(
                        self.x + PLAYER_WIDTH - 3, self.y - BULLET_HEIGHT / 2
                    )

            else:
                if self.attack_mode == 10:
                    Shrapnel(
                        self.x + (PLAYER_WIDTH - SHRAPNEL_RADIUS * 2) / 2, self.y - SHRAPNEL_RADIUS
                    )
                    # 播放声音

                elif self.attack_mode == 11:
                    Shrapnel(
                        self.x - 3, self.y - SHRAPNEL_RADIUS
                    )
                    Shrapnel(
                        self.x + PLAYER_WIDTH - 3, self.y - SHRAPNEL_RADIUS
                    )
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


    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h, 15)