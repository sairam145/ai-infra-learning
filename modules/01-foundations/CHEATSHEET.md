# Module 1 Cheat Sheet: AI Infrastructure Foundations

> Everything from Module 1 on one page: the ideas, the numbers, and the commands. Detailed explanations are in each [lesson README](README.md).

**Contents:** [Concepts](#1-concepts-in-one-line-each) · [Numbers & formulas](#2-numbers-and-formulas) · [Daily workflow](#3-daily-workflow) · [Linux & WSL](#4-linux--wsl) · [Python & venv](#5-python--virtual-environments) · [Git](#6-git--github) · [Docker](#7-docker) · [Compose](#8-docker-compose) · [Kubernetes](#9-kubernetes-kubectl) · [minikube / kind](#10-local-clusters-minikube--kind) · [Helm](#11-helm) · [AWS CLI](#12-aws-cli) · [Terraform](#13-terraform) · [PyTorch](#14-pytorch-inference-snippets) · [FastAPI](#15-fastapi--uvicorn) · [curl](#16-testing-apis-with-curl) · [Prometheus](#17-prometheus-metrics) · [vLLM](#18-vllm-preview) · [GPU](#19-gpu-commands) · [Status codes](#20-http-status-codes) · [Troubleshooting](#21-troubleshooting) · [Security rules](#22-security-rules)

---

## 1. Concepts in one line each

### ML infrastructure
| Concept | One line |
|---|---|
| ML infrastructure | Everything that gets a model's answers to real users: fast, reliable, affordable |
| The analogy | The model is the chef; infrastructure is the restaurant |
| ML vs. normal DevOps | Same foundation, plus changing models, data/model versioning, and quality monitoring |
| **Silent failure** | The server stays healthy while answers get worse; the #1 ML risk |
| MLOps | ML + DevOps + data engineering, run as a loop |
| Three pillars | People, Process, **Platform** (my part) |

### The ML lifecycle
```
Data → Train → Evaluate → Deploy → Monitor → Retrain → (back to Data)
```
| Term | One line |
|---|---|
| Training | The model learns from labeled examples |
| Inference / serving | The model answers new requests, live |
| Test set | Examples hidden during training, used only for grading |
| Accuracy | How often it's right overall |
| Precision | When it says "yes," how often it's really yes |
| Recall | Of all real "yes" cases, how many it caught |
| Model registry | Library of every model version plus its scores (MLflow, S3) |
| Quality gate | Automatic rule: don't release a model below a minimum score |
| Rollback | Switch back to the last good version |
| Data drift | Real-world input changes away from the training data |
| System metric | Is the server healthy? (latency, errors, CPU/GPU) |
| Model metric | Are the answers good? (predictions, confidence, accuracy) |

### Release strategies
| Strategy | One line |
|---|---|
| Blue-green | Two environments; switch all traffic at once; switch back if broken |
| Canary | New version to ~5% of users first, then more |
| Shadow | New version sees real traffic, but users only get the old answers |
| Rolling update | Kubernetes replaces pods gradually; no downtime |

### Frameworks and models
| Concept | One line |
|---|---|
| PyTorch | The framework that matters for LLMs (vLLM, Hugging Face) |
| Weights | The numbers a model learned; the architecture is the skeleton |
| `state_dict` | Weights only: the production way to save and load |
| `eval()` + `no_grad()` | "Exam mode": correct answers, less memory, faster |
| Device | Model and input must both be on CPU or both on the same GPU |
| Batching | Many requests per pass: higher throughput, slightly more wait |
| Warm-up | Fake requests at startup so the first real user isn't slow |
| Quantization | Shrink numbers (FP32 → INT8, FP16 → 4-bit): smaller, faster, small quality drop |
| ONNX | Universal model format ("PDF for models") |

### Serving
| Approach | Use |
|---|---|
| Embedded model | Tiny models, prototypes |
| Model as a service (FastAPI) | Most custom models |
| Serving engine | **vLLM** for LLMs; Triton/TensorRT-LLM; ONNX Runtime |
| Cloud ML platform | SageMaker, Vertex AI, Azure ML: fast start, less control |
| Dynamic batching | Run a batch when it's full **or** a max wait time passes |

### Containers and Kubernetes
| Concept | One line |
|---|---|
| Image | The packed box (template) |
| Container | A running copy of an image |
| Layer cache | Unchanged Dockerfile steps are reused, so order matters |
| Multi-stage build | Build in a full box, ship only the result in a clean small box |
| Pod | One running copy of a container in Kubernetes |
| Deployment | "Keep N pods of this image running" |
| Service | One stable address spreading traffic across pods |
| ConfigMap / Secret | Settings / passwords stored outside the image |
| Liveness probe | Alive? No → restart |
| Readiness probe | Ready for traffic? No → no traffic yet (big models load slowly) |
| HPA | Add/remove pods based on load |
| Taint / toleration | "GPU only" sign on a node / a pod's pass to enter |

### Cloud
| Concept | One line |
|---|---|
| IaaS / PaaS / SaaS | Rent machines / just deploy the app / just use the software |
| VPC | My private network in the cloud |
| Public / private subnet | Faces the internet / hidden from it |
| NAT gateway | Lets private servers reach out without being reachable |
| Security group | Firewall rules for a machine |
| S3 / ECR / EKS | Files & model weights / container images / managed Kubernetes |
| IAM | Who can do what; use roles, least privilege |
| Spot instances | Up to ~90% off; AWS can take them back with **2 minutes'** notice |

---

## 2. Numbers and formulas

### VRAM math
```
Model size  = parameters × bytes per parameter
              FP32 = 4 bytes · FP16 = 2 · INT8 = 1 · 4-bit ≈ 0.5
GPU memory  = model weights + KV cache (per-user notes) + ~1–2 GB overhead
KV cache    ≈ 128 KB per token for an 8B model (~0.5 GB per 4,000-token conversation)
```
| Model | FP16 | 4-bit | Fits a 16 GB T4? |
|---|---|---|---|
| 1.5B | 3 GB | ~1 GB | ✅ |
| 7–8B | 14–16 GB | ~4–5 GB | Only at 4-bit |
| 70B | 140 GB | ~35–40 GB | ❌ Needs bigger or multiple GPUs |

### My measured results
| Lab | Result |
|---|---|
| Lesson 03 spam detector | 67% accuracy on ~7 test messages; v2 "healthy" but wrong → rollback |
| DistilBERT FP32 (67M params) | 268 MB (= 67M × 4 bytes) |
| DistilBERT INT8 | 139 MB (1.9× smaller; embeddings stay FP32) |
| Batch of 8 on CPU | 44.6 ms → 18.5 ms with INT8 (2.4× faster) |

### Latency language
| Term | Meaning |
|---|---|
| p50 / p95 / p99 | 50% / 95% / 99% of requests finish faster than this |
| TTFT | Time to first token: the wait before an LLM's first word |
| Tokens/sec | How fast words come after the first one |
| Throughput | Total requests (or tokens) per second |

### Cost rules of thumb
| Option | Saving |
|---|---|
| Spot | up to ~90% |
| Reserved / Savings Plans (1–3 yr) | ~30–60% |
| Right-sizing | often 50%+ |
| My GPU learning cluster | ~$0.80/hour → `terraform destroy` every session |

---

## 3. Daily workflow

```bash
cd ~/ai-infra-learning
git pull                     # get the latest first
activate-ai                  # = source ~/ai-infra-venv/bin/activate
code .                       # VS Code (terminal: Ctrl + `)
# ... work ...
git add . && git commit -m "message" && git push
./verify-setup.sh            # check every tool anytime
```

---

## 4. Linux & WSL

| Command | What it does |
|---|---|
| `wsl -l -v` *(PowerShell)* | List WSL distros and versions (want VERSION 2) |
| `wsl --shutdown` *(PowerShell)* | Restart WSL (e.g., after editing `.wslconfig`) |
| `cd ~` | Go to the Linux home folder (keep projects here, not `/mnt/c/`) |
| `pwd` / `ls -la` | Where am I / list files including hidden |
| `mkdir -p a/b/c` | Make nested folders |
| `cat file` / `less file` | Show a file / scroll through it |
| `tail -f file.log` | Follow a log live |
| `grep -E "error|warn" file` | Find matching lines |
| `chmod +x script.sh` / `chmod 600 file` | Make executable / owner-only read-write |
| `sudo apt update && sudo apt install -y <pkg>` | Install software |
| `uname -m` | CPU architecture (`x86_64`) |
| `df -h` / `free -h` | Disk / memory usage |
| `ps aux \| grep uvicorn` / `pkill -f uvicorn` | Find / stop a process |
| `ss -ltnp \| grep 8000` | What's using port 8000 |
| `clear` | Clear the screen (do this before copying output after secrets) |
| `cmd1 && cmd2` | Run cmd2 only if cmd1 succeeded |
| `cat > file << 'EOF' ... EOF` | Write a multi-line file from the terminal |

**WSL memory** (`C:\Users\<you>\.wslconfig`):
```
[wsl2]
memory=8GB
```

---

## 5. Python & virtual environments

| Command | What it does |
|---|---|
| `python3 -m venv ~/ai-infra-venv` | Create an isolated environment |
| `source ~/ai-infra-venv/bin/activate` / `deactivate` | Enter / leave it |
| `which python` | Confirm you're inside the venv |
| `pip install -r requirements.txt` | Install a project's packages |
| `pip install --upgrade pip` | Update pip |
| `pip freeze > requirements.txt` | Save exact installed versions |
| `pip list` / `pip show torch` | List packages / details of one |
| `python script.py` | Run a script |
| `python -c "import torch; print(torch.__version__)"` | One-line check |

**Code-quality tools**
| Command | What it does |
|---|---|
| `ruff format src tests` | Auto-format code |
| `ruff check src tests` | Find bugs and bad patterns |
| `mypy src` | Check types |
| `pytest` / `pytest -x` / `pytest -k name` / `pytest -m unit` | Run tests / stop at first fail / by name / by tag |
| `pre-commit install` | Run the checks automatically on every commit |

---

## 6. Git & GitHub

| Command | What it does |
|---|---|
| `git config --global user.name "Sai Ram N."` | Set identity (also `user.email`) |
| `ssh-keygen -t ed25519 -C "<email>"` | Create an SSH key |
| `cat ~/.ssh/id_ed25519.pub` | Public key to paste into GitHub (safe to share) |
| `ssh -T git@github.com` | Test the GitHub connection |
| `git init` / `git clone <url>` | New repo / copy an existing one |
| `git status` | What changed (check before every commit) |
| `git add .` / `git add -A` | Stage changes / including deletions and renames |
| `git commit -m "msg"` | Save a snapshot |
| `git push` / `git pull` | Upload / download changes |
| `git remote add origin git@github.com:<user>/<repo>.git` | Link to GitHub (no `< >` brackets!) |
| `git remote set-url origin <url>` | Fix a wrong remote |
| `git push -u origin main` | First push of a new repo |
| `git log --oneline` | History, one line each |
| `git diff` | Exact line changes |
| `git checkout -- <file>` | Throw away uncommitted changes to a file |
| `git mv old new` | Rename/move a file, tracked |
| `git rev-parse --short HEAD` | Current commit ID (good image tag) |

`.gitignore` must block: `venv/ .env .aws/ *.tfstate .terraform/ models/ *.pth *.pt *.safetensors *.gguf *.bin`

---

## 7. Docker

### Dockerfile pattern (ML)
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN useradd -m appuser
COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser src/ ./src/
ENV PYTHONUNBUFFERED=1
USER appuser
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```
**Rules:** requirements before code · multi-stage · pin versions · non-root · clean up in the same `RUN` · `.dockerignore` · **CPU-only PyTorch** without a GPU: `pip install torch --index-url https://download.pytorch.org/whl/cpu`

