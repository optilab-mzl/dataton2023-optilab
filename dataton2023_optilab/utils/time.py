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


FRANJAS = list(range(30,76))
H2F = {h:f for f,h in zip(FRANJAS, generar_franjas((7,30), (18,45)))}
F2H = {f:h for f,h in zip(FRANJAS, generar_franjas((7,30), (18,45)))}