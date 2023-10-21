from .day import set_constraints_day
import numpy as np 


def set_constraints_worker(model, variables, contrato='TC'):
    days, franjas, estados = zip(*variables.keys())

    days = np.unique(days)
    franjas = np.unique(franjas)
    estados = np.unique(estados)
    
    for day in days:
    
        if contrato == "MT":
            numero_franjas_trabajo = 16 
        elif contrato == "TC" and day == 'Sábado':
            numero_franjas_trabajo = 20
        else:
            numero_franjas_trabajo = 32

        variables_day = {}
        for franja in franjas:
            for estado in estados:
                variables_day[(franja, estado)] = variables[(day, franja, estado)]
            
        set_constraints_day(model, variables_day, day, numero_franjas_trabajo)

    
    #De lunes a viernes deben tener el mismo horarario de inicio
    dasy_no_s = list(days)
    dasy_no_s.remove('Sábado')
    
    for f in franjas:
        first_value = variables[(dasy_no_s[0], f, 'Nada')] 
        for day in dasy_no_s[1:]:
            model.Add(variables[(day, f, 'Nada')] == first_value)

    # Almuerzo constante para los de tiempo completo
    if contrato == "TC":
        for f in franjas:
            first_value = variables[(dasy_no_s[0], f, 'Almuerza')] 
            for day in dasy_no_s[1:]:
                model.Add(variables[(day, f, 'Almuerza')] == first_value)

    


        