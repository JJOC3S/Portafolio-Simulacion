import java.io.File;
import java.io.PrintWriter;

/**
 * Comprueba de forma experimental el período real del LCG de la guía.
 * Avanza el generador hasta que vuelve a aparecer la semilla (X = 12345).
 * Son 2^32 pasos, por lo que tarda unos segundos.
 *
 * Uso (desde la carpeta raíz del proyecto):
 *     java -cp java/out PeriodoReal
 */
public class PeriodoReal {
    public static void main(String[] args) throws Exception {
        LCG generador = new LCG(LCG.SEMILLA);

        long pasos = 0;
        long x;
        do {
            x = generador.siguiente();
            pasos++;
        } while (x != LCG.SEMILLA);

        new File("resultados").mkdirs();
        try (PrintWriter salida = new PrintWriter("resultados/periodo_real_java.txt")) {
            salida.println(pasos);
        }

        System.out.println("[Java] La semilla " + LCG.SEMILLA + " reaparece tras " + pasos + " pasos (2^32 = " + LCG.M + ")");
    }
}
