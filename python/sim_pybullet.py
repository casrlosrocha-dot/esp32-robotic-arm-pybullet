"""
Simulación del brazo en PyBullet controlada por el ESP32.
PyBullet simulation of the arm, driven by the ESP32 potentiometers.

Uso / Usage:
    python sim_pybullet.py --port COM3     # con el ESP32 conectado
    python sim_pybullet.py --demo          # sin hardware: movimiento automático
"""

import argparse
import math
import os
import time

import pybullet as p
import pybullet_data

URDF = os.path.join(os.path.dirname(__file__), "..", "urdf", "brazo.urdf")

# Límites del URDF (pueden ser más estrechos que los del firmware)
J2_URDF = 1.57      # rad
DEDO_MAX = 0.02     # m, carrera de cada dedo prismático
GRIP_MAX = 0.05     # m, valor máximo que envía el firmware


def cargar_robot(gui=True):
    p.connect(p.GUI if gui else p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")
    robot = p.loadURDF(URDF, [0, 0, 0], useFixedBase=True)
    juntas = {p.getJointInfo(robot, i)[1].decode(): i for i in range(p.getNumJoints(robot))}
    return robot, juntas


def aplicar(robot, juntas, j1, j2, grip):
    """Lleva las articulaciones a la posición pedida (control de posición)."""
    j2 = max(-J2_URDF, min(J2_URDF, j2))
    dedo = (max(0.0, min(GRIP_MAX, grip)) / GRIP_MAX) * DEDO_MAX
    objetivos = {
        "joint_1": j1,
        "joint_2": j2,
        "joint_dedo_izq": dedo,
        "joint_dedo_der": dedo,
    }
    for nombre, valor in objetivos.items():
        p.setJointMotorControl2(robot, juntas[nombre], p.POSITION_CONTROL,
                                targetPosition=valor, force=100)


def demo(t):
    """Trayectoria suave para probar sin hardware."""
    return 2.0 * math.sin(0.5 * t), 1.0 * math.sin(0.8 * t), 0.025 * (1 + math.sin(1.5 * t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--demo", action="store_true", help="sin ESP32")
    args = ap.parse_args()

    robot, juntas = cargar_robot(gui=True)

    conexion = None
    if not args.demo:
        from serial_link import conectar_serial, leer_datos
        conexion = conectar_serial(args.port)
        if conexion is None:
            print("Sin ESP32: usa --demo para probar la simulación.")
            return

    t0 = time.time()
    try:
        while p.isConnected():
            if args.demo:
                j1, j2, grip = demo(time.time() - t0)
            else:
                datos = leer_datos(conexion)
                if datos is None:
                    continue
                j1, j2, grip = datos["j1"], datos["j2"], datos["grip"]
            aplicar(robot, juntas, j1, j2, grip)
            p.stepSimulation()
            time.sleep(1 / 240)
    except KeyboardInterrupt:
        pass
    finally:
        if conexion is not None:
            conexion.close()


if __name__ == "__main__":
    main()
