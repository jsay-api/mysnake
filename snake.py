#coding: utf-8
__author__='julia sayapina'

import os, sys
from time import sleep
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint

WIDTH = 120
HEIGHT = 30
MAX_X = WIDTH - 2
MAX_Y = HEIGHT - 2
TIMEOUT = 100
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
        #self.window.addstr(self.y, self.x, self.sym)  

    def shift(self, offset, direction):
        if direction == Direction.RIGHT:
            self.x += offset
        elif direction == Direction.LEFT:
            self.x -= offset
        elif direction == Direction.UP:
            self.y -= offset
        elif direction == Direction.DOWN:
            self.y += offset

    def clear(self):
        self.sym = " "
        self.draw()

    def crossed(self, point):
        return self.x == point.x and self.y == point.y


class Figure(object):
    # def __init__(self):
    #   self.plist = []
    plist = [] 
    def ldraw(self):
        for i in self.plist: 
            i.draw()


class Snake(Figure):
    #body = []
    def __init__(self, tail, length, direction, window):
        self.body = []
        self.tail = tail
        self.length = length
        self.direction = direction
        self.window = window

    @property
    def ahead(self):
        return self.GetNextPoint()

    def render(self):
        for i in range(self.length):
            p = Point(self.tail.x, self.tail.y)
            p.shift(i, self.direction)
            self.body.append(p)
            p.draw()
        return self.body

    def GetNextPoint(self):
        head = self.body[-1]
        nextPoint = Point(head.x, head.y)
        nextPoint.shift(1, self.direction)
        return nextPoint


    def update(self):
        tail = Point(self.body[0].x, self.body[0].y)
        del self.body[0]
        head = self.GetNextPoint()
        self.body.append(head)

        tail.clear()
        head.draw()

    def get(self, event):
        if event == 32:
            key = -1
            while key != 32:
                key = self.window.getch()
        elif event == KEY_UP:
            self.direction = Direction.UP
            #sleep(0.1)
        elif event == KEY_LEFT:
            self.direction = Direction.LEFT
            #sleep(0.1)
        elif event == KEY_DOWN:
            self.direction = Direction.DOWN
            #sleep(0.1)
        elif event == KEY_RIGHT:
            self.direction = Direction.RIGHT
            #sleep(0.1)
        elif event == 27:
            gameOver()


    def eat(self, food):
        #head = self.GetNextPoint()
        if self.ahead.crossed(food):
            food.sym = self.ahead.sym
            self.body.append(food)
            food.clear()
            self.update()
            # food.__init__('$')
            # food.render()
            return True

    def hitborder(self):
        #head = self.GetNextPoint()
        for i in range(2):  #crossing top and left borders
            for j in range(WIDTH+1):
                if self.ahead.crossed(Point(i,j)) or self.ahead.crossed(Point(j,i)):
                    return True
        for i in range(HEIGHT, HEIGHT+1): #crossing the bottom border
            for j in range(WIDTH+1):
                if self.ahead.crossed(Point(j,i)):
                    return True
        for i in range(WIDTH-1, WIDTH+1):   #crossing the right border
            for j in range(HEIGHT+1):
                if self.ahead.crossed(Point(i,j)):
                    return True

    def eatbody(self):
        #head = self.GetNextPoint()
        for i in self.body:
            if self.ahead.crossed(i):
                return True


class Food(Point):
    def __init__(self, sym):
        self.x = randint(2, MAX_X)
        self.y = randint(2, MAX_Y)
        self.sym = sym

    def render(self):
        food = Point(self.x, self.y, self.sym)
        food.draw()
     

class Direction(object):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

def gameOver():
    print ("Game over!")
    sys.exit(0)


def main():
    #os.system("clear")
    curses.initscr()
    window = curses.newwin(HEIGHT, WIDTH, 0, 0)
    window.timeout(TIMEOUT)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)

    p1 = Point(50,20,'*')
    p2 = Point(2, 20)
    fsym = '@'
    snake = Snake(p1, 4, Direction.LEFT, window)
    food = Food(fsym)

    while True:
        window.clear()
        window.border(0)
        snake.render()
        window.addstr(0, 5, 'George the Snake')
        event = window.getch()

        while True:
            event = window.getch()
            food.render()
            if snake.eat(food):
                food.__init__(fsym)
                food.render()
            snake.get(event) 
            snake.update()
            sleep(0.1)
            if snake.hitborder() or snake.eatbody():
                gameOver()

    curses.endwin()
    


if __name__ == '__main__':
    main()

