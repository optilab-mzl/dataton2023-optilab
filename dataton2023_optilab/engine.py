import pandas as pd
from .utils.time import F2H, FRANJAS
from .utils.load import load_demanda
from ortools.sat.python import cp_model
from .constraints import set_program_workers_constraints, set_optmization

def main(df_demanda,df_workers, df_path_out):

    model = cp_model.CpModel()
    demanda = load_demanda(df_demanda)

    trabajadores = list(df_workers['documento'].unique())
    franjas = FRANJAS
    posibles_estados = ["Trabaja", "Pausa Activa", "Almuerza", "Nada"]
    psibles_estados_wn = ["Trabaja", "Pausa Activa", "Almuerza"]

    
    variables = set_program_workers_constraints(model, demanda, trabajadores,
                                     franjas, posibles_estados,
                                      psibles_estados_wn)

    set_optmization(model, demanda, trabajadores, variables)


    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    solver.log_callback = print  # (str)->None
    solver.parameters.num_search_workers = 7

    solver.Solve(model)

    resultado_trabajador = []
    resultado_franja = []
    resultado_estado = []
    for trabajador in trabajadores:
        for franja in franjas:
            for estado in posibles_estados:
                if solver.Value(variables[(trabajador,franja, estado)]) == 1:
                    resultado_franja.append(franja)
                    resultado_estado.append(estado)
                    resultado_trabajador.append(trabajador)


    restults = pd.DataFrame({'hora_franja':resultado_franja,
                    'estado':resultado_estado,
                    'documento':resultado_trabajador
                    })
    restults['suc_cod'] = 60
    restults['fecha'] = "2024-04-22"
    restults['hora'] = [F2H[f] for f in resultado_franja]
    restults.to_csv(df_path_out, index=False)

    