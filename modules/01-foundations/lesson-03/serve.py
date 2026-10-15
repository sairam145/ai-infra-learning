import glob, joblib
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, make_asgi_app

# STAGE 4: DEPLOY the newest version from the registry
latest = sorted(glob.glob("models/spam-*.joblib"))[-1]
model = joblib.load(latest)
VERSION = latest.split("spam-")[1].removesuffix(".joblib")

app = FastAPI()
app.mount("/metrics", make_asgi_app())   # STAGE 5: Prometheus reads metrics here

PREDICTIONS = Counter("predictions_total", "Predictions made", ["model_version", "label"])
LATENCY = Histogram("inference_seconds", "Time per prediction")

class Message(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok", "model_version": VERSION}

@app.post("/predict")
def predict(msg: Message):
    with LATENCY.time():
        label = model.predict([msg.text])[0]
    PREDICTIONS.labels(VERSION, label).inc()
    return {"label": label, "model_version": VERSION}
