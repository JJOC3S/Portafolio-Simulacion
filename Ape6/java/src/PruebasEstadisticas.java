import java.util.Arrays;

/**
 * Algoritmo 2 (Chi-cuadrado) y Algoritmo 3 (Kolmogorov-Smirnov).
 * H0: X ~ U(0,1)  vs  H1: X no sigue U(0,1),  alfa = 0.05.
 * Sin librerías externas: los p-valores se calculan a mano.
 */
public class PruebasEstadisticas {

    public static final double ALFA = 0.05;

    public static String decision(double p) {
        return p >= ALFA ? "No se rechaza H0" : "Se rechaza H0";
    }

    // ------------------------------------------------------------------ Chi-cuadrado
    public static class ResultadoChi {
        public long[] observadas;
        public double esperada, chi2, p;
        public int gl;
        public String decision;
    }

    public static ResultadoChi chiCuadrado(double[] u, int k) {
        int n = u.length;
        ResultadoChi r = new ResultadoChi();
        r.esperada = (double) n / k;
        r.observadas = new long[k];
        for (double v : u) {
            int idx = (int) (v * k);
            if (idx > k - 1) idx = k - 1;
            r.observadas[idx]++;
        }
        double chi2 = 0.0;
        for (int i = 0; i < k; i++) {
            double dif = r.observadas[i] - r.esperada;
            chi2 += dif * dif / r.esperada;
        }
        r.chi2 = chi2;
        r.gl = k - 1;
        r.p = gammaQ(r.gl / 2.0, chi2 / 2.0);   // P(X >= chi2) con gl grados de libertad
        r.decision = decision(r.p);
        return r;
    }

    // ------------------------------------------------------------------ Kolmogorov-Smirnov
    public static class ResultadoKS {
        public double dMas, dMenos, d, p, xD;
        public String decision;
    }

    public static ResultadoKS kolmogorovSmirnov(double[] u) {
        int n = u.length;
        double[] x = u.clone();
        Arrays.sort(x);
        double dMas = 0.0, dMenos = 0.0, xMas = 0.0, xMenos = 0.0;
        for (int i = 1; i <= n; i++) {
            double f = x[i - 1];                    // F(x) = x en U(0,1)
            double dp = (double) i / n - f;         // diferencia positiva
            double dm = f - (double) (i - 1) / n;   // diferencia negativa
            if (dp > dMas) { dMas = dp; xMas = f; }
            if (dm > dMenos) { dMenos = dm; xMenos = f; }
        }
        ResultadoKS r = new ResultadoKS();
        r.dMas = dMas;
        r.dMenos = dMenos;
        r.d = Math.max(dMas, dMenos);
        r.xD = dMas >= dMenos ? xMas : xMenos;
        r.p = pKs(r.d, n);
        r.decision = decision(r.p);
        return r;
    }

    /** p-valor asintótico de Kolmogorov con corrección de Stephens (igual que Python). */
    static double pKs(double d, int n) {
        double lam = (Math.sqrt(n) + 0.12 + 0.11 / Math.sqrt(n)) * d;
        double suma = 0.0, signo = 1.0, previo = 0.0;
        for (int k = 1; k <= 100; k++) {
            double termino = signo * Math.exp(-2.0 * k * k * lam * lam);
            suma += termino;
            if (Math.abs(termino) <= 1e-10 * Math.abs(previo) || Math.abs(termino) <= 1e-16 * suma) {
                return Math.min(1.0, Math.max(0.0, 2.0 * suma));
            }
            signo = -signo;
            previo = termino;
        }
        return 1.0;
    }

    // ------------------------------------------------------------------ Gamma incompleta
    private static final double[] LANCZOS = {
        0.99999999999980993, 676.5203681218851, -1259.1392167224028,
        771.32342877765313, -176.61502916214059, 12.507343278686905,
        -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7
    };

    /** ln Γ(z) por Lanczos (z > 0.5). */
    static double lgamma(double z) {
        z -= 1.0;
        double x = LANCZOS[0];
        for (int i = 1; i < 9; i++) x += LANCZOS[i] / (z + i);
        double t = z + 7.5;
        return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    }

    /** Q(a,x): función gamma incompleta regularizada superior (cola de la chi-cuadrado). */
    static double gammaQ(double a, double x) {
        if (x <= 0.0) return 1.0;
        if (x < a + 1.0) return 1.0 - gammaSerie(a, x);
        return gammaFraccionContinua(a, x);
    }

    private static double gammaSerie(double a, double x) {
        double ap = a, suma = 1.0 / a, del = suma;
        for (int i = 0; i < 1000; i++) {
            ap += 1.0;
            del *= x / ap;
            suma += del;
            if (Math.abs(del) < Math.abs(suma) * 1e-16) break;
        }
        return suma * Math.exp(-x + a * Math.log(x) - lgamma(a));
    }

    private static double gammaFraccionContinua(double a, double x) {
        final double FPMIN = 1e-300;
        double b = x + 1.0 - a, c = 1.0 / FPMIN, d = 1.0 / b, h = d;
        for (int i = 1; i <= 1000; i++) {
            double an = -i * (i - a);
            b += 2.0;
            d = an * d + b;
            if (Math.abs(d) < FPMIN) d = FPMIN;
            c = b + an / c;
            if (Math.abs(c) < FPMIN) c = FPMIN;
            d = 1.0 / d;
            double del = d * c;
            h *= del;
            if (Math.abs(del - 1.0) < 1e-16) break;
        }
        return Math.exp(-x + a * Math.log(x) - lgamma(a)) * h;
    }
}
