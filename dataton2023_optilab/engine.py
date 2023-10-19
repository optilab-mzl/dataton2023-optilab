"""
Generates schedule for workers

Usage:
  get_schedule <excel_path> <output_path>
"""
from docopt import docopt
import pandas as pd
from .utils.time import F2H, FRANJAS
from .utils.load import load_demanda, load_workers
from ortools.sat.python import cp_model
#from .constraints import set_program_workers_constraints, set_optmization

from .constraints.branch import set_branch_contraints
from .optimization import set_optmization

def get_schedule(df_demanda, df_workers, df_path_out):

    for branch in df_workers['suc_cod'].unique():
        df_d = df_demanda[df_demanda['suc_cod']==branch]
        df_w = df_workers[df_workers['suc_cod']==branch]
        
        demanda, day2date = load_demanda(df_d, return_day2date=True)
        trabajadores = load_workers(df_w)

        model = cp_model.CpModel()

        franjas = FRANJAS
        posibles_estados = ["Trabaja", "Pausa Activa", "Almuerza", "Nada"]
        
        variables = set_branch_contraints(model, demanda, trabajadores,
                                         franjas, posibles_estados)

    
        set_optmization(model, demanda, variables)

        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        solver.log_callback = print  # (str)->None
        solver.parameters.num_search_workers = 7
        #solver.parameters.set_cp_model_presolve = False

        print(solver.Solve(model))

        days = []
        resultado_trabajador = []
        resultado_franja = []
        resultado_estado = []
        fechas = []
        for i, day in enumerate(demanda.keys()):
            for trabajador in trabajadores:
                for franja in franjas:
                    for estado in posibles_estados:
                        if solver.Value(variables[(trabajador,day,franja, estado)]) == 1:
                            resultado_franja.append(franja)
                            resultado_estado.append(estado)
                            resultado_trabajador.append(trabajador)
                            days.append(day)
                            fechas.append(day2date[day])


        restults = pd.DataFrame({
                        'dia':days,
                        'hora_franja':resultado_franja,
                        'estado':resultado_estado,
                        'documento':resultado_trabajador,
                        'fecha': fechas
                        })
                        
        restults['suc_cod'] = branch

        # fecha = df_demanda['fecha_hora'].iloc[0]
        # restults['fecha'] = f"{fecha.year}-{fecha.month:02d}-{fecha.day:02d}"

        restults['hora'] = [F2H[f] for f in resultado_franja]
        restults.to_csv(df_path_out, index=False)

        break

def main():
    arguments = docopt(__doc__)
    excel_path = arguments['<excel_path>']
    output_path = arguments['<output_path>']

    df_demanda = pd.read_excel(excel_path, sheet_name="demand")
    df_workers = pd.read_excel(excel_path, sheet_name="workers")

    get_schedule(df_demanda, df_workers, output_path)
