import game
import pygame
import random
import numpy
import time

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

env = game.Game()


def play_random_games(initial_games=100000, score_requirement=5):
    start_time = time.time()

    training_data = []
    accepted_scores = []
    all_scores = []
    apples_eaten = []

    for game_index in range(initial_games):
        env.reset(False)

        score = 0

        game_memory = []
        previous_observation = []

        while not env.lost:
            action = random.randrange(0, 4)
            if action == 0:
                env.snake.change_direction_to(0)
            elif action == 1:
                env.snake.change_direction_to(1)
            elif action == 2:
                env.snake.change_direction_to(2)
            elif action == 3:
                env.snake.change_direction_to(3)

            observation, action, reward = env.play()

            score += reward

            if len(previous_observation) > 0:
                game_memory.append([previous_observation, action])

            previous_observation = observation

        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                action_sample = [0, 0, 0, 0]
                action_sample[data[1]] = 1
                training_data.append([data[0], action_sample])
            apples_eaten.append(env.score)

        all_scores.append(score)

    print('Average Score:', str(sum(all_scores) / len(all_scores)))
    print('Highest Reward:', max(all_scores))
    if len(apples_eaten) > 0: print('Highest Score:', max(apples_eaten))
    print('Elapsed Time:', str(time.time() - start_time))

    print(accepted_scores)

    return training_data, len(accepted_scores), max(all_scores)


def play_using_model(trained_model, games=1, size=None):
    scores = []
    choices = []
    for each_game in range(games):
        score = 0
        prev_obs = []
        apples_eaten = []

        env.reset(True) if size is None else env.reset(True, size)

        while not env.lost:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    env.lost = True
            if len(prev_obs) == 0:
                action = random.randrange(0, 4)
            else:
                num = numpy.argmax(trained_model.predict(numpy.array(prev_obs)))
                action = num

            # 0 = Right
            # 1 = Left
            # 2 = Up
            # 3 = Down

            if action == 0:
                env.snake.change_direction_to(0)
            elif action == 1:
                env.snake.change_direction_to(1)
            elif action == 2:
                env.snake.change_direction_to(2)
            elif action == 3:
                env.snake.change_direction_to(3)

            observation, action, reward = env.play()

            choices.append(action)

            prev_obs = [observation]
            score += reward

        scores.append(score)
        apples_eaten.append(env.score)

    print(scores)
    print('Average Score:', sum(scores) / len(scores))
    print('Highest Reward:', max(scores))
    if len(apples_eaten) > 0: print('Highest Score:', max(apples_eaten))

    pygame.quit()


def train_generation(trained_model, initial_games=100000, score_requirement=5):
    start_time = time.time()

    training_data = []
    accepted_scores = []
    all_scores = []
    apples_eaten = []

    for game_index in range(initial_games):
        env.reset(False)

        score = 0

        game_memory = []
        prev_obs = []

        while not env.lost:
            if len(prev_obs) == 0:
                action = random.randrange(0, 4)
            else:
                num = numpy.argmax(trained_model.predict(numpy.array(prev_obs).reshape(1, len(prev_obs))))
                action = num

            # 0 = Right
            # 1 = Left
            # 2 = Up
            # 3 = Down

            if action == 0:
                env.snake.change_direction_to(0)
            elif action == 1:
                env.snake.change_direction_to(1)
            elif action == 2:
                env.snake.change_direction_to(2)
            elif action == 3:
                env.snake.change_direction_to(3)

            observation, action, reward = env.play()

            score += reward

            if len(prev_obs) > 0:
                game_memory.append([prev_obs, action])

            prev_obs = observation

        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                action_sample = [0, 0, 0, 0]
                action_sample[data[1]] = 1
                training_data.append([data[0], action_sample])

        apples_eaten.append(env.score)
        all_scores.append(score)

    print('Average Score:', str(sum(all_scores) / len(all_scores)))
    print('Highest Reward:', max(all_scores))
    if len(apples_eaten) > 0: print('Highest Score:', max(apples_eaten))
    print('Elapsed Time:', str(time.time() - start_time))

    print(accepted_scores)

    return training_data, len(accepted_scores), max(apples_eaten)


def train_model(training_data):
    X = numpy.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
    y = numpy.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
    model = build_model(input_size=len(X[0]), output_size=len(y[0]))

    model.fit(X, y, epochs=10)
    return model


def build_model(input_size, output_size):
    model = Sequential()
    model.add(Dense(128, input_dim=input_size, activation='relu'))
    model.add(Dense(52, activation='relu'))
    model.add(Dense(output_size, activation='linear'))
    model.compile(loss='mse', optimizer=Adam())

    return model


def play_as_human(games=1, size=None):
    for i in range(games):
        env.reset(True) if size is None else env.reset(True, size)
        while not env.lost:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        env.snake.change_direction_to(0)
                    elif event.key == pygame.K_LEFT:
                        env.snake.change_direction_to(1)
                    elif event.key == pygame.K_UP:
                        env.snake.change_direction_to(2)
                    elif event.key == pygame.K_DOWN:
                        env.snake.change_direction_to(3)
            env.play()
