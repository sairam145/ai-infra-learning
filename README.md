# AI Infrastructure Learning

My learning log for becoming an **AI / GPU DevOps engineer**: running AI models on GPUs in production, reliably and cheaply.

I learn by building. Every lesson ends with something working, committed here.

---

## 1. Goal

- **Role:** AI Infrastructure / GPU DevOps engineer
- **Method:** follow the [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license) and build my own enterprise-grade LLM platform on AWS alongside it
- **Pace:** ~50 hours/week
- **End result:** a public repo showing a model served on GPUs in Kubernetes, with real latency and cost numbers

---

## 2. Progress

### Curriculum: Module 1 (Foundations)

| # | Lesson | Status |
|---|---|---|
| 01 | Introduction to ML Infrastructure | ✅ Done |
| 02 | Development Environment Setup | ✅ Done |
| 03 | ML Infrastructure Basics | ⏳ Next |
| 04 | ML Frameworks | ⬜ |
| 05 | Cloud Intro | ⬜ |
| 06 | Model Serving Basics | ⬜ |
| 07 | Docker Basics | ⬜ |
| 08 | API Development | ⬜ |

### Main project: LLM platform on AWS

| Phase | What I build | Status |
|---|---|---|
| 1 | VPC + EKS + GPU node pool (Terraform) | ⬜ Code ready, waiting on GPU quota |
| 2 | NVIDIA GPU Operator | ⬜ |
| 3 | vLLM serving via Helm | ⬜ |
| 4 | Observability: Prometheus, Grafana, DCGM, vLLM metrics | ⬜ |
| 5 | Autoscaling: Karpenter + KEDA | ⬜ |
| 6 | GitOps + security: ArgoCD, Trivy, Kyverno | ⬜ |
| 7 | API gateway + RAG (Qdrant) | ⬜ |
| 8 | Failure drills, runbooks, cost report | ⬜ |

---

## 3. Skills I am building

**Master (these get me hired):**
1. **vLLM:** deploying and tuning the LLM serving engine
2. **Inference performance:** batching, KV cache, TTFT, tokens/sec
3. **VRAM math and model formats:** will a model fit, and how many users fit
4. **Kubernetes GPU scheduling:** GPU node pools, taints/tolerations, GPU Operator, Karpenter
5. **NVIDIA stack:** `nvidia-smi`, CUDA/driver versions, GPU debugging
6. **GPU observability:** Prometheus + Grafana + DCGM + vLLM metrics
7. **Terraform for GPU infra**

**Working knowledge:** Hugging Face, Ollama, ArgoCD, Trivy, Kyverno/OPA, RAG + vector DB, Backstage

**Later:** Go, LangChain/LangGraph

**Already have (refresh only):** Kubernetes (CKA), Docker, Helm, Terraform, AWS/Azure, CI/CD, Linux, Bash, Python, Prometheus, Grafana

---

## 4. Concepts learned so far

### What ML infrastructure is (Lesson 01)
- **The model is the chef; infrastructure is the restaurant.** A model alone serves nobody. My job is building everything that gets its answers to users.
- **Why it's harder than normal DevOps:** models change, data quality decides results, GPUs are expensive, scale is huge, and failures are *silent*: the server stays up while the answers get worse.
- **MLOps loop:** Data → Training → Deployment → Feedback → repeat. Infrastructure automates the loop.
- **Three pillars:** People, Process, Platform. My part is the platform.

### vLLM: the #1 skill
- **What it is:** the open-source engine that serves LLMs on GPUs through an OpenAI-compatible API. It's the industry default.
- **GPU memory = recipe book + customer notes.**
  - Recipe book = model weights (fixed size)
  - Customer notes = **KV cache**, the per-conversation memory, which grows with every user and every word
  - Out of memory almost always means too many notes.
- **Why vLLM is fast:**
  - **PagedAttention:** hands out note space in small pages, only as needed, so nothing is wasted
  - **Continuous batching:** starts the next request as soon as a slot frees up

### The two speeds
- **TTFT (time to first token):** how long until the first word appears. Set by the *reading* phase (prefill).
- **Tokens/sec:** how fast words keep coming. Set by the *writing* phase (decode).
- More users at once means a cheaper GPU per user but slower answers for each user. The job is finding the balance.

### Why a server gets slow
1. **Line at the door:** too many requests waiting, so TTFT rises
2. **Notes full:** KV cache near 100%, so requests get paused
3. **One giant document** blocks everyone else

### vLLM speed tricks
| Problem | Fix |
|---|---|
| Same opening text reread for every user | Prefix caching (on by default) |
| One huge document blocks others | Chunked prefill (on by default) |
| Words come out too slowly | Speculative decoding (small model guesses, big model checks) |
| Not enough memory, or writing too slow | Quantization (smaller model) |

### Main vLLM settings
| Setting | Meaning |
|---|---|
| `--gpu-memory-utilization` | Share of GPU memory vLLM may use (default 0.9) |
| `--max-model-len` | Longest conversation allowed. Lower means more users fit. |
| `--max-num-seqs` | Most requests handled at once |
| `--tensor-parallel-size` | Split a big model across several GPUs |

