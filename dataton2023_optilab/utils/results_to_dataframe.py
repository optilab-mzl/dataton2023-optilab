import pandas as pd
import numpy as np
from collections import defaultdict 
from .time import F2H


def results_to_dataframe(solver, variables, day2date):
    keys = zip(*variables.keys())
    trabajadores, days, franjas, posibles_estados = list(map(np.unique, keys))

    results = defaultdict(list)

    for day in days:
        for trabajador in trabajadores:
            for franja in franjas:
                for estado in posibles_estados:
                    index = trabajador, day,franja, estado
                    variable_value = solver.Value(variables[index]) 
                    if variable_value == 1:
                        results['dia'].append(day)
                        results['hora_franja'].append(franja)
                        results['estado'].append(estado)
                        results['documento'].append(trabajador)
                        results['fecha'].append(day2date[day])

    df = pd.DataFrame(results)
    df['hora'] = df['hora_franja'].apply(lambda f: F2H[f])
    mask = (df['dia'] == "Sábado") & (df['hora_franja'] >= 59)
    df = df[~mask]
    df = df.drop(columns=['dia'])                  
    return df