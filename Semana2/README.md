# APE2 modelos determinísticos, estocásticos, discretos y continuos

Sistema de estudio: crecimiento poblacional.

```
Semana2/
├── main.py                      # punto de entrada
├── requirements.txt
├── data/datos.py                # arreglo de entrada (editable)
├── simulacion/
│   ├── config.py                # parámetros (P0, r, sigma, dt, tiempo) y estimación de r
│   ├── models/                  # un archivo por modelo
│   │   ├── deterministic.py     # P(t)=P0 e^(rt)
│   │   ├── discrete.py          # P(t+1)=P(t)+rP(t)
│   │   ├── stochastic.py        # + ruido N(0, sigma^2)
│   │   └── continuous.py        # Euler: dP/dt = rP
│   ├── analysis/                # métricas y análisis de sensibilidad
│   ├── visualization/plots.py   # gráficas
│   └── netlogo/bridge.py        # opcional: pyNetLogo
├── outputs/                     # CSV y figuras generadas
└── docs/preguntas_control.md
```

## Ejecución
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py          # o: python main.py --show
```

