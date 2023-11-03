#Packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.dates as mdates


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
    st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>Selecciona una fecha para la cual desea visualizar la curva de demanda en la sucursal seleccionada:</p>", unsafe_allow_html=True)
    selected_fecha = st.selectbox("", unique_dates)
    #st.write("Has seleccionado la fecha:", selected_fecha)
        
    # Copy info demand with "fecha_sin_hora"
    info_demand_copy=info_demand.copy()
    
    #Original info demand
    info_demand=info_demand.drop("fecha_sin_hora",axis=1)
    
    info_demand_copy=info_demand_copy[info_demand_copy["suc_cod"]==selected_sucursal]
    info_demand_copy=info_demand_copy[info_demand_copy["fecha_sin_hora"]==selected_fecha]
   
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
    
    if st.button("Programar el horario de los empleados para la sucursal seleccionada"):
        #Show the schedule
        st.dataframe(info_workers_suc, width=800, height=300)
        
        #Show the plot
        st.pyplot(fig)
        









    
  





