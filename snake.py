#coding: utf-8
__author__='julia sayapina'

import os
import turtle
from tkinter import *

x1 = 20
y1 = 30
sym1 = '*'

# #creating canvas
# root = Tk()
# #setting the canvas' name
# root.title("Snake game")
# #launching the canvas
# root.mainloop()

# #canvas sizes vars
# WIDTH = 800
# HEIGHT = 600

# # создаем экземпляр класса Canvas (его мы еще будем использовать) и заливаем все зеленым цветом
# c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
# c.grid()
# # Наводим фокус на Canvas, чтобы мы могли ловить нажатия клавиш
# c.focus_set()


class Point(object):
	def __init__(self, x = 0, y = 0, sym = "*"):
		self.x = x
		self.y = y
		self.sym = sym
	
	def draw(self):
		print("\033[%d;%dH%s" % (self.y, self.x, self.sym))

	def shift(self, offset, direction):
		if direction == Direction.RIGHT:
			self.x = self.x + offset
		elif direction == Direction.LEFT:
			self.x = self.x - offset
		elif direction == Direction.UP:
			self.y = self.y - offset
		elif direction == Direction.DOWN:
			self.y = self.y + offset

	def clear(self):
		self.sym = " "
		self.draw()


class Figure(object):
	# def __init__(self):
	# 	self.plist = []
	plist = [] 
	def ldraw(self):
		for i in self.plist: 
			i.draw()


class HorizontalLine(Figure):
	def __init__(self, xleft, xright, y = 0, symb = "*"):
		super().__init__()
		self.xleft = xleft
		self.xright = xright
		self.y = y
		self.symb = symb

	def pappend(self):
		for i in range(self.xleft, self.xright):
			p = Point(i, self.y, self.symb)
			self.plist.append(p)
		return self.plist
		

class VerticalLine(Figure):
	def __init__(self, x, yup, ybottom, symb = "*"):
		super().__init__()
		#Figure.__init__(self)
		self.x = x
		self.yup = yup
		self.ybottom = ybottom
		self.symb = symb
	
	def pappend(self):	
		for i in range(self.yup, self.ybottom):
			p = Point(self.x, i, self.symb)
			self.plist.append(p)
		return self.plist


class Snake(Figure):
	plist2 = []
	#head = Point()
	def __init__(self, tail, length, direction):
		self.tail = tail
		self.length = length
		self.direction = direction

	def position(self):
		for i in range(self.length):
			p = Point(self.tail.x, self.tail.y)
			p.shift(i, self.direction)
			self.plist2.append(p)
			p.draw()
		return self.plist2

	def GetNextPoint(self):
		head = self.plist2[-1]
		nextPoint = Point(head.x, head.y)
		nextPoint.shift(1, self.direction)
		return nextPoint


	def move(self):
		tail = Point(self.plist2[0].x, self.plist2[0].y)
		del self.plist2[0]
		head = self.GetNextPoint()
		self.plist2.append(head)

		tail.clear()
		head.draw()




class Direction(object):
	LEFT = 0
	RIGHT = 1
	UP = 2
	DOWN = 3
	direction = [LEFT, RIGHT, UP, DOWN]




def main():
	p1 = Point(10,20,'*')
	p2 = Point()
	h1 = HorizontalLine(3,10,20,"+")
	h1.pappend()	
	h2 = VerticalLine(3, 20, 25, "-")
	h2.pappend()
	snake = Snake(p1, 4, Direction.LEFT)
	snake.position(), snake.move()


if __name__ == '__main__':
    main()

