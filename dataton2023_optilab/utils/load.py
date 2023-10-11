from .time import H2F

def load_demanda(df):
    demanda = {}
    for index, row in df.iterrows():
        fecha = row.fecha_hora
        franja =  f"{fecha.hour:02d}:{fecha.minute:02d}"
        demanda[H2F[franja]] = row.demanda
    return demanda