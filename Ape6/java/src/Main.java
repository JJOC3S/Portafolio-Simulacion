import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Validacion estadistica de numeros pseudoaleatorios (Java).
 * Uso (desde la raíz del proyecto):  java -cp java/out Main [carpeta_raiz]
 */
public class Main {

    static final int N_BASE = 10_000;
    static final int K = 10;
    static final int[] TAMANOS = {1_000, 10_000, 100_000, 1_000_000};

    /** nombre, semilla, a, c, m */
    static final Object[][] CONFIGS = {
        {"A: Numerical Recipes (Practica 05)", 12345L, 1664525L, 1013904223L, 1L << 32},
        {"B: glibc (a=1103515245)",            12345L, 1103515245L, 12345L, 1L << 31},
        {"C: RANDU (a=65539, c=0)",            1L,     65539L,      0L,     1L << 31},
        {"D: Degenerado (a=1, c=1)",           12345L, 1L,          1L,     1L << 32},
    };

    static class Corrida {
        double[] u;
        PruebasEstadisticas.ResultadoChi chi;
        PruebasEstadisticas.ResultadoKS ks;
        double ms;
    }

    static Corrida ejecutar(int n, Object[] cfg) {
        long t0 = System.nanoTime();
        long m = (Long) cfg[4];
        long[] xs = Lcg.generarEnteros(n, (Long) cfg[1], (Long) cfg[2], (Long) cfg[3], m);
        Corrida r = new Corrida();
        r.u = Lcg.aUniformes(xs, m);
        r.chi = PruebasEstadisticas.chiCuadrado(r.u, K);
        r.ks = PruebasEstadisticas.kolmogorovSmirnov(r.u);
        r.ms = (System.nanoTime() - t0) / 1e6;
        return r;
    }

    static double mejorTiempo(int n, Object[] cfg) {
        double mejor = Double.MAX_VALUE;
        for (int i = 0; i < 3; i++) mejor = Math.min(mejor, ejecutar(n, cfg).ms);
        return mejor;
    }

    static String dec12(double v) {
        return new BigDecimal(v).setScale(12, RoundingMode.HALF_EVEN).toPlainString();
    }

    static String fila(String exp, String cfg, int n, Corrida r, double ms) {
        return String.join(",", exp, cfg, String.valueOf(n),
            Double.toString(r.chi.chi2), String.valueOf(r.chi.gl), Double.toString(r.chi.p),
            r.chi.decision, Double.toString(r.ks.d), Double.toString(r.ks.p),
            r.ks.decision, Double.toString(ms));
    }

    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        Path raiz = Paths.get(args.length > 0 ? args[0] : ".");
        Path res = raiz.resolve("resultados");
        Files.createDirectories(res);
        List<String> filas = new ArrayList<>();

        // Calentamiento de la JVM para que los tiempos sean representativos
        for (int i = 0; i < 5; i++) ejecutar(100_000, CONFIGS[0]);

        // ---- Secuencia de la configuración A ----
        Object[] a = CONFIGS[0];
        long m = (Long) a[4];
        long[] xs = Lcg.generarEnteros(N_BASE, (Long) a[1], (Long) a[2], (Long) a[3], m);
        double[] u = Lcg.aUniformes(xs, m);
        try (PrintWriter pw = new PrintWriter(res.resolve("secuencia_java.csv").toFile(), "UTF-8")) {
            pw.print("indice,X,U\n");
            for (int i = 0; i < N_BASE; i++) pw.print((i + 1) + "," + xs[i] + "," + dec12(u[i]) + "\n");
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 10; i++) sb.append(String.format("%.6f", u[i])).append(i < 9 ? ", " : "");
        System.out.println("Primeros 10 numeros (config A): " + sb);

        // ---- Experimento 1: configuraciones (N = 10 000) ----
        System.out.printf("%n=== Configuraciones del generador (N=%d, k=%d, alfa=%.2f) ===%n",
            N_BASE, K, PruebasEstadisticas.ALFA);
        System.out.printf("%-38s%9s%10s%10s%10s  %s%n", "Configuracion", "chi2", "p(chi2)", "D", "p(KS)", "Decision");
        for (Object[] cfg : CONFIGS) {
            Corrida r = ejecutar(N_BASE, cfg);
            double t = mejorTiempo(N_BASE, cfg);
            String nombre = (String) cfg[0];
            System.out.printf("%-38s%9.3f%10.4f%10.5f%10.4f  chi2: %s | KS: %s%n", nombre,
                r.chi.chi2, r.chi.p, r.ks.d, r.ks.p, r.chi.decision, r.ks.decision);
            filas.add(fila("configuraciones", nombre.substring(0, 1), N_BASE, r, t));
            if (cfg == CONFIGS[0]) {
                System.out.println("\nFrecuencias observadas (config A): "
                    + java.util.Arrays.toString(r.chi.observadas) + " | esperada: " + r.chi.esperada + "\n");
            }
        }

        // ---- Experimento 2: tamanos y tiempos (config A) ----
        System.out.printf("%n=== Config A: efecto del tamano N y tiempos ===%n");
        System.out.printf("%10s%10s%10s%10s%10s%16s%n", "N", "chi2", "p(chi2)", "D", "p(KS)", "t Java (ms)");
        for (int n : TAMANOS) {
            Corrida r = ejecutar(n, CONFIGS[0]);
            double t = mejorTiempo(n, CONFIGS[0]);
            System.out.printf("%10d%10.3f%10.4f%10.5f%10.4f%16.2f%n", n, r.chi.chi2, r.chi.p, r.ks.d, r.ks.p, t);
            filas.add(fila("tamanos", "A", n, r, t));
        }

        try (PrintWriter pw = new PrintWriter(res.resolve("resultados_java.csv").toFile(), "UTF-8")) {
            pw.print("experimento,configuracion,N,chi2,gl,p_chi2,decision_chi2,D,p_ks,decision_ks,tiempo_ms\n");
            for (String f : filas) pw.print(f + "\n");
        }
        System.out.println("\nResultados guardados en: " + res.toAbsolutePath().normalize());
    }
}
