"""
Generates schedule for workers

Usage:
  get_schedule <excel_path> <output_path>
"""
from docopt import docopt
import pandas as pd
from .utils.load import load_demanda, load_workers
from ortools.sat.python import cp_model
from .utils.callbacks import SolutionPrinter
from .constraints.branch import set_branch_contraints
from .optimization import set_optmization
from .utils.results_to_dataframe import results_to_dataframe


def get_schedule(df_demanda, df_workers, df_path_out):
    
    dfs_results = []
    best_objective = []
    for branch in df_workers['suc_cod'].unique():

        print("#"*20, branch, "#"*20)

        df_d = df_demanda[df_demanda['suc_cod']==branch]
        df_w = df_workers[df_workers['suc_cod']==branch]
        
        demanda, day2date = load_demanda(df_d, return_day2date=True)
        trabajadores = load_workers(df_w)

        model = cp_model.CpModel()

        variables = set_branch_contraints(model, demanda, trabajadores)

        set_optmization(model, demanda, variables)
        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        solver.log_callback = print  # (str)->None
        solver.parameters.num_search_workers = 0
        solver.parameters.random_seed = 42
        solver.parameters.preferred_variable_order = 0
        solver.parameters.max_time_in_seconds = 360
        solver.parameters.detect_table_with_cost = True
        solver.parameters.linearization_level = 1
        #solver.parameters.search_branching = cp_model.FIXED_SEARCH
        #solver.parameters.use_lns_only = True 
        solver.parameters.num_violation_ls = 1
        solver.parameters.initial_polarity = 1
        #model.ExportToFile('some_filename.pbtxt')
        # Enumerate all solutions.
        #solver.parameters.enumerate_all_solutions = True
        model.set_cp_model_presolve = True
        max_no_improvement=10
        solution_printer = SolutionPrinter(model, max_no_improvement)
        status = solver.SolveWithSolutionCallback(model, solution_printer)

        print(status)
        best_bound = solver.ObjectiveValue()
        best_objective.append(best_bound)

        results = results_to_dataframe(solver, variables, day2date)
        
        results['suc_cod'] = branch
        dfs_results.append(results)

    dfs_results = pd.concat(dfs_results)
    dfs_results.to_csv(df_path_out, index=False)
    print(sum(best_objective), best_objective)
     

def main():
    arguments = docopt(__doc__)
    excel_path = arguments['<excel_path>']
    output_path = arguments['<output_path>']

    df_demanda = pd.read_excel(excel_path, sheet_name="demand")
    df_workers = pd.read_excel(excel_path, sheet_name="workers")

    get_schedule(df_demanda, df_workers, output_path)
