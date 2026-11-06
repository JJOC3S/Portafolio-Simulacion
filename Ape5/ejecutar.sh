#!/usr/bin/env bash
# Ejecuta toda la práctica desde la carpeta raíz del proyecto.
#   ./ejecutar.sh            -> genera todo (el período real tarda unos segundos)
set -e
cd "$(dirname "$0")"

echo "== 1. Compilar Java =="
mkdir -p java/out
javac -d java/out java/src/*.java

echo "== 2. Generar secuencias (semilla de la guía y semilla alternativa) =="
for semilla in 12345 54321; do
    python3 python/main.py "$semilla" 10000
    java -cp java/out Main "$semilla" 10000
done

echo "== 3. Período real del generador (2^32 pasos en Java) =="
java -cp java/out PeriodoReal

echo "== 4. Comparar, graficar y armar tablas =="
python3 comparacion/comparar.py
