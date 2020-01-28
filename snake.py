import pygame
from random import randrange
from config import *

class Snake:
    def __init__(self, size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        self.rectangles = [None]
        # self.x = size[0] / SQUARE_DISTANCE
        # self.y = size[1] / SQUARE_DISTANCE

        self.x = randrange(SCREEN_WIDTH / SQUARE_DISTANCE) * SQUARE_DISTANCE
        self.y = randrange(SCREEN_HEIGHT / SQUARE_DISTANCE) * SQUARE_DISTANCE

        # 0 = Right
        # 1 = Left
        # 2 = Up
        # 3 = Down
        self.direction = 0

        self.moved = False
        self.moves = 0
        self.time_alive = 0
        self.moves_since_last_food = 0
        self.reward = 0

        for i in range(len(self.rectangles)):
            self.rectangles[i] = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)
            self.x -= SQUARE_DISTANCE

    def adjust_snake(self):
        for i in range(len(self.rectangles)-1, 0, -1):
            self.rectangles[i] = self.rectangles[i-1].copy()

    def change_direction_to(self, direction):
        if self.moved is True:
            if direction == 0 and not self.direction == 1:
                self.direction = 0
            if direction == 1 and not self.direction == 0:
                self.direction = 1
            if direction == 2 and not self.direction == 3:
                self.direction = 2
            if direction == 3 and not self.direction == 2:
                self.direction = 3
        self.moved = False

    def move_snake(self):
        self.adjust_snake()

        if self.direction == 0:
            self.rectangles[0].move_ip(SQUARE_DISTANCE, 0)
        elif self.direction == 1:
            self.rectangles[0].move_ip(-SQUARE_DISTANCE, 0)
        elif self.direction == 2:
            self.rectangles[0].move_ip(0, -SQUARE_DISTANCE)
        elif self.direction == 3:
            self.rectangles[0].move_ip(0, SQUARE_DISTANCE)
        self.moved = True
        self.moves += 1

        return self.direction

    def grow_snake(self):
        self.rectangles.insert(-1, self.rectangles[-1].copy())
