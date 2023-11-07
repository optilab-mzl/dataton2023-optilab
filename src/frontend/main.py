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
import base64


#Run the backend in  this url:
backend_api_url = "http://0.0.0.0:8080"

####FUNCTIONS:
def get_schedule(input):
    """Make request to get_schedule endpoint.

    Returns
    -------
    schedule : dict
    """
    response = requests.post(url=f"{backend_api_url}/get_schedule", json=input)
    schedule = response.json()
    return schedule

def demand_jobs_to_json(df_d, df_w):
    """ 
    Convierte dos DataFrames en un diccionario en formato JSON que representa la información de demanda y trabajadores.

    Parámetros
    ----------
    df_d : pandas.DataFrame
        DataFrame que contiene la información de demanda. Debe contener al menos las columnas 'fecha_hora' y 'demanda'.
    df_w : pandas.DataFrame
        DataFrame que contiene la información de los trabajadores. Debe contener al menos las columnas 'documento' y 'contrato'.

    Retorna
    -------
    dict
        Un diccionario en formato JSON que representa la información de demanda y trabajadores.
    """
    
    output_dict = {}
    output_dict['demand'] = {}
    output_dict['workers'] = {}

    df_d['fecha_hora'] = df_d['fecha_hora'].apply(lambda x: str(x))

    output_dict['demand']['demand_time_points'] = df_d[['fecha_hora','demanda']].to_dict(orient="records")
    
    output_dict['workers']['list_of_workers'] = df_w[['documento','contrato']].to_dict(orient="records")

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
    

    pivot_df = df.pivot_table(index='hora_franja', 
                            columns='documento',
                            values='estado', aggfunc='first')
    cmap = sns.color_palette(['yellow', 'blue', 'green', 'gray'])
    state_mapping = {'Trabaja': 0, 'Almuerza': 1, 'Pausa Activa': 2, 'Nada':3}
    mapped_data = pivot_df.replace(state_mapping)

    show = False
    if not ax:
        fig, ax = plt.subplots(figsize=(8, 9))
        show = True
    
    legend_labels = list(state_mapping.keys())
    sns.heatmap(mapped_data, cmap=cmap, annot=False, fmt='',
                cbar=True, cbar_kws={'ticks': [0, 1, 2, 3], 'label': 'Estado'},
                linewidths=0.5, ax=ax)

    cbar = ax.collections[0].colorbar
    cbar.set_ticks([i for i in range(len(legend_labels))])
    cbar.set_ticklabels(legend_labels)

    ax.set_title(f'Cronograma')
    ax.set_xlabel('Empleado')
    ax.set_ylabel('Franja')
    plt.suptitle(title)
    if show:
        plt.tight_layout()
        plt.show()
        
    
    st.pyplot(fig)
    pivot_df["capacidad"]=pivot_df.apply(contar_trabaja, axis=1)
    
    
    return pivot_df

@st.cache_resource
def programming(input_service:dict):
    output_service=get_schedule(input_service)
    output=output_service["rows"]
    df_output=pd.DataFrame(output)
        
    return df_output

    


#VISUAL CONFIGURATION:
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
        background-color: #FFFFFF; /* White */
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



# Load Bancolombia Logotipo
st.image("Bancolombia_S.A._logo.svg.png", use_column_width=True)

# Application Title
st.title('Programación Horaria Empleados de Caja')



# Create the tabs:
tab1, tab2 = st.tabs(["Información General", "Programación Horaria"])

# General Information Tab:
with tab1:
    # Load File Element
    uploaded_file = st.file_uploader("Cargar", type=["xlsx"])

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
        
        
        
        info_workers_suc=info_workers[info_workers["suc_cod"]==selected_sucursal]
        info_workers_suc=info_workers_suc.reset_index(drop=True)
        
        
        
        
        
        
        # Show the workers info:
        st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Información de los Empleados de Caja de la Sucursal {selected_sucursal}:</p>", unsafe_allow_html=True)
        st.dataframe(info_workers_suc, width=800, height=300)
            
        # Select to choose a fecha
        st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Selecciona una fecha para la cual desea visualizar la información de la sucursal seleccionada:</p>", unsafe_allow_html=True)
        selected_fecha = st.selectbox("", unique_dates)
            
        # Copy info demand with "fecha_sin_hora"
        info_demand_copy=info_demand.copy()
        
        #Original info demand
        info_demand=info_demand.drop("fecha_sin_hora",axis=1)
        
        info_demand_copy=info_demand_copy[info_demand_copy["suc_cod"]==selected_sucursal]
        info_demand_copy_input=info_demand_copy.copy()
        info_demand_copy=info_demand_copy[info_demand_copy["fecha_sin_hora"]==selected_fecha]
        
        st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Información de la demanda en la sucursal {selected_sucursal} en el día {str(selected_fecha)}:</p>", unsafe_allow_html=True)
        
        
        # Configuration plot Demand
        fig, ax = plt.subplots(figsize=(10, 5))
        ax = sns.lineplot(x=info_demand_copy["fecha_hora"], y=info_demand_copy["demanda"], ci=None, color="black", dashes=(5, 2))
        ax.fill_between(info_demand_copy["fecha_hora"], 0, info_demand_copy["demanda"], color="#FFFFCC")
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))  # Format the labels to "HH:MM"
        ax.set_xlabel("Hora del Día")
        ax.set_ylabel("Demanda de Empleados")
        ax.set_title("Demanda Horaria")
        ax.set_xlim(info_demand_copy["fecha_hora"].min(), info_demand_copy["fecha_hora"].max())
        plt.xticks(rotation=90)
        #Show the plot
        st.pyplot(fig)
        

    

