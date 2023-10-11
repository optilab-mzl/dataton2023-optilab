def set_program_worker_constraints(model, demanda, franjas, posibles_estados, psibles_estados_wn, variables):
    for franja in franjas:
        model.Add(sum(variables[(franja,estado)] for estado in posibles_estados) == 1)

    # 36 horas de trabajo
    model.Add(sum(variables[(franja, 'Nada')] for franja in franjas)==8)
    for f in franjas[8:-8]:
        model.Add(variables[(f, 'Nada')]==0)

    trabajando = {}
    for idx in range(len(franjas)-37):
        sub_franjas = franjas[idx:idx+38]
        trabajando[idx] = model.NewBoolVar("")
        model.Add(sum(variables[(f, e)] for e in psibles_estados_wn for f in sub_franjas)==38).OnlyEnforceIf(trabajando[idx])
        model.Add(sum(variables[(f, e)] for e in psibles_estados_wn for f in sub_franjas)!=38).OnlyEnforceIf(trabajando[idx].Not())
    model.AddBoolXOr(trabajando.values())


    model.Add(variables[(franjas[-1], 'Pausa Activa')] == 0)
    for idx in range(len(franjas)):
        pausa_activa = variables[(franjas[idx], 'Pausa Activa')]

        if idx<len(franjas)-1:
            model.Add(variables[(franjas[idx]+1, "Nada")]==0).OnlyEnforceIf(pausa_activa)

        sub_franjas = franjas[idx:idx+5]
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==4).OnlyEnforceIf(pausa_activa)

        sub_franjas = franjas[max(idx-4,0):idx]
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==4).OnlyEnforceIf(pausa_activa)

        sub_franjas = franjas[max(idx-8,0):idx]
        #print(sub_franjas, idx)
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)>=4).OnlyEnforceIf(pausa_activa)
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)<=8).OnlyEnforceIf(pausa_activa)

        ocho_horas = model.NewBoolVar("")
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)==8).OnlyEnforceIf(ocho_horas)
        model.Add(sum(variables[(f, "Trabaja")]  for f in sub_franjas)!=8).OnlyEnforceIf(ocho_horas.Not())

        model.AddAtLeastOne(variables[(franjas[idx], "Pausa Activa")], variables[(franjas[idx], "Almuerza")]).OnlyEnforceIf(ocho_horas)

    for f in franjas[20:26]:
        model.Add(variables[(f, "Pausa Activa")]==0)

    #si hay almuerzo debe haber seis horas y entre las horas especificadas

    hay_almuerzo = model.NewBoolVar("")
    model.Add(sum(variables[(f, "Almuerza")] for f in franjas) >=1).OnlyEnforceIf(hay_almuerzo)
    model.Add(sum(variables[(f, "Almuerza")] for f in franjas) ==1).OnlyEnforceIf(hay_almuerzo.Not())
  

    model.Add(sum(variables[(f, "Almuerza")] for f in franjas[16:30]) ==6).OnlyEnforceIf(hay_almuerzo)

    for f in  [*franjas[:16],*franjas[30:]]:
        model.Add(variables[(f, "Almuerza")]==0)

    almorzando = {}
    for idx in range(len(franjas)-5):
        sub_franjas = franjas[idx:idx+6]
        almorzando[idx] = model.NewBoolVar("")
        model.Add(sum(variables[(f, "Almuerza")] for f in sub_franjas)==6).OnlyEnforceIf(almorzando[idx])
        model.Add(sum(variables[(f, "Almuerza")] for f in sub_franjas)!=6).OnlyEnforceIf(almorzando[idx].Not())
    model.AddBoolXOr(almorzando.values())



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
    cuadrados = []
    for i,(franja, demand) in enumerate(demanda.items()):

        trabjadores_en_franja = model.NewIntVar(0, len(trabajadores), '')
        model.Add(trabjadores_en_franja == sum(variables[(t,franja,'Trabaja')] for t in trabajadores))

        demanda_alta = model.NewBoolVar("")
        model.Add(trabjadores_en_franja < demanda[franja]).OnlyEnforceIf(demanda_alta)
        model.Add(trabjadores_en_franja >= demanda[franja]).OnlyEnforceIf(demanda_alta.Not())

        resta = model.NewIntVar(0, 16, '')
        model.Add(resta == (demanda[franja] - trabjadores_en_franja) ).OnlyEnforceIf(demanda_alta)
        #model.Add(resta == (trabjadores_en_franja-demanda[franja]) ).OnlyEnforceIf(demanda_alta.Not())
        model.Add(resta == 0 ).OnlyEnforceIf(demanda_alta.Not())

        #cuadrado = model.NewIntVar(0, 296, '')#1000000
        #model.AddMultiplicationEquality(cuadrado, [resta, resta])

        #abs = model.NewIntVar(0, 16, '')
        #model.AddAbsEquality(abs, resta)
        cuadrados.append(resta)
        # if i >= 8:
        #     print(i)
        #     break
    
    objetivo = sum(cuadrados)
    model.Minimize(objetivo)