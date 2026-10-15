"""Punto de entrada: ejecuta la Práctica 02 completa.

Uso:
    python main.py            # guarda gráficas en outputs/figures
    python main.py --show     # además las muestra en pantalla
"""
import argparse

import matplotlib
import numpy as np

from data.datos import DATOS
from simulacion.config import DIR_RESULTADOS, parametros_por_defecto
from simulacion.models import (
    modelo_deterministico,
    modelo_discreto,
    modelo_estocastico,
    modelo_continuo_euler,
)
from simulacion.analysis import barrido_r, barrido_sigma, barrido_dt, corridas_estocasticas
from simulacion.analysis.metrics import tabla_comparativa, resumen_rmse
from simulacion.visualization import (
    grafica_comparativa,
    grafica_influencia_r,
    grafica_influencia_sigma,
    grafica_corridas,
    grafica_error_dt,
)


def main(mostrar: bool):
    if not mostrar:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    p = parametros_por_defecto(DATOS)
    print(f"Parámetros: P0={p.p0}, r={p.r:.4f}, sigma={p.sigma}, dt={p.dt}, tiempo={p.tiempo}")

    # 1) Cuatro modelos
    det = modelo_deterministico(p.p0, p.r, p.tiempo)
    dis = modelo_discreto(p.p0, p.r, p.tiempo)
    est = modelo_estocastico(p.p0, p.r, p.sigma, p.tiempo, p.semilla)
    con = modelo_continuo_euler(p.p0, p.r, p.tiempo, p.dt)
    grafica_comparativa(DATOS, det, dis, est, con)

    # 2) Tabla y errores
    df = tabla_comparativa(DATOS, p)
    print("\nTabla comparativa:\n", df.to_string(index=False))
    print("\nRMSE vs datos:\n", resumen_rmse(df).to_string())
    df.to_csv(DIR_RESULTADOS / "tabla_comparativa.csv", index=False)

    # 3) Influencia de r (incluye decrecimiento)
    grafica_influencia_r(barrido_r(p, [-0.10, 0.0, p.r / 2, p.r, p.r * 1.5]))

    # 4) Influencia de sigma y de la aleatoriedad
    grafica_influencia_sigma(barrido_sigma(p, [0, 30, 100, 250]), det)
    t, corridas = corridas_estocasticas(p)
    grafica_corridas(t, corridas, (det[0], det[1]))

    # 5) Función de dt
    grafica_error_dt(barrido_dt(p, [1, 0.5, 0.25, 0.1, 0.05, 0.01]))

    print(f"\nGráficas guardadas en {DIR_RESULTADOS / 'figures'}")
    if mostrar:
        plt.show()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true", help="mostrar las gráficas")
    main(ap.parse_args().show)
