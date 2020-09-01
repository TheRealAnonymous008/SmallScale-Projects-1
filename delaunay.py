# Python program to generate the delaunay triangulation of a point set via the Bowyer-Watson Algorithm.

import pygame
import random
import math
import sys
from time import sleep
from operator import attrgetter

pygame.init()
(SWIDTH, SHEIGHT) = (800, 600)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
POINTS = 500

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loc = (x, y)
        self.neighbors = []
        self.incident = []
    
    def draw(self, color = (255, 255, 255)):
        x, y = self.loc
        pygame.draw.circle(screen, color, (int(x), int(y)), 4)

class Triangle:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.edges = [(v1, v2), (v2, v3), (v3, v1)]
        self.triangleEdges = [Edge(v1, v2), Edge(v2, v3), Edge(v1, v3)]
        self.vertices = [v1, v2, v3]
    def draw(self):
        pygame.draw.aaline(screen, (255, 255, 255), self.v1.loc, self.v2.loc)
        pygame.draw.aaline(screen, (255, 255, 255), self.v2.loc, self.v3.loc)
        pygame.draw.aaline(screen, (255, 255, 255), self.v3.loc, self.v1.loc)

    def check(self, point):
        (x1, y1) = self.v1.loc
        (x2, y2) = self.v2.loc
        (x3, y3) = self.v3.loc

        # Midpt 12
        x12 = (x1 + x2) /2
        y12 = (y1 + y2) / 2

        # Midpt 23
        x23 = (x2 + x3) / 2
        y23 = (y2 + y3) / 2

            

        # Slope 12perp:
        a = 0
        if x1 -x2 != 0:
            slope = (y1 - y2) / (x1 - x2)
            if slope != 0:
                a = -1 / (slope)
            else:
                a = 10000000000
        elif x1 - x3 != 0:
            slope = (y1 - y3) / (x1 - x3)
            if slope != 0:
                a = -1 / (slope)
            else:
                a = 10000000000
            x12 = (x1 + x3 ) / 2
            y12 = (y1 + y3) / 2
        else:
            return False

        # Slope 23 perp
        b = 0
        if x2 - x3 != 0:
            slope = (y2 - y3) / (x2 - x3)
            if slope != 0:
                b = -1 / (slope)
            else:
                b = 10000000000
        else:
            slope = (y1 - y3) / (x1 - x3)
            y23 = (y1 + y3) /2
            x23 = (x1 + x3) / 2
            if slope != 0:
                b = -1 / (slope)
            else:
                b = 10000000000


        # y-int 12 
        c = y12 - a * x12
        d = y23 - b * x23
        
        if a != b:
            cx = (d- c) / (a - b)
        else:
            return False
        cy = a * cx + c
        (px, py) = point.loc

        
        dpx = px - cx
        dpy = py - cy

        dtx = x1 - cx
        dty = y1 - cy

        distpoint = dpx * dpx + dpy * dpy
        disttri = dtx * dtx + dty * dty
        
        if distpoint <= disttri:
            return True
        else:
            return False

class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        v1.neighbors.append(v2)
        v2.neighbors.append(v1)
        v1.incident.append(self)
        v2.incident.append(self)

    def draw(self, color = (255, 0, 0)):
        loc1 = self.v1.loc
        loc2 = self.v2.loc 

        pygame.draw.aaline(screen, color, loc1, loc2)


def delaunay(points):
    cx, cy  = (SWIDTH / 2, SHEIGHT / 2)
    v1 = Point(cx + SWIDTH * 2 * math.cos(math.radians(0)), cy + SHEIGHT * 2 * math.sin(math.radians(0)))
    v2 = Point(cx + SWIDTH * 2* math.cos(math.radians(120)), cy  + SHEIGHT * 2* math.sin(math.radians(120)))
    v3 = Point(cx + SWIDTH * 2 * math.cos(math.radians(240)), cy + SHEIGHT * 2* math.sin(math.radians(240)))
    superTriangle = Triangle(v1, v2, v3)

    triangulation = []
    badtriangles = []
    triangulation.append(superTriangle)

    for point in points:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
        badtriangles = []
        for triangle in triangulation:
            inside = triangle.check(point)
            # if the point is in the triangle
            if  inside:
                badtriangles.append(triangle)
        
        polygon = []
        for triangle in badtriangles:
            for edge in triangle.edges:
                isShared = False
                for other in badtriangles:
                    if other != triangle:
                        for ed in other.edges:
                            (q1, q2) = edge
                            (q3, q4) = ed

                            if (q1 == q3 and q2 == q4) or (q1 == q4 and q2 == q3):
                                isShared = True
                    if isShared:
                        break
                if isShared == False:
                    polygon.append(edge)

        print("Term")
        for triangle in badtriangles:
            triangulation.remove(triangle)
        
        for edge in polygon:
            (q1, q2) = edge
            newTriangle = Triangle(q1, q2, point)
            triangulation.append(newTriangle)

        screen.fill((0, 0, 0))
        
        for pt in points:
            pt.draw((0, 0, 0))
        point.draw((0, 255, 0))
        for tri in triangulation:
            tri.draw()
        pygame.display.flip()

    banned = []
    for triangle in triangulation:
        for vert in triangle.vertices:
            if vert in superTriangle.vertices:
                banned.append(triangle)
                break

    for triangle in banned:
        triangulation.remove(triangle)

    screen.fill((0, 0, 0))

    edges = []
    edgeSet = []
    for triangle in triangulation:
        triangle.draw()
        # Adjust all points' neighbors
        v1 = triangle.v1
        v2 = triangle.v2
        v3 = triangle.v3
        
        if (v1, v2) not in edges and (v2, v1) not in edges:
            e1 = Edge(v1, v2)
            edgeSet.append(e1)
            edges.append((v1, v2))
            
        if (v3, v2) not in edges and (v2, v3) not in edges:
            e2 = Edge(v2, v3)
            edges.append((v2, v3))
            edgeSet.append(e2)
            
        if (v1, v3) not in edges and (v3, v1) not in edges:
            e3 = Edge(v1, v3)
            edges.append((v1, v3))
            edgeSet.append(e3)

    return edgeSet

 
def main():
    points = []
    vals = []
    edges = []
    for p in range(0, POINTS):
        x = random.randrange(0, SWIDTH)
        y = random.randrange(0, SHEIGHT)

        if(x, y) not in vals:
            points.append(Point(x, y))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    points *= 0
                    vals *= 0
                    for p in range(0, POINTS):
                        x = random.randrange(0, SWIDTH)
                        y = random.randrange(0, SHEIGHT)

                        if(x, y) not in vals:
                            points.append(Point(x, y))
                    screen.fill((0, 0, 0))
                    pygame.display.flip()
                    points.sort(key = attrgetter('x'))
                    delaunay(points)
                


        pygame.display.flip()

main()