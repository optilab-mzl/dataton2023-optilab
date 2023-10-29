from .time import H2F, DAYS2DIAS
from datetime import datetime


def load_demanda(demanda, return_day2date=False, complete_franjas=True):
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


def load_workers(trabajadores):
    trabajadores_results = {}
    for record in trabajadores:
        documento = record['documento']
        contrato = record['contrato']
        trabajadores_results[documento] = contrato
    return trabajadores_results