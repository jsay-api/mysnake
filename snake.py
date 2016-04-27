#!/usr/bin/python3
#coding: utf-8
__author__='julia sayapina'

import os
import turtle
from tkinter import *

x1 = 30
y1 = 30
sym1 = '*'

def draw(x,y,sym):
	print("\033[%d;%dH%s" % (x, y, sym))

draw(10, 20, '#')
