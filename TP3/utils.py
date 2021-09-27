import numpy as np

identity = lambda x: x

tanh = lambda x: np.tanh(x*2)
tanh_prima = lambda h: 1- np.power(tanh(h), 2)

sigmoid = lambda h: 1/(1 + np.exp(-h))
sigmoid_prima = lambda h: np.dot(h, 1-h)

def minmaxnormalization(arr: np.array):
    new_arr = []
    if len(arr.shape) == 1:
        if arr.max() - arr.min() == 0:
            return arr.copy()
        return -1 + (arr - arr.min()) * 2 / (arr.max() - arr.min())

    for i in range(arr.shape[1]):
        col = arr[:, i]
        if col.max() - col.min() == 0:
            n_col = col
        else:
            n_col = -1 + (col - col.min()) * 2 / (col.max() - col.min())
        new_arr.append(n_col)
    return np.column_stack(new_arr)


def deminmaxnormalization(original: np.array, results: np.array):
    return (results + 1) * (original.max() - original.min()) / 2 + original.min()


