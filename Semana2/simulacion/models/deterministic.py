import numpy as np


def modelo_deterministico(p0, r, tiempo, puntos=200):
    """P(t) = P0 * e^(r t). Sin aleatoriedad. Devuelve (t, P)."""
    t = np.linspace(0, tiempo, puntos)
    return t, p0 * np.exp(r * t)
