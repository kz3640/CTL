import random
import pickle

import numpy as np
import pandas as pd
from nltk.tokenize import RegexpTokenizer

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Activation
from tensorflow.keras.optimizers import RMSprop


if __name__ == "__main__":
    print("loading")
    text_df = pd.read_csv("Dataset/pop_lyrics.csv")
    print("trimming to lyirics")
    text = list(text_df.lyrics.values)
    joined_text = " ".join(text)

    partial_text = joined_text[:1000000]

    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(partial_text.lower())

    tokens.remove("chorus")
    tokens.remove("verse")

    print("grabbing unique tokens")

    unique_tokens = np.unique(tokens)
    unique_token_index = {token: idx for idx, token in enumerate(unique_tokens)}

    n_words = 10
    input_words = []
    next_words = []

    print("generating training data")

    for i in range(len(tokens) - n_words):
        input_words.append(tokens[i:i+n_words])
        next_words.append(tokens[i+n_words])

    X = np.zeros((len(input_words), n_words, len(unique_tokens)), dtype=bool)
    Y = np.zeros((len(next_words), len(unique_tokens)), dtype=bool)

    for i, words in enumerate(input_words):
        for j, word in enumerate(words):
            X[i, j, unique_token_index[word]] = 1
        Y[i, unique_token_index[next_words[i]]] = 1

    print("setting model parameters")

    model = Sequential()
    model.add(LSTM(128, input_shape=(n_words, len(unique_tokens)), return_sequences = True))
    model.add(LSTM(128))
    model.add(Dense(len(unique_tokens)))
    model.add(Activation("softmax"))

    print("fitting the model")

    model.compile(loss="categorical_crossentropy", optimizer=RMSprop(learning_rate=0.01), metrics=["accuracy"])
    model.fit(X,Y, batch_size=128, epochs=10, shuffle=True)

    model.save("Models/mymodel1M.h5")


def predict_next_word(input_text, n_best):
    input_text = input_text.lower()
    X = np.zeros((1, n_words, len(unique_tokens)))
    for i, word in enumerate(input_text.split()):
        X[0, i, unique_token_index[word]] = 1

    predictions = model.predict(X)[0]
    return np.argpartition(predictions, -n_best)[-n_best:]