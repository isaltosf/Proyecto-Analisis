import re
def es_matricula_valida(matricula):
    # Retorna True si cumple el formato y la variedad, False si no.
    return bool(re.match(r"^20(?!(?:.*(\d)\1{3}))\d{7}$", matricula))