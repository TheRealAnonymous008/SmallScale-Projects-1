import pygame
import sys
import math
from time import sleep

pygame.init()
(SWIDTH, SHEIGHT) = (800, 800)
screen = pygame.display.set_mode((800, 800))

RESOLUTION = 50

class Circle:
    def __init__ (self):
        self.points = []

        turn = math.radians(360 / RESOLUTION)
        centerx = int(SWIDTH / 2)
        centery = int(SHEIGHT / 2)
        for i in range(0, RESOLUTION):
            x = centerx + 300 * math.cos(i * turn)
            y = centery + 300 * math.sin(i * turn)
            self.points.append((int(x), int(y)))

    def draw(self, n):
        for p in self.points:
            pygame.draw.circle(screen, (255, 255, 255), p , 4)

        # Draw lines:
        for i in range(0, RESOLUTION):
            currp = self.points[i]
            # Determine the next point, the other endpoint
            j = n * i

            j = int(j) % RESOLUTION
            nextp = self.points[j]

            pygame.draw.aaline(screen, (255, 0, 0), currp, nextp)

def main():
    circle = Circle()
    n = 2
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    n += 0.1
                elif e.key == pygame.K_a:
                    n -= 0.1
        n += 0.05
        if n > RESOLUTION:
            n = RESOLUTION
        screen.fill((0, 0, 0))
        circle.draw(n)

        pygame.display.flip()
        sleep(0.01)


main()
            
