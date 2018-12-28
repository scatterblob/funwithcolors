#!/usr/local/bin/python3
import numpy as np
import pygame
import random
from PIL import Image

h, w = 800, 800
border = 0
N = 0
leFrame = None


def create_random_image():
    data = np.zeros((w, h, 3), dtype=np.uint8)
    for x in range(0, w):
        for y in range(0, h):
            for color in range(3):
                data[x, y, color] = random.randint(0, 255)
    return data


start_x = 0


def sort_vertical(a, color=0):
    global start_x
    for y in range(0, h):
        min_index = start_x
        mi = 255
        for x in range(start_x, w):
            if a[x, y, color] < mi:
                mi = a[x, y, color]
                min_index = x
        a[min_index, y, color], a[start_x, y, color] = a[start_x, y, color], a[min_index, y, color]
    return a


start_y = 0


def sort_horizontal(a, color=1):
    global start_y
    for x in range(0, w):
        min_index = start_y
        mi = 255
        for y in range(start_y, h):
            if a[x, y, color] < mi:
                mi = a[x, y, color]
                min_index = y
        a[x, min_index, color], a[x, start_y, color] = a[x, start_y, color], a[x, min_index, color]
    return a


def get_frame():
    global leFrame, start_x, start_y
    hor, vert = False, False
    if leFrame is None:
        leFrame = create_random_image()
    if not vert:
        try:
            leFrame = sort_vertical(leFrame)
        except IndexError:
            vert = True
    if not hor:
        try:
            leFrame = sort_horizontal(leFrame)
        except IndexError:
            hor = True

    start_x = start_x + 1 if start_x < w else start_x
    start_y = start_y + 1 if start_y < h else start_y
    return leFrame


pygame.init()
screen = pygame.display.set_mode((w+(2*border), h+(2*border)))
pygame.display.set_caption("Loooool die Drugs")
done = False
clock = pygame.time.Clock()


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        # Clear screen to white before drawing
        screen.fill((255, 255, 255))

        # Get a numpy array to display from the simulation
        npimage = get_frame()

        # Convert to a surface and splat onto screen offset by border width and height
        surface = pygame.surfarray.make_surface(npimage)
        screen.blit(surface, (border, border))

        N = N + 1

        pygame.display.flip()
        clock.tick(30)
