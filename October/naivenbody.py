# The following program implements a naive approach to simulating the N-body problem. The time complexity of this program is O(n^2)
# The program does this by obtaining changes in acceleration of one point caused by all other points.


import pygame
import sys
import random
import math

pygame.init()
(SWIDTH, SHEIGHT) = (600, 600)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

white = (255, 255, 255)
POINTS = 50
GCONST = 0.01
VEL = GCONST * 3.5

class Planet:
    def __init__(self):
        self.x = random.randint(SWIDTH / 2 - 200, SWIDTH / 2 + 200)
        self.y = random.randint(SHEIGHT / 2 - 200, SHEIGHT / 2  +200)
        self.xvel = random.uniform(-VEL, VEL)
        self.yvel = random.uniform(-VEL, VEL)
        self.xacc = 0
        self.yacc = 0
        self.mass = random.randint(1, 10)
        self.rad = min(math.sqrt(self.mass), 100)
        self.fixed = False
        self.destroyed = False

        self.rh = self.rad * self.rad
        self.rw = self.rh
        self.rx = self.x - self.rw
        self.ry = self.y - self.rh

    def draw(self, color = white):
        self.rad = min(math.sqrt(self.mass), 100)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)) , int(self.rad))

        self.rh = self.rad * self.rad
        self.rw = self.rh
        self.rx = self.x - self.rw
        self.ry = self.y - self.rh

    def merge(self, other):
        if self == None or other == None or self == other:       return

        if other.mass >= self.mass:
            other.mass += self.mass
            self.destroyed = True

            return

        else:
            self.mass += other.mass
            other.destroyed = True
            return

    def update(self, other):
        if other == self:       return
        if self.destroyed:      return
        
        x1, y1 = self.x , self.y
        x2, y2 = other.x, other.y

        dx = x2 - x1
        dy = y2 - y1

        distance = dx * dx + dy * dy

        # Check if they collide
        if math.sqrt(distance) <= (self.rad + other.rad):
            self.merge(other)
            return
        
        # Don't update if it is a fixed point:

        if self.fixed:      return

        acc = float(GCONST * other.mass / distance)
        angle = math.atan2(dy, dx)

        # Update parameters

        self.xacc = acc * math.cos(angle)
        self.yacc = acc * math.sin(angle)
        self.xvel += self.xacc
        self.yvel += self.yacc
        self.x += self.xvel
        self.y += self.yvel

def main():
    planets = []
    sun = Planet()
    sun.x = SWIDTH / 2
    sun.y = SHEIGHT / 2
    sun.mass = 100
    sun.fixed = True

    
    # Generate planets:
    for i in range(0, POINTS):
        x = Planet()
        planets.append(x)
    planets.append(sun)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:       sys.exit()
        
        screen.fill((0, 0, 0))

        for p in planets:
            for q in planets:
                if p.destroyed: break
                if q.destroyed: continue
                p.update(q)

        for p in planets:
            if p.destroyed:     planets.remove(p)
            else:               p.draw()


        pygame.display.flip()

main()
