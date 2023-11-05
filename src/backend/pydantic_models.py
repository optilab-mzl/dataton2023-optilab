from typing import List, Literal

from pydantic import BaseModel


class DemandTimePoint(BaseModel):
    fecha_hora: str
    demanda: int


class Demand(BaseModel):
    demand_time_points: List[DemandTimePoint]


class Worker(BaseModel):
    documento: int
    contrato: Literal["TC", "MT"]


class Workers(BaseModel):
    list_of_workers: List[Worker]


class RowScheduling(BaseModel):
    hora_franja: int
    estado: str
    documento: int
    fecha: str
    hora: str


class Scheduling(BaseModel):
    rows: List[RowScheduling]
