"""Métricas para comparar los modelos con los datos observados."""
import numpy as np
import pandas as pd

from simulacion.models import (
    modelo_deterministico,
    modelo_discreto,
    modelo_estocastico,
    modelo_continuo_euler,
)


def error_rmse(observado, simulado) -> float:
    observado, simulado = np.asarray(observado), np.asarray(simulado)
    return float(np.sqrt(np.mean((observado - simulado) ** 2)))


def tabla_comparativa(datos, params) -> pd.DataFrame:
    """Evalúa cada modelo en los instantes enteros y calcula el RMSE vs datos."""
    t_ent = np.arange(len(datos))
    _, p_det = modelo_deterministico(params.p0, params.r, params.tiempo, puntos=len(datos))
    _, p_dis = modelo_discreto(params.p0, params.r, params.tiempo)
    _, p_est = modelo_estocastico(params.p0, params.r, params.sigma, params.tiempo, params.semilla)
    t_c, p_con = modelo_continuo_euler(params.p0, params.r, params.tiempo, params.dt)
    p_con_ent = np.interp(t_ent, t_c, p_con)

    df = pd.DataFrame(
        {
            "t": t_ent,
            "Datos": datos,
            "Determinístico": p_det,
            "Discreto": p_dis,
            "Estocástico": p_est,
            "Continuo (Euler)": p_con_ent,
        }
    ).round(2)
    return df


def resumen_rmse(df: pd.DataFrame) -> pd.Series:
    modelos = [c for c in df.columns if c not in ("t", "Datos")]
    return pd.Series({m: error_rmse(df["Datos"], df[m]) for m in modelos}).round(2)
