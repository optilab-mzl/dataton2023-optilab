#Packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import requests
import os 
import json



# def generar_franjas(inicio, final):
#     horas = []
#     hora, minuto = inicio
#     while (hora, minuto) <= final:
#         horas.append(f"{hora:02d}:{minuto:02d}")
#         if minuto + 15 >= 60:
#             hora += 1
#             minuto = 0
#         else:
#             minuto += 15
#     return horas


# FRANJAS = list(range(30,76))
# H2F = {h:f for f,h in zip(FRANJAS, generar_franjas((7,30), (18,45)))}
# F2H = {f:h for f,h in zip(FRANJAS, generar_franjas((7,30), (18,45)))}

def demand_jobs_to_json(df_d, df_w):
    output_dict = {}
    output_dict['demand'] = {}
    output_dict['workers'] = {}

    df_d['fecha_hora'] = df_d['fecha_hora'].apply(lambda x: str(x))

    output_dict['demand']['demand_time_points'] = df_d[['fecha_hora','demanda']].to_dic(orient="records")
    
    output_dict['workers']['list_of_workers'] = df_w[['documento','contrato']].to_dic(orient="records")

    return output_dict

# Función para contar el número de veces que "Trabaja" aparece en una fila
def contar_trabaja(row):
    return row.str.count('Trabaja').sum()

def schedule_day(df_schedule: pd.DataFrame, day: str = None, ax: plt.Axes = None, title: str = None):
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
    
    #df['hora_franja'] = df['hora_franja'].apply(lambda x: f"{x}-{F2H[x]}")

    pivot_df = df.pivot_table(index='hora_franja', 
                            columns='documento',
                            values='estado', aggfunc='first')
    print("PIVOT_DF",type(pivot_df),pivot_df)
    # Map categorical values to integers
    cmap = sns.color_palette(['green', 'blue', 'red', 'gray'])
    state_mapping = {'Trabaja': 0, 'Almuerza': 1, 'Pausa Activa': 2, 'Nada':3}
    mapped_data = pivot_df.replace(state_mapping)

    show = False
    if not ax:
        fig, ax = plt.subplots(figsize=(8, 9))
        show = True
    
    print("MAPPED_DATA",type(mapped_data),mapped_data)
    sns.heatmap(mapped_data, cmap=cmap, annot=False, fmt='',
                cbar=False, linewidths=0.5, ax=ax)

    ax.set_title(f'Cronograma {day}')
    ax.set_xlabel('Empleado')
    ax.set_ylabel('Franja')
    plt.suptitle(title)
    if show:
        plt.tight_layout()
        plt.show()
        
    

    #st.pyplot(fig)
    pivot_df["capacidad"]=pivot_df.apply(contar_trabaja, axis=1)
    st.dataframe(pivot_df, width=800, height=300)
    
    
    return pivot_df

    
    
# Load Bancolombia Logotipo
st.image("Bancolombia_S.A._logo.svg.png", use_column_width=True)

# Application Title
st.title('Programación Horaria Empleados de Caja')


