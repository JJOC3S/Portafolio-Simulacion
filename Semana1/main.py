"""
main.py -> une todo: datos + modelo + tablas (imagen) + gráficas.
Ejecutar:  python main.py
"""
import modelo
import graficas

# (hora, humedad %, nubosidad %, temperatura °C) - datos de la guía
DATOS = [
    ("06:00", 65, 40, 14),
    ("08:00", 70, 50, 16),
    ("10:00", 68, 45, 18),
    ("12:00", 60, 30, 22),
    ("14:00", 75, 70, 20),
    ("16:00", 85, 85, 18),
    ("18:00", 92, 95, 16),
    ("20:00", 88, 90, 17),
    ("22:00", 80, 75, 15),
]


def main():
    original = modelo.simular(DATOS, modelo.ORIGINAL)
    ajustado = modelo.simular(DATOS, modelo.AJUSTADO)

    # modelo original y tabla + gráficas
    graficas.tabla_imagen(original, "Modelo original: I = 0.5H + 0.3N + 0.2Tf", "1_tabla_original")
    graficas.grafica_variables(original, "Modelo original: variables e índice", "2_variables_original")
    graficas.grafica_indice(original, "Modelo original: índice y estado", "3_indice_original")

    # modelo ajustado y tabla + gráficas
    graficas.tabla_imagen(ajustado, "Modelo ajustado: I = 0.4H + 0.4N + 0.2Tf", "4_tabla_ajustado")
    graficas.grafica_variables(ajustado, "Modelo ajustado: variables e índice", "5_variables_ajustado")
    graficas.grafica_indice(ajustado, "Modelo ajustado: índice y estado", "6_indice_ajustado")

    graficas.grafica_comparacion(original, ajustado, "7_comparacion")

    print("Tablas y gráficas guardadas en la carpeta 'graficas'.")
    graficas.mostrar()


if __name__ == "__main__":
    main()