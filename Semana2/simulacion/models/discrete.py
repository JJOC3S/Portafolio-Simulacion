import numpy as np


def modelo_discreto(p0, r, tiempo):
    """P(t+1) = P(t) + r P(t), en períodos enteros. Devuelve (t, P)."""
    poblacion = [p0]
    for _ in range(1, int(tiempo) + 1):
        actual = poblacion[-1]
        poblacion.append(actual + r * actual)
    return np.arange(int(tiempo) + 1), np.array(poblacion)
