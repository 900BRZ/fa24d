from fastapi import FastAPI
from dataclasses import dataclass
from .lib.csv import read

app = FastAPI()


@dataclass
class FileDesc:
    path: str
    lap_number: int


@app.post("/compare")
def read_root(baseline: FileDesc, experiment: FileDesc):
    baseline_res = read(baseline.path)[baseline.lap_number - 1]
    experiment_res = read(experiment.path)[experiment.lap_number - 1]

    return {
        "baseline": baseline_res.lap_number,
        "experiment": experiment_res.lap_number,
    }


@app.post("/view")
def read_item(file: FileDesc):
    return {"lap": read(file.path)}
