from .day import set_constraints_day
import numpy as np 


def set_constraints_worker(model, variables):
    days, franjas, estados = zip(*variables.keys())

    days = np.unique(days)
    franjas = np.unique(franjas)
    estados = np.unique(estados)

    for day in days:
        variables_day = {}
        for franja in franjas:
            for estado in estados:
                variables_day[(franja, estado)] = variables[(day, franja, estado)]
        set_constraints_day(model, variables_day)
        