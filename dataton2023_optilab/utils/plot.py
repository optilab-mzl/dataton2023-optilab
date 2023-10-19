"""
Generates plots

Usage:
  get_plot <type> <input_csv> [--day=<day>]
"""
from docopt import docopt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
import pandas as pd
from .time import F2H
from .load import load_demanda


def schedule_day(df_schedule, day=None, ax=None):
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

    show =False
    if not ax:
        fig, ax = plt.subplots(figsize=(8, 9))
        show =True
    
    sns.heatmap(mapped_data, cmap=cmap, annot=False, fmt='',
                 cbar=False, linewidths=0.5, ax=ax)

    ax.set_title(f'Cronograma {day}')
    ax.set_xlabel('Empleado')
    ax.set_ylabel('Franja')

    if show:
        plt.tight_layout()
        plt.show()


def schedule_week(df_schedule):
    df = df_schedule  # No need to create a copy

    # Get unique days for iterating
    unique_days = df['dia'].unique()

    fig, axes = plt.subplots(1, 6, figsize=(12, 6), sharey=True)

    for i, day in enumerate(unique_days):
        ax = axes[i]
        # Create the heatmap in the current subplot
        schedule_day(df_schedule, day=day, ax=ax)

    # Adjust the overall figure layout
    plt.tight_layout()
    plt.show()


# def schedule_day(df_schedule):
#     df = df_schedule.copy()

#     df['hora_franja'] = df['hora_franja'].apply(lambda x: f"{x}-{F2H[x]}")

#     # Create a pivot table to prepare the data for the heatmap
#     pivot_df = df.pivot_table(index='hora_franja', 
#                              columns='documento',
#                              values='estado', aggfunc='first')

#     # Map categorical values to integers
#     cmap = sns.color_palette(['green', 'blue', 'red', 'gray'])
#     state_mapping = {'Trabaja': 0, 'Almuerza': 1, 'Pausa Activa': 2, 'Nada':3}
#     mapped_data = pivot_df.replace(state_mapping)

#     # Create the heatmapNada
#     plt.figure(figsize=(8, 9))
#     sns.heatmap(mapped_data, cmap=cmap, annot=False, fmt='',
#                  cbar=False, linewidths=0.5)

#     plt.title(f'Cronograma {day}')
#     plt.xlabel('Empleado')
#     plt.ylabel('Franja')
#     plt.show()


def load_capacidad_demanda(df_schudel, df_demand):
    df = df_schudel[['hora_franja','estado']].copy()
    df['estado'] = df['estado'] == "Trabaja"
    capacidad =df.groupby('hora_franja').sum()
    demanda = load_demanda(df_demand)
    return capacidad, demanda


def capacidad_vs_demanda(df_schudel, df_demand):

    capacidad, demanda = load_capacidad_demanda(df_schudel, df_demand)

    hora = F2H.values()
    fig, ax = plt.subplots(figsize=(10,5))

    # Plot 'oferta' data as bars
    ax.step(hora, capacidad['estado'], label='Capacidad', color='red',
                     where='mid', linestyle='-')  # Discrete lines for 'Demanda'

    # Plot 'demanda' data as bars
    ax.bar(hora, demanda.values(), label='Demanda', color='blue')

    ax.tick_params(axis='x', rotation=90)
    # Add labels, title, and legend
    ax.set_xlabel('Hora Franja')
    #ax.set_ylabel('Count')
    ax.set_title('Capacida vs. Demanda')
    ax.legend()

    # Show the plot
    plt.show()



def diff_capacidad_vs_demanda(df_schudel, df_demand):

    capacidad, demanda = load_capacidad_demanda(df_schudel, df_demand)

    diff = np.array(list(demanda.values()) - capacidad['estado'])
    colors = ['red' if val < 0 else 'blue' for val in diff]

    hora = F2H.values()

    fig, ax = plt.subplots(figsize=(9,5))
    ax.bar(hora, diff, color=colors)

    legend_labels = ['Baja Capacidad', 'Sobre Capacida']
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color='red'), plt.Rectangle((0, 0), 1, 1, color='blue')]
    ax.legend(legend_handles, legend_labels)

    ax.tick_params(axis='x', rotation=90)
    ax.set_title('Demanda - Capacidad')
    ax.set_xlabel('Franja')
    ax.set_ylabel('Demanda - Capacidad')
    plt.show()



def main():
    arguments = docopt(__doc__)
    type_ =arguments['<type>']
    csv_path = arguments['<input_csv>']
    day = arguments['--day']

    #df_schudel = pd.read_csv("/home/juan/dev/dataton2023-optilab/data/out.csv")
    df_schudel = pd.read_csv(csv_path)

    # df_demand = pd.read_excel("/home/juan/dev/dataton2023-optilab/data/Dataton 2023 Etapa 1.xlsx", sheet_name="demand")
    # workers = pd.read_excel("/home/juan/dev/dataton2023-optilab/data/Dataton 2023 Etapa 1.xlsx", sheet_name="workers")
    if not day:
        schedule_week(df_schudel)
    elif day:
        schedule_day(df_schudel, day)

    # capacidad_vs_demanda(df_schudel, df_demand)

    # diff_capacidad_vs_demanda(df_schudel, df_demand)




if __name__ == "__main__":
    main()
