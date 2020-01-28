from training import *

if __name__ == '__main__':
    trained_model = load_model("models/generation6.h5")
    play_using_model(trained_model, 20)