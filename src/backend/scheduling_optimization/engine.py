"""
==================================
Generador de Programación Horaria
==================================

Este módulo proporciona una función principal que genera la programación horaria de los trabajadores de una sucursal teniendo en cuenta las restricciones laborales definidas.

Función Principal
-----------------
"""
from .utils.load import transform_demanda, transform_workers
from ortools.sat.python import cp_model
from .constraints.branch import set_branch_contraints
from .optimization import set_optmization
from .utils.results_to_dataframe import results_to_dataframe
import multiprocessing


def get_schedule(demanda: list[dict], trabajadores: list[dict],
                 log_search_progress=True, log_callback=print,
                 num_search_workers=multiprocessing.cpu_count(),
                 random_seed=42,
                 preferred_variable_order=1,
                 max_time_in_seconds=360,
                 detect_table_with_cost=False,
                 linearization_level=1,
                 num_violation_ls=1,
                 initial_polarity=1,
                 set_cp_model_presolve=True,
                 return_best_objective=False,
                 solution_printer=None,
                 variable_selection_strategy=2,
                 domain_reduction_strategy=3,
                 violation_ls_perturbation_period=100,
                 shared_tree_num_workers=0,
                 min_num_lns_workers=2,
                 interleave_search=False,
                 search_branching=0,
                 exploit_best_solution=False,
                 exploit_relaxation_solution=False,
                 cp_model_probing_level=2,
                 use_optional_variables=False,
                 )-> list[dict]:
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
        El número de trabajadores de búsqueda paralela (predeterminado: cpu_count).

    random_seed : int, opcional
        Una semilla para controlar la aleatoriedad en la búsqueda (predeterminado: 42).

    preferred_variable_order : int, opcional
        El orden de variables preferido en la búsqueda (predeterminado: 1).

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
    
    return_best_objective: bool, opcional
        Indica se de debe retorna el mejor valor alcanzado en la optimización (predeterminado: False).
    
    solution_printer: function
        Una función para mostrar los resultados de forma personalizada (predeterminado: None)

    Retorna
    -------
    results_dict : list
        Una lista de diccionarios que contiene la programación generada. 
        Cada diccionario incluye las claves 'hora_franja', 'estado', 'documento', 'fecha' y 'hora'.
        'hora_franja' es una franja horaria (valor entero), 'estado' es el estado del empleado en ese momento (Trabaja, Pausa Activa, Almuerza, Nada), 
        'documento' es el ID del empleado, 'fecha' es la fecha correspondiente a la programación y 'hora' es la hora correspondiente a la franja horaria.

    best_objective: int 
        Si return_best_objective es igual a True. Es el mejor valor alcanzado en la optimización 

    Ejemplo de Uso
    -------------
    >>> programacion = get_schedule(demanda_horaria, lista_trabajadores)
    >>> print(programacion)

    Referencias
    -----------

    .. [1] `Parámetros de cp_model de ortools`_

    .. [2] `Parámetros del solver de ortools`_

    .. _`Parámetros de cp_model de ortools`: https://github.com/google/or-tools/blob/stable/ortools/sat/cp_model.proto

    .. _`Parámetros del solver de ortools`: https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto

    """
    demanda, day2date = transform_demanda(demanda, return_day2date=True)
    trabajadores = transform_workers(trabajadores)

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
    solver.parameters.violation_ls_perturbation_period = violation_ls_perturbation_period
    solver.parameters.shared_tree_num_workers = shared_tree_num_workers
    solver.parameters.min_num_lns_workers = min_num_lns_workers
    solver.parameters.interleave_search = interleave_search
    solver.parameters.search_branching = search_branching
    solver.parameters.exploit_best_solution = exploit_best_solution
    solver.parameters.exploit_relaxation_solution = exploit_relaxation_solution
    solver.parameters.cp_model_probing_level = cp_model_probing_level
    solver.parameters.use_optional_variables = use_optional_variables

    model.variable_selection_strategy = variable_selection_strategy
    model.set_cp_model_presolve = set_cp_model_presolve
    model.domain_reduction_strategy = domain_reduction_strategy

    #solver.Solve(model)

    status = solver.SolveWithSolutionCallback(model, solution_printer)
    best_objective = solver.ObjectiveValue()
    results = results_to_dataframe(solver, variables, day2date)
    
    results_dict = results.to_dict(orient="records")

    if best_objective:
        return results_dict, best_objective
    return results_dict