"""Todas las gráficas. Cada función guarda un PNG y devuelve la figura."""
import matplotlib.pyplot as plt
import numpy as np

from simulacion.config import DIR_FIGURAS


def _cerrar(fig, nombre):
    DIR_FIGURAS.mkdir(parents=True, exist_ok=True)
    ruta = DIR_FIGURAS / nombre
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    return ruta


def _estilo(ax, titulo):
    ax.set_title(titulo)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Población")
    ax.legend()
    ax.grid(True, alpha=0.3)


def grafica_comparativa(datos, det, dis, est, con):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(np.arange(len(datos)), datos, "ko", label="Datos observados")
    ax.plot(*det, label="Determinístico (exponencial)")
    ax.step(dis[0], dis[1], where="post", marker="s", label="Discreto")
    ax.plot(*est, marker="^", label="Estocástico")
    ax.plot(*con, "--", label="Continuo (Euler)")
    _estilo(ax, "Comparación de los cuatro modelos")
    return _cerrar(fig, "01_comparativa.png")


def grafica_influencia_r(curvas):
    fig, ax = plt.subplots(figsize=(9, 5))
    for r, (t, p) in curvas.items():
        ax.plot(t, p, label=f"r = {r:.3f}")
    _estilo(ax, "Influencia de r (crecimiento y decrecimiento)")
    return _cerrar(fig, "02_influencia_r.png")


def grafica_influencia_sigma(trayectorias, referencia):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(*referencia, "k--", label="Determinístico")
    for s, (t, p) in trayectorias.items():
        ax.plot(t, p, marker="o", label=f"sigma = {s}")
    _estilo(ax, "Influencia del nivel de ruido (sigma)")
    return _cerrar(fig, "03_influencia_sigma.png")


def grafica_corridas(t, corridas, referencia):
    fig, ax = plt.subplots(figsize=(9, 5))
    for fila in corridas:
        ax.plot(t, fila, color="tab:blue", alpha=0.15)
    ax.plot(t, corridas.mean(axis=0), color="tab:red", lw=2, label="Media de corridas")
    ax.fill_between(
        t,
        corridas.mean(axis=0) - corridas.std(axis=0),
        corridas.mean(axis=0) + corridas.std(axis=0),
        color="tab:red", alpha=0.2, label="±1 desv. estándar",
    )
    ax.plot(*referencia, "k--", label="Determinístico")
    _estilo(ax, f"Efecto de la aleatoriedad ({len(corridas)} corridas)")
    return _cerrar(fig, "04_corridas_estocasticas.png")


def grafica_error_dt(errores):
    fig, ax = plt.subplots(figsize=(7, 5))
    dts = list(errores.keys())
    ax.loglog(dts, list(errores.values()), "o-", label="Error de Euler en t final")
    ax.set_title("Función de dt: error de Euler vs tamaño de paso")
    ax.set_xlabel("dt")
    ax.set_ylabel("|P_Euler - P_exacto|")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    return _cerrar(fig, "05_error_dt.png")
