"""
============================================
Módulo de Generación de Programación Horaria
============================================

Este módulo permite generar la programación horaria de los trabajadores de una sucursal teniendo en cuenta las restricciones laborales definidas.

Función principal
-----------------
"""
from time import time

from backend.pydantic_models import Demand, RowScheduling, Scheduling, Workers
from backend.scheduling_optimization import get_schedule as gs


def cambiar_nombres_claves(diccionario, mapeo):
    return {mapeo.get(clave, clave): valor for clave, valor in diccionario.items()}


def get_schedule(
    demanda: Demand,
    trabajadores: Workers,
) -> Scheduling:
    """
    Genera una programación horaria para los trabajadores de una sucursal.

    Parámetros
    ----------
    sucursal_codigo : int
        El código de identificación de la sucursal.

    demanda : list[dict]
        Una lista de diccionarios que especifica la demanda horaria de la sucursal.
        Cada diccionario debe contener las siguientes claves:
            - "fecha_hora": Una fecha y hora en formato ISO.
            - "demanda": Un entero que representa la demanda en ese momento.

    trabajadores : list[dict]
        Una lista de diccionarios que describe a los trabajadores disponibles para la programación.
        Cada diccionario debe contener las siguientes claves:
            - "documento": El ID del empleado.
            - "contrato": El tipo de contrato (TP, MT).

    Retorno
    -------
    programacion : list[dict]
        Una lista de diccionarios que contiene la programación generada. Cada diccionario incluye las siguientes claves:
            - "hora_franja": Una franja horaria (valor entero).
            - "estado": El estado del empleado en ese momento (Trabaja, Pausa Activa, Almuerza, Nada).
            - "documento": El ID del empleado.
            - "fecha": La fecha correspondiente a la programación.
            - "hora": La hora correspondiente a la franja horaria.

    Ejemplo de uso
    -------------
    >>> programacion = generar_programacion_horaria(123, demanda_horaria, lista_trabajadores)
    >>> print(programacion)

    """
    demanda = [dict(i) for i in demanda]
    # mapeo_claves = {'date': 'fecha_hora', 'demand': 'demanda'}
    # demanda = [cambiar_nombres_claves(d, mapeo_claves) for d in demanda]

    trabajadores = [dict(i) for i in trabajadores]
    # mapeo_claves = {'id': 'documento', 'type_of_contract': 'contrato'}
    # trabajadores = [cambiar_nombres_claves(t, mapeo_claves) for t in trabajadores]

    programacion = gs(demanda, trabajadores)

    # mapeo_claves = {'hora_franja':'time_slot_id', 'estado':'status', 'documento':'worker_id', 'fecha':'date', 'hora':'hour'}
    # programacion = [cambiar_nombres_claves(t, mapeo_claves) for p in programacion]
    rows = [RowScheduling(**p) for p in programacion[0]]
    return Scheduling(rows=rows)


if __name__ == "__main__":
    import json

    def load_json(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data

    for b in [569, 834, 60, 311, 487]:
        print("#" * 10, b, "#" * 10)
        demanda_path = (
            f"/home/juan/dev/dataton2023-optilab/test/data/input/demanda_{b}.json"
        )
        trabajadores_path = (
            f"/home/juan/dev/dataton2023-optilab/test/data/input/trabajadores_{b}.json"
        )

        demanda = load_json(demanda_path)
        trabajadores = load_json(trabajadores_path)

        programacion = generar_programacion_horaria(123, demanda, trabajadores)
