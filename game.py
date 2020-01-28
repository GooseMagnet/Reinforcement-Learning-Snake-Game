import pygame
import sys
import numpy
from snake import Snake
from food import Food
from config import *
from scipy.spatial import distance


class Game():
    def __init__(self):
        pygame.init

    def up_score(self):
        self.score += 1

    def reset(self, display, size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        self.lost = False
        self.snake = Snake(size)
        self.food = Food(self.snake, size)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.display = display
        self.screen = None

        self.previous_distance_to_apple = 100000

        self.width = size[0]
        self.height = size[1]

        if display:
            self.screen = pygame.display.set_mode(size)

    def draw(self, color, rectangles):
        for rec in rectangles:
            pygame.draw.rect(self.screen, color, rec)

    def render(self):
        self.draw(WHITE, self.snake.rectangles)
        self.draw(RED, [self.food.food_rectangle])
        pygame.display.update()
        self.screen.fill(pygame.Color(0, 0, 0))

        self.clock.tick(FPS)
        self.snake.time_alive += FPS

    def check_collision(self, snake, food):
        snake.moves_since_last_food += 1

        # Distance to food
        snake_pos = snake.rectangles[0].x, snake.rectangles[0].y
        food_pos = self.food.x, self.food.y
        current_distance_to_apple = distance.euclidean(snake_pos, food_pos)
        #
        if current_distance_to_apple > self.previous_distance_to_apple:
            snake.reward = -0.15
        else:
            snake.reward = 0.1

        self.previous_distance_to_apple = current_distance_to_apple
        # snake.reward = 0

        if snake.rectangles[0].x == self.width or snake.rectangles[0].x < 0:
            self.lost = True
            snake.reward = -10
        elif snake.rectangles[0].y == self.height or snake.rectangles[0].y < 0:
            self.lost = True
            snake.reward = -10
        elif snake.rectangles[0].collidelist(snake.rectangles[1:]) >= 0:
            self.lost = True
            snake.reward = -10
        elif snake.rectangles[0].colliderect(food.food_rectangle) > 0:
            self.up_score()
            snake.reward = 100
            snake.moves_since_last_food = 0
            snake.grow_snake()
            return Food(snake, (self.width, self.height))
        elif snake.moves_since_last_food >= self.width + self.height:
            self.lost = True
            snake.reward = -10

        return food

    def direction_to_apple(self):
        # 0 = Right
        # 1 = Left
        # 2 = Up
        # 3 = Down

        direction_to_apple = [0, 0, 0, 0]

        if self.snake.rectangles[0].x < self.food.x:
            direction_to_apple[0] = 1
        if self.snake.rectangles[0].x > self.food.x:
            direction_to_apple[1] = 1
        if self.snake.rectangles[0].y > self.food.y:
            direction_to_apple[2] = 1
        if self.snake.rectangles[0].y < self.food.y:
            direction_to_apple[3] = 1

        if sum(direction_to_apple) is 1:
            if self.snake.direction is 0 and direction_to_apple[1] is 1:
                direction_to_apple = [0, 0, 0, 0]
            elif self.snake.direction is 1 and direction_to_apple[0] is 1:
                direction_to_apple = [0, 0, 0, 0]
            elif self.snake.direction is 2 and direction_to_apple[3] is 1:
                direction_to_apple = [0, 0, 0, 0]
            elif self.snake.direction is 3 and direction_to_apple[2] is 1:
                direction_to_apple = [0, 0, 0, 0]

        return direction_to_apple

    def play(self):
        action = self.snake.move_snake()

        # Collision Detection
        self.food = self.check_collision(self.snake, self.food)

        # Observation & Wall Detection
        if not self.lost and self.display:
            self.render()


        if self.snake.direction is 0:
            is_left_clear = False
        else:
            is_left_clear = self.snake.rectangles[0].x - SQUARE_DISTANCE >= 0

            temp = self.snake.rectangles[0].copy()
            temp.x -= SQUARE_DISTANCE
            is_left_clear &= temp.collidelist(self.snake.rectangles) < 0

        if self.snake.direction is 1:
            is_right_clear = False
        else:
            is_right_clear = self.snake.rectangles[0].x + SQUARE_DISTANCE < SCREEN_WIDTH

            temp = self.snake.rectangles[0].copy()
            temp.x += SQUARE_DISTANCE
            is_right_clear &= temp.collidelist(self.snake.rectangles) < 0

        if self.snake.direction is 2:
            is_down_clear = False
        else:
            is_down_clear = self.snake.rectangles[0].y + SQUARE_DISTANCE < SCREEN_HEIGHT

            temp = self.snake.rectangles[0].copy()
            temp.y += SQUARE_DISTANCE
            is_down_clear &= temp.collidelist(self.snake.rectangles) < 0

        if self.snake.direction is 3:
            is_up_clear = False
        else:
            is_up_clear = self.snake.rectangles[0].y - SQUARE_DISTANCE >= 0

            temp = self.snake.rectangles[0].copy()
            temp.y -= SQUARE_DISTANCE
            is_up_clear &= temp.collidelist(self.snake.rectangles) < 0

        direction_to_apple = self.direction_to_apple()

        # return [is_left_clear, is_right_clear, is_up_clear, is_down_clear], action, self.snake.reward
        # return [is_left_clear, is_right_clear, is_up_clear, is_down_clear,
        #         direction_to_apple[0], direction_to_apple[1], direction_to_apple[2], direction_to_apple[3],
        #         self.previous_distance_to_apple], action, self.snake.reward
        # return [is_left_clear, is_right_clear, is_up_clear, is_down_clear,
        #         direction_to_apple[0], direction_to_apple[1], direction_to_apple[2], direction_to_apple[3],
        #         self.previous_distance_to_apple], action, self.snake.reward
        return [is_left_clear, is_right_clear, is_up_clear, is_down_clear,
                direction_to_apple[0], direction_to_apple[1], direction_to_apple[2],
                direction_to_apple[3]], action, self.snake.reward
