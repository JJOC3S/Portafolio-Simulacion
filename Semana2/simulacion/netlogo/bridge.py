"""Puente OPCIONAL Python -> NetLogo con pyNetLogo.

La guía indica que Python calcula los parámetros y NetLogo los visualiza.
Requiere NetLogo instalado y un modelo .nlogo que defina los globals
`p0`, `r`, `sigma` y los procedimientos `setup` y `go`.
"""


def enviar_a_netlogo(params, ruta_netlogo, ruta_modelo, ticks=None):
    try:
        import pynetlogo
    except ImportError as e:
        raise RuntimeError("Instala pynetlogo: pip install pynetlogo") from e

    nl = pynetlogo.NetLogoLink(gui=True, netlogo_home=ruta_netlogo)
    try:
        nl.load_model(ruta_modelo)
        nl.command(f"set p0 {params.p0}")
        nl.command(f"set r {params.r}")
        nl.command(f"set sigma {params.sigma}")
        nl.command("setup")
        nl.command(f"repeat {ticks or params.tiempo} [ go ]")
        input("Presiona Enter para cerrar NetLogo...")
    finally:
        nl.kill_workspace()
