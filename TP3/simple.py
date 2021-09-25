import random
import unittest
import numpy as np
from numpy import genfromtxt
import plotly.express as px
import pandas as pd

def perceptron_simple_lineal_single_input(training_set_name, X: np.ndarray, Y: np.ndarray, n=0.1, cota=10, plot=False):
    # Agregamos columna de unos (1)
    P, N = X.shape
    X = np.c_[X, np.ones(P)]  # add a column
    i = 0
    w = np.zeros(N + 1)
    w_min = None
    error = 1
    error_min = float("inf")
    errors = []
    while error > 0 and i < cota:
        errors.append(error_min)
        i_x = random.randint(0, P - 1)
        o = X[i_x].dot(w)
        dw = n * (Y[i_x] - o) * X[i_x]
        w = w + dw
        error = 0.5 * np.power(Y - X.dot(w), 2).sum()
        if error < error_min:
            error_min = error
            w_min = w
        i += 1
    print(training_set_name, i, error_min, error, w_min)
    if plot:
        fig = px.line(pd.DataFrame(errors, index=range(1, i+1)), log_x=True)
        fig.update_layout(title=f"Perceptron Simple lineal. Training set: {training_set_name}, n={n}")
        fig.update_xaxes(title="Iteraciones")
        fig.update_yaxes(title="Min Error")
        fig.show()
    return w_min, error_min

def perceptron_simple_lineal_multiple_input(training_set_name, X: np.ndarray, Y: np.ndarray, n=0.1, cota=10, plot=False):
    # Agregamos columna de unos (1)
    P, N = X.shape
    X = np.c_[X, np.ones(P)]  # add a column
    i = 0
    w = np.zeros(N + 1)
    w_min = None
    error = 1
    error_min = float("inf")
    errors = []
    while error > 0 and i < cota:
        errors.append(error_min)
        o = X.dot(w)
        dw = n * (Y - o).dot(X)
        w = w + dw
        error = 0.5 * np.power(Y - X.dot(w), 2).sum()
        if error < error_min:
            error_min = error
            w_min = w
        i += 1
    print(training_set_name, i, error_min, error, w_min)
    if plot:
        fig = px.line(pd.DataFrame(errors, index=range(1, i+1)), log_x=True)
        fig.update_layout(title=f"Perceptron Simple lineal. Training set: {training_set_name}, n={n}")
        fig.update_xaxes(title="Iteraciones")
        fig.update_yaxes(title="Mínimo Error cuadrado")
        fig.show()
    return w_min, error_min

def perceptron_simple_act(training_set_name, X: np.ndarray, Y: np.ndarray, n=0.1, cota=10, plot=False):
    def error_func(w):
        return np.absolute(Y - np.sign(X.dot(w))).sum()

    # Agregamos columna de unos (1)
    P, N = X.shape
    X = np.c_[X, np.ones(P)]  # add a column
    i = 0
    w = np.zeros(N + 1)
    w_min = None
    error = 1
    error_min = P * 2
    errors = []
    while error > 0 and i < cota:
        errors.append(error_min)
        i_x = random.randint(0, P - 1)
        h = X[i_x].dot(w)
        o = 1 if h >= 0 else -1
        dw = n * (Y[i_x] - o) * X[i_x]
        w = w + dw
        error = error_func(w)
        if error < error_min:
            error_min = error
            w_min = w
        i += 1
    print(training_set_name, i, error_min, error, w_min)
    if plot:
        fig = px.line(pd.DataFrame(errors, index=range(1, i+1)), log_x=True)
        fig.update_layout(title=f"Perceptron Simple lineal. Training set: {training_set_name}, n={n}")
        fig.update_xaxes(title="Iteraciones")
        fig.update_yaxes(title="Min Error")
        fig.show()
    return w_min, error_min

    #    w = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)

class TestStringCalculator(unittest.TestCase):
    X_XOR = np.array([
        [-1, 1],
        [1, -1],
        [-1, -1],
        [1, 1]
    ])
    Y_XOR = np.array([1, 1, -1, -1])

    X_AND = np.array([
        [-1, 1],
        [1, -1],
        [-1, -1],
        [1, 1]
    ])
    Y_AND = np.array([-1, -1, -1, 1])

    X_FILE = genfromtxt('files/input_ej_2.txt', delimiter=',')
    Y_FILE = genfromtxt('files/output_ej_2.txt', delimiter=',')
    def test_PSA_AND_returns_error_0(self):
        w, e = perceptron_simple_act("AND", self.X_AND, self.Y_AND, cota=10000)
        expected_w = np.array([1, 1, -1])
        self.assertEqual(0, e)
        self.assertTrue((expected_w == np.sign(w)).all())

    def test_PSA_XOR_returns_error_not_0(self):
        w, e = perceptron_simple_act("XOR", self.X_XOR, self.Y_XOR, cota=10000)
        expected_w = np.array([1, 1, -1])
        self.assertNotEqual(0, e)
        self.assertFalse((expected_w == np.sign(w)).all())

    def test_PSL_single_input_AND_returns_error_not_0(self):
        w, e = perceptron_simple_lineal_single_input("AND", self.X_AND, self.Y_AND, cota=10000)
        self.assertNotEqual(0, e)

    def test_PSL_single_input_FILE_returns_expected_w(self):
        w, e = perceptron_simple_lineal_single_input("File", self.X_FILE, self.Y_FILE, cota=100000, n=0.0001, plot=True)
        P, _ = self.X_FILE.shape
        X = np.c_[self.X_FILE, np.ones(P)]  # add a column
        expected_w = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(self.Y_FILE)
        self.assertTrue(np.isclose(expected_w, w).all())

    def test_PSL_multiple_input_FILE_returns_expected_w(self):
        w, e = perceptron_simple_lineal_multiple_input("File", self.X_FILE, self.Y_FILE, cota=100000, n=0.0001, plot=True)
        P, _ = self.X_FILE.shape
        X = np.c_[self.X_FILE, np.ones(P)]  # add a column
        expected_w = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(self.Y_FILE)
        self.assertTrue(np.isclose(expected_w, w).all())

