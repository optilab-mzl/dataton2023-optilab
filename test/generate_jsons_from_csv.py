import pandas as pd 
import os 
import json

df_demanda = pd.read_excel("data/Dataton 2023 Etapa 2.xlsx", sheet_name="demand")
df_workers = pd.read_excel("data/Dataton 2023 Etapa 2.xlsx", sheet_name="workers")

branches = df_demanda['suc_cod'].unique()

output_folder = 'test/data/input'

# for branch in branches:
#     output_path_d = os.path.join(output_folder, f"{branch}.json")

#     output_dict = {}
#     output_dict['demand'] = {}
#     output_dict['workers'] = {}

#     df_d = df_demanda[df_demanda['suc_cod']==branch].copy()
#     df_d['fecha_hora'] = df_d['fecha_hora'].apply(lambda x: str(x))

#     output_dict['demand']['demand_time_points'] = df_d[['fecha_hora','demanda']].to_dict(orient="records")

#     output_path_w = os.path.join(output_folder, f"trabajadores_{branch}.json")
#     df_w = df_workers[df_workers['suc_cod']==branch]
#     output_dict['workers']['list_of_workers'] = df_w[['documento','contrato']].to_dict(orient="records")

#     with open(output_path_d, 'w') as archivo:
#         json.dump(output_dict, archivo, indent=4)



df_result = pd.read_csv("temp/baseline.csv")
print(df_result)
branches = df_result['suc_cod'].unique()

output_folder = 'test/data/output'


for branch in branches:
    output_path_d = os.path.join(output_folder, f"{branch}.json")

    output_dict = {}
    output_dict['rows'] = {}
    
    df_r = df_result[df_result['suc_cod']==branch].copy()

    df_r['fecha'] = df_r['fecha'].apply(lambda x: str(x))
    output_dict['rows'] =  df_r[['hora_franja', 'estado', 'documento', 'fecha', 'hora']].to_dict(orient="records")

    with open(output_path_d, 'w') as archivo:
        json.dump(output_dict, archivo, indent=4)