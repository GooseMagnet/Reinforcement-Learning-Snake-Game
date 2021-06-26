from training import *
from keras.models import load_model

if __name__ == '__main__':
    trained_model = load_model("models/generation2.h5")
    play_using_model(trained_model, 10)