from .worker import set_constraints_worker
from ..utils.time import FRANJAS, POSIBLES_ESTADOS


def set_branch_contraints(model, damanda, trabajadores):

    franjas = FRANJAS
    posibles_estados = POSIBLES_ESTADOS
    
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
    

    # Debe haber por lo menos un trabajador en cada franja horaria que tenga una demanda mayor o igual a uno
    for day in days:
        for franja in franjas:
            if damanda[day][franja] >= 1:
                model.AddAtLeastOne(variables[(t, day, franja, 'Trabaja')] for t in trabajadores)

    return variables