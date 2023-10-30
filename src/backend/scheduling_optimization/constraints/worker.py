"""
====================================
Restricciones de Programación Horaria a Nivel de Trabajador
====================================

Esta función define las restricciones a nivel de trabajador y de los días individuales para la generación de la programación horaria. Asegura que se cumplan las restricciones, como la asignación de una hora fija de inicio y finalización de la jornada laboral y los tiempos de almuerrzo en toda la semana.

Función Principal
-----------------
"""
from .day import set_constraints_day
import numpy as np
from ortools.sat.python import cp_model


def set_constraints_worker(model: cp_model.CpModel,
                           variables: dict, contrato='TC'):
    """
    Define las restricciones de programación horaria para un trabajador de una sucursal.

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.

    variables : dict
         Un diccionario que contiene las variables de interés a nivel de trabajador definidas como variables booleanas de la clase `model.NewBoolVar` con índices (día, franja, estado). 

    contrato: str
        Tipo de contrato del trabajador (TC, MT) (predeterminado: TC)
    """
    days, franjas, estados = zip(*variables.keys())

    days = np.unique(days)
    franjas = np.unique(franjas)
    estados = np.unique(estados)
    
    for day in days:
    
        if contrato == "MT":
            numero_franjas_trabajo = 16 
        elif contrato == "TC" and day == 'Sábado':
            numero_franjas_trabajo = 20
        else:
            numero_franjas_trabajo = 28

        variables_day = {}
        for franja in franjas:
            for estado in estados:
                variables_day[(franja, estado)] = variables[(day, franja, estado)]
            
        set_constraints_day(model, variables_day, day, numero_franjas_trabajo)

    #De lunes a viernes deben tener el mismo horarario de inicio
    dasy_no_s = list(days)
    dasy_no_s.remove('Sábado')
    
    for f in franjas:
        first_value = variables[(dasy_no_s[0], f, 'Nada')] 
        for day in dasy_no_s[1:]:
            model.Add(variables[(day, f, 'Nada')] == first_value)

    # Almuerzo constante para los de tiempo completo
    if contrato == "TC":
        for f in franjas:
            first_value = variables[(dasy_no_s[0], f, 'Almuerza')] 
            for day in dasy_no_s[1:]:
                model.Add(variables[(day, f, 'Almuerza')] == first_value)