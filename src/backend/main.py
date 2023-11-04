import datetime

import uvicorn
from fastapi import FastAPI
from model import get_schedule as gs
from pydantic_models import Demand, Workers, Scheduling


app = FastAPI()


@app.post("/get_schedule", response_model=Scheduling)
async def get_schedule(demand: Demand, workers: Workers):
    out = gs(demanda=demand.demand_time_points, trabajadores=workers.list_of_workers)
    # row = RowScheduling(
    #     time_slot_id=30,
    #     status="Trabaja",
    #     worker_id=1046,
    #     date="2023-12-14",
    #     hour="07:30",
    # )

    # out = Scheduling(rows=[row, row])
    return out


if __name__ == "__main__":
    uvicorn.run("main:app", port=5001, log_level="info", reload=True)
