# Práctica 05 – Generador Congruencial Lineal (LCG) en Python y Java

**Asignatura:** Simulación · **Unidad 2:** Generación de números pseudoaleatorios y de variables aleatorias

Implementación del mismo generador LCG en dos lenguajes, comparación de las secuencias, análisis del período y del efecto de cambiar la semilla.

## 1. Fundamento

Relación recursiva y normalización:

```
X(n+1) = (a · X(n) + c) mod m
U(n)   = X(n) / m          → valor en [0, 1)
```

Parámetros de la guía: `a = 1664525`, `c = 1013904223`, `m = 2^32`, `semilla = X(0) = 12345`.
El primer valor generado es `X(1)`; la semilla no se cuenta como observación.

## 2. Estructura del proyecto

```
practica05_lcg/
├── README.md
├── ejecutar.sh              ← ejecuta todo de una vez
├── python/
│   ├── lcg.py               ← clase LCG
│   └── main.py              ← genera la secuencia y la guarda en CSV
├── java/src/
│   ├── LCG.java             ← clase LCG
│   ├── Main.java            ← genera la secuencia y la guarda en CSV
│   └── PeriodoReal.java     ← mide el período real (2^32 pasos)
├── comparacion/
│   └── comparar.py          ← compara, grafica y arma las tablas (PNG)
└── resultados/              ← CSV, tablas y gráficas generadas
```

Ambos lenguajes escriben un CSV con las columnas `n, x, u`; `comparar.py` los lee y los compara valor por valor.

## 3. Cómo ejecutarlo

Requisitos: Python 3 con `matplotlib` y `numpy` (`pip install matplotlib numpy`) y JDK (`javac` y `java`).

```bash
./ejecutar.sh
```

O paso a paso desde la carpeta raíz:

```bash
mkdir -p java/out && javac -d java/out java/src/*.java

python3 python/main.py 12345 10000          # Python, semilla de la guía
java -cp java/out Main 12345 10000          # Java, semilla de la guía
python3 python/main.py 54321 10000          # Python, otra semilla
java -cp java/out Main 54321 10000          # Java, otra semilla

java -cp java/out PeriodoReal               # opcional: tarda unos segundos
python3 comparacion/comparar.py             # tablas y gráficas
```

## 4. Resultados

### 4.1 Comparación Python vs Java (primeras 20 observaciones, semilla 12345)

| n | X Python | X Java | U Python | U Java | ¿Igual? |
|---|----------|--------|----------|--------|---------|
| 1 | 87628868 | 87628868 | 0.0204026857 | 0.0204026857 | Sí |
| 2 | 71072467 | 71072467 | 0.0165478482 | 0.0165478482 | Sí |
| 3 | 2332836374 | 2332836374 | 0.5431557945 | 0.5431557945 | Sí |
| 4 | 2726892157 | 2726892157 | 0.6349040561 | 0.6349040561 | Sí |
| 5 | 3908547000 | 3908547000 | 0.9100295138 | 0.9100295138 | Sí |
| 6 | 483019191 | 483019191 | 0.1124616691 | 0.1124616691 | Sí |
| 7 | 2129828778 | 2129828778 | 0.4958894053 | 0.4958894053 | Sí |
| 8 | 2355140353 | 2355140353 | 0.5483488443 | 0.5483488443 | Sí |
| 9 | 2560230508 | 2560230508 | 0.5961001171 | 0.5961001171 | Sí |
| 10 | 3364893915 | 3364893915 | 0.7834504161 | 0.7834504161 | Sí |
| 11 | 171172990 | 171172990 | 0.0398543174 | 0.0398543174 | Sí |
| 12 | 3194601925 | 3194601925 | 0.7438012224 | 0.7438012224 | Sí |
| 13 | 4148119648 | 4148119648 | 0.9658093676 | 0.9658093676 | Sí |
| 14 | 316399679 | 316399679 | 0.0736675409 | 0.0736675409 | Sí |
| 15 | 3004788882 | 3004788882 | 0.6996069294 | 0.6996069294 | Sí |
| 16 | 1976948425 | 1976948425 | 0.4602941743 | 0.4602941743 | Sí |
| 17 | 1702883732 | 1702883732 | 0.3964835154 | 0.3964835154 | Sí |
| 18 | 4121112547 | 4121112547 | 0.9595212869 | 0.9595212869 | Sí |
| 19 | 1744294886 | 1744294886 | 0.4061253010 | 0.4061253010 | Sí |
| 20 | 4092090893 | 4092090893 | 0.9527641565 | 0.9527641565 | Sí |

Comparando los 10 000 valores completos, los enteros `X` y los valores `U` coinciden en **10 000 de 10 000** (con ambas semillas probadas). Imagen: `resultados/tabla_comparacion.png`.

### 4.2 Gráficas de la secuencia

