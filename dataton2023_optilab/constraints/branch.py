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
        set_constraints_worker(model, variables_trabajador)

    return variables
