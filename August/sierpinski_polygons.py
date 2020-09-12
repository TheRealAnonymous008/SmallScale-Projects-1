# The following is a program which will draw the sierpinski triangle on screen

import pygame
import sys
import math
from time import sleep

SDIMENSIONS = (700, 700)
white = (255, 255, 255 )
pygame.init()
screen = pygame.display.set_mode(SDIMENSIONS)
clock  = pygame.time.Clock()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loc = (x, y)

def drawSierpinski(depth, centerx, centery, radius, vertices):
    if depth == 0 or radius == 0:
        return
    else: 
        points = []
        turn = 360 / vertices
        halfr = radius / 2
        for i in range(0, vertices):
            points.append(Point(centerx + radius * math.cos(math.radians(90  +i * turn)), centery + radius * math.sin(math.radians(90 + i * turn))))


        for i in range(0, vertices):
            if depth == 1:
                pygame.draw.aaline(screen, white, points[i].loc, points[(i + 1)%vertices].loc, 2)
            newx = centerx + halfr * math.cos(math.radians(90 + i * turn))
            newy = centery + halfr * math.sin(math.radians(90 + i * turn))
            drawSierpinski(depth - 1, newx, newy, radius / 2, vertices)
            sleep(0.005)

                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
            pygame.display.flip()
            


def main():
    loopran = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

        (width, height) = SDIMENSIONS
        if not loopran:
            loopran = True
            drawSierpinski(6, width / 2 , height / 2, 300, 3)



main()
