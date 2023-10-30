"""
Genera gráficos de programación y capacidad vs. demanda.

Usage:
  get_plot <tipo> <archivo_csv> <código_sucursal> [--dia=<día>] [--demand_csv=archivo_demanda]

Arguments:
  <tipo>              Tipo de gráfico que se generará. Puede ser "schedule" para gráficos de programación o "capacity_vs_demand" para gráficos de capacidad vs. demanda.
  <archivo_csv>       Ruta al archivo CSV que contiene los datos de programación.
  <código_sucursal>   Código de la sucursal para la cual se generará el gráfico.
  
Options:
  --dia=<día>                     (Opcional) Día específico para el que se generará un gráfico de programación.
  --demand_csv=archivo_demanda    (Opcional) Ruta al archivo de demanda (en formato Excel) que se utilizará para gráficos de capacidad vs. demanda.
"""
from docopt import docopt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from .time import F2H, DAYS2DIAS
from .load import transform_demanda
from datetime import datetime
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt

# Constante que mapea días de la semana a números para ordenarlos
VALORES_DIAS = {
    "Lunes": 1,
    "Martes": 2,
    "Miércoles": 3,
    "Jueves": 4,
    "Viernes": 5,
    "Sábado": 6,
}


def schedule_day(df_schedule: pd.DataFrame, day: str = None, 
                 ax: plt.Axes = None, title: str = None) -> None:
     """
    Genera un gráfico de programación para un día específico.

    Parámetros
    ----------
    df_schedule : pd.DataFrame
        El DataFrame que contiene los datos de programación.
    day : str, opcional
        El día para el cual se generará el gráfico de programación.
    ax : plt.Axes, opcional
        El eje en el que se dibujará el gráfico.
    title : str, opcional
        El título del gráfico.

    Retorno
    -------
    None
    """
    df = df_schedule.copy()
    if day:
        df = df[df['dia']==day]
    
    df['hora_franja'] = df['hora_franja'].apply(lambda x: f"{x}-{F2H[x]}")

    pivot_df = df.pivot_table(index='hora_franja', 
                             columns='documento',
                             values='estado', aggfunc='first')

    # Map categorical values to integers
    cmap = sns.color_palette(['green', 'blue', 'red', 'gray'])
    state_mapping = {'Trabaja': 0, 'Almuerza': 1, 'Pausa Activa': 2, 'Nada':3}
    mapped_data = pivot_df.replace(state_mapping)

    show = False
    if not ax:
        fig, ax = plt.subplots(figsize=(8, 9))
        show = True
    
    sns.heatmap(mapped_data, cmap=cmap, annot=False, fmt='',
                 cbar=False, linewidths=0.5, ax=ax)

    ax.set_title(f'Cronograma {day}')
    ax.set_xlabel('Empleado')
    ax.set_ylabel('Franja')
    plt.suptitle(title)
    if show:
        plt.tight_layout()
        plt.show()


def schedule_week(df_schedule: pd.DataFrame,
                  axes: list = [], title: str = None) -> None:
    """
    Genera gráficos de programación para toda la semana.

    Parámetros
    ----------
    df_schedule : pd.DataFrame
        El DataFrame que contiene los datos de programación.
    axes : list, opcional
        Una lista de ejes en la que se dibujarán los gráficos diarios.
    title : str, opcional
        El título de los gráficos.

    Retorno
    -------
    None
    """
    df = df_schedule  # No need to create a copy

    # Get unique days for iterating
    unique_days = df['dia'].unique()
    unique_days = sorted(unique_days, key=lambda x: VALORES_DIAS[x])

    show = False
    if not any(axes):
        fig, axes = plt.subplots(1,6,figsize=(8, 9), sharey=True)
        show = True

    axes = axes[::-1]
    for i, day in enumerate(unique_days[::-1]):
        ax = axes[i]
        # Create the heatmap in the current subplot
        schedule_day(df_schedule, day=day, ax=ax)
    plt.suptitle(title)
    # Adjust the overall figure layout
    if show:
        plt.tight_layout()
        plt.show()


def load_capacidad_demanda(df_schedule: pd.DataFrame,
                           df_demand: pd.DataFrame
                           ) -> (pd.Series, dict):
    """
    Carga datos de capacidad y demanda para su posterior representación en gráficos.

    Parámetros
    ----------
    df_schedule : pd.DataFrame
        El DataFrame que contiene los datos de programación.
    df_demand : pd.DataFrame
        El DataFrame que contiene los datos de demanda.

    Retorno
    -------
    capacidad : pd.Series
        Datos de capacidad.
    demanda : dict
        Datos de demanda.
    """
    df = df_schedule[['hora_franja','estado']].copy()
    df['estado'] = df['estado'] == "Trabaja"
    capacidad = df.groupby('hora_franja').sum()
    demanda = transform_demanda(df_demand)
    return capacidad, demanda


