import json

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
INPUT_PATH = "data/input/487.json"
OUTPUT_PATH = "data/input/487.json"


def test_get_schedule():
    with open(INPUT_PATH, "r") as f:
        input = json.load(f)

    with open(OUTPUT_PATH, "r") as f:
        output = json.load(f)

    print("INPUT = ", input)
    print("OUTPUT = ", output)

    response = client.post("/get_schedule", json=input)

    assert response.status_code == 200
    assert response.json() == output
