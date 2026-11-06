# Práctica 06 – Validación estadística de números pseudoaleatorios (Chi-cuadrado y Kolmogorov-Smirnov)

**Asignatura:** Simulación – Ciclo 5 – Carrera de Computación, UNL
**Unidad 2:** Generación de números pseudoaleatorios y generación de variables aleatorias
**Hipótesis:** H0: X ~ U(0,1) vs H1: X no sigue U(0,1) · **α = 0.05**

Se genera una secuencia con el **Generador Congruencial Lineal (LCG)** `X(n+1) = (a·Xn + c) mod m`, `U = X/m`, y se valida su uniformidad con **Chi-cuadrado** (k = 10 subintervalos, gl = 9) y **Kolmogorov-Smirnov**. Todo está implementado **en Python y en Java** con los mismos algoritmos de la guía (sin usar funciones ya hechas para el estadístico; solo `scipy` en Python para obtener el p-valor de χ² y para verificar).

## Estructura

```
Practica06_Simulacion/
├── python/
│   ├── lcg.py          # Actividad 1: generador LCG
│   ├── pruebas.py      # Algoritmos Chi-cuadrado y Kolmogorov-Smirnov
│   ├── graficas.py     # Histogramas, ECDF vs teórica, tiempos
│   ├── main.py         # Ejecuta todo y guarda resultados
│   ├── comparar.py     # Compara Python vs Java
│   └── requirements.txt
├── java/src/
│   ├── Lcg.java
│   ├── PruebasEstadisticas.java   # incluye p-valores implementados a mano
│   └── Main.java
├── resultados/         # CSV, salidas de consola y gráficas (ya generados)
├── ejecutar.bat        # Windows: compila y corre Java + Python + comparación
├── ejecutar.sh         # Linux / macOS
└── README.md
```

## Cómo ejecutar

Requisitos: Python 3 con `numpy scipy matplotlib pandas` (`pip install -r python/requirements.txt`) y JDK 8 o superior.

Desde la raíz del proyecto:

```bash
# Todo de una vez
./ejecutar.sh          # Linux / macOS
ejecutar.bat           # Windows

# O por separado
javac -d java/out java/src/Lcg.java java/src/PruebasEstadisticas.java java/src/Main.java
java -cp java/out Main
python python/main.py
python python/comparar.py
```

En IntelliJ/Eclipse/NetBeans basta con abrir la carpeta `java/src` como fuente y ejecutar `Main` con la raíz del proyecto como directorio de trabajo (o pasar la ruta de la raíz como argumento). En VS Code abre la carpeta del proyecto y corre `python/main.py`.

## Configuraciones del generador

| Config | Semilla | a | c | m | Comentario |
|---|---|---|---|---|---|
| A | 12345 | 1664525 | 1013904223 | 2³² | Parámetros de la Práctica 05 (Numerical Recipes) |
| B | 12345 | 1103515245 | 12345 | 2³¹ | Tipo glibc |
| C | 1 | 65539 | 0 | 2³¹ | RANDU (generador históricamente defectuoso) |
| D | 12345 | 1 | 1 | 2³² | Degenerado (X crece de 1 en 1): sirve de contraste |

## Resultados (N = 10 000, k = 10, α = 0.05)

| Config | χ² (gl=9) | p (χ²) | D (KS) | p (KS) | Decisión χ² | Decisión KS |
|---|---|---|---|---|---|---|
| A | 14.160 | 0.1167 | 0.00596 | 0.8686 | No se rechaza H0 | No se rechaza H0 |
| B | 6.642 | 0.6743 | 0.00809 | 0.5281 | No se rechaza H0 | No se rechaza H0 |
| C | 8.812 | 0.4548 | 0.00636 | 0.8127 | No se rechaza H0 | No se rechaza H0 |
| D | 90000.0 | 0.0000 | 0.99999 | 0.0000 | **Se rechaza H0** | **Se rechaza H0** |

Frecuencias observadas (config A): `[1016, 993, 1049, 940, 949, 1063, 1014, 1016, 984, 976]`, esperada = 1000 por intervalo.
Valor crítico χ²(0.05, 9) = 16.919: solo la config D lo supera.

## Tabla comparativa Python vs Java (config A, variando N)

> La guía trae la columna «π estimado / Error», que corresponde a otra práctica (Monte Carlo); aquí la tabla se adaptó a los estadísticos de esta práctica. Los tiempos incluyen generación + ambas pruebas (mejor de 3 corridas) y dependen de tu computador.

