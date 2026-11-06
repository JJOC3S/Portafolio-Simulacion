"""Compara las salidas de Python y Java (misma secuencia y mismos estadísticos).

Ejecutar desde la raíz del proyecto, después de correr ambos programas:
    python python/comparar.py
"""
import csv
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(RAIZ, "resultados")


def leer(ruta):
    with open(ruta, newline="") as f:
        return list(csv.DictReader(f))


def main():
    # 1) Secuencia
    py = leer(os.path.join(RES, "secuencia_python.csv"))
    jv = leer(os.path.join(RES, "secuencia_java.csv"))
    iguales = len(py) == len(jv) and all(
        a["X"] == b["X"] and a["U"] == b["U"] for a, b in zip(py, jv))
    print(f"Secuencia ({len(py)} números): {'IDÉNTICA en Python y Java' if iguales else 'DIFERENTE'}")

    # 2) Estadísticos
    rp = leer(os.path.join(RES, "resultados_python.csv"))
    rj = leer(os.path.join(RES, "resultados_java.csv"))
    max_dif = 0.0
    misma_decision = True
    print(f"\n{'Exp.':<16}{'Cfg':<5}{'N':>9}{'Δchi2':>12}{'Δp(chi2)':>12}{'ΔD':>12}{'Δp(KS)':>12}")
    for a, b in zip(rp, rj):
        assert (a["experimento"], a["configuracion"], a["N"]) == (
            b["experimento"], b["configuracion"], b["N"]), "Filas desalineadas"
        difs = [abs(float(a[k]) - float(b[k])) for k in ("chi2", "p_chi2", "D", "p_ks")]
        max_dif = max(max_dif, *difs)
        misma_decision &= (a["decision_chi2"] == b["decision_chi2"]
                           and a["decision_ks"] == b["decision_ks"])
        print(f"{a['experimento']:<16}{a['configuracion']:<5}{a['N']:>9}"
              + "".join(f"{d:>12.2e}" for d in difs))
    print(f"\nMáxima diferencia absoluta entre lenguajes: {max_dif:.2e}")
    print(f"Mismas decisiones estadísticas: {'SÍ' if misma_decision else 'NO'}")


if __name__ == "__main__":
    main()
