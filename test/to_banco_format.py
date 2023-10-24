import pandas as pd 

df = pd.read_csv("/home/juan/dev/dataton2023-optilab/temp/baseline.csv")

mask = (df['dia']=="Sábado")  & (df['hora_franja'] >= 59)
df = df[~mask]

df = df.drop(columns=['dia'])

df.to_csv('2624.csv', index=False)