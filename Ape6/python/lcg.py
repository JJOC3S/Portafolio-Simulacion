"""Actividad 1: Generador Congruencial Lineal (LCG).

    X_{n+1} = (a * X_n + c) mod m        U_n = X_{n+1} / m

La semilla X_0 NO se incluye en la secuencia: el primer valor devuelto es X_1.
Es exactamente el mismo algoritmo que implementa java/src/Lcg.java.
"""
import numpy as np


def generar(n, semilla, a, c, m):
    """Devuelve (enteros X_1..X_n, uniformes U_1..U_n en [0,1))."""
    xs = [0] * n
    x = semilla
    for i in range(n):
        x = (a * x + c) % m
        xs[i] = x
    enteros = np.array(xs, dtype=np.int64)
    uniformes = enteros / float(m)
    return enteros, uniformes
