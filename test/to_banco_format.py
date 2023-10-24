import pandas as pd 


df = pd.read_csv("/home/juan/dev/dataton2023-optilab/temp/baseline.csv")


mask = (df['dia']=="Sábado")  & (df['hora_franja'] >= 59)
df = df[~mask]


mask = df['hora_franja'] == 78

#df = df[~mask]


df = df.drop(columns=['dia'])

df.to_csv('base_out.csv', index=False)