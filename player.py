from training import *
from multiprocessing import Pool

env = game.Game()


def firstgeneration(pool=Pool()):
    score_requirement = 200
    min_games = 10
    training_data = []
    len_scores = 0

    while len_scores < min_games:
        results = []
        for i in range(8):
            t1 = pool.apply_async(play_random_games, (1000, score_requirement))
            results.append(t1)
        for result in results:
            if (len_scores >= min_games): break
            training_data += result.get()[0]
            len_scores += result.get()[1]

    generation_0 = train_model(training_data)
    generation_0.save("models/generation0.h5")

    return generation_0


if __name__ == '__main__':

    pool = Pool()
    trained_model = firstgeneration(pool)
    min_games = 1000
    score_requirement = 0
    generation = 0
    max_all_time = 0

    while True:
        training_data = []
        len_scores = 0
        generation += 1
        score_requirement += 500

        print('Generation:' + str(generation))

        while len_scores < min_games:
            results = []
            for i in range(8):
                t1 = pool.apply_async(train_generation, (trained_model, 1000, score_requirement))
                results.append(t1)
            for result in results:
                training_data += result.get()[0]
                len_scores += result.get()[1]
                max_all_time = max(max_all_time, result.get()[2])

        print('generation: ', generation, ' initial population: ', len(training_data))

        model = train_model(training_data)
        trained_model = model
        model.save("models/generation" + str(generation) + ".h5")
