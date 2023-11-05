from fastapi import FastAPI

from backend.model import get_schedule as gs
from backend.pydantic_models import Demand, Scheduling, Workers

app = FastAPI()


@app.post("/get_schedule", response_model=Scheduling)
async def get_schedule(demand: Demand, workers: Workers):
    schedule = gs(
        demanda=demand.demand_time_points, trabajadores=workers.list_of_workers
    )
    return schedule
