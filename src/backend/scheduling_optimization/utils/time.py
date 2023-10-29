def generar_franjas(inicio, final):
    horas = []
    hora, minuto = inicio
    while (hora, minuto) <= final:
        horas.append(f"{hora:02d}:{minuto:02d}")
        if minuto + 15 >= 60:
            hora += 1
            minuto = 0
        else:
            minuto += 15
    return horas


POSIBLES_ESTADOS = ["Trabaja", "Pausa Activa", "Almuerza", "Nada"]
FRANJAS_HORA = generar_franjas((7, 30), (19, 30))
FRANJAS = list(range(30, len(FRANJAS_HORA)+30))
H2F = {h: f for f, h in zip(FRANJAS, FRANJAS_HORA)}
F2H = {f: h for f, h in zip(FRANJAS, FRANJAS_HORA)}

DAYS2DIAS = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'}
