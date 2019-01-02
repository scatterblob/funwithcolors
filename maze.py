#!/usr/local/bin/python3
import random
import sys
import time

import numpy as np
import pygame

np.set_printoptions(threshold=np.nan)


class Maze:

    def __init__(self):
        print("Initialize Maze...")
        self.width = 79
        self.height = 59
        self.map = np.zeros((self.height, self.width), dtype=np.uint8)
        self.laststep = [1, 1]
        self.active = []
        self.loop_points = []

    def neighbors_free(self, x, y):

        count = 0
        edge = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.map[i, j] == 1:
                    edge += 1
                if self.map[i, j] == 2:
                    count += 1
        print("Neighbor Check:\t{}\t{}\tOccupied: {}\tEdge: {}".format(x, y, count, edge))
        if count > 2:
            return False
        return True

    def walk(self, nx, ny, step=1):
        print("Walking...")

        free = list()
        up = self.map[nx - step, ny]
        print("up\t{}".format(up))
        if up == 0 and self.neighbors_free(nx - step, ny):
            free.append((nx - step, ny))
        down = self.map[nx + step, ny]
        print("down\t{}".format(down))
        if down == 0 and self.neighbors_free(nx + step, ny):
            free.append((nx + step, ny))
        left = self.map[nx, ny - step]
        print("left\t{}".format(left))
        if left == 0 and self.neighbors_free(nx, ny - step):
            free.append((nx, ny - step))
        right = self.map[nx, ny + step]
        print("right\t{}".format(right))
        if right == 0 and self.neighbors_free(nx, ny + step):
            free.append((nx, ny + step))

        if len(free) == 0:
            print("Der Weg ist versperrt")
            return None
        c = random.choice(free)
        print("chose{}".format(c))
        return c

    def clean_track(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.map[j, i] > 2:
                    self.map[j, i] = 2

    def is_corner(self, y, x):
        # print('Corner:\t{}\t{}'.format(x, y))
        left = self.map[x-1, y]
        right = self.map[x+1, y]
        up = self.map[x, y-1]
        down = self.map[x, y+1]

        # print(left, right, up, down)

        if left == right or up == down:
            return False
        return True

    def create_loop(self):
        print("Create Loop...")
        print(self.map)
        point = self.loop_points.pop(0)
        x = point[1]
        y = point[0]
        direction = point[2].pop(0)
        print(point, direction)
        x_op = 0
        y_op = 0
        if "y" in direction:
            x_op = 1 if self.map[x, y+1] == 0 else -1
            y_op = 1 if "+" in direction else -1
        if "x" in direction:
            y_op = 1 if self.map[x+1, y] == 0 else -1
            x_op = 1 if "+" in direction else -1

        print(x_op, y_op)

        if "y" in direction:
            self.map[y, x + x_op] = 5
            self.map[y, x + (2 * x_op)] = 5
            self.map[y + (2 * y_op), x + x_op] = 5
            self.map[y + (2 * y_op), x + (2 * x_op)] = 5
            self.map[y + y_op, x + (2 * x_op)] = 5
            self.map[y + y_op, x] = 0

    def is_loop_point(self, y, x):
        if x < 3 or y < 3 or y > self.height-4 or x > self.width-4:
            return list()

        if self.is_corner(x, y):
            self.map[y, x] = 4
        else:
            return list()

        possible = list()
        for i in range(x - 3, x):
            if not self.map[y, i] in range(2, 5):
                break
            if i == x - 1:
                possible.append("x-")

        for i in range(y - 3, y):
            if not self.map[i, x]in range(2, 5):
                break
            if i == y - 1:
                possible.append("y-")

        for i in range(x+1, x+4):
            if not self.map[y, i] in range(2, 5):
                break
            if i == x + 3:
                possible.append("x+")

        for i in range(y, y+4):
            if not self.map[i, x] in range(2, 5):
                break
            if i == y + 3:
                possible.append("y+")

        return possible

    def get_loop_points(self):
        self.loop_points = list()
        print("get Loop-points...")
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.map[y, x] in range(2, 5):
                    directions = self.is_loop_point(y, x)
                    if len(directions) > 0:
                        self.loop_points.append([y, x, directions])
                        self.map[y, x] = 3

    def random_double_euler_track(self, x1, y1, x2, y2):
        print('Euler Track...')
        xnow, ynow = x1, y1
        while xnow < x2-1 or ynow < y2-1:
            self.map[xnow, ynow] = 2
            if x2-1 > xnow and y2-1 > ynow:
                if random.randint(0, 1):
                    self.map[xnow+1, ynow] = 2
                    xnow += 2
                    continue
                else:
                    self.map[xnow, ynow+1] = 2
                    ynow += 2
                    continue
            if xnow < x2-1:
                self.map[xnow + 1, ynow] = 2
                xnow += 2
            if ynow < y2-1:
                self.map[xnow, ynow + 1] = 2
                ynow += 2

    def create_simple_path(self, x1, y1, x2, y2):
        for i in range(x1, x2 + 1):
            self.map[i, y1] = 2
        for j in range(y1, y2):
            self.map[x2, j] = 2

    def add_points(self, n):
        for i in range(n):
            x, y = random.choice(range(2, 57, 2)), random.choice(range(2, 77, 2))
            self.map[x, y] = 1
            self.active.append((x, y))

    def create_track_step(self, x, y):
        print('create Step...')
        nx, ny = self.walk(x, y)

        self.map[nx, ny] = 2
        self.laststep = [nx, ny]


class Player:
    x = 1
    y = 1

    def update_position(self, x, y):
        self.x += x
        self.y += y


class App:
    windowWidth = 790
    windowHeight = 590

    def __init__(self):
        print('Initializing App...')
        self._running = True
        self.surface = None
        self.screen = None
        self.array = None
        self.maze = None
        self.active = None
        self.player = Player()

    def on_init(self):
        print('ON Init...')
        pygame.init()
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self.array = np.zeros((self.windowWidth, self.windowHeight, 3), dtype=np.uint8)

        pygame.display.set_caption('Maze')
        self._running = True
        self.maze = Maze()

    def get_array(self):
        print("Creating Array...")
        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                for xx in range(10):
                    for yy in range(10):
                        if self.maze.map[y, x] == 0:
                            self.array[10 * x + xx, 10 * y + yy] = (0, 0, 0)
                            continue
                        if self.maze.map[y, x] == 1:
                            self.array[10 * x + xx, 10 * y + yy] = (255, 255, 255)
                            continue
                        if self.maze.map[y, x] == 2:
                            self.array[10 * x + xx, 10 * y + yy] = (255, 0, 0)
                            continue
                        if self.maze.map[y, x] == 3:
                            self.array[10 * x + xx, 10 * y + yy] = (255, 255, 0)
                            continue
                        if self.maze.map[y, x] == 4:
                            self.array[10 * x + xx, 10 * y + yy] = (0, 0, 255)
                            continue
                        else:
                            print(self.maze.map[10 * x + xx, 10 * y + yy])
        print("finished")

    def update_surface(self):
        print('Updating Surface...')
        self.surface = pygame.surfarray.make_surface(self.array)

    def update_screen(self):
        self.get_array()
        self.update_surface()
        pygame.image.save(self.surface, "./img/{}.jpeg".format(time.time()))
        print("blitting...")
        self.screen.blit(self.surface, (0, 0))
        print('flipping...')
        pygame.display.flip()

    def on_loop(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def bfs_step(self):
        for (a, b) in self.maze.active:
            x, y = self.maze.walk(a, b)
            self.maze.map[x, y] = 1
            self.maze.active.append((x, y))

    def create_map(self):
        print("creating map...")
        self.maze.map[0] = 1
        self.maze.map[-1] = 1
        self.maze.map[:, 0] = 1
        self.maze.map[:, -1] = 1
        self.maze.map[1, 1] = 2
        self.maze.map[self.maze.height - 2, self.maze.width - 2] = 2

        self.maze.random_double_euler_track(1, 1, self.maze.height - 2, self.maze.width - 2)
        self.maze.get_loop_points()
        self.update_screen()

        # self.maze.add_points(1)

        for i in range(1):
            self.maze.create_loop()
            self.maze.clean_track()
            self.maze.get_loop_points()
            self.update_screen()

        # for i in range(500):
        #     self.bfs_step()
        #     if i % 10 == 0:
        #         self.update_screen()

        # for i in range(500):
        #     self.maze.create_track_step(self.maze.laststep[0], self.maze.laststep[1])
        #     if i % 2 == 0:
        #         self.update_screen()

    def on_execute(self):
        self.on_init()
        self.create_map()
        while self._running:
            print(self.maze.map)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False

            print('Updating Screen...')
            self.update_screen()

        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
