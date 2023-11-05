"""
====================
Problema de optimización
====================

El problema de optimización se establece como minimizar la diferencia entre la demanda y la capacidad, solo cuando la demanda es mayor que la capacidad.

.. math::
    
    P^* = \\arg \max_{P} \sum_d \sum_f \max(0, D_{d,f}- \sum_t P^{+}_{t,d,f})

   \\text{Sujeto a } C_1(P) \land C_2(P) \land \dots \land  C_n(P)

Donde:

- :math:`P` : Programación semanal para los trabajadores de una sola sucursal.
- :math:`D` : Demanda en cada dìa y franja de la semana.
- :math:`d` : Día de la semana.
- :math:`f` : Franja del día.
- :math:`t` : Trabjador.
"""
import numpy as np 
from ortools.sat.python import cp_model


def set_optmization(model: cp_model.CpModel, 
                    demanda: dict, variables: dict)-> None:
    """ Define el problema de optimización en el modelo de cp-sat

    Parámetros
    ----------
    model :
        modelo cp-sat 
    demanda :
        Dicccionario con las demandas por día y por franja horaria.
    variables:
        Diccionario con las variables de interes del problema de optimización.
    """
    trabajadores, days, franjas, _ = zip(*variables.keys())

    trabajadores = np.unique(trabajadores)
    days = np.unique(days)
    franjas = np.unique(franjas)
    restas = []

    for day in days: 
        for franja in franjas:

            demanda_day_franja = demanda[day][franja]

            if demanda_day_franja > 0:

                trabjadores_en_franja = sum(variables[(t, day, franja, 'Trabaja')] for t in trabajadores)
            
                resta = model.NewIntVar(0, demanda_day_franja, '')
                damanda_menos_capacidad = demanda_day_franja - trabjadores_en_franja
                capacidad_menos_demanda = trabjadores_en_franja - demanda_day_franja
                # Solo interesa cuando es positivo (Demanda màs alta que capacidad)
                model.AddMaxEquality(resta, [0, damanda_menos_capacidad])

                restas.append(resta)

    objetivo = sum(restas)
    model.Minimize(objetivo)
