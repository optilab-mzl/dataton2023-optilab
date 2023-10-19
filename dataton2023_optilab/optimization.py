import numpy as np 

def set_program_workers_constraints(model, demanda, trabajadores,
                                     franjas, posibles_estados,
                                      psibles_estados_wn):
    variables = {}
    for trabajador in trabajadores:
        for franja in franjas:
            for estado in posibles_estados:
                variables[(trabajador,franja,estado)] = model.NewBoolVar(f"{trabajador}-{franja}-{estado}")

    for trabajador in trabajadores:
        variables_trabajador = {}
        for franja in franjas:
            for estado in posibles_estados:
                variables_trabajador[(franja, estado)] = variables[(trabajador,franja,estado)]
        set_program_worker_constraints(model, demanda, franjas, posibles_estados, psibles_estados_wn, variables_trabajador)


    for franja in franjas:
        model.AddAtLeastOne(variables[(t,franja,'Trabaja')] for t in trabajadores)

    return variables



def set_optmization(model, demanda, trabajadores, variables):
    days, franjas, _ = zip(*variables.keys())

    days = np.unique(days)
    franjas = np.unique(franjas)
    
    restas = []
    for day in days:
        for franja in franjas:
            trabjadores_en_franja = model.NewIntVar(0, len(trabajadores), '')
            model.Add(trabjadores_en_franja == sum(variables[(t, day, franja, 'Trabaja')] for t in trabajadores))
 
            demanda_alta = model.NewBoolVar("")
            model.Add(trabjadores_en_franja < demanda[day][franja]).OnlyEnforceIf(demanda_alta)
            model.Add(trabjadores_en_franja >= demanda[day][franja]).OnlyEnforceIf(demanda_alta.Not())

            resta = model.NewIntVar(0, max(demanda.values()), '')
            model.Add(resta == (demanda[day][franja] - trabjadores_en_franja) ).OnlyEnforceIf(demanda_alta)

            model.Add(resta == 0 ).OnlyEnforceIf(demanda_alta.Not())
            restas.append(resta)
    
    
    objetivo = sum(restas)
    model.Minimize(objetivo)