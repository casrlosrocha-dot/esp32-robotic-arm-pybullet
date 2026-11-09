"""
Consola de estado del brazo: muestra en la terminal lo que envía el ESP32.
Terminal status console: prints the joint commands coming from the ESP32.
"""

import argparse
import math
import time

from serial_link import conectar_serial, leer_datos


def mostrar_estado(datos):
    print("\n" + "=" * 46)
    print("ESTADO DEL BRAZO ROBOTICO / ARM STATUS")
    print("=" * 46)
    print(f"  Joint 1 (base):      {math.degrees(datos['j1']):7.1f} deg")
    print(f"  Joint 2 (hombro):    {math.degrees(datos['j2']):7.1f} deg")
    apertura = datos["grip"] * 1000
    estado = "ABIERTA" if apertura > 25 else "CERRADA"
    print(f"  Pinza:               {apertura:7.1f} mm  ({estado})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    args = ap.parse_args()

    conexion = conectar_serial(args.port)
    if conexion is None:
        return

    validas = invalidas = 0
    try:
        while True:
            datos = leer_datos(conexion)
            if datos is None:
                invalidas += 1
                continue
            validas += 1
            if validas % 10 == 0:          # ~2 veces por segundo
                mostrar_estado(datos)
            time.sleep(0.005)
    except KeyboardInterrupt:
        print(f"\nDetenido. Lecturas validas: {validas} | descartadas: {invalidas}")
    finally:
        conexion.close()


if __name__ == "__main__":
    main()
