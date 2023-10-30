"""
==================================
Generador de Programación Horaria
==================================

Este módulo proporciona una función principal que genera la programación horaria de los trabajadores de una sucursal teniendo en cuenta las restricciones laborales definidas.

Función Principal
-----------------
"""
from .utils.load import load_demanda, load_workers
from ortools.sat.python import cp_model
from .constraints.branch import set_branch_contraints
from .optimization import set_optmization
from .utils.results_to_dataframe import results_to_dataframe


def get_schedule(demanda: list[dict], trabajadores: list[dict],
                 log_search_progress=True, log_callback=print,
                 num_search_workers=0, random_seed=42,
                 preferred_variable_order=0,
                 max_time_in_seconds=360,
                 detect_table_with_cost=True,
                 linearization_level=1,
                 num_violation_ls=1,
                 initial_polarity=1,
                 set_cp_model_presolve=True)-> list[dict]:
    """
    Genera una programación horaria para los trabajadores de una sucursal dada.

    Parámetros
    ----------
    demanda : list[dict]
        Una lista que describe la demanda de personal en la sucursal. 
        Lista de diccionarios con las claves 'fecha_hora' y 'demanda', 
        donde 'fecha_hora' es una fecha en formato ISO y 'demanda' es un entero 
        que representa la demanda en ese momento.

    trabajadores : list[dict]
        Una lista que describe a los trabajadores disponibles. 
        Debe ser una lista de diccionarios con las claves 'documento' y 'contrato', 
        donde 'documento' es el ID del empleado y 'contrato' es el tipo de contrato (TP, MT).

    log_search_progress : bool, opcional
        Indica si se debe registrar el progreso de la búsqueda (predeterminado: True).

    log_callback : function, opcional
        Una función de registro personalizada que se utiliza para registrar el progreso.

    num_search_workers : int, opcional
        El número de trabajadores de búsqueda paralela (predeterminado: 0).

    random_seed : int, opcional
        Una semilla para controlar la aleatoriedad en la búsqueda (predeterminado: 42).

    preferred_variable_order : int, opcional
        El orden de variables preferido en la búsqueda (predeterminado: 0).

    max_time_in_seconds : int, opcional
        El tiempo máximo en segundos para la búsqueda (predeterminado: 360).

    detect_table_with_cost : bool, opcional
        Indica si se debe detectar una tabla de costos (predeterminado: True).

    linearization_level : int, opcional
        El nivel de linearización de restricciones (predeterminado: 1).

    num_violation_ls : int, opcional
        El número de violaciones de búsqueda local (predeterminado: 1).

    initial_polarity : int, opcional
        La polaridad inicial de búsqueda (predeterminado: 1).

    set_cp_model_presolve : bool, opcional
        Indica si se debe utilizar la optimización preprocesada del modelo (predeterminado: True).

    Retorna
    -------
    results_dict : list
        Una lista de diccionarios que contiene la programación generada. 
        Cada diccionario incluye las claves 'hora_franja', 'estado', 'documento', 'fecha' y 'hora'.
        'hora_franja' es una franja horaria (valor entero), 'estado' es el estado del empleado en ese momento (Trabaja, Pausa Activa, Almuerza, Nada), 
        'documento' es el ID del empleado, 'fecha' es la fecha correspondiente a la programación y 'hora' es la hora correspondiente a la franja horaria.

    Ejemplo de Uso
    -------------
    >>> programacion = get_schedule(demanda_horaria, lista_trabajadores)
    >>> print(programacion)

    """
    demanda, day2date = load_demanda(demanda, return_day2date=True)
    trabajadores = load_workers(trabajadores)

    model = cp_model.CpModel()
    variables = set_branch_contraints(model, demanda, trabajadores)
    set_optmization(model, demanda, variables)
    solver = cp_model.CpSolver()

    solver.parameters.log_search_progress = log_search_progress
    solver.log_callback = log_callback
    solver.parameters.num_search_workers = num_search_workers
    solver.parameters.random_seed = random_seed
    solver.parameters.preferred_variable_order = preferred_variable_order
    solver.parameters.max_time_in_seconds = max_time_in_seconds
    solver.parameters.detect_table_with_cost = detect_table_with_cost
    solver.parameters.linearization_level = linearization_level
    solver.parameters.num_violation_ls = num_violation_ls
    solver.parameters.initial_polarity = initial_polarity
    model.set_cp_model_presolve = set_cp_model_presolve

    solver.Solve(model)
    #print(solver.ObjectiveValue())
    results = results_to_dataframe(solver, variables, day2date)
    
    results_dict = results.to_json(orient="records", 
                                   date_format='iso', index=False)

    return results_dict

