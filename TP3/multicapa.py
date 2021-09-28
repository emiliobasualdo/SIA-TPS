import random

import numpy as np

import ej2
from TP3 import ej3
from TP3.utils import identity, sigmoid, sigmoid_prima, tanh, tanh_prima
import plotly.express as px
import plotly.graph_objs as go

class Multilayer_perceptron:
    def __init__(self, X, Y, n, hidden_layers, cota, e_error, G=identity, G_prima=identity, momentum_alpha=0.):
        self.X = X
        self.Y = Y
        self.L = 1 if len(Y.shape) == 1 else Y.shape[1]
        self.P, self.N = X.shape
        self.weights = []
        self.layers_conf = [self.N] + hidden_layers + [self.L]
        for i in range(len(self.layers_conf)):
            if i == 0: continue
            W_m = np.random.uniform(size=(self.layers_conf[i], self.layers_conf[i-1]), low=-1, high=1)
            self.weights.append(W_m)
        self.n = n
        self.cota = cota
        self.e_error = e_error
        self.G = G
        self.G_prima = G_prima
        self.momentum_alpha = momentum_alpha

    def train(self):
        error = float("inf")
        i = 0
        errors = []
        last_hs = [0] * self.P
        momentum_dw = [np.zeros(m.shape) for m in reversed(self.weights)]
        while error > self.e_error and i < self.cota:
            i+=1
            i_x = random.randint(0, self.P - 1)
            V_0 = self.X[i_x]
            # Propagar la entrada hasta a capa de salida
            V_m = V_0
            h_V_m = [(V_m, V_m)]
            for W_m in self.weights:
                V_m_1 = V_m
                # W_m * V_m_1 = V_M
                # 3x5  *  5x1  = 3x1
                h_m = W_m.dot(V_m_1)
                V_m = self.G(h_m)
                #assert V_m.shape[0] == W_m.shape[0]
                h_V_m.append((h_m, V_m))
            # Calcular δ para la capa de salida
            # G'(h_m)    * (Y_u - V_m) = δ
            # capa[-1]x1 *     1xL       = capa[-1]xL
            # 1x1* 1x1 = 1x1
            h_m, V_m = h_V_m.pop()
            D_m = np.dot(self.G_prima(h_m), self.Y[i_x] - V_m)
            # guardo el V_m para el historial
            last_hs[i_x] = h_m
            # Retropropagar δM
            for j, W_m in enumerate(reversed(self.weights)):
                h_m_1, V_m_1 = h_V_m.pop()
                D_m_1 = np.multiply(self.G_prima(h_m_1), np.dot(D_m, W_m))
                #  Actualizar los pesos de las conexiones de acuerdo
                dw = self.n * np.dot(D_m.T, np.array([V_m_1]))
                W_m += dw + self.momentum_alpha * momentum_dw[j]
                # gaurdamos el cambio para le momentum
                momentum_dw[j] = dw
                D_m = D_m_1

            # calculamos el error
            if i % self.L == 0:
                error = 0.5 * np.power(np.array([self.Y]).T - last_hs, 2).mean()
                errors.append(float(error))

        self.last_hs = last_hs
        self.errors = errors
        self.error = error
        self.i = i
        self.converged = i < self.cota

    def eval(self, X):
        def _eval(x):
            V_m = x
            for W_m in self.weights:
                V_m_1 = V_m
                h_m = W_m.dot(V_m_1)
                V_m = self.G(h_m)
            return V_m
        return np.apply_along_axis(_eval, axis=1, arr=X).flatten()

def multi_XOR():
    hidden_layers = [3]
    n = 0.03
    cota = 4000
    fig = go.Figure()
    sum_err = 0
    k = 3
    momentum_alpha = 0.2
    for i in range(k):
        m = Multilayer_perceptron(ej2.X_XOR_2, ej2.Y_XOR, n=n, hidden_layers=hidden_layers, cota=cota, e_error=0.04, G=tanh, G_prima=tanh_prima, momentum_alpha=momentum_alpha)
        m.train()
        fig.add_trace(go.Scatter(x=list(range(m.i)), y=m.errors))
        sum_err += m.error
        # print(m.eval(ej2.X_XOR_2), ej2.Y_XOR)
        # print(m.last_hs, ej2.Y_XOR)
        # print("converged", m.converged, m.error)
    fig.update_layout(title=f"Multilayer XOR n={n}, cota={cota} mean_err={round(sum_err/k,5)} hidden_l={hidden_layers}, alpha={momentum_alpha}", font=dict(size=22))
    fig.update_xaxes(title="Iteraciones")
    fig.update_yaxes(title="Error cuadrado medio")
    fig.show()

def multi_parity_error():
    hidden_layers_opts =[
        [10],
        [10,10],
        [10,10, 10]
    ]
    n = 0.03
    cota = 5000
    fig = go.Figure()
    momentum_alpha = 0.5
    for hidden_layers in hidden_layers_opts:
        m = Multilayer_perceptron(ej3.X2, ej3.Y, n=n, hidden_layers=hidden_layers, cota=cota, e_error=0.04, G=tanh, G_prima=tanh_prima, momentum_alpha=momentum_alpha)
        m.train()
        fig.add_trace(go.Scatter(x=list(range(m.i)), y=m.errors, name=str(hidden_layers)))
    fig.update_layout(
        title=f"Multilayer binary n={n}, cota={cota}, alpha={momentum_alpha}",
        font=dict(size=22))
    fig.update_xaxes(title="Iteraciones")
    fig.update_yaxes(title="Error cuadrado medio")
    fig.show()


def binary_accuracy(predictions, observations):
    prediction_error = (np.sign(predictions) - observations) == 0
    certainty = np.abs(predictions[prediction_error]).sum()
    return certainty/ len(observations)

def multi_parity_accuracy():
    cota = 5000
    hidden_layers = [3]
    training_pct = 0.8
    #n = 0.03
    MS = [0.001, 0.01, 0.05, 0.1, 0.3, 0.5]
    momentum_alpha = 0.3
    fig = go.Figure()
    test_acc = []
    training_acc = []
    for n in MS:
        training_set_len = int(ej3.X2.shape[0] * training_pct)
        training_set_X = ej3.X2[0:training_set_len,:]
        training_set_Y = ej3.Y[0:training_set_len]
        testing_set_X = ej3.X2[training_set_len:,:]
        testing_set_Y = ej3.Y[training_set_len:]
        m = Multilayer_perceptron(training_set_X, training_set_Y, n=n, hidden_layers=hidden_layers, cota=cota,
                                  e_error=0.04, G=tanh, G_prima=tanh_prima, momentum_alpha=momentum_alpha)
        m.train()
        test_acc.append(binary_accuracy(m.eval(testing_set_X), testing_set_Y))
        training_acc.append(binary_accuracy(m.eval(training_set_X), training_set_Y))

    MS_STR = [str(m) for m in MS]
    fig.add_trace(go.Bar(x=MS_STR, y=test_acc, name="test"))
    fig.add_trace(go.Bar(x=MS_STR, y=training_acc, name="training"))
    fig.update_layout(title=f"Multilayer binary momentum={momentum_alpha}, cota={cota}, t_pct={training_pct}, hidden_l={hidden_layers}",font=dict(size=22))
    fig.update_xaxes(title="Tasa de aprendizaje")
    fig.update_yaxes(title="Accuracy")
    fig.show()

if __name__ == '__main__':
    # multi_XOR()
    # multi_parity_error()
    multi_parity_accuracy()