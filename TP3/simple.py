import math
import multiprocessing
import random
import unittest
from itertools import repeat

import numpy as np
from numpy import genfromtxt
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

from TP3.utils import deminmaxnormalization, identity
import ej2

class Perceptron:
    def __init__(self, training_set_name, X: np.ndarray, Y: np.ndarray, n, cota, G=None, G_prima=None):
        self.training_set_name = training_set_name
        self.X = X
        self.Y = Y
        self.n = n
        self.cota = cota
        if G is None:
            self.G = identity
            self.G_prima = identity
        else:
            self.G = G
            self.G_prima = G_prima
        self.error = None
        self.w = None
        self.errors = []
        self.iterations = None

    def train(self):
        P, N = self.X.shape
        i = 0
        w = np.random.random(N)
        w_min = None
        error = 1
        error_min = float("inf")
        G = self.G
        G_prima = self.G_prima
        X = self.X
        Y = self.Y
        n = self.n
        while error > 0 and i < self.cota:
            self.errors.append(error_min)
            i_x = random.randint(0, P - 1)
            o = G(X[i_x].dot(w))
            dw = n * (Y[i_x] - o) * G_prima(X[i_x].dot(w)) * X[i_x]
            w = w + dw
            error = 0.5 * np.power(Y - G(X.dot(w)), 2).sum()
            if error < error_min:
                error_min = error
                w_min = w
            i += 1

        self.w = w_min
        self.error = error_min
        self.iterations = i


def perceptron_simple_no_lineal_single_input(training_set_name, X: np.ndarray, Y: np.ndarray, n=0.1, cota=10,
                                             plot=False):
    P, N = X.shape
    i = 0
    w = np.zeros(N)
    w_min = None
    error = 1
    error_min = float("inf")
    errors = []
    G = np.tanh
    G_prima = lambda h: (1 - G(h) ** 2)
    while error > 0 and i < cota:
        errors.append(error_min)
        i_x = random.randint(0, P - 1)
        o = G(X[i_x].dot(w))
        dw = n * (Y[i_x] - o) * G_prima(X[i_x].dot(w)) * X[i_x]
        w = w + dw
        error = 0.5 * np.power(Y - G(X.dot(w)), 2).sum()
        if error < error_min:
            error_min = error
            w_min = w
        i += 1
    print(training_set_name, i, error_min, error, w_min)
    if plot:
        fig = px.line(pd.DataFrame(errors, index=range(1, i + 1)), log_x=True)
        fig.update_layout(title=f"Perceptron Simple lineal. Training set: {training_set_name}, n={n}")
        fig.update_xaxes(title="Iteraciones")
        fig.update_yaxes(title="Min Error")
        fig.show()
    return w_min, error_min


def perceptron_simple_lineal_single_input(training_set_name, X: np.ndarray, Y: np.ndarray, n=0.1, cota=10, plot=False):
    P, N = X.shape
    i = 0
    w = np.zeros(N)
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
        fig = px.line(pd.DataFrame(errors, index=range(1, i + 1)), log_x=True)
        fig.update_layout(title=f"Perceptron Simple lineal. Training set: {training_set_name}, n={n}")
        fig.update_xaxes(title="Iteraciones")
        fig.update_yaxes(title="Min Error")
        fig.show()
    return w_min, error_min


def perceptron_simple_lineal_multiple_input(training_set_name, X: np.ndarray, Y: np.ndarray, n=0.1, cota=10,
                                            plot=False):
    P, N = X.shape
    i = 0
    w = np.zeros(N)
    w_min = None
    error = 1
    error_min = float("inf")
    errors = []
    while error > 0 and i < cota:
        errors.append(error_min)
        o = np.inner(X, w)
        dw = n * (Y - o).dot(X)
        w = w + dw
        error = 0.5 * np.power(Y - np.inner(X, w), 2).sum()
        if error < error_min:
            error_min = error
            w_min = w
        i += 1
    print(training_set_name, i, error_min, error, w_min)
    if plot:
        fig = px.line(pd.DataFrame(errors, index=range(1, i + 1)), log_x=True)
        fig.update_layout(title=f"Perceptron Simple lineal. Training set: {training_set_name}, n={n}")
        fig.update_xaxes(title="Iteraciones")
        fig.update_yaxes(title="Mínimo Error cuadrado")
        fig.show()
    return w_min, error_min


def perceptron_simple_act(training_set_name, X: np.ndarray, Y: np.ndarray, n=0.1, cota=10, plot=False):
    def error_func(w):
        return np.absolute(Y - np.sign(X.dot(w))).sum()

    P, N = X.shape
    i = 0
    w = np.zeros(N)
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
        fig = px.line(pd.DataFrame(errors, index=range(1, i + 1)), log_x=True)
        fig.update_layout(title=f"Perceptron Simple lineal. Training set: {training_set_name}, n={n}")
        fig.update_xaxes(title="Iteraciones")
        fig.update_yaxes(title="Min Error")
        fig.show()
    return w_min, error_min

    #    w = np.linalg.inv(X.T.dX_FILE(X)).dot(X.T).dot(Y)



