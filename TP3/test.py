import unittest

import numpy as np

from TP3.simple import perceptron_simple_act, perceptron_simple_lineal_single_input, \
    perceptron_simple_lineal_multiple_input
import ej2

class TestPerceptron(unittest.TestCase):

    def test_PSA_AND_returns_error_0(self):
        w, e = perceptron_simple_act("AND", ej2.X_AND, ej2.Y_AND, cota=20)
        expected_w = np.array([1, 1, -1])
        self.assertEqual(0, e)
        self.assertTrue((expected_w == np.sign(w)).all())

    def test_PSA_XOR_returns_error_not_0(self):
        w, e = perceptron_simple_act("XOR", ej2.X_XOR, ej2.Y_XOR, cota=10000)
        expected_w = np.array([1, 1, -1])
        self.assertNotEqual(0, e)
        self.assertFalse((expected_w == np.sign(w)).all())

    def test_PSL_single_input_AND_returns_error_not_0(self):
        w, e = perceptron_simple_lineal_single_input("AND", ej2.X_AND, ej2.Y_AND, cota=10000)
        self.assertNotEqual(0, e)

    def test_PSL_single_input_FILE_returns_expected_w(self):
        w, e = perceptron_simple_lineal_single_input("File", ej2.X_N_FILE, ej2.Y_N_FILE, cota=100000, n=0.1,
                                                     plot=False)
        expected_w = np.linalg.inv(ej2.X_N_FILE.T.dot(ej2.X_N_FILE)).dot(ej2.X_N_FILE.T).dot(ej2.Y_N_FILE)
        self.assertTrue(np.isclose(expected_w, w).all())

    def test_PSL_multiple_input_FILE_returns_expected_w(self):
        w, e = perceptron_simple_lineal_multiple_input("File", ej2.X_N_FILE, ej2.Y_N_FILE, cota=100000, n=0.01,
                                                       plot=False)
        expected_w = np.linalg.inv(ej2.X_N_FILE.T.dot(ej2.X_N_FILE)).dot(ej2.X_N_FILE.T).dot(ej2.Y_N_FILE)
        self.assertTrue(np.isclose(expected_w, w).all())