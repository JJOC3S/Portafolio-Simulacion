/**
 * Actividad 1: Generador Congruencial Lineal (LCG).
 *
 *   X_{n+1} = (a * X_n + c) mod m        U_n = X_{n+1} / m
 *
 * La semilla X_0 no se incluye en la secuencia: el primer valor es X_1.
 * Es el mismo algoritmo que python/lcg.py.
 */
public class Lcg {

    /** Genera X_1..X_n. Con m <= 2^32 y a < 2^31 el producto a*x cabe en un long. */
    public static long[] generarEnteros(int n, long semilla, long a, long c, long m) {
        long[] xs = new long[n];
        long x = semilla;
        for (int i = 0; i < n; i++) {
            x = (a * x + c) % m;
            xs[i] = x;
        }
        return xs;
    }

    /** Normaliza a [0,1): U = X / m. */
    public static double[] aUniformes(long[] xs, long m) {
        double[] u = new double[xs.length];
        for (int i = 0; i < xs.length; i++) {
            u[i] = (double) xs[i] / (double) m;
        }
        return u;
    }
}
