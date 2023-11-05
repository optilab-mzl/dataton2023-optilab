import pandas as pd 
import os 
import json


def demand_jobs_to_json(df_d, df_w):
    output_dict = {}
    output_dict['demand'] = {}
    output_dict['workers'] = {}

    df_d['fecha_hora'] = df_d['fecha_hora'].apply(lambda x: str(x))

    output_dict['demand']['demand_time_points'] = df_d[['fecha_hora','demanda']].to_dic(orient="records")
    
    output_dict['workers']['list_of_workers'] = df_w[['documento','contrato']].to_dic(orient="records")

    return output_dict


def schedule_to_json(df_r):
    output_dict = {}
    output_dict['rows'] = {}
    
    df_r['fecha'] = df_r['fecha'].apply(lambda x: str(x))
    output_dict['rows'] =  df_r[['hora_franja', 'estado', 'documento', 'fecha', 'hora']].to_dict(orient="records")
    
    return output_dict
        


if __name__ == "__main__":
    df_demanda = pd.read_excel("data/Dataton 2023 Etapa 2.xlsx", sheet_name="demand")
    df_workers = pd.read_excel("data/Dataton 2023 Etapa 2.xlsx", sheet_name="workers")

    ## Ejemplo salida para mandar demanda y trabajadores

    branches = df_demanda['suc_cod'].unique()
    for branch in branches:
        df_d = df_demanda[df_demanda['suc_cod']==branch].copy()
        df_w = df_workers[df_workers['suc_cod']==branch].copy()
        json_output = demand_jobs_to_json(df_d, df_w)
        print(json_output)



