import numpy as np


def modelo_continuo_euler(p0, r, tiempo, dt):
    """dP/dt = rP aproximado con Euler: P(t+dt) = P(t) + dt * r * P(t). Devuelve (t, P)."""
    n_pasos = int(round(tiempo / dt))
    t = np.arange(n_pasos + 1) * dt
    poblacion = [p0]
    for _ in range(n_pasos):
        actual = poblacion[-1]
        cambio = r * actual
        poblacion.append(actual + dt * cambio)
    return t, np.array(poblacion)
