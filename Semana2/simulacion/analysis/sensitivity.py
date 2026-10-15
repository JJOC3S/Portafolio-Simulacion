"""Análisis del efecto de r, sigma, dt y de la aleatoriedad."""
import numpy as np

from simulacion.models import (
    modelo_deterministico,
    modelo_discreto,
    modelo_estocastico,
    modelo_continuo_euler,
)


def barrido_r(params, valores_r):
    """Curvas determinísticas para varios r (incluye r<0: decrecimiento)."""
    return {
        r: modelo_deterministico(params.p0, r, params.tiempo)
        for r in valores_r
    }


def barrido_sigma(params, valores_sigma):
    """Una trayectoria estocástica por cada sigma."""
    return {
        s: modelo_estocastico(params.p0, params.r, s, params.tiempo, params.semilla)
        for s in valores_sigma
    }


def corridas_estocasticas(params):
    """Matriz (n_corridas x períodos+1) de trayectorias estocásticas."""
    corridas = []
    for i in range(params.n_corridas):
        t, p = modelo_estocastico(params.p0, params.r, params.sigma, params.tiempo, params.semilla + i)
        corridas.append(p)
    return t, np.array(corridas)


def barrido_dt(params, valores_dt):
    """Error de Euler en t final respecto de la solución exacta, para varios dt."""
    exacto = params.p0 * np.exp(params.r * params.tiempo)
    resultados = {}
    for dt in valores_dt:
        _, p = modelo_continuo_euler(params.p0, params.r, params.tiempo, dt)
        resultados[dt] = abs(p[-1] - exacto)
    return resultados
