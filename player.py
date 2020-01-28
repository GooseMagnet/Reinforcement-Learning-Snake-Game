from training import *

env = game.Game()

if __name__ == '__main__':
    score_requirement = 250
    min_games = 100

    training_data, len_scores = play_random_games(10000, score_requirement)
    while len_scores < min_games:
        training_data_new, scores = play_random_games(10000, score_requirement)
        training_data += training_data_new
        len_scores += scores

    trained_model = train_model(training_data)
    generation = 0
    # play_using_model(trained_model, 50)
    trained_model.save("models/generation" + str(generation) + ".h5")

    score_requirement = 3000

    while True:
        generation += 1
        score_requirement += 250

        print('Generation:', generation)

        generation_data, gen_scores = train_generation(trained_model, 1000, score_requirement)
        while gen_scores < min_games:
            generation_data_new, new_scores = train_generation(trained_model, 1000, score_requirement)
            generation_data += generation_data_new
            gen_scores += new_scores

        training_data = generation_data

        print('generation: ', generation, ' initial population: ', len(training_data))

        model = train_model(training_data)

        trained_model = model
        model.save("models/generation" + str(generation) + ".h5")

# if __name__ == '__main__':
#     play_as_human(5, (400, 400))
