import pandas as pd 
import random 
from dataton2023_optilab.utils.time import generar_franjas

def generate_workers(num_workers=10, num_suc=1, num_tc=8):
    df = pd.DataFrame(columns=('suc_cod', 'documento', 'contrato'))

    df['documento'] = list(range(1,num_workers+1))
    df['suc_cod'] = random.choices(range(1,num_suc+2), k=num_workers)

    weights = [num_tc/num_workers, (num_workers-num_tc)/num_workers]
    df['contrato'] = random.choices(['TC', 'MD'],
                                    weights=weights, k=num_workers)

    return df 
    
    
def generate_week_demand(num_suc=1, min_demand=0, max_demand=16):
    
    suc_cods = range(1,num_suc+2)
    franjas = generar_franjas((7,30), (18,45))
    days = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]
    
    dfs = []
    for suc_cod in suc_cods:
        for day in days:
            df = pd.DataFrame(columns=('suc_cod', 'fecha_hora', 'demanda'))
            df['fecha_hora'] = [f"{day} {f}" for f in franjas]
            df['suc_cod'] = suc_cod
            df['demanda'] =  random.choices(range(min_demand, max_demand+1), k=len(franjas))
            dfs.append(df)

    return pd.concat(dfs)



if __name__ == "__main__":
    df1 = generate_week_demand()
    df2 = generate_workers()
    
    excel_file = "Simulate.xlsx"
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name='demand', index=False)
        df2.to_excel(writer, sheet_name='workers', index=False)