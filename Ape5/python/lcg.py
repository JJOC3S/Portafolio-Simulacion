"""Generador Congruencial Lineal (LCG) en Python.

Relación recursiva:   X(n+1) = (a * X(n) + c) mod m
Valor normalizado:    U(n)   = X(n) / m      (queda en el intervalo [0, 1))

Convención usada (igual en Java): X(0) es la semilla y el primer valor
generado es X(1).
"""

# Parámetros pedidos en la guía
A = 1664525
C = 1013904223
M = 2 ** 32
SEMILLA = 12345


class LCG:
    def __init__(self, semilla=SEMILLA, a=A, c=C, m=M):
        self.a = a
        self.c = c
        self.m = m
        self.x = semilla  # estado actual: X(0) = semilla

    def siguiente(self):
        """Avanza un paso y devuelve el entero X(n+1)."""
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    def generar(self, n):
        """Devuelve una lista de n pares (X, U)."""
        valores = []
        for _ in range(n):
            x = self.siguiente()
            valores.append((x, x / self.m))
        return valores
