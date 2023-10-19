"""
Constraints for one day of a worker
"""
import numpy as np 


def no_franjas_repetidas(model, variables):
    franjas, posibles_estados = zip(*variables.keys())

    franjas = np.unique(franjas)
    posibles_estados = np.unique(posibles_estados)

    for franja in franjas:
        model.Add(sum(variables[(franja,estado)] for estado in posibles_estados) == 1)


def horas_de_trabajo(model, variables, numero_de_franjas=38):
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    franjas_en_nada = len(franjas)-numero_de_franjas

    #el total de franjas en nada
    model.Add(sum(variables[(franja, 'Nada')] for franja in franjas) == franjas_en_nada)

    # CIertas frnajas nunca van a tener el estado de "Nada"
    franja = len(franjas) - numero_de_franjas
    for f in franjas[franja:-franja]:
        model.Add(variables[(f, 'Nada')]==0)


def horas_continuas_de_trabajo(model, variables, numero_de_franjas=38):
    franjas, posibles_estados = zip(*variables.keys())
    
    franjas = np.unique(franjas)
    posibles_estados = np.unique(posibles_estados)
    
    posibles_estados = list(posibles_estados)
    posibles_estados.remove('Nada')

    trabajando = {}
    for idx in range(len(franjas)-numero_de_franjas-1):
        sub_franjas = franjas[idx:idx+numero_de_franjas]

        trabajando[idx] = model.NewBoolVar("")
        model.Add(sum(variables[(f, e)] for e in posibles_estados for f in sub_franjas)==numero_de_franjas).OnlyEnforceIf(trabajando[idx])
        model.Add(sum(variables[(f, e)] for e in posibles_estados for f in sub_franjas)!=numero_de_franjas).OnlyEnforceIf(trabajando[idx].Not())

    model.AddBoolXOr(trabajando.values())


def pausas_activas(model, variables):
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)
    for idx in range(len(franjas)):
        pausa_activa = variables[(franjas[idx], 'Pausa Activa')]
        
        # Despues de una pausa activa no debe haber "Nada"
        # len = 10
        # i = 9
        # i = 8 len(10)-1 = 9
        if idx<len(franjas)-1:
            model.Add(variables[(franjas[idx]+1, "Nada")]==0).OnlyEnforceIf(pausa_activa)

        # Las proximás cuatro franjas necesariamnete debe estar en estado "Trabaja"
        sub_franjas = franjas[idx:idx+5]
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==4).OnlyEnforceIf(pausa_activa)

        # La cuatro anteriores franjas necesariamente debe estar en estado "Trabaja"
        sub_franjas = franjas[max(idx-4,0):idx]
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==4).OnlyEnforceIf(pausa_activa)

        # Como maximo debe estar "Trabajando" en las proximas 8 franjas
        sub_franjas = franjas[max(idx-8,0):idx]
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)>=4).OnlyEnforceIf(pausa_activa)
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)<=8).OnlyEnforceIf(pausa_activa)

        # Si las anterires fueron ocho franjas de trabajo la siguiente tiene que ser pausa activa o 
        # almuerzo 
        ocho_franjas = model.NewBoolVar("")
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==8).OnlyEnforceIf(ocho_franjas)
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)!=8).OnlyEnforceIf(ocho_franjas.Not())
        model.AddAtLeastOne(
            variables[(franjas[idx], "Pausa Activa")], variables[(franjas[idx], "Almuerza")]
            ).OnlyEnforceIf(ocho_franjas)

    for f in franjas[20:26]:
        model.Add(variables[(f, "Pausa Activa")]==0)


def almuerzo(model, variables):
    #si hay almuerzo debe haber seis horas y entre las horas especificadas
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    hay_almuerzo = model.NewBoolVar("")
    model.Add(sum(variables[(f, "Almuerza")] for f in franjas) >=1).OnlyEnforceIf(hay_almuerzo)
    model.Add(sum(variables[(f, "Almuerza")] for f in franjas) ==1).OnlyEnforceIf(hay_almuerzo.Not())
    model.Add(sum(variables[(f, "Almuerza")] for f in franjas[16:30]) ==6).OnlyEnforceIf(hay_almuerzo)
    for f in  [*franjas[:16],*franjas[30:]]:
        model.Add(variables[(f, "Almuerza")]==0)

    #continuidad del almuerzo
    almorzando = {}
    for idx in range(len(franjas)-5):
        sub_franjas = franjas[idx:idx+6]
        almorzando[idx] = model.NewBoolVar("")
        model.Add(sum(variables[(f, "Almuerza")] for f in sub_franjas)==6).OnlyEnforceIf(almorzando[idx])
        model.Add(sum(variables[(f, "Almuerza")] for f in sub_franjas)!=6).OnlyEnforceIf(almorzando[idx].Not())
    model.AddBoolXOr(almorzando.values())


def set_constraints_day(model, variables,
                    numero_franjas_trabajo=38):

    # No se admiten franjas repetidas                                    
    no_franjas_repetidas(model, variables)

    # 36 horas de trabajo
    horas_de_trabajo(model, variables,
                     numero_de_franjas=numero_franjas_trabajo)

    # Las horas de la jornada deben ser continuas 
    horas_continuas_de_trabajo(model, variables,
                             numero_de_franjas=numero_franjas_trabajo)

    pausas_activas(model, variables)

    almuerzo(model, variables)