### VRAM math
```
Model size  = parameters × bytes per parameter
              FP16 = 2 bytes · 8-bit = 1 byte · 4-bit (AWQ/GPTQ) ≈ 0.5 byte
Overhead    ≈ 1–2 GB
KV cache    ≈ 128 KB per token for an 8B model (≈ 0.5 GB per 4,000-token conversation)
```
- 8B model at FP16 = 16 GB, so it **doesn't fit** on a 16 GB T4
- 8B at 4-bit ≈ 5 GB, leaving ~8 GB for notes on a T4: about 16 long or 64 short conversations at once
- 70B at FP16 = 140 GB, so it won't fit on one 80 GB GPU without 4-bit or multiple GPUs

### Inference engines in the market
| Engine | When to use |
|---|---|
| **vLLM** | Default for most companies, widest hardware support. **Learn first.** |
| SGLang | Faster for chatbots/agents/RAG with shared prompt text |
| TensorRT-LLM + Triton (NVIDIA Dynamo) | Lowest latency on NVIDIA, but models must be compiled first |
| LMDeploy | Fast, less widely used |
| Hugging Face TGI | Maintenance mode since Dec 2025, legacy only |
| Ollama / llama.cpp | Local laptop testing, not production |

### Key vLLM commands
```bash
nvidia-smi                       # GPU, memory, processes
vllm serve <model> [settings]    # start the server
curl localhost:8000/health       # alive?
curl localhost:8000/v1/models    # which model is loaded
curl localhost:8000/metrics      # live numbers for monitoring
vllm bench serve                 # load test: TTFT and tokens/sec
pkill -f vllm                    # stop
```

---

## 5. My development environment (Lesson 02)

**Setup:** Windows + **WSL2 (Ubuntu 24.04)**. I work inside Ubuntu; only Docker Desktop and VS Code run on Windows.

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.12.3 | Language of AI tooling |
| Virtual env | `~/ai-infra-venv` | Isolated packages. Activate with `activate-ai`. |
| PyTorch | 2.14.1 | ML framework (runs on CPU on my laptop, `GPU: False`) |
| Transformers, FastAPI, uvicorn, pytest | latest | Models, APIs, tests |
| Git | 2.43 | Version control, SSH key linked to GitHub |
| Docker | 29.0.1 | Docker Desktop with WSL integration |
| kubectl | 1.37.1 | Kubernetes CLI |
| Helm | 3.22.0 | Kubernetes package manager |
| minikube | 1.39.0 | Local practice cluster |
| AWS CLI | 2.38.1 | IAM user `sairam-cli`, region `us-east-1` |
| Terraform | 1.16.6 | Infrastructure as code |
| VS Code | Windows + WSL extension | Opens Ubuntu files directly |

Check everything anytime:
```bash
./verify-setup.sh
```

### Daily workflow
```bash
cd ~/ai-infra-learning
activate-ai          # enter the Python environment
code .               # open VS Code (terminal: Ctrl + `)
# ... build ...
git add . && git commit -m "message" && git push
```

### Local Kubernetes
```bash
minikube start --driver=docker --memory=4096   # wait for "Done!"
kubectl get nodes                              # minikube   Ready
minikube stop                                  # free RAM when done
```

---

## 6. Lessons learned the hard way

**Security**
- **AWS secret keys go into the terminal only.** Never into chat, screenshots, GitHub, or videos. A leaked key can run up thousands of dollars within hours.
- If a key leaks: IAM → Users → Security credentials → **Deactivate → Delete**, then create a new one.
- Run `clear` after `aws configure` before copying any terminal output.
- `chmod 600 ~/.aws/credentials` keeps the key file private.
- `.gitignore` blocks `.env`, `.aws/`, `*.tfstate`, and model files from ever being committed.
- Use an IAM user, never the root account's keys.

**Setup gotchas**
- At `aws configure` prompts, type real values (`us-east-1`, `json`), not "yes."
- Don't press Ctrl+C during `minikube start`. The first run takes 3–5 minutes. If interrupted: `minikube delete`, then start again.
- Paste slow or interactive commands **one at a time**.
- `< >` in instructions means "replace this." Type the value without the brackets.
- Keep projects in Ubuntu's home (`~/`), not `/mnt/c/`. The Windows side is slow from WSL.
- Docker in WSL: enable **Settings → Resources → WSL Integration → Ubuntu** in Docker Desktop, and don't install a second Docker inside Ubuntu.
- GPU quotas are **per region**. Pick one region and use it everywhere.

---

## 7. Next steps

1. **Lesson 03:** ML Infrastructure Basics
2. **Request the AWS GPU quota:** Service Quotas → EC2 → *Running On-Demand G and VT instances* → 8 vCPUs in **us-east-1**
3. **Phase 1 of the platform:** `terraform apply` the EKS + GPU node pool, then confirm Kubernetes sees the GPU
4. **Cost rule:** GPU cluster ≈ $0.80/hour. Run `terraform destroy` at the end of every session.

---

## 8. Repo structure

```
ai-infra-learning/
├── modules/01-foundations/   # notes + code per module
├── projects/                 # the LLM platform build
├── exercises/                # practice exercises
├── notes/                    # errors and fixes, interview stories
├── verify-setup.sh           # environment check
└── README.md                 # this file
```