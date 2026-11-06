/**
 * Generador Congruencial Lineal (LCG) en Java.
 *
 * Relación recursiva:   X(n+1) = (a * X(n) + c) mod m
 * Valor normalizado:    U(n)   = X(n) / m      (queda en [0, 1))
 *
 * Convención (igual que en Python): X(0) es la semilla y el primer
 * valor generado es X(1).
 */
public class LCG {

    // Parámetros pedidos en la guía
    public static final long A = 1664525L;
    public static final long C = 1013904223L;
    public static final long M = 4294967296L; // 2^32
    public static final long SEMILLA = 12345L;

    private final long a;
    private final long c;
    private final long m;
    private long x; // estado actual: X(0) = semilla

    public LCG(long semilla) {
        this(semilla, A, C, M);
    }

    public LCG(long semilla, long a, long c, long m) {
        this.x = semilla;
        this.a = a;
        this.c = c;
        this.m = m;
    }

    /** Avanza un paso y devuelve el entero X(n+1). */
    public long siguiente() {
        // a * x cabe en un long (máx. ~7.1e15), por eso no hay desbordamiento
        x = (a * x + c) % m;
        return x;
    }

    /** Convierte un entero X en su valor normalizado U = X / m. */
    public double normalizar(long valor) {
        return (double) valor / m;
    }
}
