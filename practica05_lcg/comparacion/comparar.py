"""Compara las secuencias de Python y Java, analiza el período y las semillas.

Uso (desde la carpeta raíz del proyecto, después de generar los CSV):
    python3 comparacion/comparar.py

Genera en la carpeta resultados/ las tablas y gráficas como imágenes PNG.
"""
import csv
import os
from math import gcd

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SEMILLA_1 = 12345  # semilla de la guía
SEMILLA_2 = 54321  # semilla alternativa para el punto 7
CARPETA = "resultados"
AZUL = "#2a6fb0"
NARANJA = "#d9822b"


# ---------------------------------------------------------------- utilidades
def leer_csv(ruta):
    """Devuelve tres listas: n, x (enteros) y u (texto tal como se guardó)."""
    n, x, u = [], [], []
    with open(ruta) as f:
        lector = csv.DictReader(f)
        for fila in lector:
            n.append(int(fila["n"]))
            x.append(int(fila["x"]))
            u.append(fila["u"])
    return n, x, u


def tabla_png(titulo, columnas, filas, archivo, ancho=10, colores_col=None):
    """Dibuja una tabla y la guarda como imagen."""
    alto = 0.4 * (len(filas) + 2) + 0.8
    fig, ax = plt.subplots(figsize=(ancho, alto))
    ax.axis("off")
    ax.set_title(titulo, fontsize=13, fontweight="bold", pad=12)
    tabla = ax.table(cellText=filas, colLabels=columnas, loc="center", cellLoc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.auto_set_column_width(list(range(len(columnas))))
    tabla.scale(1, 1.4)
    for (fila, col), celda in tabla.get_celld().items():
        celda.set_edgecolor("#cccccc")
        if fila == 0:
            celda.set_facecolor("#2a6fb0")
            celda.set_text_props(color="white", fontweight="bold")
        elif fila % 2 == 0:
            celda.set_facecolor("#f2f6fa")
    fig.savefig(f"{CARPETA}/{archivo}", dpi=150, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)


def estadisticas(x, m=2 ** 32):
    u = np.array(x) / m
    return {
        "media": u.mean(),
        "varianza": u.var(),
        "minimo": u.min(),
        "maximo": u.max(),
        "corr": np.corrcoef(u[:-1], u[1:])[0, 1],
    }


# ------------------------------------------- 1) Comparación Python vs Java
def comparar_python_java():
    n, xp, up = leer_csv(f"{CARPETA}/python_semilla_{SEMILLA_1}.csv")
    _, xj, uj = leer_csv(f"{CARPETA}/java_semilla_{SEMILLA_1}.csv")

    x_iguales = sum(1 for a, b in zip(xp, xj) if a == b)
    u_iguales = sum(1 for a, b in zip(up, uj) if a == b)
    total = len(n)

    # Tabla con las primeras 20 observaciones
    filas = []
    for i in range(20):
        igual = "Sí" if xp[i] == xj[i] and up[i] == uj[i] else "No"
        filas.append([n[i], xp[i], xj[i], up[i], uj[i], igual])
    tabla_png(
        f"Primeras 20 observaciones - Python vs Java (semilla {SEMILLA_1})",
        ["n", "X Python", "X Java", "U Python", "U Java", "¿Igual?"],
        filas,
        "tabla_comparacion.png",
    )

    # Gráfica de la secuencia (10 000 valores), un panel por lenguaje
    fig, ejes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
    for eje, nombre, u, color in [(ejes[0], "Python", up, AZUL), (ejes[1], "Java", uj, NARANJA)]:
        eje.scatter(n, [float(v) for v in u], s=2, color=color)
        eje.set_title(f"Secuencia U(n) generada en {nombre}")
        eje.set_xlabel("n")
        eje.grid(alpha=0.3)
    ejes[0].set_ylabel("U(n)")
    fig.tight_layout()
    fig.savefig(f"{CARPETA}/grafica_secuencia.png", dpi=150)
    plt.close(fig)

    # Histograma de uniformidad
    fig, eje = plt.subplots(figsize=(7, 4.2))
    eje.hist([float(v) for v in up], bins=10, range=(0, 1), color=AZUL, edgecolor="white")
    eje.axhline(total / 10, color="#c0392b", linestyle="--", label="Frecuencia esperada (uniforme)")
    eje.set_title("Histograma de U(n) - 10 intervalos")
    eje.set_xlabel("U")
    eje.set_ylabel("Frecuencia")
    eje.legend()
    fig.tight_layout()
    fig.savefig(f"{CARPETA}/grafica_histograma.png", dpi=150)
    plt.close(fig)

    # Dispersión U(n) vs U(n+1): revisa si hay patrones entre valores consecutivos
    u_num = np.array([float(v) for v in up])
    fig, eje = plt.subplots(figsize=(5.5, 5.5))
    eje.scatter(u_num[:-1], u_num[1:], s=2, color=AZUL)
    eje.set_title("Dispersión U(n) vs U(n+1)")
    eje.set_xlabel("U(n)")
    eje.set_ylabel("U(n+1)")
    fig.tight_layout()
    fig.savefig(f"{CARPETA}/grafica_dispersion.png", dpi=150)
    plt.close(fig)

    return {"total": total, "x_iguales": x_iguales, "u_iguales": u_iguales, "x": xp}


# ------------------------------------------------ 2) Cambio de semilla
def comparar_semillas():
    _, x1, u1 = leer_csv(f"{CARPETA}/python_semilla_{SEMILLA_1}.csv")
    _, x2, u2 = leer_csv(f"{CARPETA}/python_semilla_{SEMILLA_2}.csv")
    _, j2, _ = leer_csv(f"{CARPETA}/java_semilla_{SEMILLA_2}.csv")

    # Tabla de las primeras 20 observaciones con ambas semillas
    filas = [[i + 1, x1[i], u1[i], x2[i], u2[i]] for i in range(20)]
    tabla_png(
        "Primeras 20 observaciones con dos semillas distintas",
        ["n", f"X (semilla {SEMILLA_1})", f"U (semilla {SEMILLA_1})",
         f"X (semilla {SEMILLA_2})", f"U (semilla {SEMILLA_2})"],
        filas,
        "tabla_semillas.png",
    )

    # Estadísticas de ambas secuencias
    e1, e2 = estadisticas(x1), estadisticas(x2)
    filas = []
    for nombre, e in [(SEMILLA_1, e1), (SEMILLA_2, e2)]:
        filas.append([nombre, f"{e['media']:.4f}", f"{e['varianza']:.4f}",
                      f"{e['minimo']:.5f}", f"{e['maximo']:.5f}", f"{e['corr']:+.4f}"])
    filas.append(["Teórico U(0,1)", "0.5000", "0.0833", "0", "1", "0"])
    tabla_png(
        "Estadísticas de 10 000 valores según la semilla",
        ["Semilla", "Media", "Varianza", "Mínimo", "Máximo", "Correlación lag 1"],
        filas,
        "tabla_estadisticas.png",
        ancho=9,
    )

    # Gráfica de los primeros 60 valores de cada semilla
    fig, eje = plt.subplots(figsize=(10, 4.2))
    k = 60
    eje.plot(range(1, k + 1), [float(v) for v in u1[:k]], "o-", color=AZUL, label=f"Semilla {SEMILLA_1}")
    eje.plot(range(1, k + 1), [float(v) for v in u2[:k]], "s-", color=NARANJA, label=f"Semilla {SEMILLA_2}")
    eje.set_title("Primeros 60 valores con dos semillas")
    eje.set_xlabel("n")
    eje.set_ylabel("U(n)")
    eje.grid(alpha=0.3)
    eje.legend()
    fig.tight_layout()
    fig.savefig(f"{CARPETA}/grafica_semillas.png", dpi=150)
    plt.close(fig)

    coincidencias = sum(1 for a, b in zip(x1, x2) if a == b)
    return {"e1": e1, "e2": e2, "coincidencias": coincidencias,
            "py_java_semilla2": sum(1 for a, b in zip(x2, j2) if a == b)}


# ------------------------------------------------------- 3) Período
def factores_primos(m):
    primos, d = set(), 2
    while d * d <= m:
        while m % d == 0:
            primos.add(d)
            m //= d
        d += 1
    if m > 1:
        primos.add(m)
    return primos


def hull_dobell(a, c, m):
    """Condiciones para que el LCG tenga período completo (= m)."""
    if gcd(c, m) != 1:
        return False
    for p in factores_primos(m):
        if (a - 1) % p != 0:
            return False
    if m % 4 == 0 and (a - 1) % 4 != 0:
        return False
    return True


def periodo_experimental(a, c, m, semilla):
    """Cuenta cuántos pasos pasan hasta que se repite un valor (solo para m pequeños)."""
    vistos = {}
    x, paso = semilla, 0
    while x not in vistos:
        vistos[x] = paso
        x = (a * x + c) % m
        paso += 1
    return paso - vistos[x]


def analizar_periodo(x_real):
    casos = [
        ("Guía (a=1664525, c=1013904223, m=2^32)", 1664525, 1013904223, 2 ** 32, SEMILLA_1),
        ("Ejemplo bueno (a=5, c=3, m=16)", 5, 3, 16, 7),
        ("Ejemplo malo (a=4, c=2, m=16)", 4, 2, 16, 7),
        ("Ejemplo malo (a=5, c=0, m=16)", 5, 0, 16, 7),
        ("Completo pero pobre (a=1, c=1, m=16)", 1, 1, 16, 0),
    ]
    filas = []
    for nombre, a, c, m, s in casos:
        cumple = hull_dobell(a, c, m)
        if m == 2 ** 32:
            ruta = f"{CARPETA}/periodo_real_java.txt"
            if os.path.exists(ruta):
                observado = f"{int(open(ruta).read().strip()):,}".replace(",", " ")
                observado += " (medido en Java)"
            else:
                observado = "sin repetidos en 10 000 valores" if len(set(x_real)) == len(x_real) else "hay repetidos"
            teorico = "4 294 967 296"
        else:
            observado = str(periodo_experimental(a, c, m, s))
            teorico = str(m) if cumple else "< m"
        filas.append([nombre, "Sí" if cumple else "No", teorico, observado])
    tabla_png(
        "Análisis del período (condiciones de Hull-Dobell)",
        ["Parámetros", "¿Cumple Hull-Dobell?", "Período teórico", "Período observado"],
        filas,
        "tabla_periodo.png",
        ancho=12,
    )
    return filas


# ------------------------------------------------------------------- main
if __name__ == "__main__":
    os.makedirs(CARPETA, exist_ok=True)

    r1 = comparar_python_java()
    print(f"Semilla {SEMILLA_1}: X iguales {r1['x_iguales']}/{r1['total']}, "
          f"U iguales {r1['u_iguales']}/{r1['total']}")

    r2 = comparar_semillas()
    print(f"Semilla {SEMILLA_2}: Python y Java iguales en {r2['py_java_semilla2']} valores")
    print(f"Coincidencias entre semillas {SEMILLA_1} y {SEMILLA_2}: {r2['coincidencias']}")
    for nombre, e in [(SEMILLA_1, r2["e1"]), (SEMILLA_2, r2["e2"])]:
        print(f"  semilla {nombre}: media={e['media']:.4f} var={e['varianza']:.4f} corr={e['corr']:+.4f}")

    for fila in analizar_periodo(r1["x"]):
        print("  ", fila)
    print("Imágenes guardadas en la carpeta resultados/")
