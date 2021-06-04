#Chain should
#Create a dictionary of all words
# Store all words which follow that word and their likelihood
# build a markov chain based on a randomly picked initial word
import numpy as numpy
import random as random
SentenceLength = random.randint(5,15)

def build_chain(array, chain={}):
    for text in array:
        words = text.split(' ')
        index = 1
        for word in words[index:]:
            key = words[index - 1]
            if key in chain:
                chain[key].append(word)
            else:
                chain[key] = [word]
            index += 1
    return chain
# this fixed it don't worry keep coding.
#go over what this does with me tuesday I have no idea what it's doing
# it will return the thing u asked for. i'll explain tuesday.

def generate_message(chain, count=100):
    word1 = random.choice(list(chain.keys()))
    message = word1.capitalize()

    while len(message.split(' ')) < count:
        word2 = random.choice(chain[word1])
        word1 = word2
        message += ' ' + word2

    return message