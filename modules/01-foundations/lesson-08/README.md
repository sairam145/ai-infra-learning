# Lesson 08: API Development for ML Services

> **In one sentence:** an API is the front counter of the model: it takes requests, checks them, gets the model's answer, and sends it back. FastAPI is the standard Python tool for building one.

---

## Why FastAPI for ML

| | FastAPI | Flask | Django |
|---|---|---|---|
| Speed | Fast (async) | Moderate | Moderate |
| Input checking | **Built in** (Pydantic) | Manual | Manual/forms |
| API docs | **Automatic** at `/docs` | Add-on | Add-on |
| Fit for ML services | ⭐ Best | OK for small apps | Too heavy |

vLLM's own API server is built on FastAPI.

---

## The building blocks, plainly

| Piece | Plain meaning | Example |
|---|---|---|
| **Endpoint** | A door with a specific purpose | `POST /predict`, `GET /health` |
| **Method** | What kind of action | `GET` = read, `POST` = send data |
| **Path parameter** | Part of the address | `/models/resnet18` |
| **Query parameter** | Options after `?` | `/predict?top_k=3` |
| **Request body** | The data you send (JSON) | `{"text": "hello"}` |
| **File upload** | Send a file | an image for classification |
| **Pydantic model** | A strict form: what fields, which types, which limits | `text: str`, `top_k: int` between 1 and 10 |
| **Response model** | The guaranteed shape of the answer | `{"label": str, "confidence": float}` |

### Minimal ML API

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = load_model()          # load ONCE at startup, not per request
    yield

app = FastAPI(lifespan=lifespan)

class PredictRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    top_k: int = Field(default=3, ge=1, le=10)

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/v1/predict")
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"label": model.predict(req.text), "model_version": "v1"}
```

Bad input (e.g., `top_k: 50`) automatically gets a **422** error saying exactly which field is wrong.

---

## Production essentials

| Topic | Plain meaning | Why it matters |
|---|---|---|
| **Load the model once** (`lifespan`) | Load at startup, reuse for every request | Loading per request is extremely slow |
| **Validation** (Pydantic) | Reject bad input before it reaches the model | Protects the model and gives clear errors |
| **Error handling** (`HTTPException`) | Return the right status code with a message | Callers can tell their mistake from a server problem |
| **Async** | Keep accepting requests while waiting on slow work | Better throughput |
| **Background tasks** | Do slow side-work after responding (e.g., logging to a DB) | Faster responses |
| **Prometheus metrics** | `/metrics` with counts and latencies | Dashboards and alerts |
| **Structured (JSON) logs** | Logs a machine can search | Find one request in millions |
| **Versioning** (`/v1/`, `/v2/`) | Old and new APIs side by side | Change the API without breaking existing users |
| **Rate limiting** | Max requests per client | One client can't starve everyone (use Redis for multiple servers) |
| **Auto docs** (`/docs`) | Interactive test page | Free documentation and testing |

### The async trap (important)
- A plain `def` endpoint: FastAPI runs it in a thread pool automatically, so slow model calls don't freeze the server.
- An `async def` endpoint that calls a slow model **directly**: **this does block everything.**
- In `async def`, run heavy work with `await run_in_threadpool(model.predict, x)` (from `starlette.concurrency`), or simply use plain `def`.

### Status codes
| Code | Meaning |
|---|---|
| 200 | OK |
| 400 | Bad request |
| 401 / 403 | Not logged in / not allowed |
| 404 | Not found |
| 413 | Request too big |
| 422 | Input failed validation |
| 429 | Too many requests (rate limited) |
| 500 | Server bug |
| 503 | Not ready (model loading, overloaded) |

---

## Running it

| Command | Use |
|---|---|
| `uvicorn app:app --reload` | Development: auto-restart on code change |
| `uvicorn app:app --host 0.0.0.0 --port 8000` | Production, single process |
| `uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4` | Production, 4 processes |
| `gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 4` | Same, with gunicorn managing workers |
| `uvicorn app:app --timeout-graceful-shutdown 25` | Finish in-flight requests on shutdown |

**Workers warning for ML:** each worker loads **its own copy of the model**. 4 workers = 4× the memory. On a GPU, usually run **one process per GPU** and scale with more pods instead. vLLM manages this itself.

### Testing an API
| Command | What it does |
|---|---|
| `curl localhost:8000/health` | Quick health check |
| `curl -i ...` | Also show status code and headers |
| `curl -X POST localhost:8000/v1/predict -H "Content-Type: application/json" -d '{"text":"hi"}'` | Send JSON |
| `curl -F "file=@cat.jpg" localhost:8000/predict/image` | Upload a file |
| Open `http://localhost:8000/docs` | Click "Try it out" in the browser |

---

## Why it matters for AI/GPU DevOps
vLLM already provides an OpenAI-compatible API (`/v1/chat/completions`, `/health`, `/metrics`). What I build around it is the **gateway**: API keys, rate limits, request size limits, versioning, routing between models, and the dashboards. All of these are concepts from this lesson.

---

## Self-check
1. Why load the model in `lifespan` instead of inside the endpoint?
2. What does Pydantic give you for free?
3. When does an endpoint block the whole server?
4. What does `--workers 4` do to memory for an ML service?
5. 422 vs. 503?

<details>
<summary>Answers</summary>

1. Loading is slow; do it once at startup and reuse it for every request.
2. Input validation with clear 422 errors, and automatic API docs.
3. When an `async def` endpoint runs slow, blocking work directly.
4. Four processes, each with its own model copy: about 4× the memory.
5. 422 = the client sent bad input. 503 = the server isn't ready (e.g., model still loading).

</details>

---

*Part of my [AI Infrastructure learning log](../../../README.md). Course: [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
