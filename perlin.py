# The following program generates a random texture using perlin noise

import pygame
import math
import sys
import random

(SWIDTH, SHEIGHT) = (600, 600)
pygame.init()
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

BWIDTH = 10
BHEIGHT = 10
UWIDTH = SWIDTH / BWIDTH
UHEIGHT = SHEIGHT / BHEIGHT

# Grid class is where we generate the values of each pixel on screen as well as the grid of gradients an dot products
class Grid:
    def __init__(self):
        self.grid = [[Cell(i, j) for i in range(0, SWIDTH)] for j in range(0, SHEIGHT)]
        self.gradients = [[0 for i in range(0, BWIDTH + 1)] for j in range(0, BHEIGHT  + 1)]
        self.values = [[0 for i in range(0, SWIDTH)] for j in range(0, SHEIGHT)]

        self.perlinGradient()

        
    def draw(self):
        for i in range(0, SWIDTH ):
            for j in range(0, SHEIGHT ):
                self.grid[j][i].draw(self.values[j][i])
            pygame.display.flip()

    def perlinGradient(self):
        # Start by generating unit vectors for gradients and placing them on a grid 
        for i in range(0, BWIDTH + 1):
            for j in range(0, BHEIGHT + 1):
                x =0
                y =0
                while x == 0:
                    x = random.uniform(-1, 1)
                while y == 0:
                    y = random.uniform(-1, 1)
                den = math.sqrt(x * x + y * y)
                if den != 0:
                    x /= den
                    y /= den
                else:
                    x = 0
                    y = 0

                self.gradients[j][i] = (x, y)

        def interpolate(start, end, weight):
            return start + (weight) * (end - start)

        #  For each pixel on screen, generate the dot product and interpolate
        maximum = -10000
        minimum = 10000
        for x in range(0, SWIDTH - 1):
            for y in range(0, SHEIGHT - 1):
                x0 = int(x / UWIDTH)
                y0 = int(y / UHEIGHT)
                p = x / UWIDTH 
                q = y / UHEIGHT

                # dot product of gradient to distance to the four corners of the rectangle which contains the current point 
                d1 = self.dotProduct(x0, y0, p, q)
                d2 = self.dotProduct(x0 + 1, y0, p, q)
                d3 = self.dotProduct(x0, y0 + 1, p, q)
                d4 = self.dotProduct(x0 + 1, y0 + 1, p, q)

                # Interpolator
                xval = interpolate(d1, d2, p - x0)
                yval = interpolate(d3, d4, p -  x0)

                # Interpolate one more time.
                self.values[y][x] += (interpolate(xval, yval, q - y0))
                maximum = max(maximum, self.values[y][x])
                minimum = min(minimum, self.values[y][x])

        # Interpolate one more time to map the minimum to 0 and maximum to 255 for the color values.
        m = (255 - 0) / (maximum - minimum)
        b = -1 * m * minimum

        
        for x in range(0, SWIDTH - 1):
            for y in range(0, SHEIGHT - 1):
                self.values[y][x] = m * self.values[y][x] + b


    def dotProduct(self, x0, y0, x1, y1):
        dx = x1 - float(x0)
        dy = y1 - float(y0)
        (a, b) = self.gradients[y0][x0]
        return dx * a + dy * b


class Cell:
    # Draw each pixel on screen as a rectangle with a certain color value determined by the perlin noise algorith.
    def __init__(self, i ,j):
        self.x = i
        self.y = j
        self.color = (255, 255, 255)

    def draw(self, color):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        x = color
        self.color = (int(x), int(x), int(x))
        pygame.draw.rect(screen, self.color,  ( self.x  , self.y , 1, 1))



def main():
    board = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                board = Grid()
                board.draw()

            
            pygame.display.flip()

main()