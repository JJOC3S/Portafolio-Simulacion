"""Genera la secuencia LCG en Python y la guarda en un CSV.

Uso (desde la carpeta raíz del proyecto):
    python3 python/main.py [semilla] [cantidad]

Ejemplo:
    python3 python/main.py 12345 10000
"""
import csv
import os
import sys

from lcg import LCG, SEMILLA

semilla = int(sys.argv[1]) if len(sys.argv) > 1 else SEMILLA
cantidad = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

generador = LCG(semilla)
valores = generador.generar(cantidad)

os.makedirs("resultados", exist_ok=True)
archivo = f"resultados/python_semilla_{semilla}.csv"

with open(archivo, "w", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerow(["n", "x", "u"])
    for n, (x, u) in enumerate(valores, start=1):
        escritor.writerow([n, x, f"{u:.10f}"])

print(f"[Python] semilla={semilla}  valores={cantidad}  -> {archivo}")
