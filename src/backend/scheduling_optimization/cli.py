"""
Genera un horario de trabajadores basado en la demanda.

Usage:
  get_schedule <ruta_excel> <ruta_salida> [--time_seconds=<time_seconds>] [--workers=<workers>]

Arguments:
  <ruta_excel>      Ruta al archivo Excel que contiene los datos de la demanda y los trabajadores.
  <ruta_salida>     Ruta para el archivo CSV de salida.

Options:
  --time_seconds=<time_seconds>    Tiempo en segundo para cada sucursal para terminar el proceso de búsqueda [default: 380]
  --workers=<workers>              Número de workers (procesadores) para usar búsqueda paralela [default: cpu_count]
  -h, --ayuda                      Muestra este mensaje de ayuda y sale.

"""
from docopt import docopt
from .engine import get_schedule
import pandas as pd
from tqdm import tqdm
from ortools.sat.python import cp_model
import multiprocessing


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)

    def on_solution_callback(self):
        """
        Función de devolución de llamada para mostrar la mejor solución actual.
        """
        current_solution = self.ObjectiveValue()
        log = f"Mejor solución hasta ahora: {current_solution}"
        tqdm.write(log)


def main():
    arguments = docopt(__doc__)
    excel_path = arguments['<ruta_excel>']
    output_path = arguments['<ruta_salida>']
    max_time_in_seconds = int(arguments['--time_seconds'])

    num_search_workers = arguments['--workers']

    if num_search_workers == "cpu_count":
        num_search_workers = multiprocessing.cpu_count()
    else:
        num_search_workers = int(num_search_workers)

    # Leer datos de demanda y trabajadores desde el archivo Excel
    df_demanda = pd.read_excel(excel_path, sheet_name="demand")
    df_workers = pd.read_excel(excel_path, sheet_name="workers")

    sucursales = df_demanda['suc_cod'].unique()

    barra_progreso = tqdm(sucursales, desc="Progreso", ascii=True, ncols=100)
    resultados_dfs = []
    resultados_objetivos = {}
    for sucursal in barra_progreso:
        barra_progreso.set_description(f"Procesando sucursal {sucursal}")
        tqdm.write(f"Sucursal: {sucursal}")

        # Filtrar datos para la sucursal actual
        df_d = df_demanda[df_demanda['suc_cod'] == sucursal]
        demanda = df_d[['fecha_hora', 'demanda']].to_dict(orient="records")

        df_w = df_workers[df_workers['suc_cod'] == sucursal]
        trabajadores = df_w[['documento', 'contrato']].to_dict(orient="records")

        solution_printer = SolutionPrinter()

        # Llamar a la función de programación con los argumentos apropiados
        programacion_dict, mejor_objetivo = get_schedule(
            demanda, trabajadores,
            log_search_progress=False,
            solution_printer=solution_printer,
            max_time_in_seconds=max_time_in_seconds,
            return_best_objective=True,
            preferred_variable_order=1,
            num_search_workers=num_search_workers,
            variable_selection_strategy=0,
            domain_reduction_strategy=0,
            linearization_level=20,
            num_violation_ls=2,
            violation_ls_perturbation_period=1,
            #min_num_lns_workers=8,
            #shared_tree_num_workers=0,
            interleave_search=False,
            detect_table_with_cost=False, 
            initial_polarity=0,
            #search_branching=0,
            exploit_best_solution=True,
            exploit_relaxation_solution=True,
            set_cp_model_presolve=True,
            cp_model_probing_level=2,
            use_optional_variables=True, 
        )

        df = pd.DataFrame(programacion_dict)
        df['suc_cod'] = sucursal
        resultados_dfs.append(df)
        resultados_objetivos[sucursal] = mejor_objetivo

        tqdm.write(f"Valor final: {mejor_objetivo} \n")

    print("Resultados:\n")
    for suc, val in resultados_objetivos.items():
        print(f"Sucursal {suc}: {val}")

    print("\nTotal: ", sum(resultados_objetivos.values()), "\n")
    print("Archivo de salida: ", output_path)

    resultado = pd.concat(resultados_dfs)
    resultado.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()