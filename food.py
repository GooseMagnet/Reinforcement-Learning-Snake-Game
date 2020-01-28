import pygame
from random import randrange
from config import *

class Food:
    def __init__(self, snake, size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        self.x = randrange(size[0] / SQUARE_DISTANCE) * SQUARE_DISTANCE
        self.y = randrange(size[1] / SQUARE_DISTANCE) * SQUARE_DISTANCE
        self.food_rectangle = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

        while (self.food_rectangle.collidelist(snake.rectangles) >= 0):
            self.x = randrange(size[0] / SQUARE_DISTANCE) * SQUARE_DISTANCE
            self.y = randrange(size[1] / SQUARE_DISTANCE) * SQUARE_DISTANCE
            self.food_rectangle = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)