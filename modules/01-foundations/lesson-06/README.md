# Lesson 06: Model Serving Basics

> **In one sentence:** model serving means putting a trained model behind an API so apps can get answers **fast, reliably, and at scale**, and it's the part of ML I'll spend most of my career on.

---

## Training vs. serving

| | Training | Serving (inference) |
|---|---|---|
| Analogy | A student studying for months | The student answering questions in an exam, live |
| Runs | Hours to weeks, occasionally | 24/7, every request |
| Cares about | Final accuracy | **Latency, throughput, uptime, cost per request** |
| Hardware | Many GPUs at once | Often one GPU per model copy, many copies |
| If it fails | Restart from a checkpoint | Users see errors right now |

---

## What a serving system must do

| Type | Requirements |
|---|---|
| **Performance** | Low latency (p50/p95/p99), high throughput, efficient GPU/CPU use |
| **Functional** | Correct predictions, input validation, model versioning, batch + single requests |
| **Operational** | Health checks, monitoring, logging, autoscaling, zero-downtime updates, rollback |

---

## Four ways to serve a model

| Approach | How it works | When to use | Analogy |
|---|---|---|---|
| **1. Embedded** | Model loaded inside the app itself | Tiny models, prototypes | A chef cooking in the dining room |
| **2. Model as a service** | Separate API (e.g., FastAPI) the app calls | Most custom models: scale and update independently | A separate kitchen with a service window |
| **3. Serving framework** | Purpose-built server that handles batching, versioning, metrics | Production at scale | A professional kitchen system |
| **4. Cloud ML platform** | Upload model, provider runs it | Fast start, less control, higher cost | Catering company |

### Serving frameworks: which matters now

| Framework | For | Status (2026) |
|---|---|---|
| **vLLM** | Large language models | ⭐ Industry default for LLMs. **My #1 skill.** |
| SGLang | LLMs (chat, agents, RAG) | Strong challenger |
| NVIDIA Triton / TensorRT-LLM | Many model types, lowest NVIDIA latency | Enterprise, NVIDIA-only |
| ONNX Runtime | Any model converted to ONNX | Fast, portable |
| TorchServe | PyTorch models | ⚠️ No longer actively developed. The course still teaches it. |
| TF Serving | TensorFlow models | Mature, legacy |
| FastAPI (custom) | Small/classic models | Simple, full control |

---

## The speed toolkit

| Technique | Plain meaning | Trade-off |
|---|---|---|
| **Batching** | Answer many requests in one pass | Higher throughput, slightly more wait per request |
| **Dynamic batching** | Collect requests until the batch is full **or** a max wait time passes, then run | Tune batch size vs. wait time |
| **Quantization** | Shrink the model (FP32 → INT8, 16-bit → 4-bit) | Smaller and faster; small quality drop |
| **Caching** | Remember answers to repeated inputs | Only helps repeated requests |
| **Warm-up** | Run fake requests at startup so the first real user isn't slow | Slower startup |
| **Async** | Accept new requests while waiting on slow work | More complex code |

**What I measured in Lesson 04:** INT8 quantization made DistilBERT 1.9× smaller and 2.4× faster on CPU, with the same answers. Batching raised texts/sec a lot.

---

## Releasing a new model safely

| Strategy | How it works | Analogy |
|---|---|---|
| **Blue-green** | Two full environments; switch all traffic at once; switch back if broken | Two stages, flip the spotlight |
| **Canary** | New version gets 5% of traffic first, then more | A few customers taste-test |
| **Shadow** | New version sees real traffic, but users only get the old one's answers | Trainee cooks alongside, nobody eats it |

---

## What to monitor

| Category | Metrics |
|---|---|
| Speed | Latency p50 / p95 / p99 |
| Volume | Requests per second, throughput |
| Errors | Error rate, timeouts |
| Resources | CPU, memory, **GPU utilization and GPU memory** |
| Availability | Uptime, health check status |
| **Model quality** | Prediction distribution, confidence scores, **data drift** |

The last row is what normal app monitoring misses. A server can be 100% healthy while the model gives bad answers.

---

## Key commands

| Command | What it does |
|---|---|
| `uvicorn app:app --host 0.0.0.0 --port 8000` | Run a FastAPI model service |
| `curl localhost:8000/health` | Is it alive? |
| `curl -X POST localhost:8000/predict -H "Content-Type: application/json" -d '{...}'` | Get a prediction |
| `curl localhost:8000/metrics` | Prometheus metrics |
| `vllm serve <model>` | Serve an LLM with an OpenAI-compatible API |
| `vllm bench serve` | Load-test an LLM server: TTFT and tokens/sec |

---

## Why it matters for AI/GPU DevOps
This lesson is the core of the job. In the LLM platform:
- **Serving engine:** vLLM (dynamic batching built in, called continuous batching)
- **Quantization:** load AWQ/GPTQ 4-bit models so more users fit per GPU
- **Warm-up + readiness probes:** big models take minutes to load; no traffic until ready
- **Canary rollouts:** through ArgoCD
- **Monitoring:** vLLM metrics + GPU metrics (DCGM) in Grafana

---

## Self-check
1. Three differences between training and serving?
2. Embedded model vs. model-as-a-service: when would you choose each?
3. What is dynamic batching, and what two limits control it?
4. Why do models need warm-up?
5. Which serving engine is the default for LLMs?

<details>
<summary>Answers</summary>

1. Serving runs 24/7, cares about latency and cost per request, and fails in front of users. Training is occasional and cares about final accuracy.
2. Embedded for tiny models and prototypes; as-a-service when you need to scale and update the model independently of the app.
3. Collect requests into a batch and run when it's full **or** a max wait time passes.
4. The first inference is much slower (setup, memory allocation, GPU kernel loading), so warm up before real users arrive.
5. vLLM.

</details>

---

*Part of my [AI Infrastructure learning log](../../../README.md). Course: [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
