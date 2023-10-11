import pandas as pd 

from dataton2023_optilab.utils.plot import schedule, capacidad_vs_demanda
from dataton2023_optilab.utils.plot import diff_capacidad_vs_demanda


df_schudel = pd.read_csv("/home/juan/dev/dataton2023-optilab/data/out.csv")

df_demand = pd.read_excel("/home/juan/dev/dataton2023-optilab/data/Dataton 2023 Etapa 1.xlsx", sheet_name="demand")
workers = pd.read_excel("/home/juan/dev/dataton2023-optilab/data/Dataton 2023 Etapa 1.xlsx", sheet_name="workers")

schedule(df_schudel)

capacidad_vs_demanda(df_schudel, df_demand)

diff_capacidad_vs_demanda(df_schudel, df_demand)