### Images
| Command | What it does |
|---|---|
| `docker build -t ml-app:v1 .` | Build from the Dockerfile here |
| `docker build -f Dockerfile.gpu -t ml-app:gpu .` | Use another Dockerfile |
| `docker build --no-cache -t ml-app:v1 .` | Rebuild from scratch |
| `docker images` | List images + sizes |
| `docker history ml-app:v1` | Size per layer: what made it big? |
| `docker tag ml-app:v1 <repo>:v1` | Add a name (before pushing) |
| `docker push <repo>:v1` / `docker pull <repo>:v1` | Upload / download |
| `docker rmi ml-app:v1` | Delete an image |

### Containers
| Command | What it does |
|---|---|
| `docker run --rm -p 8000:8000 ml-app:v1` | Run; laptop:8000 → container:8000; auto-delete on stop |
| `docker run -d --name api ml-app:v1` | Background, named |
| `docker run -e KEY=value ...` | Environment variable |
| `docker run -v $(pwd)/models:/app/models:ro ...` | Mount a folder read-only |
| `docker run --memory=4g --cpus=2 ...` | Resource limits |
| `docker run --read-only --tmpfs /tmp ...` | Read-only filesystem, writable `/tmp` |
| `docker run --restart unless-stopped ...` | Auto-restart on crash |
| `docker run --gpus all ...` | Give the container the GPUs |
| `docker ps` / `docker ps -a` | Running / all |
| `docker logs -f api` | Follow output |
| `docker exec -it api bash` | Shell inside |
| `docker inspect api` | All details |
| `docker stats` | Live CPU/memory |
| `docker stop api` / `docker rm api` | Stop (sends SIGTERM) / remove |
| `docker run hello-world` | Test Docker works |

