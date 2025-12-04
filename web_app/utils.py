def clasificar_consulta(texto):
    texto = texto.lower()

    # VACANTES / INSCRIPCIONES
    palabras_vacantes = ["inscribir", "inscripcion", "vacante", "cupos", "matricula"]
    if any(p in texto for p in palabras_vacantes):
        return "vacantes"

    # SALUD / ALERGIAS
    palabras_salud = ["alergia", "alergico", "asma", "medicacion", "salud"]
    if any(p in texto for p in palabras_salud):
        return "salud"

    # COMERCIAL / PRECIOS
    palabras_comercial = ["precio", "cuota", "pago", "costo", "arancel"]
    if any(p in texto for p in palabras_comercial):
        return "comercial"

    # HORARIOS
    palabras_horario = ["horario", "entrada", "salida", "jornada", "turno"]
    if any(p in texto for p in palabras_horario):
        return "horario"

    # GENERAL
    return "general"
