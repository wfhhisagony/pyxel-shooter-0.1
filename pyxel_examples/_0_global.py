#!/usr/bin/python3
# -*- coding: utf-8 -*-
from random import seed, random, randrange, uniform
import pyxel
import time

seed(time.time())       # 使用随机种子
# 宏定义
# scene
SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_WIN = 3
# 屏幕大小
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160
# star
STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5
# player
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2
# boss
BOSS_WIDTH = 28
BOSS_HEIGHT = 32
BOSS_BLOOD = 400
BOSS_ANGER = 150
BOSS_COME_TIME = 80
# 普通子弹
BULLET_WIDTH = 2
BULLET_HEIGHT = 8
BULLET_COLOR = 11
BULLET_SPEED = 4
# 榴弹
SHRAPNEL_COLOR = 7
SHRAPNEL_RADIUS = 3
LITTLE_BULLET_RADIUS = 1
LITTLE_BULLET_RADIUS_ALTER = 2
# 飞碟和章鱼
ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
ENEMY_SPEED = 1.5
# 爆炸
BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8
BLAST_COLOR_IN = 7
BLAST_COLOR_OUT = 10
# 激光
LASER_COLOR = 3

# 要画的和要更新的元素列表，作为全局变量使用
enemy_list = []
bullet_list = []
blast_list = []
boss_list = []
little_bullet_list = []
recruit_list = []
# 记录玩家当前坐标，敌人发射的子弹将根据此进行调整
player_pos = [60, 150]
# 可被更改的开始时间
start_time = 0