import numpy as np
from numpy import genfromtxt

_X_AUX = genfromtxt('files/ej3.txt', delimiter='').astype(int)
X = np.array(np.array_split(_X_AUX.flatten(), 10))
Y = np.array(list(range(10)))

X2 = np.c_[X, np.ones(X.shape[0])]