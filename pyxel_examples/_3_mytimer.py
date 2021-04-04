#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pyxel
import time

class myTimer:
    def __init__(self,start_time):
        self.current = 0
        self.start_time = start_time

    def reset(self):
        self.current = 0
        self.start_time = time.time()

# update说不定是在draw之前,也就是说要将draw的变量焕然一新
    def update(self):
        self.current = int(time.time() - self.start_time)

    def draw(self):
        pyxel.text(120 - 45, 10, "Time {:2}".format(self.current), 7)