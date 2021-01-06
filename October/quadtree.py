# The following program creates a quad tree from a point list. It also simulate random uniform motion of particles. Pressing SPACE
# toggles whether or not particles move. The quadtree is updated accordingly


import pygame
import sys
import random
import copy
from time import sleep

# Initialize pygame
pygame.init()
(SWIDTH, SHEIGHT) = (600, 600)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

white = (255, 255, 255)

POINTS  = 100
CAPACITY = 5

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rectangle = None

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 2)
    
    def update(self):
        ux = random.uniform(-5, 5)
        uy = random.uniform(-5, 5)

        self.x += ux
        self.y += uy


class Rectangle:
    def __init__(self, x, y, length, width):
        # x and y represent coordinates of the upper left corner
        self.x = x
        self.y = y
        self.length = length
        self.width = width

        self.upperleft = None
        self.upperright = None
        self.lowerleft = None
        self.lowerright = None

        self.capacity = CAPACITY 
        self.contained = []
        self.pointsInside = 0

    def draw(self):
        if self.pointsInside != 0:
            pygame.draw.rect(screen, white, (self.x,self.y, self.length, self.width), 1)

        if self.upperleft != None:      self.upperleft.draw()
        if self.upperright != None:     self.upperright.draw()
        if self.lowerleft != None:      self.lowerleft.draw()
        if self.lowerright != None:     self.lowerright.draw()
    
    def check(self, point):
        xpos = point.x 
        ypos = point.y
        if self.x <= xpos and xpos <= self.x + self.length and self.y <= ypos and ypos <= self.y + self.width:
            return True
        return False

    def decompose(self, point):
        xpos = point.x
        ypos = point.y

        # Check if point is inside the rectangle
        if self.check(point):
            self.pointsInside += 1

            if self.upperleft == None and self.pointsInside <= self.capacity:      self.contained.append(point)
        else:
            return
        

        # Check if the node is full. If it is subdivide
        if self.pointsInside >= self.capacity:
            hl = float(self.length / 2.0)
            hw = float(self.width / 2.0)
            hx = float(self.x + hl)
            hy = float(self.y + hw)
            if self.upperleft == None:      self.upperleft = Rectangle(self.x, self.y, hl, hw)
            if self.upperright == None:     self.upperright = Rectangle(hx, self.y ,hl, hw)
            if self.lowerleft == None:      self.lowerleft = Rectangle(hx, hy, hl, hw)
            if self.lowerright == None:      self.lowerright = Rectangle(self.x, hy,hl, hw)


            # We ensure that only the last nodes in the tree actually contain the points
            for pt in self.contained:
                if self.upperleft.check(pt):
                    self.upperleft.contained.append(pt)
                    self.upperleft.pointsInside += 1
                elif self.upperright.check(pt):
                    self.upperright.contained.append(pt)
                    self.upperright.pointsInside += 1
                elif self.lowerleft.check(pt):
                    self.lowerleft.contained.append(pt)
                    self.lowerleft.pointsInside += 1
                elif self.lowerright.check(pt):
                    self.lowerright.contained.append(pt)
                    self.lowerright.pointsInside += 1

            self.contained *= 0

        # If the current node has been subdivided, then recur down the tree to the children nodes
        if self.pointsInside > self.capacity:
            self.upperleft.decompose(point)
            self.upperright.decompose(point)
            self.lowerleft.decompose(point)
            self.lowerright.decompose(point)
            


def main():
    points = []
    qtree = Rectangle(0, 0, SWIDTH, SHEIGHT)

    for i in range(0, POINTS):
        x = random.randint(0, SWIDTH)
        y = random.randint(0, SHEIGHT)
        points.append(Point(x, y))

    for pt in points:
        qtree.decompose(pt)
    motion = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:       sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                points *= 0
                qtree = Rectangle(0, 0, SWIDTH, SHEIGHT)
                for i in range(0, POINTS):
                    x = random.randint(0, SWIDTH)
                    y = random.randint(0, SHEIGHT)
                    pt = Point(x, y)
                    points.append(pt)
                    qtree.decompose(pt)
                motion = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    motion = not motion

        screen.fill((0, 0, 0))

        if motion:
            qtree = Rectangle(0, 0, SWIDTH, SHEIGHT)
        for pt in points:
            if motion:   
                pt.update()
                qtree.decompose(pt)
            pt.draw()
            

        qtree.draw()
        

        pygame.display.flip()



main()
