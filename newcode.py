# Thinking about refactoring this to use an autoencoder
# probably a little overkill but could be interesting
from keras.layers import Dense,Conv2D,MaxPooling2D,UpSampling2D
from keras import Input, Model
from keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt
