# The following algorithm computes and displays the longest increasing subsequence in a list of numbers 
# Utilizing a Dynamic Programing-based approach (Time Complexity:  O(n^2), Space Complexity (O(n)))


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

NUMBERS  = 200


# Draw function
def draw(numarray, sequence, swap1 = NUMBERS + 20, swap2 = NUMBERS + 30):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))
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
        pygame.draw.rect(screen, color, (ulength * i, SHEIGHT - num * uheight,ulength, num * uheight) )
    pygame.display.flip()

def lis(numarray):
    # Dynamic programming demo on finding the longest increasing subsequence
    # Start with an array of numbers

    numbers = len(numarray)

    memoTable = [1 for i in range(0, numbers)]
    sequence = []

    for i in range(1, numbers):
        memoTable[i] = 1
        for j in range(0, i):
            sequence = []
            # DP Recurrence relation which
            if numarray[i] > numarray[j] and memoTable[i] < memoTable[j] + 1:
                memoTable[i] = memoTable[j] + 1

        # Run through the list backwards and see when the value of ctr changes. Add that to the longest increasing subsequence
        ctr = max(p for p in memoTable)
        for k in range(i, -1, -1):
            if memoTable[k] == ctr and numarray[k]:
                if len(sequence) != 0:
                    if numarray[k] > sequence[len(sequence) - 1]:
                        continue
                ctr -= 1
                sequence.append(numarray[k])

        draw(numarray, sequence, i, j)

    draw(numarray, sequence)


def main():
    numarray = [ i for i in range(1, NUMBERS) ] 

    random.shuffle(numarray)
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
            draw(numarray, [])

        elif play and not looped: 
            looped = True
            lis(numarray)


        pygame.display.flip()

main()
