#coding: utf-8
__author__='julia sayapina'

import os
import turtle
from tkinter import *
from time import sleep
import getch
import threading, os, time, itertools, queue

"""For control use keys:
s - left
d - right
e - up
x - down
q - escape
any other key – game over"""


try : # on windows
    from msvcrt import getch
except ImportError : # on unix systems
    import sys, tty, termios
    def getch() :
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try :
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally :
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# this will allow us to communicate between the two threads
# Queue is a FIFO list, the param is the size limit, 0 for infinite
commands = queue.Queue(0)

# the thread reading the command from the user input     
def control(commands) :

    while 1 :

        key = getch()
        commands.put(key) # put the command in the queue so the other thread can read it

        #  don't forget to quit here as well, or you will have memory leaks
        if key == "q" :
            print ("Exit")
            sys.exit(0)

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
    #   self.plist = []
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


    def move(self, commands):
        key = ""
        
        while True:
            tail = Point(self.plist2[0].x, self.plist2[0].y)
            del self.plist2[0]
            head = self.GetNextPoint()
            self.plist2.append(head)
            # parsing the command queue
            try:
               # false means "do not block the thread if the queue is empty"
               # a second parameter can set a millisecond time out
               key = commands.get(False) 
            except queue.Empty:
               key = ""

            # behave according to the command
            self.get(key)


        tail.clear()
        head.draw()
        sleep(0.1)

        

    def get(self, key):
        while True:
            
            if key == "e":
                self.direction = Direction.UP
                #sleep(0.1)
                break
            elif key == "s":
                self.direction = Direction.LEFT
                #sleep(0.1)
                break
            elif key == "x":
                self.direction = Direction.DOWN
                #sleep(0.1)
                break
            elif key == "d":
                self.direction = Direction.RIGHT
                #sleep(0.1)
                break
            elif key == "q":
                print ("Exit")
                sys.exit(0)
        # else: 
        #     print ("Game over!")
        #     sys.exit(0)





class Direction(object):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    direction = [LEFT, RIGHT, UP, DOWN]




def main():
    os.system("clear")
    x1 = 20
    y1 = 30
    sym1 = '*'
    p1 = Point(50,20,'*')
    p2 = Point()
    h1 = HorizontalLine(3,10,20,"+")
    h1.pappend()    
    h2 = VerticalLine(3, 20, 25, "-")
    h2.pappend()
    snake = Snake(p1, 4, Direction.LEFT)
    snake.position()
    # then start the two threads
    displayer = threading.Thread(None, # always to None since the ThreadGroup class is not implemented yet
                            snake.move, # the function the thread will run
                            None, # doo, don't remember and too lazy to look in the doc
                            (commands,), # *args to pass to the function
                             {}) # **kwargs to pass to the function

    controler = threading.Thread(None, control, None, (commands,), {})
    global key
    key = getch()
    
    
    # while True:
    #     snake.move()
    # snake.get()
        
        
    


if __name__ == '__main__':
    main()