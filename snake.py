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
		print("\033[%d;%dH%s" % (self.y, self.x, self.sym))

p1 = Point(10,20,';')
p2 = Point()
# p1.draw()
# p2.draw()

class HorizontalLine(object):
	
	def __init__(self, xleft, xright, y = 0, symb = "*"):
		self.xleft = xleft
		self.xright = xright
		self.y = y
		self.symb = symb
	def ldraw(self):	
		plist = []
		for i in range(self.xleft, self.xright):
			p = Point(i, self.y, self.symb)
			plist.append(p)
		for i in plist: 
			i.draw()

class VerticalLine(object):
	
	def __init__(self, x, yup, ybottom, symb = "*"):
		self.x = x
		self.yup = yup
		self.ybottom = ybottom
		self.symb = symb
	def ldraw(self):	
		plist = []
		for i in range(self.yup, self.ybottom):
			p = Point(self.x, i, self.symb)
			plist.append(p)
		for i in plist: 
			i.draw()

h1 = HorizontalLine(3,10,20,"+")
h1.ldraw()	
h2 = VerticalLine(3, 20, 25, "-")
h2.ldraw()

