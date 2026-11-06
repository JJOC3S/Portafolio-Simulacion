"""Gráficas: histogramas (Chi-cuadrado) y distribución acumulada (KS)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def histogramas(datos, ruta, k=10):
    """datos: lista de (nombre, uniformes, resultado_chi2)."""
    fig, ejes = plt.subplots(2, 2, figsize=(11, 7.5))
    for ax, (nombre, u, chi) in zip(ejes.ravel(), datos):
        ax.bar(np.arange(k) / k + 0.5 / k, chi["observadas"], width=1 / k * 0.9,
               color="#4C78A8", label="Observada")
        ax.axhline(chi["esperada"], color="#E45756", ls="--", label="Esperada")
        ax.set_title(f"{nombre}\nχ²={chi['chi2']:.2f}  p={chi['p']:.4f}", fontsize=10)
        ax.set_xlabel("Subintervalo de [0,1]")
        ax.set_ylabel("Frecuencia")
        ax.set_ylim(0, max(chi["observadas"].max(), chi["esperada"]) * 1.3)
        ax.legend(fontsize=8, loc="upper right", ncol=2)
    fig.suptitle("Prueba Chi-cuadrado: frecuencias observadas vs esperadas", fontsize=12)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)


def ecdf_ks(datos, ruta):
    """datos: lista de (nombre, uniformes, resultado_ks)."""
    fig, ejes = plt.subplots(2, 2, figsize=(11, 7.5))
    for ax, (nombre, u, ks) in zip(ejes.ravel(), datos):
        x = np.sort(u)
        n = len(x)
        ax.step(x, np.arange(1, n + 1) / n, where="post", color="#4C78A8",
                label="F_n(x) empírica")
        ax.plot([0, 1], [0, 1], color="#E45756", ls="--", label="F(x) = x teórica")
        ax.axvline(ks["x_d"], color="#999999", lw=0.8, ls=":")
        ax.set_title(f"{nombre}\nD={ks['D']:.5f}  p={ks['p']:.4f}", fontsize=10)
        ax.set_xlabel("x")
        ax.set_ylabel("Probabilidad acumulada")
        ax.legend(fontsize=8, loc="lower right")
    fig.suptitle("Prueba Kolmogorov-Smirnov: distribución acumulada", fontsize=12)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)


def tiempos(filas, ruta):
    """filas: lista de (N, t_python_ms, t_java_ms or None)."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ns = [f[0] for f in filas]
    ax.plot(ns, [f[1] for f in filas], "o-", color="#4C78A8", label="Python")
    if all(f[2] is not None for f in filas):
        ax.plot(ns, [f[2] for f in filas], "s-", color="#F58518", label="Java")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("N (cantidad de números)")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_title("Tiempo de generación + pruebas")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)
