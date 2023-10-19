"""
1. Una Surcursal 
1. Dias 



"""

original_list = [(1, 3), (4, 5)]
list1, list2 = zip(*original_list)

print(list1)  # Output: (1, 4)
print(list2)  # Output: (3, 5)


from dataton2023_optilab.engine import main
import pandas as pd 


df_demanda = pd.read_excel("data/Dataton 2023 Etapa 2.xlsx", sheet_name="demand")
df_workers = pd.read_excel("data/Dataton 2023 Etapa 2.xlsx", sheet_name="workers")


#print(df_demanda)

#main(df_demanda,df_workers, "out.csv")