#!/usr/local/bin/python3
import numpy as np
import pygame
import random
from PIL import Image
import socket



##############
# Init       #
##############

h, w, size = 780, 1200, 12
start_x, start_y = int((w - size) / 2), int((h - size) / 2)
end_x, end_y = int((w + size) / 2), int((h + size) / 2)
color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
N, M = 0, 10
dir_x, dir_y = 1, 0

###################
# Connection      #
###################


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("151.217.40.82", 1234)
    sock.connect(server_address)
    return sock


def send_request(sock, msg, response=False):
    sock.sendall(msg.encode())
    return sock.recv(16) if response else msg


def send_mass_request(array):
    array = get_formatted_pixels(array, 100, 100)
    msg = ''.join(array)
    print(msg)
    print(send_request(s, msg, True))


def send_pixel(x, y, c):
    send_request(s, 'PX {} {} {}\n'.format(x, y, c))


def get_formatted_pixels(pic, offset_x, offset_y):
    formatted = list()
    for p in pic:
        formatted.append('PX {} {} {}\n'.format(p[0] + offset_x, p[1] + offset_y, p[2]))
    return formatted


def create_screen(width, height):
    pygame.init()
    sc = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Wenn deine Alte chillen will")
    cl = pygame.time.Clock()
    return sc, cl


def load_image(filename):
    return np.asarray(Image.open(filename))


def create_array():
    return np.zeros((w, h, 3), dtype=np.uint8)


def change_direction(x, y):
    if x != 0:
        x = 0
        y = -1 if random.randint(0, 1) else 1
        return x, y
    if y != 0:
        y = 0
        x = -1 if random.randint(0, 1) else 1
        return x, y


def change_color(c):
    for value in range(0, 3):
        c[value] = max(min(c[value] + 5 if random.randint(0, 1) else c[value] - 5, 255), 0)
    return c


def update(frame=None):
    global color
    if frame is None:
        frame = create_array()
    color = change_color(color)
    frame, m = draw(frame)
    return frame, m


def draw(frame):
    global start_x, start_y, end_x, end_y
    print(start_x, end_x, start_y, end_y)
    m = ""
    start_x = (start_x + dir_x) % w
    start_y = (start_y + dir_y) % h
    end_x = (end_x + dir_x) % w
    end_y = (end_y + dir_y) % h
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            frame[x % w, y % h] = color
            m = m + 'PX {} {} {}\n'.format(x, y, ('%02x%02x%02x' % tuple(color)))
    return frame, m


###################
# Script          #
###################

# s = connect()
screen, clock = create_screen(w, h)


done = False

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        # Get a numpy array to display from the simulation
        if N == 0:
            npimage, message = update()
            # send_request(s, message)
        else:
            npimage, message = update(npimage)
            # send_request(s, message)
        # Convert to a surface and splat onto screen offset by border width and height
        surface = pygame.surfarray.make_surface(npimage)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        N = N + 1

        if N % M == 0:
            dir_x, dir_y = change_direction(dir_x, dir_y)
            M = random.randint(10, 200)

        clock.tick(60)
