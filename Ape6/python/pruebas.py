"""Algoritmo 2 (Chi-cuadrado) y Algoritmo 3 (Kolmogorov-Smirnov) de la guía.

Hipótesis:  H0: X ~ U(0,1)   vs   H1: X no sigue U(0,1)     (alfa = 0.05)
"""
import math

import numpy as np
from scipy import stats

ALFA = 0.05


def decision(p, alfa=ALFA):
    return "No se rechaza H0" if p >= alfa else "Se rechaza H0"


def chi_cuadrado(u, k=10, alfa=ALFA):
    """Prueba Chi-cuadrado de uniformidad con k subintervalos de igual amplitud."""
    n = len(u)
    esperada = n / k
    # intervalo i = floor(u*k); el límite superior (u==1) no ocurre en un LCG
    idx = np.minimum((u * k).astype(np.int64), k - 1)
    observadas = np.bincount(idx, minlength=k)
    chi2 = float(np.sum((observadas - esperada) ** 2 / esperada))
    gl = k - 1
    p = float(stats.chi2.sf(chi2, gl))
    return {
        "observadas": observadas, "esperada": esperada,
        "chi2": chi2, "gl": gl, "p": p, "decision": decision(p, alfa),
    }


def _p_ks(d, n):
    """p-valor asintótico de Kolmogorov (con corrección de Stephens).

    Misma fórmula que java/src/PruebasEstadisticas.java para que ambos
    lenguajes den el mismo resultado.
    """
    lam = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * d
    suma, signo, previo = 0.0, 1.0, 0.0
    for k in range(1, 101):
        termino = signo * math.exp(-2.0 * k * k * lam * lam)
        suma += termino
        if abs(termino) <= 1e-10 * abs(previo) or abs(termino) <= 1e-16 * suma:
            return min(1.0, max(0.0, 2.0 * suma))
        signo = -signo
        previo = termino
    return 1.0


def kolmogorov_smirnov(u, alfa=ALFA):
    """Prueba KS contra U(0,1): D = max(D+, D-)."""
    n = len(u)
    x = np.sort(u)
    i = np.arange(1, n + 1)
    fn_sup = i / n            # F_n justo en x_(i)
    fn_inf = (i - 1) / n      # F_n justo antes de x_(i)
    f = x                     # F(x) = x para U(0,1)
    d_mas = fn_sup - f
    d_menos = f - fn_inf
    dmax_mas, dmax_menos = float(d_mas.max()), float(d_menos.max())
    d = max(dmax_mas, dmax_menos)
    p = _p_ks(d, n)
    # punto donde ocurre D (para marcarlo en la gráfica)
    if dmax_mas >= dmax_menos:
        x_d = float(x[int(d_mas.argmax())])
    else:
        x_d = float(x[int(d_menos.argmax())])
    return {
        "d_mas": dmax_mas, "d_menos": dmax_menos, "D": d, "p": p,
        "decision": decision(p, alfa), "x_d": x_d,
    }
