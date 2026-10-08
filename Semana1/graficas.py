"""
graficas.py -> SOLO las gráficas (usa los resultados que da modelo.py).
Cada función guarda un PNG en la carpeta "graficas".
"""
import os
import matplotlib.pyplot as plt

CARPETA = "graficas"

COLORES_ESTADO = {
    "Sin lluvia": "#4caf50",
    "Baja posibilidad": "#fbc02d",
    "Lluvia probable": "#fb8c00",
    "Lluvia": "#d32f2f",
}


def _guardar(nombre):
    os.makedirs(CARPETA, exist_ok=True)
    plt.tight_layout()
    plt.savefig(f"{CARPETA}/{nombre}.png", dpi=150)

COLUMNAS = ["Hora", "Humedad", "Nubosidad", "Temp.", "H", "N", "Tf", "Índice", "Estado"]

# Colores suaves de fondo para la celda "Estado" de la tabla
FONDO_ESTADO = {
    "Sin lluvia": "#c8e6c9",
    "Baja posibilidad": "#fff59d",
    "Lluvia probable": "#ffcc80",
    "Lluvia": "#ef9a9a",
}


def tabla_imagen(resultados, titulo, nombre):
    """Dibuja la tabla de la guía como imagen (encabezado azul, filas alternadas)."""
    filas = [[r.hora, r.humedad, r.nubosidad, r.temp,
              f"{r.h:.2f}", f"{r.n:.2f}", f"{r.tf:.2f}", f"{r.indice:.3f}", r.estado]
             for r in resultados]

    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.axis("off")
    tabla = ax.table(cellText=filas, colLabels=COLUMNAS, loc="center", cellLoc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1, 1.8)
    tabla.auto_set_column_width(list(range(len(COLUMNAS))))

    for col in range(len(COLUMNAS)):
        celda = tabla[0, col]
        celda.set_facecolor("#15607f")
        celda.get_text().set_color("white")
        celda.get_text().set_weight("bold")

    for i, r in enumerate(resultados, start=1):
        for col in range(len(COLUMNAS)):
            tabla[i, col].set_facecolor("#c5e5f5" if i % 2 == 1 else "white")
        tabla[i, len(COLUMNAS) - 1].set_facecolor(FONDO_ESTADO[r.estado])

    ax.set_title(titulo, fontsize=14, weight="bold")
    _guardar(nombre)


def grafica_variables(resultados, titulo, nombre):
    """Líneas: H, N, Tf e Índice a lo largo del día."""
    horas = [r.hora for r in resultados]
    plt.figure(figsize=(9, 5))
    plt.plot(horas, [r.h for r in resultados], marker="o", label="H (humedad)")
    plt.plot(horas, [r.n for r in resultados], marker="o", label="N (nubosidad)")
    plt.plot(horas, [r.tf for r in resultados], marker="o", label="Tf (temperatura)")
    plt.plot(horas, [r.indice for r in resultados], marker="s", linewidth=3,
             color="black", label="Índice I")
    plt.title(titulo)
    plt.xlabel("Hora")
    plt.ylabel("Valor normalizado (0 a 1)")
    plt.grid(alpha=0.3)
    plt.legend()
    _guardar(nombre)


def grafica_indice(resultados, titulo, nombre):
    """Barras del índice, coloreadas por estado, con los umbrales de la tabla de reglas."""
    horas = [r.hora for r in resultados]
    colores = [COLORES_ESTADO[r.estado] for r in resultados]
    plt.figure(figsize=(9, 5))
    plt.bar(horas, [r.indice for r in resultados], color=colores)
    for umbral in (0.40, 0.60, 0.75):
        plt.axhline(umbral, color="gray", linestyle="--", linewidth=1)
        plt.text(-0.45, umbral + 0.01, str(umbral), color="gray")
    # Leyenda con los 4 estados
    for estado, color in COLORES_ESTADO.items():
        plt.bar(0, 0, color=color, label=estado)
    plt.title(titulo)
    plt.xlabel("Hora")
    plt.ylabel("Índice I")
    plt.ylim(0, 1)
    plt.legend(loc="upper left")
    _guardar(nombre)


def grafica_comparacion(res_original, res_ajustado, nombre):
    """Compara el índice del modelo original contra el ajustado."""
    horas = [r.hora for r in res_original]
    plt.figure(figsize=(9, 5))
    plt.plot(horas, [r.indice for r in res_original], marker="o", label="Modelo original")
    plt.plot(horas, [r.indice for r in res_ajustado], marker="o", label="Modelo ajustado")
    for umbral in (0.40, 0.60, 0.75):
        plt.axhline(umbral, color="gray", linestyle="--", linewidth=1)
    plt.title("Comparación del índice: original vs ajustado")
    plt.xlabel("Hora")
    plt.ylabel("Índice I")
    plt.grid(alpha=0.3)
    plt.legend()
    _guardar(nombre)


def mostrar():
    """Abre las ventanas con todas las gráficas."""
    plt.show()