"""Parámetros centralizados de la simulación."""
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

from data.datos import DATOS

RAIZ = Path(__file__).resolve().parent.parent
DIR_FIGURAS = RAIZ / "outputs" / "figures"
DIR_RESULTADOS = RAIZ / "outputs"


@dataclass(frozen=True)
class Parametros:
    p0: float          # población inicial
    r: float           # tasa de crecimiento
    sigma: float       # desviación estándar del ruido (modelo estocástico)
    dt: float          # tamaño del paso de Euler (modelo continuo)
    tiempo: int        # tiempo total / número de períodos
    semilla: int = 42  # semilla para reproducibilidad
    n_corridas: int = 30  # corridas para analizar la aleatoriedad

    def con(self, **cambios) -> "Parametros":
        """Copia con algunos parámetros modificados."""
        return replace(self, **cambios)


def estimar_r(datos=DATOS) -> float:
    """Estima r (continua) ajustando ln(P) = ln(P0) + r*t por mínimos cuadrados."""
    t = np.arange(len(datos))
    return float(np.polyfit(t, np.log(datos), 1)[0])


def parametros_por_defecto(datos=DATOS) -> Parametros:
    """Parámetros derivados del arreglo de datos de la guía."""
    return Parametros(
        p0=float(datos[0]),
        r=estimar_r(datos),
        sigma=30.0,
        dt=0.1,
        tiempo=len(datos) - 1,
    )
