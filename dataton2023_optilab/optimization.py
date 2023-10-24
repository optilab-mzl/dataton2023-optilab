import numpy as np 


# def set_optmization(model, demanda, variables):
#     trabajadores, days, franjas, _ = zip(*variables.keys())

#     trabajadores = np.unique(trabajadores)
#     days = np.unique(days)
#     franjas = np.unique(franjas)
    
#     restas = []
#     for day in days:
#         for franja in franjas:
#             #trabjadores_en_franja = model.NewIntVar(0, len(trabajadores), '')
#             trabjadores_en_franja = sum(variables[(t, day, franja, 'Trabaja')] for t in trabajadores)
#             #model.Add(trabjadores_en_franja == sum(variables[(t, day, franja, 'Trabaja')] for t in trabajadores))
 
#             demanda_alta = model.NewBoolVar("")
#             model.Add(trabjadores_en_franja < demanda[day][franja]).OnlyEnforceIf(demanda_alta)
#             model.Add(trabjadores_en_franja >= demanda[day][franja]).OnlyEnforceIf(demanda_alta.Not())

#             resta = model.NewIntVar(0, max(demanda[day].values()), '')
#             model.Add(resta == (demanda[day][franja] - trabjadores_en_franja) ).OnlyEnforceIf(demanda_alta)
#             model.Add(resta == 0 ).OnlyEnforceIf(demanda_alta.Not())
            
#             #resta = demanda[day][franja] - trabjadores_en_franja
#             restas.append(resta)
    
    
#     objetivo = sum(restas)
#     model.Minimize(objetivo)


def set_optmization(model, demanda, variables):
    trabajadores, days, franjas, _ = zip(*variables.keys())

    trabajadores = np.unique(trabajadores)
    days = np.unique(days)
    franjas = np.unique(franjas)
    
    restas = []
    for day in days: 
        for franja in franjas:

            demanda_day_franja = demanda[day][franja]#sum(demanda[day][franja] for day in days)

            trabjadores_en_franja = sum(variables[(t, day, franja, 'Trabaja')] for t in trabajadores)
            
            resta = model.NewIntVar(0, demanda_day_franja, '')
            damanda_menos_resta = demanda_day_franja - trabjadores_en_franja
            
            model.AddMaxEquality(resta, [0, damanda_menos_resta])
            restas.append(resta)
    
    
    objetivo = sum(restas)
    model.Minimize(objetivo)