"""
============================
Obtiene los resultados en formato dataframe
============================

Este módulo contiene una función para extraer los resultados de un solucionador y representarlos en un DataFrame de pandas.
"""
import pandas as pd
import numpy as np
from collections import defaultdict
from .time import F2H
from ortools.sat.python import cp_model


def results_to_dataframe(solver: cp_model.CpSolver,
                         variables: dict, day2date: dict) -> pd.DataFrame:
    """
    Extrae y representa los resultados en un DataFrame de pandas.

    Parámetros
    ----------
    solver : cp_model.CpSolver
        El solucionador que contiene la solución del modelo de optimización.
    variables : dict
        Un diccionario que contiene las variables de interés definidas como variables booleanas de la clase `model.NewBoolVar` con índices (trabajador, día, franja, estado).
    day2date : dict
        Un diccionario que mapea días de la semana a fechas.

    Retorno
    -------
    results_df : pd.DataFrame
        Un DataFrame que contiene los resultados extraídos de las variables del solucionador.
        Incluye información sobre el día, hora, estado, trabajador, fecha y hora en formato legible.
    """
    # Extraer listas únicas de trabajadores, días, franjas horarias y estados de las variables.
    keys = zip(*variables.keys())
    trabajadores, days, franjas, posibles_estados = list(map(np.unique, keys))

    # Inicializar un diccionario de resultados.
    results = defaultdict(list)

    # Iterar a través de las variables y agregar los resultados al diccionario.
    for day in days:
        for trabajador in trabajadores:
            for franja in franjas:
                for estado in posibles_estados:
                    index = trabajador, day, franja, estado
                    variable_value = solver.Value(variables[index])
                    if variable_value == 1:
                        results['dia'].append(day)
                        results['hora_franja'].append(franja)
                        results['estado'].append(estado)
                        results['documento'].append(trabajador)
                        results['fecha'].append(day2date[day])

    # Crear un DataFrame a partir de los resultados.
    df = pd.DataFrame(results)

    # Agregar una columna 'hora' convertida de la franja horaria utilizando la función F2H.
    df['hora'] = df['hora_franja'].apply(lambda f: F2H[f])

    # Filtrar las filas donde el día sea "Sábado" y la franja horaria sea mayor o igual a 59.
    mask = (df['dia'] == "Sábado") & (df['hora_franja'] >= 59)
    df = df[~mask]

    # Eliminar la columna 'dia' del DataFrame final.
    results_df = df.drop(columns=['dia'])

    return results_df