### Disk clean-up
| Command | What it does |
|---|---|
| `docker system df` | Disk used by Docker |
| `docker system prune` | Remove stopped containers, unused networks, dangling images |
| `docker volume prune` | Remove unused volumes (deletes data) |

### Push to AWS ECR
```bash
aws ecr create-repository --repository-name ml-app
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <acct>.dkr.ecr.us-east-1.amazonaws.com
docker tag ml-app:v1 <acct>.dkr.ecr.us-east-1.amazonaws.com/ml-app:v1
docker push <acct>.dkr.ecr.us-east-1.amazonaws.com/ml-app:v1
```

---

## 8. Docker Compose

| Command | What it does |
|---|---|
| `docker compose up -d` | Start all services in the background |
| `docker compose up -d --build` | Rebuild, then start |
| `docker compose ps` | What's running |
| `docker compose logs -f <service>` | Follow one service |
| `docker compose exec <service> bash` | Shell inside a service |
| `docker compose restart <service>` | Restart one service |
| `docker compose down` / `down -v` | Stop and remove / also delete volumes |

Services reach each other **by name** (`redis:6379`, `prometheus:9090`). Use `docker compose` (space); the `version:` line is obsolete.

---

## 9. Kubernetes (kubectl)

### Look around
| Command | What it does |
|---|---|
| `kubectl get nodes -o wide` | Machines in the cluster |
| `kubectl get pods` / `get pods -A` / `get pods -w` | Pods here / all namespaces / watch live |
| `kubectl get deploy,svc,cm,hpa` | Several resource types at once |
| `kubectl get pods -l app=ml-api` | Filter by label |
| `kubectl describe pod <pod>` | Full details + **Events** (first stop when broken) |
| `kubectl get events --sort-by=.lastTimestamp` | Recent events, newest last |
| `kubectl top nodes` / `top pods` | CPU/memory (needs metrics-server) |
| `kubectl config get-contexts` / `use-context <name>` | Which cluster am I talking to / switch |

