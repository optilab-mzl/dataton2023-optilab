"""
================================
Transforma demanda y trabajadores.
================================

Transforma las listas de demanda y trabajadores en formatos compatibles con los códigos de optimización.
"""
from .time import H2F, DAYS2DIAS
from datetime import datetime


def transform_demanda(demanda: list[dict],
                      return_day2date=False,
                      complete_franjas=True) -> dict:
    """ Transforma demanda en formaton compatible para optimización.

    Parámetros
    ----------
    demanda : list[dict]
        Una lista de diccionarios que especifica la demanda horaria de la sucursal. 
        Cada diccionario debe contener las siguientes claves:
            - "fecha_hora": Una fecha y hora en formato ISO.
            - "demanda": Un entero que representa la demanda en ese momento.
    return_day2date: bool
        Controla si devuelve diccionario que mapee de dias de la semana a fechas que vienen en la informaciòn de demanda.
    complete_franjas: bool
        Controla si completa el día Sábado con las franjas de los demas días, esto es requerido para el código de optmización.

    Retorno
    -------
    demanda_results : dict
        Un diccionario de diccionarios que especifica la demanda horaria. 
        La primera clave es el día y dentro de ella se encuentran las franjas horarias. 
        Los valores son enteros que representan la demanda en ese día y franja horaria.
    """
    demanda_results = {}
    day2date = {}
    for record in demanda:
        fecha = datetime.fromisoformat(record['fecha_hora'])
        dia_semana = DAYS2DIAS[fecha.strftime("%A")]
        demanda_results.setdefault(dia_semana, {})
        franja =  f"{fecha.hour:02d}:{fecha.minute:02d}"
        demanda_results[dia_semana][H2F[franja]] = record['demanda']
        day2date[dia_semana] = f"{fecha.year}-{fecha.month:02d}-{fecha.day:02d}"
    
    if complete_franjas:
        for f in H2F.values():
            if f not in demanda_results['Sábado']:
                demanda_results['Sábado'][f] = 0

    if return_day2date:
        return demanda_results, day2date
        
    return demanda_results


def transform_workers(trabajadores: list[dict]):
    """Transforma trabajadores en formaton compatible para optimización.

    Parámetros
    ----------
    trabajadores : list[dict]
        Una lista de diccionarios que describe a los trabajadores disponibles para la programación. 
        Cada diccionario debe contener las siguientes claves:
            - "documento": El ID del empleado.
            - "contrato": El tipo de contrato (TP, MT).
    
    Retorno
    -------
    trabajadores_results : dict
        Un diccionario que describe a los trabajadores disponibles. 
        La primera clave es el documento del trabajador y el valor es el tipo de contrato.
    """
    trabajadores_results = {}
    for record in trabajadores:
        documento = record['documento']
        contrato = record['contrato']
        trabajadores_results[documento] = contrato
    return trabajadores_results