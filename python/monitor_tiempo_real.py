"""
Monitor en tiempo real de las articulaciones del brazo.
Real-time plot of the joint commands sent by the ESP32.
"""

import argparse
import math
from collections import deque

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from serial_link import conectar_serial, leer_datos

N = 200  # muestras visibles (~10 s a 20 Hz)

historial = {"j1": deque(maxlen=N), "j2": deque(maxlen=N), "grip": deque(maxlen=N)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    args = ap.parse_args()

    conexion = conectar_serial(args.port)
    if conexion is None:
        print("No se pudo conectar. Verifica el puerto serial.")
        return

    fig, ejes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle("Robotic arm - real-time joint commands")
    config = [
        ("j1", "Base (deg)", (-150, 150)),
        ("j2", "Shoulder (deg)", (-120, 120)),
        ("grip", "Gripper opening (mm)", (0, 55)),
    ]
    lineas = {}
    for ax, (clave, titulo, ylim) in zip(ejes, config):
        ax.set_ylabel(titulo)
        ax.set_ylim(*ylim)
        ax.set_xlim(0, N)
        ax.grid(True)
        lineas[clave], = ax.plot([], [], linewidth=2)
    ejes[-1].set_xlabel("Sample")

    def actualizar(_):
        datos = leer_datos(conexion)
        if datos:
            historial["j1"].append(math.degrees(datos["j1"]))
            historial["j2"].append(math.degrees(datos["j2"]))
            historial["grip"].append(datos["grip"] * 1000)
            for clave, linea in lineas.items():
                linea.set_data(range(len(historial[clave])), list(historial[clave]))
        return tuple(lineas.values())

    _ani = animation.FuncAnimation(fig, actualizar, interval=20, blit=True,
                                   cache_frame_data=False)
    plt.tight_layout()
    plt.show()
    conexion.close()


if __name__ == "__main__":
    main()