if __name__ == '__main__':
    squares = np.power(ej2.Y_FILE - ej2.Y_FILE.mean(), 2).sum()
    def Perceptron_Simple_lineal(n):
        p = Perceptron("File", X=ej2.X_FILE, Y=ej2.Y_FILE, n=n, cota=1000)
        p.train()
        o = ej2.X_FILE.dot(p.w)
        residuals = np.power(ej2.Y_FILE - o, 2).sum()
        return 1 - (residuals/squares) # https://en.wikipedia.org/wiki/Coefficient_of_determination

    def Perceptron_Simple_no_lineal(n):
        G = np.tanh
        G_prima = lambda h: 1 - G(h) ** 2
        p = Perceptron("File", X=ej2.X_N_FILE, Y=ej2.Y_N_FILE, n=n, cota=1000, G=G, G_prima=G_prima)
        p.train()
        o = ej2.X_N_FILE.dot(p.w)
        n_o = deminmaxnormalization(ej2.Y_FILE, o)
        residuals = np.power(ej2.Y_FILE - n_o, 2).sum()
        # np.abs(ej2.Y_FILE - n_o).sum() / len(n_o)
        return 1 - (residuals / squares)


    def Perceptron_Simple_no_lineal_cross(args):
        n, training_X, training_Y, test_X, test_Y = args
        G = np.tanh
        G_prima = lambda h: 1 - G(h) ** 2
        p = Perceptron("File", X=training_X, Y=training_Y, n=n, cota=1000, G=G, G_prima=G_prima)
        p.train()
        # training residual
        o = training_X.dot(p.w)
        n_o = deminmaxnormalization(training_Y, o)
        residuals = np.power(training_Y - n_o, 2).sum()
        squares = np.power(training_Y - training_Y.mean(), 2).sum()
        training_err = 1 - (residuals / squares)
        # test residual
        o = test_X.dot(p.w)
        n_o = deminmaxnormalization(test_Y, o)
        residuals = np.power(test_Y - n_o, 2).sum()
        squares = np.power(test_Y - test_Y.mean(), 2).sum()
        test_err = 1 - (residuals / squares)
        return training_err, test_err

    def simple_graph(x, y, title):
        fig = px.line(x=x, y=y)
        fig.update_layout(title=title, font=dict(size=22))
        fig.update_xaxes(title="Tasa de aprendizaje", type="log")
        fig.update_yaxes(title="Coeficiente de determinación")
        fig.show()


    p = "PSL time"
    pool = multiprocessing.Pool()
    if p == "PSL":
        ns = np.linspace(0.00001, 1, 10000, endpoint=True)
        title="PSL R² en función de n"
        results = pool.map(Perceptron_Simple_lineal, ns)
        simple_graph(ns, results, title)
    elif p == "PSNL":
        ns = np.linspace(0.00001, 1, 10000, endpoint=True)
        title="PSNL: R² en función de n"
        results = pool.map(Perceptron_Simple_no_lineal, ns)
        simple_graph(ns, results, title)
    elif p == "PSL time":
        n = 0.000001
        p = Perceptron("File", X=ej2.X_FILE, Y=ej2.Y_FILE, n=n, cota=10000)
        p.train()
        fig = px.line(x=range(p.iterations), y=p.errors)
        fig.update_layout(title=f"PSL error en función de iteraciones, n={n}", font=dict(size=22))
        fig.update_xaxes(title="Iteraciones")
        fig.update_yaxes(title="Suma de error cuadrado")
        fig.show()
    elif p =="PSNL cross":
        ns = np.linspace(0.0001, 0.5, 1000, endpoint=True)
        t_pcts = {0.01:"red", 0.1:"", 0.5:"", 0.9:"blue"}
        # t_pcts = {0.1:"red", 0.9:"blue"}
        fig = go.Figure()
        title = f"PSNL: R² en función de n. Cross validation"
        for t_pct, color in t_pcts.items():
            training_len = int(ej2.X_N_FILE.shape[0] * t_pct)
            training_X = ej2.X_N_FILE[0:training_len]
            training_Y = ej2.Y_N_FILE[0:training_len]

            test_X = ej2.X_N_FILE[training_len:]
            test_Y = ej2.Y_N_FILE[training_len:]

            resp = pool.map(Perceptron_Simple_no_lineal_cross, zip(ns, repeat(training_X), repeat(training_Y), repeat(test_X), repeat(test_Y)))

            training_e, test_e = zip(*resp)
            # fig.add_trace(go.Scatter(x=ns, y=training_e, name=f"Training {t_pct}", line=dict(color=color, dash='dash')))
            fig.add_trace(go.Scatter(x=ns, y=test_e, name=f"Test {round(1-t_pct, 2)}"))#, line=dict(color=color)))

        fig.update_layout(title=title, font=dict(size=22))
        fig.update_xaxes(title="Tasa de aprendizaje", type="log")
        fig.update_yaxes(title="Coeficiente de determinación")
        fig.show()
