from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI
from torchvision.models import ResNet18_Weights, resnet18

model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the server starts: load the model before taking requests
    global model
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    model.eval()
    print("Model loaded successfully!")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "ML Model API", "model": "ResNet-18"}


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None, "torch_version": torch.__version__}


@app.get("/info")
def info():
    if model is None:
        return {"error": "Model not loaded"}
    params = sum(p.numel() for p in model.parameters())
    return {"model": "ResNet-18", "parameters": params, "device": "cpu"}
