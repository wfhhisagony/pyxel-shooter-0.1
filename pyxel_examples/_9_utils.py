#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 最好使得C1是小物体、C2是大物体
def collisionCheck(a, b):
    if (
            a.x + a.w > b.x
            and b.x + b.w > a.x
            and a.y + a.h > b.y
            and b.y + b.h > a.y
    ):
        return True
    return False

def edgeCheck(W, H, C, mode):
    if mode == 0:           # 出边界
        if C.x + C.w +0.5<0 or C.x-0.5>W or C.y+C.h+0.5<0 or C.y-0.5>H:
            return True
        else:
            return False

    if mode == 1:           # 碰边界
        if C.x +0.5<0 or C.x+C.w-0.5>W or C.y+0.5<0 or C.y-0.5+C.h> H:
            return True
        else:
            return False

class ListProcess:
    def __init__(self):
        pass

    def update_list(self, list):
        for elem in list:
            elem.update()

    def draw_list(self, list):
        for elem in list:
            elem.draw()

    def update_skill(self, list):
        for elem in list:
            elem.update()

    def draw_skill(self, list):
        for elem in list:
            elem.draw()
