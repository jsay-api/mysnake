#!/usr/bin/python3
#coding: utf-8
__author__='julia sayapina'

import os
import turtle
from tkinter import *

x1 = 20
y1 = 30
sym1 = '*'


class Point(object):
	def __init__(self, x = 0, y = 0, sym = "*"):
		self.x = x
		self.y = y
		self.sym = sym
	def draw(self):
		print("\033[%d;%dH%s" % (self.x, self.y, self.sym))

p1 = Point(10,20,';')
p2 = Point()
p1.draw()
p2.draw()
