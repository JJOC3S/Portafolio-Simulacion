"""
Modelo:  I = peso_h * H + peso_n * N + peso_t * Tf
  H  = humedad normalizada      (humedad % / 100)
  N  = nubosidad normalizada    (nubosidad % / 100)
  Tf = factor de temperatura    (tabla de la guía)
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Parametros:
    """Los parámetros (pesos) del modelo. Cambiarlos = ajustar el modelo."""
    nombre: str
    peso_h: float
    peso_n: float
    peso_t: float


# Modelo original de la guía y modelo ajustado
ORIGINAL = Parametros("Original", 0.5, 0.3, 0.2)
AJUSTADO = Parametros("Ajustado", 0.3, 0.6, 0.1)


@dataclass(frozen=True)
class Resultado:
    """Una fila de la tabla."""
    hora: str
    humedad: int
    nubosidad: int
    temp: int
    h: float
    n: float
    tf: float
    indice: float
    estado: str


def factor_temperatura(temp):
    """
    baja 0.05 por cada grado y funciona para mayores  temperaturas
    para menores de 10°C se mantiene en 0.5 y el mínimo es 0.1 
    """
    tf = 1.0 - 0.05 * (temp - 10)
    return round(min(1.0, max(0.1, tf)), 2)


def clasificar(indice):
    """da el estado """
    if indice < 0.40:
        return "Sin lluvia"
    if indice < 0.60:
        return "Baja posibilidad"
    if indice < 0.75:
        return "Lluvia probable"
    return "Lluvia"


def calcular(hora, humedad, nubosidad, temp, p):
    """calcula fila de la tabla"""
    h = humedad / 100
    n = nubosidad / 100
    tf = factor_temperatura(temp)
    indice = round(p.peso_h * h + p.peso_n * n + p.peso_t * tf, 4)
    return Resultado(hora, humedad, nubosidad, temp, h, n, tf, indice, clasificar(indice))


def simular(datos, p):
    """Aplica el modelo a toda la lista de datos """
    return [calcular(hora, hum, nub, temp, p) for hora, hum, nub, temp in datos]