# Schedule Tab:
with tab2:
    if uploaded_file is not None:
        
        with st.spinner("Encontrando la programación más eficiente..."):
            input_service=demand_jobs_to_json(info_demand_copy_input, info_workers_suc)
            df_output=programming(input_service)
        
        """with st.spinner("Encontrando la programación más eficiente..."):
            input_service=demand_jobs_to_json(info_demand_copy_input, info_workers_suc)
            output_service=get_schedule(input_service)
            output=output_service["rows"]
            df_output=pd.DataFrame(output)"""
        
        st.success("Programación Encontrada!")
        
        # Select to choose a fecha
        st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Selecciona una fecha para la cual desea visualizar la información de la sucursal seleccionada:</p>", unsafe_allow_html=True)
        selected_fecha = st.selectbox(" ", unique_dates)
        
        
        schedule_select_suc=df_output.copy()
        #Show the schedule
        st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Horario de los empleados para la sucursal {selected_sucursal} en el día {str(selected_fecha)}:</p>", unsafe_allow_html=True)


        schedule_select_suc_day=schedule_select_suc[schedule_select_suc["fecha"]==str(selected_fecha)]
        schedule_select_suc_day_trans=schedule_day(schedule_select_suc_day)
        
        info_demand_copy.index=schedule_select_suc_day_trans.index
        info_demand_work=pd.concat([info_demand_copy[["fecha_hora","demanda"]],schedule_select_suc_day_trans[["capacidad"]]],axis=1)
        
        
        info_demand_work['fecha_hora'] = pd.to_datetime(info_demand_work['fecha_hora'])
        
        st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Capacidad Vs Demanda para la sucursal {selected_sucursal} en el día {str(selected_fecha)}:</p>", unsafe_allow_html=True)

        # Plot Capacidada Vs Demanda
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(len(info_demand_work['fecha_hora'])), info_demand_work['capacidad'], width=0.4, align='center', color='yellow', label='Capacidad')
        ax.bar(range(len(info_demand_work['fecha_hora'])), info_demand_work['demanda'], width=0.4, align='center', color='none', edgecolor='gray', label='Demanda', linewidth=4)
        ax.set_xticks(range(len(info_demand_work['fecha_hora'])))
        ax.set_xticklabels([hora.strftime('%H:%M') for hora in info_demand_work['fecha_hora']])
        ax.set_xlabel('Hora del día')
        ax.set_ylabel('Capacidad/Demanda')
        ax.set_title('Capcidad Vs Demanda')
        ax.legend()
        plt.xticks(rotation=90)
        plt.tight_layout()
        #Show the plot
        st.pyplot(fig)
        
        
        #Plot Difference Demanda Vs Capacidad
        fig, ax = plt.subplots(figsize=(10, 6))
        diferencia = info_demand_work['demanda'] - info_demand_work['capacidad']
        colores = ['red' if diff > 0 else 'green' for diff in diferencia]
        ax.bar(range(len(info_demand_work['fecha_hora'])), diferencia, width=0.4, align='center', color=colores, label='Diferencia')
        ax.set_xticks(range(len(info_demand_work['fecha_hora'])))
        ax.set_xticklabels([hora.strftime('%H:%M') for hora in info_demand_work['fecha_hora']])
        ax.set_xlabel('Hora del día')
        ax.set_ylabel('Demanda - Capacidad')
        ax.set_title('Demanda - Capacidad')
        ax.legend(handles=[
            plt.Line2D([0], [0], color='red', lw=3, label='Baja Capacidad'),
            plt.Line2D([0], [0], color='green', lw=3, label='Sobre Capacidad')
        ])
        plt.xticks(rotation=90)
        plt.tight_layout()
        #Show the plot
        st.pyplot(fig)
        
         # Botton to Download the schedule of a sucursal in a csv file:
        if st.button(f"Descargar csv con la programación de la semana para la sucursal {selected_sucursal}"):
            csv_file = schedule_select_suc.to_csv(index=False)
            b64 = base64.b64encode(csv_file.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Descargar CSV</a>'
            st.markdown(href, unsafe_allow_html=True)



    
    
    
    
    


        
        









    
  





