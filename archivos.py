import os
from utils import es_matricula_valida

# --------------------------------------------------------------
# Lee todas las líneas de un archivo, limpia saltos y espacios
# --------------------------------------------------------------
def leer_lineas_archivo(path):
    with open(path, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f.readlines()]
    return lineas


# --------------------------------------------------------------
# Procesa y codifica cada línea usando el contexto Strategy
# tipo = "matricula" o "cadena"
# --------------------------------------------------------------
def procesar_lineas(lineas, tipo, contexto, clave=None):
    nuevas_lineas = []
    lineas_invalidas = []

    for idx, linea in enumerate(lineas, start=1):

        # Línea vacía → ignorar
        if not linea:
            lineas_invalidas.append((idx, linea, "Línea vacía"))
            continue

        # Debe ser numérica
        if not linea.isdigit():
            lineas_invalidas.append((idx, linea, "No es numérica"))
            continue

        # Validación específica
        if tipo == "matricula":
            if not es_matricula_valida(linea):
                lineas_invalidas.append((idx, linea, "Matrícula inválida"))
                continue

        # Codificar usando Strategy
        nueva = contexto.ejecutar(linea)
        nuevas_lineas.append(nueva)

    return nuevas_lineas, lineas_invalidas


# --------------------------------------------------------------
# Guarda archivo de salida con mismo nombre + "_codificado"
# --------------------------------------------------------------
def guardar_archivo_salida(path_original, nuevas_lineas):
    nombre, ext = os.path.splitext(path_original)
    nuevo_path = nombre + "_codificado" + ext

    with open(nuevo_path, "w", encoding="utf-8") as f:
        for linea in nuevas_lineas:
            f.write(linea + "\n")

    return nuevo_path
