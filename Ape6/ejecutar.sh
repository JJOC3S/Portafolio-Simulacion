#!/usr/bin/env bash
# Compila y ejecuta Java y Python, luego compara ambos resultados.
set -e
cd "$(dirname "$0")"
mkdir -p java/out
javac -encoding UTF-8 -d java/out java/src/Lcg.java java/src/PruebasEstadisticas.java java/src/Main.java
echo "===== JAVA ====="
java -cp java/out Main
echo
echo "===== PYTHON ====="
python3 python/main.py
echo
echo "===== COMPARACION ====="
python3 python/comparar.py