### Create and change
| Command | What it does |
|---|---|
| `kubectl apply -f file.yaml` / `-f folder/` | Create or update |
| `kubectl delete -f file.yaml` | Remove |
| `kubectl create namespace ml` / `-n ml` | Make / use a namespace |
| `kubectl edit cm ml-api-config` | Edit live |
| `kubectl scale deploy/ml-api --replicas=3` | Set the pod count |

### Debug
| Command | What it does |
|---|---|
| `kubectl logs <pod>` / `logs -f <pod>` | Output / follow |
| `kubectl logs <pod> --previous` | Logs of the **crashed** copy |
| `kubectl logs -l app=ml-api --all-containers` | Logs from all matching pods |
| `kubectl exec -it <pod> -- bash` | Shell inside |
| `kubectl exec <pod> -- env` | See environment variables |
| `kubectl port-forward svc/ml-api 8000:80` | Reach a Service at `localhost:8000` |

### Releases
| Command | What it does |
|---|---|
| `kubectl set image deploy/ml-api ml-api=ml-app:v3` | Roll out a new image |
| `kubectl rollout status deploy/ml-api` | Watch it finish |
| `kubectl rollout history deploy/ml-api` | Past versions |
| `kubectl rollout undo deploy/ml-api` | **Roll back** |
| `kubectl rollout undo deploy/ml-api --to-revision=1` | Roll back to a specific version |
| `kubectl rollout restart deploy/ml-api` | Restart pods (pick up new config) |

