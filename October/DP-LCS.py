
# Program to compute the longest common subsequence via a Dynamic Programming approach.

import pygame
import sys
import random
import copy
from time import sleep

# Initialize pygame
pygame.init()
(SWIDTH, SHEIGHT) = (800, 600)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

NUMBERS = 200



# Draw function
def draw(numarray, sequence,  swap1 = NUMBERS + 20, swap2 = NUMBERS + 30, orientation = 1):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
    ulength = SWIDTH / NUMBERS
    uheight = SHEIGHT / NUMBERS
    for i in range(0, len(numarray)):
        color = white
        if i == swap1 and swap1 <= NUMBERS:
            color = green
        if i == swap2 and swap2 <= NUMBERS:
            color = red

        # Sequence doesnt store indices, rather values
        if numarray[i] in sequence:
            color = blue
        num = numarray[i]

        if orientation == 1:
            pygame.draw.rect(screen, color, (ulength * i, SHEIGHT / 2 - num * uheight / 2,ulength,  num * uheight / 2) )

        else:
            pygame.draw.rect(screen, color, (ulength * i, SHEIGHT ,ulength, -num * uheight / 2) )


# The following function implements a DP approach to finding the LCS
def lcs(first, second):
    lenfirst = len(first)
    lensecond = len(second)

    memotable = [[0 for i in range(0, lenfirst + 1)] for j in range(0, lensecond + 1)]
    sequence1 = []
    sequence2 = []

    for i in range(1, len(second)):
        for j in range(1, len(first)):
            if first[j] == second[i]:
                memotable[i][j] = memotable[i - 1][j - 1] + 1
            else:
                memotable[i][j] = max(memotable[i- 1][j], memotable[i][j - 1])

        sequence1 = []
        sequence2 = []

        k = j
        l = i
        
        while k != 0 and l != 0:
            if first[k] == second[l]:
                sequence1.append(first[k])
                sequence2.append(second[l])
                k -= 1
                l -= 1

            elif memotable[l][k - 1] > memotable[l - 1][k]:     k -= 1
            else:   l -= 1


        screen.fill((0, 0, 0))
        draw(first, sequence1, i , orientation= 1)
        draw(second, sequence2, i, orientation= -1)
        pygame.display.flip()

    screen.fill((0, 0, 0))
    draw(first, sequence1, orientation= 1)
    draw(second, sequence2, orientation= -1)
    pygame.display.flip()

        
        

def main():
    firstarray = [ i for i in range(1, NUMBERS) ] 
    secondarray = [ i for i in range(1, NUMBERS)]

    random.shuffle(firstarray)
    random.shuffle(secondarray)
    play = False 
    looped = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                play = True

        # Draw the shuffled board . Start with calculating the unit length and height
        if not play:
            screen.fill((0, 0, 0))
            draw(firstarray, [], orientation= 1)
            draw(secondarray, [], orientation= -1)
            pygame.display.flip()

        elif play and not looped: 
            looped = True
            lcs(firstarray, secondarray)


        pygame.display.flip()

main()
