"""
====================================
Restricciones de Programación Horaria a Nivel de Sucursal
====================================

Esta función define las restricciones a nivel de la sucursal y de los trabajadores individuales para la generación de la programación horaria. Asegura que se cumplan las restricciones, como la asignación de al menos un empleado cuando la demanda sea mayor o igual a uno en una franja horaria específica.

Función Principal
-----------------
"""

from .worker import set_constraints_worker
from ..utils.time import FRANJAS, POSIBLES_ESTADOS
from ortools.sat.python import cp_model


def set_branch_contraints(model: cp_model.CpModel,
                          demanda: dict,
                          trabajadores: dict) -> dict:
    """
    Define las restricciones de programación horaria para los trabajadores de una sucursal.

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.

    demanda : dict
        Un diccionario de diccionarios que especifica la demanda horaria. 
        La primera clave es el día y dentro de ella se encuentran las franjas horarias. 
        Los valores son enteros que representan la demanda en ese día y franja horaria.

    trabajadores : dict
        Un diccionario que describe a los trabajadores disponibles. 
        La primera clave es el documento del trabajador y el valor es el tipo de contrato.

    Retorno
    -------
    variables : dict
        Un diccionario que contiene las variables de interés definidas como variables booleanas de la clase `model.NewBoolVar` con índices (trabajador, día, franja, estado).

    Ejemplo de Uso
    -------------
    >>> variables = set_branch_contraints(model, demanda_horaria, lista_trabajadores)
    >>> print(variables)

    """
    franjas = FRANJAS
    posibles_estados = POSIBLES_ESTADOS
    days = demanda.keys()

    # Creación de variables
    variables = {}
    for trabajador in trabajadores:
        for day in days:
            for franja in franjas:
                for estado in posibles_estados:
                    index = (trabajador, day, franja, estado)
                    name_var = f"{trabajador}-{day}-{franja}-{estado}"
                    variables[index] = model.NewBoolVar(name_var)
                    
    # Debe haber al menos un trabajador en cada franja horaria que tenga una demanda mayor o igual a uno
    for day in days:
        for franja in franjas:
            if demanda[day][franja] >= 1:
                model.AddAtLeastOne(variables[(t, day, franja, 'Trabaja')] for t in trabajadores)


    # Agregar restricciones a nivel de trabajador
    for trabajador in trabajadores:
        variables_trabajador = {}
        for day in days: 
            for franja in franjas:
                for estado in posibles_estados:
                    variables_trabajador[(day, franja, estado)] = variables[(trabajador, day, franja, estado)]
        set_constraints_worker(model, variables_trabajador, contrato=trabajadores[trabajador])

    return variables