st.markdown(
    """
    <style>
    body {
        font-family: 'OpenSans', sans-serif; /* Source Bancolombia */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Change the color to the depth
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFFF; /* White */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Change the color to the title and to the text
st.markdown(
    """
    <style>
    .st-DZXFf.jMlnKc, .st-dz {
        color: #000000; /* Negro */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Change the color to the interactive colors
st.markdown(
    """
    <style>
    .st-eb, .st-ec, .st-dh, .st-bg, .st-dl, .st-bp, .st-eh, .st-dn {
        background-color: #FFFF66; /* Amarillo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Personalize the widget of drag and drop with HTML and CSS
st.markdown(
    """
    <style>
    /* Cambiar el color de fondo y el borde del área de arrastrar y soltar */
    .st-draggable.draggable {
        background-color: #FFD100; /* Amarillo */
        border: 2px dashed #000; /* Borde negro */
    }
    
    /* Cambiar el color del texto del área de arrastrar y soltar */
    .st-draggable.draggable .content {
        color: #000; /* Texto negro */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Load File Element
uploaded_file = st.file_uploader("Upload", type=["xlsx"])

if uploaded_file is not None:
    # Load the demand Sheet
    info_demand = pd.read_excel(uploaded_file, sheet_name="demand")
    # Adding a date column without the time
    info_demand["fecha_sin_hora"] = info_demand["fecha_hora"].dt.date
    # Dates
    unique_dates = list(info_demand["fecha_sin_hora"].unique())
    #Sucursals
    sucursals=list(info_demand["suc_cod"].unique())
    
    # Load the worker Sheet
    info_workers = pd.read_excel(uploaded_file, sheet_name="workers")

    
    
    
    # Select to choose a sucursal
    st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Selecciona la sucursal para la cual desea programar los horarios de los empleados:</p>", unsafe_allow_html=True)
    selected_sucursal = st.selectbox("", sucursals)
    
    #st.write("Has seleccionado la sucursal:", selected_sucursal)
    
    
    
    info_workers_suc=info_workers[info_workers["suc_cod"]==selected_sucursal]
    info_workers_suc=info_workers_suc.reset_index(drop=True)
    
    
    
    
    # Personalize the table style:
    st.markdown(
        """
        <style>
        .dataframe {
            text-align: center; /* Centrar el texto en la tabla */
            background-color: #FFFFCC; /* Fondo amarillo claro */
            color: #000000; /* Texto negro */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Show the workers info:
    st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Información de los Empleados de Caja de la Sucursal {selected_sucursal}:</p>", unsafe_allow_html=True)
    st.dataframe(info_workers_suc, width=800, height=300)
        
    # Select to choose a fecha
    st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Selecciona una fecha para la cual desea visualizar la información de la sucursal seleccionada:</p>", unsafe_allow_html=True)
    selected_fecha = st.selectbox("", unique_dates)
    #st.write("Has seleccionado la fecha:", selected_fecha)
        
    # Copy info demand with "fecha_sin_hora"
    info_demand_copy=info_demand.copy()
    
    #Original info demand
    info_demand=info_demand.drop("fecha_sin_hora",axis=1)
    
    info_demand_copy=info_demand_copy[info_demand_copy["suc_cod"]==selected_sucursal]
    info_demand_copy_input=info_demand_copy.copy()
    info_demand_copy=info_demand_copy[info_demand_copy["fecha_sin_hora"]==selected_fecha]
    
    st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Información de la demanda en la sucursal seleccionada en el día seleccionado:</p>", unsafe_allow_html=True)
    st.dataframe(info_demand_copy.drop("fecha_sin_hora"), width=800, height=300)
   
    # Time line Demand
    #st.write("Demanda Horaria:")
    
    # Configurar el estilo Seaborn
    #sns.set(style="whitegrid")
    
    
    # Configuration plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax = sns.lineplot(x=info_demand_copy["fecha_hora"], y=info_demand_copy["demanda"], ci=None, color="black")
    ax.fill_between(info_demand_copy["fecha_hora"], 0, info_demand_copy["demanda"], color="#FFFFCC")

    # To sure to show all the time in the x axis
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

    # setting the fotmat of the label of the x axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))  # Format the labels to "HH:MM"

    ax.set_xlabel("Hora del Día")
    ax.set_ylabel("Demanda de Empleados")
    ax.set_title("Demanda Horaria")

    # Limits x Axis
    ax.set_xlim(info_demand_copy["fecha_hora"].min(), info_demand_copy["fecha_hora"].max())

    # To Rotate the x Axis Labels
    plt.xticks(rotation=90)
    
    #Show the plot
    st.pyplot(fig)
    #schedule_select_suc=pd.read_json(f"{selected_sucursal}.json")
    

    
    input_data=demand_jobs_to_json(info_demand_copy_input,info_workers_suc)
    backend_api_url="http://localhost:5000/"
    response = requests.post(url=backend_api_url + "/get_schedule",json=input_data)
    whats_list = response.json()["get_schedule"]
    
    
    #Show the schedule
    st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Horario de los empleados para la sucursal seleccionda en el día seleccionado:</p>", unsafe_allow_html=True)
    #st.dataframe(schedule_select_suc, width=800, height=300)


    
    #st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Selecciona una fecha para la cual desea visualizar la programación de la sucursal seleccionada:</p>", unsafe_allow_html=True)
    #selected_fecha_sche = st.selectbox(" ", unique_dates)
    schedule_select_suc_day=schedule_select_suc[schedule_select_suc["fecha"]==str(selected_fecha)]
    schedule_select_suc_day_trans=schedule_day(schedule_select_suc_day)
    
    #schedule_select_suc_day_trans.reset_index(inplace=True)
    #schedule_select_suc_day_trans.set_index("")
    print(schedule_select_suc_day_trans.columns)
    info_demand_copy.index=schedule_select_suc_day_trans.index
    info_demand_work=pd.concat([info_demand_copy[["fecha_hora","demanda"]],schedule_select_suc_day_trans[["capacidad"]]],axis=1)
    #st.dataframe(info_demand_work, width=800, height=300)
    
    

    # Convierte la columna 'fecha_hora' en tipo datetime
    info_demand_work['fecha_hora'] = pd.to_datetime(info_demand_work['fecha_hora'])

    # Crea un objeto fig, ax y un gráfico de líneas de tiempo
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(info_demand_work['fecha_hora'], info_demand_work['demanda'], label='Demanda',color="black")
    ax.plot(info_demand_work['fecha_hora'], info_demand_work['capacidad'], label='Capacidad',color="gray")

    # Colorear el área entre las curvas de demanda y capacidad
    ax.fill_between(info_demand_work['fecha_hora'], info_demand_work['demanda'], info_demand_work['capacidad'], where=(info_demand_work['demanda'] > info_demand_work['capacidad']),
                    interpolate=True, color='red', alpha=0.3, label='Demanda > Capacidad')
    ax.fill_between(info_demand_work['fecha_hora'], info_demand_work['demanda'], info_demand_work['capacidad'], where=(info_demand_work['demanda'] <= info_demand_work['capacidad']),
                    interpolate=True, color='green', alpha=0.3, label='Demanda <= Capacidad')

    ax.set_xlabel('Hora del día')
    ax.set_ylabel('Valores')
    ax.set_title('Evolución de Demanda y Capacidad a lo largo del tiempo')
    ax.legend()

    # Formatear el eje x para mostrar solo la hora
    date_format = DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(date_format)

    plt.xticks(rotation=45)

    plt.tight_layout()
    #plt.show()

    
    #Show the plot
    st.pyplot(fig)
    
    


        
        









    
  





