"""Pruebas del parser serial (no necesitan el ESP32). Run: python -m pytest"""

import os
import sys
import types

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))

# Permite correr las pruebas aunque pyserial no esté instalado
if "serial" not in sys.modules:
    try:
        import serial  # noqa: F401
    except ImportError:
        fake = types.ModuleType("serial")
        fake.Serial = object
        fake.SerialException = Exception
        sys.modules["serial"] = fake

from serial_link import parsear_linea  # noqa: E402


def test_linea_valida():
    assert parsear_linea("j1:0.512,j2:-1.204,grip:0.031\r\n") == {
        "j1": 0.512, "j2": -1.204, "grip": 0.031}


def test_extremos_del_firmware():
    assert parsear_linea("j1:-2.500,j2:2.000,grip:0.050") is not None
    assert parsear_linea("j1:2.500,j2:-2.000,grip:0.000") is not None


def test_linea_incompleta():
    # p. ej. al abrir el puerto a mitad de una línea
    assert parsear_linea("2:-1.204,grip:0.031") is None
    assert parsear_linea("") is None


def test_valor_corrupto():
    assert parsear_linea("j1:0.5x,j2:0.1,grip:0.01") is None


def test_fuera_de_rango():
    assert parsear_linea("j1:3.5,j2:0.0,grip:0.01") is None
    assert parsear_linea("j1:0.0,j2:0.0,grip:0.2") is None
