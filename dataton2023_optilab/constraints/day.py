"""
Constraints for one day of a worker
"""
import numpy as np 


def solo_un_estado_por_franja(model, variables):
    franjas, posibles_estados = zip(*variables.keys())

    franjas = np.unique(franjas)
    posibles_estados = np.unique(posibles_estados)

    for franja in franjas:
        model.AddExactlyOne(variables[(franja, estado)] for estado in posibles_estados)



def posible_inicios_de_trabajo(model, variables, day):
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    if day == 'Sábado':
        model.AddAtLeastOne(variables[f, 'Trabaja'] for f in franjas[:15])
    else:
        model.AddAtLeastOne(variables[f, 'Trabaja'] for f in franjas[:37])



def horas_de_trabajo(model, variables, numero_de_franjas=38):
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    franjas_en_nada = len(franjas)-numero_de_franjas

    #el total de franjas en nada
    model.Add(sum(variables[(franja, 'Nada')] for franja in franjas) == franjas_en_nada)

    #CIertas frnajas nunca van a tener el estado de "Nada"
    if len(franjas)/numero_de_franjas < 2:
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
    for idx in range(len(franjas)-numero_de_franjas + 1):
        sub_franjas = franjas[idx:idx+numero_de_franjas]
        
        trabajando[idx] = model.NewBoolVar("")
        model.Add(sum(variables[(f, e)] for e in posibles_estados for f in sub_franjas)==numero_de_franjas).OnlyEnforceIf(trabajando[idx])
        model.Add(sum(variables[(f, e)] for e in posibles_estados for f in sub_franjas)!=numero_de_franjas).OnlyEnforceIf(trabajando[idx].Not())

    #model.AddBoolXOr(trabajando.values())
    model.AddAtMostOne(trabajando.values())
    model.AddAtLeastOne(trabajando.values())
    #model.Add(sum(trabajando.values())==1)


def maximo_ocho_franjas_continuas(model, variables, numero_de_franjas=38):
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    for idx in range(8, len(franjas)):
        #pausa_activa = variables[(franjas[idx], 'Pausa Activa')]
        sub_franjas = franjas[idx-8: idx]
        franjas_trabajando = sum(variables[(f, "Trabaja")]  for f in sub_franjas)
        
        ocho_franjas = model.NewBoolVar("")
        model.Add(franjas_trabajando == 8).OnlyEnforceIf(ocho_franjas)
        model.Add(franjas_trabajando != 8).OnlyEnforceIf(ocho_franjas.Not())

        model.Add(variables[(franjas[idx], "Trabaja")] == 0).OnlyEnforceIf(ocho_franjas)
        #model.Add(variables[(franjas[idx], "Pausa Activa")] + variables[(franjas[idx], "Almuerza")] >= 1).OnlyEnforceIf#(ocho_franjas)
        #model.AddAtLeastOne(
        #   variables[(franjas[idx], "Pausa Activa")], variables[(franjas[idx], "Almuerza")]
        #   ).OnlyEnforceIf(ocho_franjas)
        

def pausas_activas(model, variables, numero_de_franjas=38):
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    # Debe haber como m´inimo 4 franjas antes de pausa activa
    for idx in range(len(franjas)):
        pausa_activa = variables[(franjas[idx], 'Pausa Activa')]
        sub_franjas = franjas[max(idx-4, 0): idx]
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==4).OnlyEnforceIf(pausa_activa)

    # Como mínimo debe haber 4 franjas despues de pausa activa 
    for idx in range(len(franjas)):
        pausa_activa = variables[(franjas[idx], 'Pausa Activa')]
        sub_franjas = franjas[idx: idx+5]
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==4).OnlyEnforceIf(pausa_activa)

    #No puede haber pausas activas en horaio de almuerzo
    if len(franjas)/numero_de_franjas < 2:
        for f in franjas[20:26]:
            model.Add(variables[(f, "Pausa Activa")]==0)


def almuerzo(model, variables):
    #si hay almuerzo debe haber seis horas y entre las horas especificadas
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    hay_almuerzo = model.NewBoolVar("")
    model.Add(sum(variables[(f, "Almuerza")] for f in franjas) >= 1).OnlyEnforceIf(hay_almuerzo)
    model.Add(sum(variables[(f, "Almuerza")] for f in franjas) < 1).OnlyEnforceIf(hay_almuerzo.Not())
    model.Add(sum(variables[(f, "Almuerza")] for f in franjas[16:30]) == 6).OnlyEnforceIf(hay_almuerzo)

    # # Debe haber como m´inimo 4 franjas antes de almuerzo
    for idx in range(1,len(franjas)-1):

        inicio_almuerzo = model.NewBoolVar("")
        patron_iniciando_almuerzo = sum((variables[(franjas[idx-1], 'Trabaja')], variables[(franjas[idx], 'Almuerza')], variables[(franjas[idx+1], 'Almuerza')]))
        model.Add(patron_iniciando_almuerzo == 3).OnlyEnforceIf(inicio_almuerzo)
        model.Add(patron_iniciando_almuerzo != 3).OnlyEnforceIf(inicio_almuerzo.Not())

        sub_franjas = franjas[max(idx-4, 0): idx]
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==4).OnlyEnforceIf(inicio_almuerzo)

    for f in  [*franjas[:16],*franjas[30:]]:
        model.Add(variables[(f, "Almuerza")]==0)

    #continuidad del almuerzo

    #sub_franjas = frnajas[16:30]
    almorzando = {}
    for idx in range(len(franjas)-5):
        sub_franjas = franjas[idx:idx+6]
        almorzando[idx] = model.NewBoolVar("")
        model.Add(sum(variables[(f, "Almuerza")] for f in sub_franjas)==6).OnlyEnforceIf(almorzando[idx])
        model.Add(sum(variables[(f, "Almuerza")] for f in sub_franjas)!=6).OnlyEnforceIf(almorzando[idx].Not())
    model.AddBoolXOr(almorzando.values())


def set_constraints_day(model, variables, day, 
                    numero_franjas_trabajo=32):
    

    if numero_franjas_trabajo > 20:
        # Para tener en cuenta el almuerzo
        numero_franjas_trabajo += 6

    # No se admiten franjas repetidas                                    
    solo_un_estado_por_franja(model, variables)
                                    
    posible_inicios_de_trabajo(model, variables, day)

    # 36 horas de trabajo
    horas_de_trabajo(model, variables,
                     numero_de_franjas=numero_franjas_trabajo)

    # Las horas de la jornada deben ser continuas 
    horas_continuas_de_trabajo(model, variables,
                             numero_de_franjas=numero_franjas_trabajo)

    # maximo_ocho_franjas_continuas(model, variables, 
                                    # numero_de_franjas=numero_franjas_trabajo)

    pausas_activas(model, variables,
                   numero_de_franjas=numero_franjas_trabajo)
    
    maximo_ocho_franjas_continuas(model, variables, 
                                    numero_de_franjas=numero_franjas_trabajo)

    if numero_franjas_trabajo > 20:
        almuerzo(model, variables)
    else:
        franjas, _ = zip(*variables.keys())
        franjas = np.unique(franjas)
        for f in franjas:
            model.Add(variables[(f, "Almuerza")]==0)

    if day == "Sábado":
        for f in franjas[29:]:
            model.Add(variables[(f, "Trabaja")]==0)


