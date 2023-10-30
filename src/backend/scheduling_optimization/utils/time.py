"""
=============================================
Definición de constantes temporales y estados
=============================================

Este módulo define constantes y mapeos que se utilizan en todo el sistema. Incluye las siguientes funciones y constantes:

Funciones
---------
1. `generar_franjas(inicio: list, final: list)`: Genera franjas de 15 minutos a partir de una hora de inicio y una hora de final.

Constantes
----------
1. `POSIBLES_ESTADOS`: Una lista de cadenas que representa los posibles estados, como "Trabaja", "Pausa Activa", "Almuerza" y "Nada".

2. `FRANJAS_HORA`: Una lista de franjas horarias en formato de cadena. Se genera utilizando la función `generar_franjas`.

3. `FRANJAS`: Una lista de números enteros que representa las franjas empesando desde 30 = 7:30 y asi sucesivamente.

4. `H2F`: Un diccionario que asigna franjas de tiempo a franjas horarias representadas en enteros. 

5. `F2H`: Un diccionario que asigna franjas de enteros a franjas horarias en formato de cadena.

6. `DAYS2DIAS`: Un diccionario que mapea los nombres de los días de la semana en inglés a sus equivalentes en español, por ejemplo, de 'Monday' a 'Lunes'.

"""


def generar_franjas(inicio: list, final: list):
    """ Genera franjas de 15 minutos a partir de un tiempo de inicio y un tiempo de final.

    Parámetros
    ----------
    inicio: list
        Una lista con dos elementos, donde el primero es la hora y el segundo son los minutos.
    final: list
        Una lista con dos elementos, donde el primero es la hora y el segundo son los minutos.

    Retornos
    --------
    horas: list
        Una lista con las franjas en formato de cadena, en incrementos de 15 minutos.
    """
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
FRANJAS = list(range(30, len(FRANJAS_HORA) + 30))
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