def plot_capacidad_vs_demand(capacidad: pd.Series,
                             demanda: dict, ax: plt.Axes,
                             title: str = None) -> None:
    """
    Genera un gráfico de capacidad vs. demanda para un día específico.

    Parámetros
    ----------
    capacidad : pd.Series
        Datos de capacidad.
    demanda : dict
        Datos de demanda.
    ax : matplotlib.axes._subplots.AxesSubplot
        El eje en el que se dibujará el gráfico.
    title : str, opcional
        El título del gráfico.

    Retorno
    -------
    None
    """
    # Plot 'oferta' data asb ars
    hora = [F2H[f] for f in demanda.keys()]
    ax.step(hora[:len(capacidad)], capacidad['estado'], label='Capacidad', color='red',
                    where= 'mid', linestyle='-')  # Discrete lines for 'Demanda'
    # Plot 'demanda' data as bars
    ax.bar(hora, demanda.values(), label='Demanda', color='blue')
    ax.tick_params(axis='x', rotation=90)
    # Add labels, title, and legend
    ax.legend()
    ax.set_title(title)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))

    
def capacidad_vs_demanda(df_schedule: pd.DataFrame,
                         df_demand: pd.DataFrame,
                         title: str = None) -> None:
    """
    Genera gráficos de capacidad vs. demanda para toda la semana.

    Parámetros
    ----------
    df_schedule : pd.DataFrame
        El DataFrame que contiene los datos de programación.
    df_demand : pd.DataFrame
        El DataFrame que contiene los datos de demanda.
    title : str, opcional
        El título de los gráficos.

    Retorno
    -------
    None
    """
    demanda_days = transform_demanda(df_demand, complete_franjas=False)

    fig, axes = plt.subplots(2, 6, figsize=(15, 5), sharex=True)

    unique_days = df_schedule['dia'].unique()
    unique_days = sorted(unique_days, key=lambda x: VALORES_DIAS[x])

    for i, day in enumerate(unique_days): 
        ax1 = axes[0, i]
        ax2 = axes[1, i]

        df = df_schedule[df_schedule['dia']==day]
        df = df[['hora_franja','estado']].copy()
        df['estado'] = df['estado'] == "Trabaja"

        capacidad = df.groupby('hora_franja').sum()
        demanda = demanda_days[day]

        plot_capacidad_vs_demand(capacidad, demanda, ax1, title=day)
        plot_diff_capacidad_vs_demanda(capacidad, demanda, ax2)

    _ = [ax.get_legend().remove() for ax in axes[0,:-1]]
    _ = [ax.get_legend().remove() for ax in axes[1,:-1]]

    axes[0,0].set_ylabel('Demanda y capacidad')
    
    axes[1,0].set_ylabel('Demanda - Capacidad')

    plt.tight_layout()
    plt.suptitle(title)

    plt.show()


def plot_diff_capacidad_vs_demanda(capacidad: pd.Series, demanda:dict,
                                   ax: plt.Axes) -> None:
    """
    Genera un gráfico de diferencias entre capacidad y demanda para un día específico.

    Parámetros
    ----------
    capacidad : pd.Series
        Datos de capacidad.
    demanda : dict
        Datos de demanda.
    ax : matplotlib.axes._subplots.AxesSubplot
        El eje en el que se dibujará el gráfico.

    Retorno
    -------
    None
    """
    hora = [F2H[f] for f in demanda.keys()]
    diff = np.array(list(demanda.values()) - capacidad['estado'])
    colors = ['red' if val < 0 else 'blue' for val in diff]

    ax.bar(hora, diff, color=colors)

    legend_labels = ['Baja Capacidad', 'Sobre Capacida']
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color='red'), plt.Rectangle((0, 0), 1, 1, color='blue')]
    ax.legend(legend_handles, legend_labels)

    ax.tick_params(axis='x', rotation=90)
    ax.set_xlabel('Franja')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
    

def transform_date(df: pd.DataFrame) -> pd.DataFrame:
     """
    Transforma la fecha en el DataFrame para su posterior uso en los gráficos.

    Parámetros
    ----------
    df : pd.DataFrame
        El DataFrame que contiene los datos.

    Retorno
    -------
    df : pd.DataFrame
        El DataFrame con la fecha transformada.
    """
    dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
    df['fecha'] = df['fecha'].apply(dateparse)
    df['dia'] = df['fecha'].apply(
        lambda fecha: DAYS2DIAS[fecha.strftime("%A")]
    )
    return df


def main():
    """
    Función principal para el script.

    Parámetros
    ----------
    Ninguno

    Retorno
    -------
    None
    """
    arguments = docopt(__doc__)
    type_ = arguments['<type>']
    csv_path = arguments['<input_csv>']
    demand_csv = arguments['--demand_csv']
    day = arguments['--day']
    branch = arguments['<suc_cod>']

    df_schedule = pd.read_csv(csv_path)
    df_schedule = transform_date(df_schedule)
    df_schedule = df_schedule[df_schedule['suc_cod']==int(branch)]
    title = f"Còdigo Sucursal {branch}"

    if type_ == "schedule":
        if not day:
            schedule_week(df_schedule, title=title)
            #schedule_branchs(df_schedule)
        elif day:
            schedule_day(df_schedule, day, title=title)
    elif type_ == "capacity_vs_demand":
        df_demand = pd.read_excel(demand_csv, sheet_name="demand")
        df_demand = df_demand[df_demand['suc_cod']==int(branch)]
        capacidad_vs_demanda(df_schedule, df_demand, title)


if __name__ == "__main__":
    main()
