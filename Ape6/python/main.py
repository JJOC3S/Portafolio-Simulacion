"""Práctica 06 - Validación estadística de números pseudoaleatorios (Python).

Ejecutar desde la raíz del proyecto:   python python/main.py
"""
import csv
import os
import sys
import time

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graficas  # noqa: E402
from lcg import generar  # noqa: E402
from pruebas import ALFA, chi_cuadrado, kolmogorov_smirnov  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(RAIZ, "resultados")

N_BASE = 10_000
K = 10

# Configuraciones del generador (nombre, semilla, a, c, m)
CONFIGS = [
    ("A: Numerical Recipes (Práctica 05)", 12345, 1664525, 1013904223, 2**32),
    ("B: glibc (a=1103515245)", 12345, 1103515245, 12345, 2**31),
    ("C: RANDU (a=65539, c=0)", 1, 65539, 0, 2**31),
    ("D: Degenerado (a=1, c=1)", 12345, 1, 1, 2**32),
]
TAMANOS = [1_000, 10_000, 100_000, 1_000_000]


def ejecutar(n, semilla, a, c, m):
    """Genera n números y aplica ambas pruebas. Devuelve (u, chi, ks, ms)."""
    t0 = time.perf_counter()
    _, u = generar(n, semilla, a, c, m)
    chi = chi_cuadrado(u, K)
    ks = kolmogorov_smirnov(u)
    ms = (time.perf_counter() - t0) * 1000.0
    return u, chi, ks, ms


def mejor_tiempo(n, cfg, repeticiones=3):
    return min(ejecutar(n, *cfg[1:])[3] for _ in range(repeticiones))


def main():
    os.makedirs(RES, exist_ok=True)
    filas_csv = []

    # ---- Secuencia de la configuración A (para compararla con Java) ----
    nombre_a, semilla, a, c, m = CONFIGS[0]
    enteros, u = generar(N_BASE, semilla, a, c, m)
    with open(os.path.join(RES, "secuencia_python.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["indice", "X", "U"])
        for i in range(N_BASE):
            w.writerow([i + 1, int(enteros[i]), f"{u[i]:.12f}"])
    print("Primeros 10 números (config A):", ", ".join(f"{v:.6f}" for v in u[:10]))

    # ---- Experimento 1: comparación de configuraciones (N = 10 000) ----
    print(f"\n=== Configuraciones del generador (N={N_BASE}, k={K}, alfa={ALFA}) ===")
    print(f"{'Configuración':<38}{'chi2':>9}{'p(chi2)':>10}{'D':>10}{'p(KS)':>10}  Decisión")
    datos_hist, datos_ks = [], []
    for cfg in CONFIGS:
        u, chi, ks, ms = ejecutar(N_BASE, *cfg[1:])
        tiempo = mejor_tiempo(N_BASE, cfg)
        print(f"{cfg[0]:<38}{chi['chi2']:>9.3f}{chi['p']:>10.4f}{ks['D']:>10.5f}{ks['p']:>10.4f}"
              f"  χ²: {chi['decision']} | KS: {ks['decision']}")
        datos_hist.append((cfg[0], u, chi))
        datos_ks.append((cfg[0], u, ks))
        filas_csv.append({
            "experimento": "configuraciones", "configuracion": cfg[0].split(":")[0], "N": N_BASE,
            "chi2": chi["chi2"], "gl": chi["gl"], "p_chi2": chi["p"],
            "decision_chi2": chi["decision"], "D": ks["D"], "p_ks": ks["p"],
            "decision_ks": ks["decision"], "tiempo_ms": tiempo,
        })
        if cfg is CONFIGS[0]:
            print("\nFrecuencias observadas (config A):", chi["observadas"].tolist(),
                  "| esperada:", chi["esperada"])
            print("Verificación con scipy -> chi2:",
                  round(float(stats.chisquare(chi["observadas"]).statistic), 6),
                  "| KS D:", round(float(stats.kstest(u, "uniform").statistic), 6), "\n")

    graficas.histogramas(datos_hist, os.path.join(RES, "histogramas.png"), K)
    graficas.ecdf_ks(datos_ks, os.path.join(RES, "ks_ecdf.png"))

    # ---- Experimento 2: tamaño de muestra y tiempos (config A) ----
    print(f"\n=== Config A: efecto del tamaño N y tiempos ===")
    print(f"{'N':>10}{'chi2':>10}{'p(chi2)':>10}{'D':>10}{'p(KS)':>10}{'t Python (ms)':>16}")
    filas_t = []
    for n in TAMANOS:
        u, chi, ks, _ = ejecutar(n, *CONFIGS[0][1:])
        tiempo = mejor_tiempo(n, CONFIGS[0])
        print(f"{n:>10}{chi['chi2']:>10.3f}{chi['p']:>10.4f}{ks['D']:>10.5f}{ks['p']:>10.4f}{tiempo:>16.2f}")
        filas_t.append((n, tiempo))
        filas_csv.append({
            "experimento": "tamanos", "configuracion": "A", "N": n,
            "chi2": chi["chi2"], "gl": chi["gl"], "p_chi2": chi["p"],
            "decision_chi2": chi["decision"], "D": ks["D"], "p_ks": ks["p"],
            "decision_ks": ks["decision"], "tiempo_ms": tiempo,
        })

    campos = ["experimento", "configuracion", "N", "chi2", "gl", "p_chi2", "decision_chi2",
              "D", "p_ks", "decision_ks", "tiempo_ms"]
    with open(os.path.join(RES, "resultados_python.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas_csv)

    # Gráfica de tiempos (incluye Java si ya existe su CSV)
    t_java = {}
    ruta_java = os.path.join(RES, "resultados_java.csv")
    if os.path.exists(ruta_java):
        with open(ruta_java) as f:
            for fila in csv.DictReader(f):
                if fila["experimento"] == "tamanos":
                    t_java[int(fila["N"])] = float(fila["tiempo_ms"])
    graficas.tiempos([(n, t, t_java.get(n)) for n, t in filas_t],
                     os.path.join(RES, "tiempos.png"))
    print(f"\nResultados guardados en: {RES}")


if __name__ == "__main__":
    main()
