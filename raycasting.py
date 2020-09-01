# The following program simulates a raycast and using a raycast simulates line of sight in a paritioned plane

import pygame
import math 
import random
import sys

#Initialize pygame
pygame.init()
(SWIDTH, SHEIGHT) = (800, 600)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
white = (255, 255, 255)
yellow = (255, 255, 0)

# Define important constants
RAYCOUNT = 400
FOV = 45
currangle = math.radians(FOV/RAYCOUNT) 
WALLCOUNT = 10


#Create a wall class. When light strikes it, it will not pass through
class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        pygame.draw.aaline(screen, white, self.start, self.end)


# Point class serves as a singleton for light source.
class Point:
    def __init__(self, loc, walls, objects):
        self.loc = loc    
        self.walls = walls
        self.rays = []
        self.objects = objects

        (x, y) = self.loc
        (a, b) = pygame.mouse.get_pos()

        angle = math.atan2((y - b), (x - a))

        self.mouseangle = angle - FOV / 2
        cangle = math.radians(FOV / RAYCOUNT)
        for j in range(0, RAYCOUNT):
            angle = cangle * j
            u = 1000 * math.cos(angle)
            v = 1000 * math.sin(angle)
            self.rays.append(Ray((0,0), (u, v)))
    
    def draw(self, depth = 1):
        
        (x, y) = self.loc
        (a, b) = pygame.mouse.get_pos()

        angle = math.atan2((y - b), (x - a))

        self.mouseangle = angle - FOV / 2

        if depth == 0:
            return
        for i in range(0, RAYCOUNT):
            r = self.rays[i]
            angle = i * currangle + self.mouseangle 
            r.draw(self.walls, self.objects, self.loc, angle, depth)

        # Get the distance of each ray and render on the right side

        offset = (SWIDTH / 2 + 1)
        width = ((SWIDTH / 2) / RAYCOUNT)
        half = SHEIGHT / 2

        for i in range(0, RAYCOUNT):
            ray = self.rays[i]
            (x, y) = ray.start
            (a, b) = ray.end

            dx = x - a
            dy = y - b
            dist = math.sqrt(dx * dx + dy * dy)

            q = 0
            if int(dist) != 0:
                q = SHEIGHT / 2 * (FOV / int(dist))

            height = max(0,  SHEIGHT / 2 - q )
            alpha = min(255, dist)
            color = ((255 - alpha, 255 - alpha, 255 - alpha))

            pygame.draw.rect(screen, color, (offset + i * width, SHEIGHT - height ,width, 2 * height - SHEIGHT ))

# Objects are drawn only when light shines on them.

class Object:
    def __init__(self, loc):
        self.loc = loc
    
    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), self.loc, 10)


# Rays is a class which contains information about the ray of light drawn emanating from a point

class Ray: 
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def draw(self, walls, objects,  mouse, angle, depth = 5):

        if depth == 0:
            return 

        self.end = (10000 * math.cos(angle), 10000 * math.sin(angle))
        refangle = 0 
        altered = False

        # distnaces array will help in rendering the view

        # Draw rays
        for w in walls:
            (x1, y1) = mouse
            (x2, y2) = self.end
            (x3, y3) = w.start
            (x4, y4) = w.end 
            denum = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

            # Determine if parallel
            if denum == 0:
                continue

            # Determine via determinants if the rays intersect 
            else: 
                t = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
                u = -1 *( (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3) )

                t/=denum 
                u/=denum
                
                #If rays intersect then the endpoint must be found along the wall, otherwise, the ray extends to infinity.
                if 0 <= t <= 1 and 0 <= u <= 1: 
                    x2prime = x3 + u * x4 -  u * x3 
                    y2prime = y3 + u * y4 - u * y3
                    self.end = (x2prime, y2prime)
                    altered = True

        # Draw objects in sight
        for obj in objects: 
            (x1, y1) = mouse
            (x2, y2) = obj.loc

            angle = math.atan2((y2 - y1), (x2 - x1))

            if angle < 0 or angle > math.radians(FOV):
                continue

            inter = False

            # Check if the object is behind each wall using the determinant method above.
            for w in walls:
                (x3, y3) = w.start
                (x4, y4) = w.end 
                denum = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

                if denum == 0:
                    continue
                else: 
                    t = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
                    u = -1 *( (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3) )

                    t/=denum 
                    u/=denum
                    
                    # Stop when the ray from the mouse to object intersects with any wall. 
                    if  (0 <= t <= 1 and  0 <= u <= 1): 
                        inter = True
                        break

            # Only draw if the object can be seen. 
            if not inter:
                obj.draw()

        self.start = mouse
        pygame.draw.aaline(screen, yellow, self.start, self.end)


def main():
    walls = []
    rays = []
    objects = []

    # Generate a list of walls, rays, and objects
    for i in range(0, WALLCOUNT):
        x = random.randrange(0, SWIDTH / 2)
        u = random.randrange(0, SWIDTH / 2)
        v = random.randrange(0, SHEIGHT)
        y = random.randrange(0, SWIDTH / 2)
        r = random.randint(0, 1)
        if r == 0:
            walls.append(Wall((x, v), (y ,v)))
        else:
            walls.append(Wall((u,x ), (u, y)))
    walls.append(Wall((SWIDTH / 2, 0), (SWIDTH/ 2, SHEIGHT)))
    walls.append(Wall((0, 0), (SWIDTH/ 2, 0)))
    walls.append(Wall((0, 0), (0, SHEIGHT)))
    walls.append(Wall((SWIDTH / 2, SHEIGHT), (0,  SHEIGHT)))


    cangle = math.radians(FOV / RAYCOUNT)
    for j in range(0, RAYCOUNT):
        angle = cangle * j
        u = 1000 * math.cos(angle)
        v = 1000 * math.sin(angle)
        rays.append(Ray((0,0), (u, v)))

    # Make objects
    for j in range(0, 10):
        x = random.randrange(0, SWIDTH / 2)
        y = random.randrange(0,SHEIGHT)
        objects.append(Object((x,y)))

    # Make point
    point = Point((100, 100), walls, objects)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                (x, y) = point.loc
                if e.key == pygame.K_w:
                    y -= 10
                if e.key == pygame.K_a:
                    x -= 10
                if e.key == pygame.K_s:
                    y += 10
                if e.key == pygame.K_d:
                    x += 10
                point.loc = (x, y)
    
        screen.fill((0, 0, 0))
        # Draw all walls
        for wall in walls:
            wall.draw()

        # Draw mouse pointer

        point.draw()
        
        pygame.display.flip()





main()