"""
============================================
Restricciones de Programación Horaria a Nivel de Día
============================================

Este módulo define las restricciones a nivel de día para la generación de la programación horaria. Asegura que se cumplan las restricciones, como las horas permitidas de almuerzo, gestion de pausas activas etc.
"""
import numpy as np
from ortools.sat.python import cp_model


def solo_un_estado_por_franja(model: cp_model.CpModel,
                              variables: dict) -> None:
    """
    Define la restricción de solo tener un tipo de estado en cada franja horaria. Recordar que las variables se definieron booleanas, por lo que sin esta restriccion podrian existir dos estados en la misma franja con valor boleano True.

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.
    variables : dict
        Un diccionario que contiene las variables de interés a nivel de día definidas como variables booleanas de la clase `model.NewBoolVar` con índices (franja, estado). 
    """
    franjas, posibles_estados = zip(*variables.keys())
    franjas = np.unique(franjas)
    posibles_estados = np.unique(posibles_estados)

    for franja in franjas:
        model.AddExactlyOne(variables[(franja, estado)] for estado in posibles_estados)


def posible_inicios_de_trabajo(model: cp_model.CpModel,
                               variables: dict, day: str) -> None:
    """
    Define la restricción de los posibles inicios de la jornada laboral

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.
    variables : dict
        Un diccionario que contiene las variables de interés a nivel de día definidas como variables booleanas de la clase `model.NewBoolVar` con índices (franja, estado).
    day: str
        Día de la semana. El Sábado tiene su propio inicio de jornada laboral. 
    """
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    if day == 'Sábado':
        model.AddAtLeastOne(variables[f, 'Trabaja'] for f in franjas[:15])
    else:
        model.AddAtLeastOne(variables[f, 'Trabaja'] for f in franjas[:37])


def horas_de_trabajo(model: cp_model.CpModel,
                     variables: dict, numero_de_franjas: int = 38) -> None:
    """
    Define el número de franjas de trabajo.

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.
    variables : dict
        Un diccionario que contiene las variables de interés a nivel de día definidas como variables booleanas de la clase `model.NewBoolVar` con índices (franja, estado).
    numero_de_franjas: int
        Número de franjas diferentes a el estado "Nada" o franajas de trabajo incluyendo el almuerzo y las pausas activas
    """
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


def horas_continuas_de_trabajo(model: cp_model.CpModel,
                               variables: dict,
                               numero_de_franjas: int = 38) -> None:
    """
    Define que las franjas de trabajo sean continuas

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.
    variables : dict
        Un diccionario que contiene las variables de interés a nivel de día definidas como variables booleanas de la clase `model.NewBoolVar` con índices (franja, estado).
    numero_de_franjas: int
        Número de franjas diferentes a el estado "Nada" o franajas de trabajo incluyendo el almuerzo y las pausas activas (Predeterminado: 38).
    """                           
    franjas, _ = zip(*variables.keys())
    
    franjas = np.unique(franjas)
    trabajando = {}
    for idx in range(len(franjas)-numero_de_franjas):
        sub_franjas = franjas[idx:idx+numero_de_franjas]
        trabajando[idx] = model.NewBoolVar("")
        model.Add(sum(variables[(f, "Nada")] for f in sub_franjas)==0).OnlyEnforceIf(trabajando[idx])
        model.Add(sum(variables[(f, "Nada")] for f in sub_franjas)!=0).OnlyEnforceIf(trabajando[idx].Not())
    model.AddExactlyOne(trabajando.values())


def maximo_ocho_franjas_continuas(model: cp_model.CpModel, variables: dict) -> None:
    """
    Define que el número de franjas continuas en estado "Trabaja" sea como máximo 8.

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.
    variables : dict
        Un diccionario que contiene las variables de interés a nivel de día definidas como variables booleanas de la clase `model.NewBoolVar` con índices (franja, estado).
    """
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    for idx in range(8, len(franjas)):
        sub_franjas = franjas[idx-8: idx]
        franjas_trabajando = sum(variables[(f, "Trabaja")]  for f in sub_franjas)
        
        ocho_franjas = model.NewBoolVar("")
        model.Add(franjas_trabajando == 8).OnlyEnforceIf(ocho_franjas)
        model.Add(franjas_trabajando != 8).OnlyEnforceIf(ocho_franjas.Not())

        model.Add(variables[(franjas[idx], "Trabaja")] == 0).OnlyEnforceIf(ocho_franjas)


