from docopt import docopt
import pandas as pd
from .utils.load import load_demanda, load_workers
from ortools.sat.python import cp_model
from .constraints.branch import set_branch_contraints
from .optimization import set_optmization
from .utils.results_to_dataframe import results_to_dataframe


def get_schedule(demanda, trabajadores):

    demanda, day2date = load_demanda(demanda, return_day2date=True)
    trabajadores = load_workers(trabajadores)

    model = cp_model.CpModel()
    variables = set_branch_contraints(model, demanda, trabajadores)
    set_optmization(model, demanda, variables)
    solver = cp_model.CpSolver()

    solver.parameters.log_search_progress = True
    solver.log_callback = print 
    solver.parameters.num_search_workers = 0
    solver.parameters.random_seed = 42
    solver.parameters.preferred_variable_order = 0
    solver.parameters.max_time_in_seconds = 360
    solver.parameters.detect_table_with_cost = True
    solver.parameters.linearization_level = 1
    solver.parameters.num_violation_ls = 1
    solver.parameters.initial_polarity = 1
    model.set_cp_model_presolve = True
    status = solver.Solve(model)
    print(status)
    best_bound = solver.ObjectiveValue()
    results = results_to_dataframe(solver, variables, day2date)
    
    results_dict = results.to_json(orient="records", 
                                   date_format='iso', index=False)
                                   
    return results_dict, best_bound