- `resultados/grafica_secuencia.png`: los 10 000 valores `U(n)` de Python y de Java, lado a lado. Se ven idénticos y cubren todo el intervalo [0, 1).
- `resultados/grafica_histograma.png`: 10 intervalos con frecuencias entre 940 y 1063 (esperado 1000 si fuera uniforme perfecta).
- `resultados/grafica_dispersion.png`: `U(n)` contra `U(n+1)`; no se aprecia ningún patrón evidente entre valores consecutivos.

### 4.3 Período

El LCG cumple las condiciones de Hull-Dobell, así que su período es el máximo posible, `m = 2^32 = 4 294 967 296`:

1. `c` y `m` son primos relativos (`c` es impar).
2. `a − 1 = 1664524` es divisible por todos los factores primos de `m` (solo el 2).
3. Como `m` es múltiplo de 4, `a − 1` también es múltiplo de 4 (`1664524 / 4 = 416131`).

Se comprobó de forma experimental con `PeriodoReal.java`: partiendo de la semilla 12345, la semilla vuelve a aparecer exactamente a los **4 294 967 296 pasos**. En los 10 000 valores generados no hay ningún valor repetido. Imagen: `resultados/tabla_periodo.png`, que además muestra ejemplos con parámetros malos (`a=4, c=2, m=16` cae en período 1; `a=5, c=0, m=16` en período 4).

### 4.4 Cambio de semilla (12345 vs 54321)

| Semilla | Media | Varianza | Mínimo | Máximo | Correlación lag 1 |
|---------|-------|----------|--------|--------|-------------------|
| 12345 | 0.4988 | 0.0830 | 0.00006 | 0.99993 | −0.0153 |
| 54321 | 0.4989 | 0.0836 | 0.00008 | 0.99985 | −0.0020 |
| Teórico U(0,1) | 0.5000 | 0.0833 | 0 | 1 | 0 |

Las dos secuencias no tienen ningún valor en común en las mismas posiciones (0 coincidencias de 10 000), pero ambas tienen estadísticas muy cercanas a las de una U(0,1). Imágenes: `tabla_semillas.png`, `tabla_estadisticas.png`, `grafica_semillas.png`.

## 5. Conclusiones

1. Con los mismos parámetros y la misma semilla, Python y Java producen **exactamente la misma secuencia** (10 000 de 10 000 valores iguales). El algoritmo es determinista: el resultado no depende del lenguaje, solo de `a`, `c`, `m` y la semilla.
2. En Java se usó `long` (64 bits) porque `a · X` puede llegar a unos 7.1 × 10^15, que cabe en un `long`; con `int` habría desbordamiento y la secuencia sería distinta. Python no tiene este problema porque sus enteros crecen sin límite.
3. Los valores normalizados `U(n)` se distribuyen de forma aproximadamente uniforme en [0, 1): media ≈ 0.5, varianza ≈ 1/12 ≈ 0.0833 y un histograma casi plano.
4. El período del generador es completo (2^32), muy superior a los 10 000 valores necesarios, y se verificó tanto con la teoría (Hull-Dobell) como midiéndolo en Java.
5. Cambiar la semilla produce otra secuencia completamente distinta con las mismas propiedades estadísticas; solo cambia el punto de partida dentro del mismo ciclo.
6. Un período completo no basta por sí solo: con `a=1, c=1` el período también es completo, pero la secuencia es 1, 2, 3, … (nada aleatoria). Por eso hay que elegir bien los parámetros y revisar las gráficas.

## 6. Preguntas de control

**1. ¿Qué significa pseudoaleatorio?**
Que los números parecen aleatorios y pasan pruebas estadísticas de uniformidad e independencia, pero en realidad los produce un algoritmo determinista: con los mismos parámetros y la misma semilla siempre se obtiene la misma secuencia.

**2. ¿Qué función cumple la semilla?**
Es el valor inicial `X(0)` del que arranca la recursión. Determina en qué punto del ciclo comienza la secuencia: otra semilla da otra secuencia, y la misma semilla permite reproducir los resultados exactamente.

**3. ¿Qué significa período?**
Es la cantidad de números distintos que genera el algoritmo antes de que la secuencia comience a repetirse. Aquí es `2^32 = 4 294 967 296`.

**4. ¿Qué ocurre si se utilizan parámetros inadecuados?**
El período se acorta (por ejemplo, con `a=4, c=2, m=16` la secuencia se queda en un solo valor), aparecen patrones o correlaciones entre valores consecutivos, o la distribución deja de ser uniforme. Los resultados de la simulación dejan de ser confiables.

**5. ¿Qué ventaja tiene implementar el mismo algoritmo en dos lenguajes?**
Permite validar que la implementación es correcta (si ambas dan la misma secuencia, es difícil que las dos tengan el mismo error), reproducir resultados entre plataformas y descubrir diferencias propias de cada lenguaje, como el desbordamiento de enteros en Java frente a los enteros sin límite de Python.
