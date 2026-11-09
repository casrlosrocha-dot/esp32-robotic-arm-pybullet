"""
Enlace serial con el ESP32 / Serial link with the ESP32.

El firmware envía una línea por muestra (cada ~50 ms):
The firmware sends one line per sample (every ~50 ms):

    j1:<rad>,j2:<rad>,grip:<m>
    e.g.  j1:0.512,j2:-1.204,grip:0.031
"""

import time

import serial

PUERTO_SERIAL = "COM3"   # Windows: COM3, COM4... | Linux: /dev/ttyUSB0
BAUDIOS = 115200

# Rangos que usa el firmware (ver brazo_esp32.ino)
LIMITES = {
    "j1":   (-2.5, 2.5),    # rad, rotación de la base
    "j2":   (-2.0, 2.0),    # rad, hombro
    "grip": (0.0, 0.05),    # m, apertura de la pinza
}


def conectar_serial(puerto=PUERTO_SERIAL, baudios=BAUDIOS):
    """Abre el puerto y espera a que el ESP32 se reinicie."""
    try:
        conexion = serial.Serial(puerto, baudios, timeout=1)
        time.sleep(2)
        print(f"Conectado a {puerto} @ {baudios} baudios")
        return conexion
    except serial.SerialException as e:
        print(f"Error al conectar: {e}")
        return None


def parsear_linea(linea):
    """Convierte 'j1:0.5,j2:-1.2,grip:0.03' en un diccionario.

    Devuelve None si la línea está incompleta o un valor está fuera de rango.
    """
    datos = {}
    for parte in linea.strip().split(","):
        if ":" not in parte:
            continue
        clave, valor = parte.split(":", 1)
        try:
            datos[clave.strip()] = float(valor)
        except ValueError:
            return None

    if not all(clave in datos for clave in LIMITES):
        return None
    for clave, (minimo, maximo) in LIMITES.items():
        # pequeño margen por redondeo del firmware
        if not (minimo - 1e-3 <= datos[clave] <= maximo + 1e-3):
            return None
    return datos


def leer_datos(conexion):
    """Lee una línea del puerto y la parsea."""
    try:
        linea = conexion.readline().decode("utf-8", errors="ignore")
    except serial.SerialException:
        return None
    return parsear_linea(linea)
