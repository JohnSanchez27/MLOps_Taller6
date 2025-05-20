
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# Cargar modelo
model = joblib.load("model.pkl")

# Inicializar app
app = FastAPI(title="Penguin Classifier API")

# Esquema de entrada
class PenguinInput(BaseModel):
    island: str
    sex: str
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float

# Métricas Prometheus
REQUEST_COUNT = Counter("predict_requests_total", "Número total de predicciones")
REQUEST_LATENCY = Histogram("predict_request_latency_seconds", "Latencia de predicción en segundos")
PREDICTED_CLASS = Counter("predicted_class", "Clases predichas", ["species"])

@app.post("/predict")
@REQUEST_LATENCY.time()
def predict(penguin: PenguinInput):
    REQUEST_COUNT.inc()
    start_time = time.time()

    input_data = [[
        penguin.culmen_length_mm,
        penguin.culmen_depth_mm,
        penguin.flipper_length_mm,
        penguin.body_mass_g,
        penguin.island,
        penguin.sex
    ]]

    # Convertir a DataFrame con columnas ordenadas
    import pandas as pd
    input_df = pd.DataFrame(input_data, columns=[
        "culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g", "island", "sex"
    ])

    prediction = model.predict(input_df)[0]
    PREDICTED_CLASS.labels(species=prediction).inc()

    duration = time.time() - start_time
    return {"prediction": prediction, "duration_seconds": duration}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
