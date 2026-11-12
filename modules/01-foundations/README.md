# Module 1: Foundations ✅

> **What this module gave me:** the full picture of how a machine learning model gets from a laptop into production, and the tools to do it: Python, Docker, Kubernetes, the cloud, APIs, and monitoring.

---

## Lessons

| # | Lesson | In one line | Hands-on |
|---|---|---|---|
| 01 | [Introduction to ML Infrastructure](lesson-01/README.md) | The model is the chef; infrastructure is the restaurant | — |
| 02 | [Development Environment Setup](lesson-02/README.md) | WSL2 + Docker + kubectl + Helm + minikube + AWS CLI + Terraform | [`verify-setup.sh`](../../verify-setup.sh) |
| 03 | [ML Infrastructure Basics](lesson-03/README.md) | The 6-stage ML lifecycle loop | Spam detector: train → evaluate → version → serve → monitor → **rollback** |
| 04 | [ML Frameworks](lesson-04/README.md) | Load, run, speed up, and troubleshoot PyTorch models | DistilBERT benchmark: warm-up, batching, INT8 quantization |
| 05 | [Cloud Computing for ML](lesson-05/README.md) | Rent compute, storage, and GPUs securely and cheaply | — |
| 06 | [Model Serving Basics](lesson-06/README.md) | Put a model behind an API: fast, reliable, at scale | — |
| 07 | [Docker Basics](lesson-07/README.md) | Pack apps into containers; multi-stage, non-root, GPU images | — |
| 08 | [API Development](lesson-08/README.md) | FastAPI: validation, errors, async, metrics, versioning | — |

**Exercises:** [all 10 explained in plain words, with commands](exercises/README.md)

**📋 [Cheat sheet](CHEATSHEET.md):** every concept, number, and command from Module 1 on one page

---

## What I built and measured

### Lesson 03: mini ML lifecycle (`lesson-03/`)
- `train.py` trains, evaluates, and saves **versioned** models; `serve.py` serves the newest one with `/health`, `/predict`, `/metrics`.
- **Real incident:** version 2 deployed "healthy" but called a scam message `ham`. Both versions scored 67% on a ~7-message test set. Fixed by **rolling back**.
- **Lesson:** a healthy server is not a good model. Gate deploys on evaluation, and use a test set big enough to compare versions.

### Lesson 04: PyTorch inference benchmark (`lesson-04/`)
| Measurement | Result |
|---|---|
| DistilBERT FP32 weights | **268 MB** (67M params × 4 bytes: the VRAM math checks out) |
| INT8 quantized weights | **139 MB** (1.9× smaller; embeddings stay FP32, so not 4×) |
| Batch of 8 on CPU | **44.6 ms → 18.5 ms** (2.4× faster) |
| Answer quality after quantization | Unchanged (POSITIVE, 1.00) |

---

## Labs (built into the main project)

Module 1 has five labs. I'm doing them as part of my main project rather than as separate exercises:

| Lab | What it teaches | Where it happens in the project |
|---|---|---|
| 01 Python dev environment | ruff, mypy, pytest, pre-commit on every commit | Project repo setup + CI |
| 02 First Docker container | Multi-stage Dockerfile, image vs. container | Model server and gateway images |
| 03 Local Kubernetes with kind | Deploy, Service, port-forward | Local testing before EKS |
| 04 Serve a scikit-learn model | FastAPI + Pydantic + container + K8s | Already done in Lesson 03; vLLM in the project |
| 05 Prometheus instrumentation | Metrics → scrape → PromQL | Phase 4: Prometheus + Grafana + DCGM + vLLM metrics |

---

## The 10 things I'm taking from Module 1

1. **ML infra = DevOps + changing models + quality monitoring.** Same foundation, extra layers.
2. **The lifecycle is a loop:** data → train → evaluate → deploy → monitor → retrain.
3. **Silent failures are the real danger.** Monitor model quality, not just server health.
4. **Version everything** (code, data, models) so you can compare and roll back.
5. **Release safely:** blue-green, canary, shadow.
6. **Inference basics:** `eval()` + `no_grad()`, same device, warm up, batch.
7. **Quantization** makes models smaller and faster for little quality loss. Know *what* got quantized.
8. **Docker images:** requirements before code, multi-stage, non-root, CPU-only PyTorch when there's no GPU.
9. **APIs:** load the model once, validate input, clear status codes, metrics, versioned endpoints.
10. **Cloud cost discipline:** right-size, spot for interruptible work, budget alerts, destroy when done.

---

## Corrections to the course material (as of late 2026)

| Course says | Reality |
|---|---|
| `torch==2.1.0` | Doesn't install on Python 3.12; use current versions |
| `resnet18(pretrained=True)` | Old syntax; now `weights=ResNet18_Weights.DEFAULT` |
| `@app.on_event("startup")` | Deprecated; use `lifespan` |
| `torch.load('model_complete.pth')` | Fails by default since PyTorch 2.6; save/load `state_dict` |
| TorchScript for optimization | Maintenance mode; use `torch.compile` / `torch.export` |
| `torch.ao.quantization` | Deprecated; replaced by **torchao**. For LLMs, use pre-quantized AWQ/GPTQ models. |
| TorchServe for serving | No longer actively developed; **vLLM** for LLMs |
| Spot "30-second notice" | That's GCP. **AWS gives 2 minutes.** |
| A 7B LLM needs "28 GB+" | That's for training. Serving: ~14 GB at FP16, ~4–5 GB at 4-bit. |
| Healthchecks using `curl`/`requests` | Not in slim images; use Python's `urllib` |
| `docker-compose` + `version: '3.8'` | Now `docker compose`; the `version` line is obsolete |

---

## Next: Module 2: Cloud Computing

---

*Part of my [AI Infrastructure learning log](../../README.md). Course: [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
