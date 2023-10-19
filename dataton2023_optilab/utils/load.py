from .time import H2F
import datetime

dias_semana = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'}


def load_demanda(df, return_day2date=False):
    demanda = {}
    day2date = {}
    for index, row in df.iterrows():
        fecha = row.fecha_hora
        dia_semana = dias_semana[fecha.strftime("%A")]
        demanda.setdefault(dia_semana, {})
        franja =  f"{fecha.hour:02d}:{fecha.minute:02d}"
        demanda[dia_semana][H2F[franja]] = row.demanda
        day2date[dia_semana] = f"{fecha.year}-{fecha.month:02d}-{fecha.day:02d}"


    for f in H2F.values():
        if f not in demanda['Sábado']:
            demanda['Sábado'][f] = 0 

    if return_day2date:
        return demanda, day2date
        
    return demanda


def load_workers(df):
    return df.set_index('documento')['contrato'].to_dict()