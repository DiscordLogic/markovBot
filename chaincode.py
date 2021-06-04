#Chain should
#Create a dictionary of all words
# Store all words which follow that word and their likelihood
# build a markov chain based on a randomly picked initial word
import numpy as numpy
import random as random
import markovify
SentenceLength = random.randint(5,15)


def build_chain(array):
    text = ""
    for x in array:
        text = text + x + ". "
    print("THIS IS THE CODE" + "\n\n" + text)
    text_model = markovify.Text(text)
    return text_model.make_short_sentence(320)



