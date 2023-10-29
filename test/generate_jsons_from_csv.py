import pandas as pd 
import os 

df_demanda = pd.read_excel("data/Dataton 2023 Etapa 2.xlsx", sheet_name="demand")
df_workers = pd.read_excel("data/Dataton 2023 Etapa 2.xlsx", sheet_name="workers")

branches = df_demanda['suc_cod'].unique()

output_folder = 'test/data/input'

for branch in branches:
    output_path_d = os.path.join(output_folder, f"demanda_{branch}.json")
    df_d = df_demanda[df_demanda['suc_cod']==branch]
    df_d[['fecha_hora','demanda']].to_json(output_path_d, orient="records", date_format='iso')

    output_path_w = os.path.join(output_folder, f"trabajadores_{branch}.json")
    df_w = df_workers[df_workers['suc_cod']==branch]
    df_w[['documento','contrato']].to_json(output_path_w, orient="records", date_format='iso')

df_result = pd.read_csv("temp/baseline.csv")

branches = df_result['suc_cod'].unique()

output_folder = 'test/data/output'

for branch in branches:
    output_path_d = os.path.join(output_folder, f"{branch}.json")
    df_r = df_result[df_result['suc_cod']==branch]
    df_r[['hora_franja', 'estado', 'documento', 'fecha', 'hora']].to_json(output_path_d, orient="records", date_format='iso')
