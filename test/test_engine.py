from dataton2023_optilab.engine import main
import pandas as pd 


df_demanda = pd.read_excel("data/Dataton 2023 Etapa 1.xlsx", sheet_name="demand")
df_workers = pd.read_excel("data/Dataton 2023 Etapa 1.xlsx", sheet_name="workers")
main(df_demanda,df_workers, "out.csv")