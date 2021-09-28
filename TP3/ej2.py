import numpy as np
from numpy import genfromtxt

from TP3.utils import minmaxnormalization

X_XOR = np.array([
    [-1, 1],
    [1, -1],
    [-1, -1],
    [1, 1]
])
X_XOR_2 = np.c_[X_XOR, np.ones(4)]
Y_XOR = np.array([1, 1, -1, -1])

X_AND = np.array([
    [-1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [1, 1, 1]
])
Y_AND = np.array([-1, -1, -1, 1])

X_FILE = genfromtxt('files/training_set.txt', delimiter='')
Y_FILE = genfromtxt('files/expected_out.txt', delimiter='')
# Agregamos una columna a X
P, _ = X_FILE.shape
X_FILE = np.c_[X_FILE, np.ones(P)]

X_N_FILE = minmaxnormalization(X_FILE)
Y_N_FILE = minmaxnormalization(Y_FILE)