def pausas_activas(model: cp_model.CpModel,
                   variables: dict, numero_de_franjas: int = 38) -> None:
    """
    Define las restricciones concernientes a las pausas activas.

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.
    variables : dict
        Un diccionario que contiene las variables de interés a nivel de día definidas como variables booleanas de la clase `model.NewBoolVar` con índices (franja, estado).
    numero_de_franjas: int
        Número de franjas diferentes a el estado "Nada" o franajas de trabajo incluyendo el almuerzo y las pausas activas (Predeterminado: 38).
    """
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
            model.Add(variables[(f, "Pausa Activa")] == 0)


def almuerzo(model: cp_model.CpModel, variables: dict) -> None:
    """
    Define las restricciones concernientes al almuerzo.

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.
    variables : dict
        Un diccionario que contiene las variables de interés a nivel de día definidas como variables booleanas de la clase `model.NewBoolVar` con índices (franja, estado).
    """
    #si hay almuerzo debe haber seis horas y entre las horas especificadas
    franjas, _ = zip(*variables.keys())
    franjas = np.unique(franjas)

    model.Add(sum(variables[(f, "Almuerza")] for f in franjas[16:30]) == 6)

    # # Debe haber como m´inimo 4 franjas antes de almuerzo
    for idx in range(1,len(franjas)-1):

        inicio_almuerzo = model.NewBoolVar("")
        patron_iniciando_almuerzo = sum((variables[(franjas[idx-1], 'Trabaja')], variables[(franjas[idx], 'Almuerza')], variables[(franjas[idx+1], 'Almuerza')]))
        model.Add(patron_iniciando_almuerzo == 3).OnlyEnforceIf(inicio_almuerzo)
        model.Add(patron_iniciando_almuerzo != 3).OnlyEnforceIf(inicio_almuerzo.Not())

        sub_franjas = franjas[max(idx-4, 0): idx]
        model.Add(sum(variables[(f, "Trabaja")] for f in sub_franjas) == 4).OnlyEnforceIf(inicio_almuerzo)

    for f in [*franjas[:16], *franjas[30:]]:
        model.Add(variables[(f, "Almuerza")] == 0)

    _franjas = franjas[16:30]
    almorzando = {}
    for i, idx in enumerate(_franjas):
        sub_franjas = _franjas[i:i+6]
        almorzando[i] = model.NewBoolVar("")
        model.Add(sum(variables[(f, "Almuerza")] for f in sub_franjas) == 6).OnlyEnforceIf(almorzando[i])
        model.Add(sum(variables[(f, "Almuerza")] for f in sub_franjas) != 6).OnlyEnforceIf(almorzando[i].Not())
    model.AddExactlyOne(almorzando.values())


def set_constraints_day(model: cp_model.CpModel, variables: dict, day: str, 
                        numero_franjas_trabajo: int = 32) -> None:
    """
    Define las restricciones de un día de trabajo.

    Parámetros
    ----------
    model : cp_model.CpModel
        El modelo en el que se definen las restricciones.
    variables : dict
        Un diccionario que contiene las variables de interés a nivel de día definidas como variables booleanas de la clase `model.NewBoolVar` con índices (franja, estado).
    day: str
        Día de la semana. El Sábado tiene su propio inicio de jornada laboral.
    numero_de_franjas: int
        Número de franjas que el trabajador debe estar en estado "Trabaja" y "Pausa Activa" (Predeterminado: 32).
    """
    # Por fàcilidad de los posteriores procesos se agrega las hora de almuerzo en franja de trabajo
    if numero_franjas_trabajo > 20:
        # Para tener en cuenta el almuerzo
        numero_franjas_trabajo += 6

    # No se admiten franjas repetidas                                    
    solo_un_estado_por_franja(model, variables)

    #no es necesario tener en cuenta esto debido al que se pone el inicio y el final de la jornada                                
    #posible_inicios_de_trabajo(model, variables, day)

    # 36 horas de trabajo
    horas_de_trabajo(model, variables,
                     numero_de_franjas=numero_franjas_trabajo)

    # Las horas de la jornada deben ser continuas
    horas_continuas_de_trabajo(model, variables,
                               numero_de_franjas=numero_franjas_trabajo)

    # Restricciones de pausas activas
    pausas_activas(model, variables,
                   numero_de_franjas=numero_franjas_trabajo)
    
    # Máximo ocho franjas continuas, luego almuerzo o puasa activa o nada
    maximo_ocho_franjas_continuas(model, variables)

    # Solo se programa almuerzo si las franjas laborales son superiores a 20
    if numero_franjas_trabajo > 20:
        almuerzo(model, variables)
    else:
        franjas, _ = zip(*variables.keys())
        franjas = np.unique(franjas)
        for f in franjas:
            model.Add(variables[(f, "Almuerza")]==0)

    # El Sábado no se trabaja todo el día
    if day == "Sábado":
        for f in franjas[29:]:
            model.Add(variables[(f, "Nada")]==1)