| N | χ² | p (χ²) | D | p (KS) | Tiempo Python (ms) | Tiempo Java (ms) |
|---|---|---|---|---|---|---|
| 1 000 | 4.120 | 0.9033 | 0.02864 | 0.3800 | 0.21 | 0.14 |
| 10 000 | 14.160 | 0.1167 | 0.00596 | 0.8686 | 1.50 | 1.67 |
| 100 000 | 9.160 | 0.4226 | 0.00207 | 0.7829 | 16.29 | 9.87 |
| 1 000 000 | 16.023 | 0.0664 | 0.00094 | 0.3346 | 176.23 | 103.43 |

**Verificación de equivalencia:** `python/comparar.py` confirma que los 10 000 enteros `X` y los uniformes `U` son **idénticos** en ambos lenguajes (`resultados/secuencia_python.csv` vs `secuencia_java.csv`) y que χ², D y los p-valores difieren como máximo en 3.6·10⁻¹⁵ (ruido de punto flotante), con las mismas decisiones estadísticas.

Gráficas en `resultados/`: `histogramas.png` (Chi-cuadrado), `ks_ecdf.png` (distribución acumulada empírica vs teórica, con el punto donde ocurre D) y `tiempos.png`.

## Conclusiones

1. **Las configuraciones A, B y C no rechazan H0** con ninguna de las dos pruebas: con α = 0.05 no hay evidencia de que sus valores se aparten de U(0,1). La config D se rechaza de forma contundente (todos los valores caen en el primer subintervalo, χ² = 90 000 y D ≈ 1), lo que confirma que las pruebas sí detectan un mal generador.
2. **Ambas pruebas coinciden** en todas las configuraciones, pero miden cosas distintas: χ² compara frecuencias por intervalo (depende de cómo se agrupe), KS compara las distribuciones acumuladas punto a punto sin agrupar.
3. **El p-valor varía con N de forma aleatoria**, no sistemática: para la config A pasó de 0.90 (N=1 000) a 0.066 (N=1 000 000) en χ², cerca del umbral pero sin rechazar. Con α = 0.05 es esperable rechazar H0 en ~5 % de las muestras aunque el generador sea bueno.
4. **RANDU pasa ambas pruebas** a pesar de ser un generador muy defectuoso (sus tripletas consecutivas caen en pocos planos). Esto muestra que χ² y KS solo evalúan *uniformidad marginal*, no independencia entre valores.
5. **Python y Java producen exactamente la misma secuencia** con los mismos parámetros. Java fue ~1.7× más rápido a partir de N = 100 000 (bucle compilado JIT frente al bucle de Python); para N pequeños la diferencia es despreciable.

## Preguntas de control

1. **¿Qué es la hipótesis nula?** Es la afirmación que se asume cierta de partida y que se intenta refutar con los datos; aquí H0: los números generados siguen una distribución U(0,1). H1 es su negación.
2. **¿Qué representa el valor p?** La probabilidad, suponiendo que H0 es cierta, de obtener un estadístico tan extremo o más que el observado. No es la probabilidad de que H0 sea cierta.
3. **¿Qué significa rechazar H0?** Que, con α = 0.05, los datos son demasiado improbables bajo uniformidad (p < 0.05), así que se concluye que la secuencia no se ajusta a U(0,1). Hay una probabilidad α de rechazar equivocadamente (error tipo I).
4. **¿Diferencia entre Chi-cuadrado y KS?** χ² agrupa los datos en k intervalos y compara frecuencias observadas con esperadas (estadístico Σ(O−E)²/E, gl = k−1); sirve con datos discretos o agrupados y depende de k. KS compara la distribución acumulada empírica con la teórica (D = sup|Fn − F|), usa cada dato individual sin agrupar y es más sensible a diferencias en la forma global de la distribución.
5. **¿Por qué una prueba no demuestra que un generador sea verdaderamente aleatorio?** Porque no rechazar H0 solo indica falta de evidencia en contra, no prueba de lo contrario; cada prueba mira una propiedad concreta (aquí, uniformidad). Además el LCG es determinista y periódico: reproduce siempre la misma secuencia y puede pasar estas pruebas siendo defectuoso (caso RANDU). Por eso se aplica una batería de pruebas (independencia, series, rachas, etc.).
