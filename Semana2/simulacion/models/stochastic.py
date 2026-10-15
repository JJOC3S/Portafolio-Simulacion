import numpy as np


def modelo_estocastico(p0, r, sigma, tiempo, semilla=None):
    """P(t+1) = P(t) + r P(t) + eps, con eps ~ N(0, sigma^2). Devuelve (t, P).

    La población nunca baja de 0.
    """
    rng = np.random.default_rng(semilla)
    poblacion = [p0]
    for _ in range(1, int(tiempo) + 1):
        actual = poblacion[-1]
        ruido = rng.normal(0.0, sigma)
        nueva = actual + r * actual + ruido
        poblacion.append(max(nueva, 0.0))
    return np.arange(int(tiempo) + 1), np.array(poblacion)