### Pod with probes, limits, and GPU (shape to remember)
```yaml
containers:
- name: model
  image: ml-app:v2
  ports: [{containerPort: 8000}]
  resources:
    requests: {cpu: "500m", memory: "1Gi"}
    limits:   {memory: "2Gi"}            # GPU: add  nvidia.com/gpu: 1
  livenessProbe:  {httpGet: {path: /health, port: 8000}, periodSeconds: 10}
  readinessProbe: {httpGet: {path: /ready,  port: 8000}, initialDelaySeconds: 20}
tolerations:                             # GPU nodes only
- {key: nvidia.com/gpu, operator: Exists, effect: NoSchedule}
```

### Pod status → first check
| Status | Meaning | Check |
|---|---|---|
| `Pending` | Nowhere to fit (CPU/mem/GPU, taint) | `describe pod` → Events |
| `ImagePullBackOff` | Can't get the image | Name/tag; `kind load docker-image` / `minikube image load` |
| `CrashLoopBackOff` | Starts, crashes, repeats | `logs --previous` |
| `OOMKilled` | Over its memory limit | Raise limit / shrink model |
| `0/1 READY` | Readiness failing (model still loading) | Probe path, `initialDelaySeconds` |

---

## 10. Local clusters (minikube / kind)

| Command | What it does |
|---|---|
| `minikube start --driver=docker --memory=4096` | Start (first run 3–5 min; don't Ctrl+C) |
| `minikube stop` / `minikube delete` | Pause / wipe completely |
| `minikube image load ml-app:v2` | Copy a local image into the cluster |
| `minikube service <svc> --url` | Get a URL for a Service |
| `minikube addons enable metrics-server` | Enable `kubectl top` / HPA |
| `kind create cluster --name dev` | Start a kind cluster |
| `kind load docker-image ml-app:v2 --name dev` | Copy a local image in |
| `kind delete cluster --name dev` | Remove it |

---

## 11. Helm

| Command | What it does |
|---|---|
| `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts` | Add a chart source |
| `helm repo update` | Refresh chart lists |
| `helm search repo prometheus` | Find charts |
| `helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace` | Install |
| `helm install <name> <chart> -f values.yaml` | Install with my settings |
| `helm upgrade --install <name> <chart> -f values.yaml` | Install or update (safe to re-run) |
| `helm list -A` | What's installed |
| `helm rollback <name> 1` | Go back to release 1 |
| `helm uninstall <name> -n <ns>` | Remove |
| `helm show values <chart>` | See all settings a chart accepts |

---

## 12. AWS CLI

| Command | What it does |
|---|---|
| `aws configure` | Set key, secret, region (`us-east-1`), output (`json`) |
| `aws sts get-caller-identity` | Who am I? (should end `:user/sairam-cli`, never `:root`) |
| `aws s3 mb s3://<bucket>` | Make a bucket |
| `aws s3 cp file s3://<bucket>/path/` | Upload |
| `aws s3 ls s3://<bucket>/` | List |
| `aws s3 sync ./models s3://<bucket>/models/` | Upload a folder (only changes) |
| `aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId,State.Name,InstanceType]" --output table` | My machines, as a table |
| `aws ec2 describe-instance-types --instance-types g4dn.xlarge` | GPU instance specs |
| `aws ec2 stop-instances` / `terminate-instances --instance-ids i-...` | Stop / delete |
| `aws service-quotas get-service-quota --service-code ec2 --quota-code L-DB2E81BA` | My GPU (G and VT) vCPU quota |
| `aws eks update-kubeconfig --region us-east-1 --name llm-platform` | Point kubectl at my EKS cluster |
| `aws iam create-access-key` / `update-access-key --status Inactive` / `delete-access-key` | Make / disable / delete a key |

**GPU quota:** Console → Service Quotas → EC2 → *Running On-Demand G and VT instances* → request 8 vCPUs. **Per region.**

---

## 13. Terraform

| Command | What it does |
|---|---|
| `terraform init` | Download providers/modules (first run, or after changes) |
| `terraform fmt` | Tidy formatting |
| `terraform validate` | Check syntax |
| `terraform plan` | **Preview** what would change (read it!) |
| `terraform apply` | Make the changes (EKS takes ~15–20 min) |
| `terraform output` | Show outputs (e.g., the kubeconfig command) |
| `terraform state list` | What Terraform is managing |
| `terraform destroy` | **Delete everything** (end of every GPU session) |

Never commit `*.tfstate` or `.terraform/`: state can contain secrets.

---

## 14. PyTorch inference snippets

```python
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

model = MyModel()
model.load_state_dict(torch.load("weights.pth", map_location=device))   # weights only
model.to(device).eval()                                                 # exam mode

with torch.no_grad():                                                   # no learning
    out = model(x.to(device))                                           # same device!

torch.save(model.state_dict(), "weights.pth")                           # save weights only
params = sum(p.numel() for p in model.parameters())                     # size: params × 4 bytes (FP32)
```

Hugging Face:
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
tok = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english").eval()
```

GPU memory checks:
```python
torch.cuda.memory_allocated() / 1e9    # GB in use by tensors
torch.cuda.memory_reserved() / 1e9     # GB reserved by PyTorch
torch.cuda.empty_cache()               # release cached memory
```

**Changed in modern PyTorch:** `weights=` not `pretrained=True` · `torch.load` of a whole model fails by default (2.6+) · TorchScript → `torch.compile`/`torch.export` · `torch.ao.quantization` → **torchao**.

---

## 15. FastAPI & uvicorn

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

@asynccontextmanager
async def lifespan(app):
    app.state.model = load_model()        # load ONCE at startup
    yield

app = FastAPI(lifespan=lifespan)

class Req(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/v1/predict")
def predict(req: Req):                    # plain def = runs in a thread pool
    return {"label": app.state.model.predict(req.text)}
```

| Command | What it does |
|---|---|
| `uvicorn app:app --reload` | Dev mode, auto-restart |
| `uvicorn app:app --host 0.0.0.0 --port 8000` | Accept outside connections (needed in containers) |
| `uvicorn app:app --workers 4` | 4 processes (**4 model copies in memory**) |
| `uvicorn app:app --timeout-graceful-shutdown 25` | Finish in-flight requests on shutdown |
| `http://localhost:8000/docs` | Auto-generated test page |

**Async trap:** a slow model call directly inside `async def` freezes the server. Use plain `def`, or `await run_in_threadpool(...)`.

---

## 16. Testing APIs with curl

| Command | What it does |
|---|---|
| `curl localhost:8000/health` | Simple GET |
| `curl -i localhost:8000/ready` | Also show status code + headers |
| `curl -s ... \| python -m json.tool` | Pretty-print JSON |
| `curl -X POST localhost:8000/v1/predict -H "Content-Type: application/json" -d '{"text":"hi"}'` | Send JSON |
| `curl -F "file=@cat.jpg" localhost:8000/predict/image` | Upload a file |
| `curl -H "X-Request-Id: test-1" ...` | Custom header (trace a request in logs) |
| `time curl ...` | Measure how long it took |
| `curl -s localhost:8000/metrics \| grep ^predictions_total` | Read one metric |

---

## 17. Prometheus metrics

```python
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app
REQS    = Counter("predictions_total", "Predictions", ["model_version", "label"])
LATENCY = Histogram("inference_seconds", "Time per prediction")
INFLIGHT = Gauge("inflight_requests", "Requests in progress")
app.mount("/metrics", make_asgi_app())

with LATENCY.time():
    label = model.predict(x)
REQS.labels("v1", label).inc()
```
| Metric type | Use |
|---|---|
| Counter | Only goes up: requests, errors, predictions |
| Gauge | Goes up and down: in-flight requests, GPU memory |
| Histogram | Distribution: latency → p50/p95/p99 |

**PromQL basics**
| Query | Meaning |
|---|---|
| `predictions_total` | Current totals |
| `rate(predictions_total[1m])` | Per-second rate over the last minute |
| `sum by (label) (rate(predictions_total[5m]))` | Rate split by label |
| `histogram_quantile(0.95, rate(inference_seconds_bucket[5m]))` | p95 latency |

Counters reset when the process restarts; Prometheus stores the history.

---

## 18. vLLM (preview)

| Command | What it does |
|---|---|
| `pip install vllm` | Install |
| `vllm serve <model> --max-model-len 4096 --gpu-memory-utilization 0.9` | Serve an LLM (OpenAI-compatible API on :8000) |
| `docker run --gpus all -p 8000:8000 vllm/vllm-openai --model <model>` | Same, in Docker |
| `curl localhost:8000/v1/models` | Which model is loaded |
| `curl localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"<model>","messages":[{"role":"user","content":"hi"}]}'` | Ask a question |
| `curl localhost:8000/metrics` | Live serving metrics |
| `vllm bench serve ...` | Load test: TTFT, tokens/sec |

| Setting | Effect |
|---|---|
| `--gpu-memory-utilization` | Share of VRAM vLLM may use; leftover after weights = KV cache |
| `--max-model-len` | Longest conversation; lower = more users fit |
| `--max-num-seqs` | Max requests at once |
| `--tensor-parallel-size` | Split a model across GPUs |
| `--dtype half` | FP16 (needed on T4: no bfloat16) |

---

## 19. GPU commands

| Command | What it does |
|---|---|
| `nvidia-smi` | GPU model, memory used, running processes |
| `watch -n 1 nvidia-smi` | Refresh every second |
| `nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv` | Compact numbers |
| `docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi` | Test Docker can see the GPU |
| `kubectl describe node <gpu-node> \| grep -A6 Allocatable` | Does Kubernetes see `nvidia.com/gpu`? |
| `python -c "import torch; print(torch.cuda.is_available())"` | Does PyTorch see a GPU? |

---

## 20. HTTP status codes

| Code | Meaning | Typical cause |
|---|---|---|
| 200 | OK | — |
| 400 | Bad request | Batch too large, malformed request |
| 401 / 403 | Not logged in / not allowed | Missing or wrong API key/token |
| 404 | Not found | Wrong path |
| 413 | Too large | Body over the size limit |
| 422 | Invalid input | Pydantic validation failed (says which field) |
| 429 | Too many requests | Rate limit; respect `Retry-After` |
| 500 | Server error | Bug in the code |
| 503 | Not ready | Model still loading / overloaded |

---

## 21. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `docker: command not found` in WSL | Docker Desktop not linked | Settings → Resources → WSL Integration → Ubuntu |
| Docker `permission denied` (Linux) | Not in the docker group | `sudo usermod -aG docker $USER`, re-login |
| Container exits immediately | App crashed | `docker logs <c>` |
| `port is already allocated` | Port in use | Stop the other process or `-p 8001:8000` |
| `no space left on device` | Old images | `docker system prune` |
| Image is many GB | CUDA PyTorch, no multi-stage | CPU-only torch, multi-stage, `.dockerignore` |
| Healthcheck always fails | `curl`/`requests` missing in slim image | Python `urllib` |
| minikube broken / `connection refused` | Interrupted first start | `minikube delete` → start again, wait |
| `CUDA out of memory` | Model/batch too big | Smaller batch, quantize, lower `--max-model-len`, bigger GPU |
| Very slow first request | No warm-up | Warm up at startup |
| `Expected tensor on cuda:0 but got cpu` | Device mismatch | Move input to the model's device |
| Shape mismatch error | Wrong input size | Validate input |
| AWS `sts.yes.amazonaws.com` SSL error | Typed "yes" as region | `aws configure` → `us-east-1` |
| `-bash: <x>: No such file` | Typed `< >` placeholders | Type the value without brackets |
| Push rejected | Local copy behind GitHub | `git pull`, then push |
| Model "healthy" but wrong answers | Silent failure | Quality gate, bigger test set, canary, rollback |

---

## 22. Security rules

1. **Secrets go in the terminal only.** Never in chat, screenshots, GitHub, or videos.
2. `clear` after `aws configure`, before copying any output.
3. Leaked key → IAM → **Deactivate → Delete** immediately → new key → check Billing and EC2.
4. `chmod 600 ~/.aws/credentials`.
5. IAM user or role, never root keys; least privilege in real teams.
6. `.gitignore` for `.env`, `.aws/`, `*.tfstate`, `.terraform/`, model files.
7. Containers run as **non-root**; read-only filesystem where possible.
8. GPU nodes and servers in **private subnets**; security groups open only what's needed.
9. Public SSH key (`.pub`) is shareable; the private key never is.
10. `terraform destroy` when done: forgotten resources are a cost *and* a security risk.

---

*Part of my [AI Infrastructure learning log](../../README.md). Course: [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
