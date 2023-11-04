from pydantic import BaseModel
from typing import List, Literal


class DemandTimePoint(BaseModel):
    fecha_hora: str
    demanda: int


class Demand(BaseModel):
    demand_time_points: List[DemandTimePoint]


class Worker(BaseModel):
    documento: int
    contrato: Literal["TP", "MT"]


class Workers(BaseModel):
    list_of_workers: List[Worker]


class RowScheduling(BaseModel):
    hora_franja: int
    estado: Literal["Trabaja", "Pausa Activa", "Almuerza", "Nada"]  #  lowecase
    documento: int
    fecha: str
    hora: str


class Scheduling(BaseModel):
    rows: List[RowScheduling]