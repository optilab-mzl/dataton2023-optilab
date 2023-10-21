from .worker import set_constraints_worker


def set_branch_contraints(model,damanda, trabajadores,
                        franjas, posibles_estados):
    
    days = damanda.keys()
    variables = {}
    for trabajador in trabajadores:
        for day in days:
            for franja in franjas:
                for estado in posibles_estados:
                    index = (trabajador, day, franja, estado)
                    name_var = f"{trabajador}-{day}-{franja}-{estado}"
                    variables[index] = model.NewBoolVar(name_var)
    

    for trabajador in trabajadores:
        variables_trabajador = {}
        for day in days: 
            for franja in franjas:
                for estado in posibles_estados:
                    variables_trabajador[(day , franja, estado)] = variables[(trabajador, day, franja,estado)]
        set_constraints_worker(model, variables_trabajador,
                              contrato = trabajadores[trabajador],
                              )
    

    # Debe haber por lo menos un trabajador en cada franja horaria
    dasy_no_s = list(days)
    dasy_no_s.remove('Sábado')
    for day in dasy_no_s:
        for franja in franjas:
            model.AddAtLeastOne(variables[(t, day, franja, 'Trabaja')] for t in trabajadores)
    
    #los sábdos no es todo el día, y debe empezar minimo en las 11
    for franja in franjas[:34]:
        model.AddAtLeastOne(variables[(t, 'Sábado', franja, 'Trabaja')] for t in trabajadores)
    for t in trabajadores:
        for franja in franjas[34:]:
            model.Add(variables[(t, 'Sábado', franja, 'Nada')]==1)

    return variables