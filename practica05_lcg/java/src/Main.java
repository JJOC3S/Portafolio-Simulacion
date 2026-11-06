import java.io.File;
import java.io.PrintWriter;
import java.util.Locale;

/**
 * Genera la secuencia LCG en Java y la guarda en un CSV.
 *
 * Uso (desde la carpeta raíz del proyecto):
 *     java -cp java/out Main [semilla] [cantidad]
 */
public class Main {
    public static void main(String[] args) throws Exception {
        long semilla = args.length > 0 ? Long.parseLong(args[0]) : LCG.SEMILLA;
        int cantidad = args.length > 1 ? Integer.parseInt(args[1]) : 10000;

        LCG generador = new LCG(semilla);

        new File("resultados").mkdirs();
        String archivo = "resultados/java_semilla_" + semilla + ".csv";

        try (PrintWriter salida = new PrintWriter(archivo)) {
            salida.println("n,x,u");
            for (int n = 1; n <= cantidad; n++) {
                long x = generador.siguiente();
                double u = generador.normalizar(x);
                salida.println(n + "," + x + "," + String.format(Locale.US, "%.10f", u));
            }
        }

        System.out.println("[Java]   semilla=" + semilla + "  valores=" + cantidad + "  -> " + archivo);
    }
}
