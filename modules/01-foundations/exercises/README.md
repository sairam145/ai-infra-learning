# Module 1 Exercises: Explained in Plain Words

> **What this page is:** a plain-language guide to every Module 1 exercise: what each one teaches, why it matters for an AI/GPU DevOps job, and the key commands with what they actually do.
>
> **How I'm using it:** instead of doing each exercise separately, I build all of these skills inside my main project (an LLM platform on AWS). This page is the reference for *what* each skill is and *why* it matters.

---

## The big picture

The 10 exercises build one thing, step by step: **a machine learning model that runs reliably in production.**

```
Ex 01  Set up my laptop
Ex 02  Pack the model app in a box          (Docker)
Ex 03  Run many boxes, self-healing         (Kubernetes)
Ex 07  Set up my own space in the cloud     (AWS: VPC, S3, IAM)
Ex 08  Make the app production-tough        (health, limits, metrics, logs)
Ex 09  Prove it works automatically         (tests + CI)
Ex 10  Put it all together, one command     (make up / make down)
```

| # | Exercise | Status | Why |
|---|---|---|---|
| 01 | Environment | ✅ Done | Completed in Lesson 2 |
| 02 | Docker | ⭐ Core | Every AI model in production runs in a container |
| 03 | Kubernetes | ⭐ Core | Where containers (and GPUs) are scheduled and scaled |
| 04 | Python env manager | ⏭️ Skipped | Building a Python CLI tool: app development, not infra |
| 05 | Framework benchmark | ◐ Partly done | PyTorch part done in Lesson 4; TensorFlow/JAX not needed |
| 06 | FastAPI template generator | ⏭️ Skipped | A code generator: app development, not infra |
| 07 | Cloud onboarding | ⭐ Core | AWS VPC, S3, IAM: the base of every cloud platform |
| 08 | Production model serving | ⭐ Core | The difference between a demo and a real service |
| 09 | API tests | ◐ Light | Know the four test types; CI that runs them |
| 10 | End-to-end mini project | ⭐ Capstone | Everything together, one command up, one command down |

---

## Exercise 02: Docker

### In one sentence
Pack the app and everything it needs into a **box (container)** so it runs the same everywhere.

### The analogy: a meal-kit box

| Docker word | Meal-kit meaning |
|---|---|
| **Dockerfile** | The recipe card: instructions to pack the box |
| **Image** | The sealed, packed box on the shelf |
| **Container** | The box opened and the meal cooking (the image *running*) |
| **Layer** | Each recipe step adds one layer to the box |
| **Registry** (Docker Hub, AWS ECR) | The warehouse where boxes are stored and shipped from |

### What the exercise covers

**Part 1: First container.** A FastAPI app that loads a model, packed with a basic Dockerfile:
```dockerfile
FROM python:3.12-slim          # start from a small Linux + Python box
WORKDIR /app                   # work inside /app
COPY requirements.txt .        # copy the shopping list first...
RUN pip install -r requirements.txt   # ...and install it (slow step)
COPY src/ ./src/               # then copy the code (fast step)
EXPOSE 8000                    # the app listens on port 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]   # how to start it
```

**Part 2: Make the box smaller and safer.**
- **CPU-only PyTorch:** the default PyTorch download includes several GB of NVIDIA GPU libraries. On a machine without a GPU that's dead weight. Installing from `https://download.pytorch.org/whl/cpu` cuts the image dramatically. *This is the single biggest size win.*
- **Multi-stage build:** use one box with all the tools to *build*, then copy only the finished result into a clean, small box to *ship*. Like cooking in a full kitchen but delivering just the plate.
- **Non-root user:** the app runs as a normal user, not the admin. If someone breaks in, they can do less damage.
- **`--no-cache-dir`:** tells pip not to keep download leftovers inside the image.
- **Layer caching:** Docker reuses unchanged steps. That's why requirements are copied *before* code: change the code and the rebuild takes seconds; change requirements and it reinstalls everything.

**Part 3: Docker Compose.** Run several containers together with one file: the API + Prometheus (collects metrics) + Grafana (dashboards). Like a stage manager that starts the whole band at once.

**Part 4: Volumes.** Keep big or changing things *outside* the box: model files (mounted read-only) and logs (survive restarts). Models can be gigabytes, so you don't rebuild the image every time the model changes.

**Part 5: Networks.** Containers on the same Compose network find each other **by name**. The API connects to `redis:6379`, not an IP address. The exercise adds a Redis cache: first request slow, repeat request fast.

**Part 6: GPU image (optional).** Build the same app on an NVIDIA CUDA base image so it can use a GPU. This is the bridge to vLLM.

### Key commands

| Command | What it does |
|---|---|
| `docker build -t ml-app:v1 .` | Pack an image from the Dockerfile in this folder, named `ml-app`, tag `v1` |
| `docker build -f Dockerfile.optimized -t ml-app:v2 .` | Same, but use a different Dockerfile |
| `docker images` | List images on this machine and their sizes |
| `docker history ml-app:v1` | Show each layer and its size: *which step made it big?* |
| `docker run --rm -p 8000:8000 ml-app:v1` | Start a container; connect laptop port 8000 → container port 8000; delete it when stopped |
| `docker run -d --name api ...` | Same, but in the background with a name |
| `docker ps` / `docker ps -a` | Running containers / all containers including stopped |
| `docker logs -f api` | Follow a container's output live |
| `docker exec -it api bash` | Open a shell *inside* a running container |
| `docker stop api` / `docker rm api` | Stop / remove a container |
| `docker compose up -d` | Start every service in `docker-compose.yml` in the background |
| `docker compose up -d --build` | Rebuild images first, then start |
| `docker compose logs -f ml-api` | Follow one service's logs |
| `docker compose down` | Stop and remove everything Compose started |
| `docker system df` / `docker system prune` | See / reclaim disk space Docker is using |

### Problems in the course's code (and the fixes)

| Course code | Problem | Fix |
|---|---|---|
| `torch==2.1.0` | Doesn't exist for Python 3.12 | Use a current version, or install CPU-only from the PyTorch index |
| `resnet18(pretrained=True)` | Old syntax | `resnet18(weights=ResNet18_Weights.DEFAULT)` |
| `@app.on_event("startup")` | Deprecated in FastAPI | Use a `lifespan` function |
| Healthcheck uses `requests` / `curl` | Neither is installed in a slim image, so the check always fails | Use `python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"` |
| Non-root user with no home folder | The model download needs a writable folder, so startup fails | `useradd -m`, or set `TORCH_HOME=/tmp` |
| `torch.save(model)` → `torch.load(path)` | Fails by default since PyTorch 2.6 (safety change) | Save and load `state_dict` instead |
| `docker-compose` + `version: '3.8'` | Old Compose v1 style | `docker compose` (with a space); drop the `version` line |
| `docker compose exec ml-api ping redis` | `ping` isn't installed in slim images | Test with Python, or `getent hosts redis` |

### Why it matters for AI/GPU DevOps
GPU images are often **10–20 GB**. Smaller images mean faster deploys, faster autoscaling when traffic spikes, and lower storage bills. vLLM itself ships as a Docker image (`vllm/vllm-openai`).

---

## Exercise 03: Kubernetes

### In one sentence
Kubernetes runs your containers across many machines, **keeps the right number alive, restarts them when they crash, and scales them with traffic.**

### The analogy: a restaurant manager
You tell the manager "I want 3 cooks on shift at all times." If one goes home sick, the manager brings in a replacement automatically. When the dinner rush hits, the manager calls in more cooks. You describe *what you want*; the manager makes it happen.

### The building blocks

| Kubernetes object | Plain meaning |
|---|---|
| **Pod** | One running copy of your container (one cook) |
| **Deployment** | "Keep N pods of this image running" (the shift plan) |
| **Service** | One stable address that spreads traffic across the pods (the front counter) |
| **ConfigMap** | Settings stored outside the image (the notice board) |
| **Secret** | Same, but for passwords and keys |
| **Liveness probe** | "Are you alive?" No → restart the pod |
| **Readiness probe** | "Are you ready for customers?" No → don't send it traffic yet. *Critical for models that take a while to load.* |
| **HPA** (Horizontal Pod Autoscaler) | Add or remove pods based on CPU/memory load |
| **Rolling update** | Replace old pods with new ones gradually, so there's no downtime |
| **Rollback** | Go back to the previous version |

### What the exercise covers
1. **Deploy** the Docker image as a Deployment, view pods and logs.
2. **Expose** it with a Service, reach it with port-forward.
3. **Configure** it with a ConfigMap; change settings without rebuilding the image.
4. **Health probes:** liveness and readiness.
5. **Autoscale:** install metrics-server, create an HPA, generate load, watch pods multiply.
6. **Roll out v3, then roll back.**
7. **Debug:** logs, describe, exec into pods, events, resource usage.

### Key commands

| Command | What it does |
|---|---|
| `minikube start` / `kind create cluster` | Start a local practice cluster |
| `minikube image load ml-app:v2` / `kind load docker-image ml-app:v2` | Copy a local image into the cluster (it can't see your laptop's images otherwise) |
| `kubectl apply -f deployment.yaml` | Create or update whatever the file describes |
| `kubectl get pods` / `get deploy` / `get svc` | List pods / deployments / services |
| `kubectl get pods -w` | Watch pods change live |
| `kubectl describe pod <name>` | Full details + **Events**: the first place to look when something's wrong |
| `kubectl logs <pod>` / `logs -f <pod>` | Show / follow a pod's output |
| `kubectl logs <pod> --previous` | Logs from the *crashed* copy, essential for crash loops |
| `kubectl logs -l app=ml-api` | Logs from all pods with that label |
| `kubectl exec -it <pod> -- bash` | Open a shell inside a pod |
| `kubectl port-forward svc/ml-api-service 8000:80` | Reach the service from your laptop at `localhost:8000` |
| `kubectl rollout restart deploy/ml-api` | Restart all pods (e.g., to pick up new ConfigMap values) |
| `kubectl set image deploy/ml-api ml-api=ml-app:v3` | Roll out a new image version |
| `kubectl rollout status deploy/ml-api` | Watch the rollout finish |
| `kubectl rollout history deploy/ml-api` | List past versions |
| `kubectl rollout undo deploy/ml-api` | **Roll back** to the previous version |
| `kubectl top nodes` / `top pods` | CPU and memory usage (needs metrics-server) |
| `kubectl get hpa -w` | Watch the autoscaler decide |
| `kubectl get events --sort-by=.lastTimestamp` | Recent cluster events, newest last |

### The most common pod problems

| Status | Plain meaning | First thing to check |
|---|---|---|
| `Pending` | No machine can fit it (not enough CPU/memory/GPU, or a taint blocks it) | `kubectl describe pod` → Events |
| `ImagePullBackOff` | Can't download the image (wrong name, private registry, not loaded into kind) | Image name/tag, `kind load docker-image` |
| `CrashLoopBackOff` | It starts, crashes, restarts, repeat | `kubectl logs <pod> --previous` |
| `OOMKilled` | Used more memory than its limit | Raise the memory limit or shrink the model |
| Running but `0/1 READY` | Readiness probe failing; model probably still loading | Probe settings, `initialDelaySeconds` |

### Why it matters for AI/GPU DevOps
This is where GPUs live. In the main project, vLLM pods run on GPU nodes with **taints/tolerations**, request `nvidia.com/gpu: 1`, use **readiness probes** (big models take minutes to load), and scale with Karpenter and KEDA.

---

## Exercise 07: Cloud onboarding

### In one sentence
Write a tool that gives a new engineer their own **safe, isolated corner of AWS** in minutes, and can remove it cleanly.

### The analogy: a new-hire welcome kit
A new employee gets a desk, a locker, and a key card that opens only their own locker and the shared library. When they leave, all of it is taken back. The tool automates the kit.

### What gets created

| AWS thing | Plain meaning | In the kit |
|---|---|---|
| **VPC + subnets** | Your private network in AWS; public subnet faces the internet, private doesn't | Their desk area |
| **S3 bucket** (versioned, encrypted, tagged `Owner=alice`) | File storage for models and data | Their locker |
| **IAM user + policy** | An identity with permissions *only* for their bucket + read-only on the shared team bucket | Their key card |
| **Access key → `.env` file** (permissions 0600) | Credentials stored where only they can read them | The key card itself |

The tool has four commands: `init` (create), `status` (what exists), `rotate-key` (new key, old one disabled), and `destroy` (remove everything; safe to run twice).

### Key ideas
- **Least privilege:** give only the permissions needed, nothing more. My `AdministratorAccess` IAM user is fine for learning; never for a team.
- **Idempotent:** running it twice doesn't create duplicates or break things. A state file tracks what already exists.
- **Clean teardown:** forgotten resources are how cloud bills explode.
- **Testing without real AWS:** the `moto` library fakes AWS so tests run for free in CI.

### Key commands (AWS CLI equivalents of what the tool does)

| Command | What it does |
|---|---|
| `aws sts get-caller-identity` | "Who am I logged in as?" |
| `aws ec2 create-vpc --cidr-block 10.0.0.0/24` | Create a private network |
| `aws s3 mb s3://ml-sandbox-alice-2026` | Make a bucket |
| `aws s3api put-bucket-versioning ...` | Keep old versions of every file |
| `aws iam create-user --user-name alice` | Create an identity |
| `aws iam put-user-policy ...` | Attach permissions to it |
| `aws iam create-access-key --user-name alice` | Generate CLI credentials |
| `aws iam update-access-key --status Inactive ...` | Disable an old key (rotation) |
| `chmod 600 file.env` | Only the owner can read the file |

**In my project I do this with Terraform**, which handles state, idempotency, and teardown (`terraform apply` / `terraform destroy`) for me.

---

## Exercise 08: Production model serving

### In one sentence
Turn a "it returns predictions" demo into a service the ops team can run **unattended at 2am**.

### The analogy: food truck → restaurant
A food truck can serve lunch. A restaurant also needs a host who seats people only when tables are ready, a fire exit, health inspections, a cap on how many people are inside, and a log of every order. Same food, very different operation.

### What gets added, and why

| Feature | Plain meaning | Why ops cares |
|---|---|---|
| `/v1/predict` and `/v1/predict/batch` (≤128 rows) | One answer, or many at once | Batching is much cheaper per prediction |
| `/v1/models` | Which model and version is live? | Debugging and audits |
| `/v1/admin/reload` + `X-Admin-Token` | Swap the model without restarting; only admins can | Updates without downtime |
| **`/health` (liveness)** | "Is the process alive?" | Kubernetes restarts it if not |
| **`/ready` (readiness)**, 503 until loaded | "Is the model loaded?" | No traffic until it can actually answer |
| **Prometheus `/metrics`** | Request count, latency, in-flight requests, predictions per class, model version | Dashboards and alerts |
| **Structured JSON logs + `request_id`** | Every log line is searchable and tagged with which request caused it | Trace one user's problem through the logs |
| **Graceful shutdown** (25s drain) | On shutdown, finish current requests, refuse new ones | Rolling updates don't drop users mid-request |
| **Validation → 422** | Bad input gets a clear error saying which field is wrong | Callers can fix their own mistakes |
| **Body size limit → 413** | Reject requests over 1 MB | Stops memory-blowing requests |
| **Rate limit → 429 + `Retry-After`** | Max 60 requests/min per IP | One client can't starve everyone else |
| **Non-root, read-only filesystem** | App can't modify its own container | Limits damage if hacked |
| **Image < 400 MB** | Small box | Fast deploys and scaling |

### HTTP status codes to know

| Code | Meaning |
|---|---|
| 200 | OK |
| 400 | Bad request (e.g., batch over 128) |
| 401 / 403 | Not logged in / not allowed (bad admin token) |
| 413 | Request too big |
| 422 | Input failed validation |
| 429 | Too many requests, slow down |
| 500 | Server bug |
| 503 | Not ready (model still loading) |

### Key commands

| Command | What it does |
|---|---|
| `uvicorn app:app --timeout-graceful-shutdown 25` | Start with a 25-second drain on shutdown |
| `curl -i localhost:8000/ready` | Check readiness (`-i` shows the status code) |
| `curl -X POST localhost:8000/v1/predict -H "Content-Type: application/json" -d '{"features":[1,2,3,4]}'` | Send a prediction |
| `curl -H "X-Request-Id: test-123" ...` | Send your own request ID, then find it in the logs |
| `docker run --read-only --tmpfs /tmp ...` | Run with a read-only filesystem (writes only to `/tmp`) |
| `docker stop api` | Sends SIGTERM, which triggers graceful shutdown |

### Why it matters for AI/GPU DevOps
vLLM already gives you most of this (`/health`, `/metrics`, an OpenAI-compatible API). My job on the platform is the rest: the **gateway** in front (keys, rate limits, size limits), readiness tuned for big models, graceful rollouts, and dashboards.

---

## Exercise 09: API tests

### In one sentence
Write automatic checks so that **a broken change gets caught before users see it.**

### The four kinds of test

| Type | What it checks | Speed | Analogy |
|---|---|---|---|
| **Unit** | One small function on its own (e.g., "rejects 2 features when 4 are required") | Milliseconds | Testing one ingredient |
| **Contract** (in-process) | Every request/response shape of the API, with a fake model | Fast | Tasting each dish in the kitchen |
| **Integration** (real container) | The real Docker image, real HTTP, real metrics | Slow | A full dinner service with real customers |
| **Consumer-driven contract** (Pact) | The API still gives what the apps *using* it expect | Medium | Asking regular customers if the dish still tastes the same |

Each catches different bugs. For example, only integration tests catch a broken Dockerfile or a missing port.

### Key commands

| Command | What it does |
|---|---|
| `pytest` | Run all tests |
| `pytest -m unit` | Run only tests tagged "unit" |
| `pytest -m "not integration"` | Skip the slow ones |
| `pytest -x` | Stop at the first failure |
| `pytest -k predict` | Run only tests with "predict" in the name |
| GitHub Actions workflow | Runs the tests on every push/PR; a red X blocks the merge |

### Why it matters for AI/GPU DevOps
In CI/CD pipelines, tests are the **quality gate**, the same idea as the accuracy gate in my Lesson 3 lab. `make image` should depend on `make test`: never ship untested code.

---

## Exercise 10: End-to-end mini platform (capstone)

### In one sentence
Everything from the previous exercises, **started with one command (`make up`) and removed with one command (`make down`).**

### The analogy: a theater show
Each earlier exercise rehearsed one part: lights, sound, actors, ticketing. This is opening night. One cue starts the show; one cue clears the stage.

### What `make up` builds, in order
1. A local Kubernetes cluster (kind)
2. NGINX Ingress: the front door into the cluster
3. kube-prometheus-stack: Prometheus + Grafana + alerting, installed with Helm
4. The model API: 2 replicas + HPA + ServiceMonitor (tells Prometheus to scrape it)
5. Port-forwards: app on `:8080`, Grafana on `:3000`, Prometheus on `:9090`
6. A summary of all URLs

**Target: under 5 minutes.** Then `make load` runs a load test (Locust), and you watch the HPA scale from 2 to 4+ pods in Grafana.

### Key commands

| Command | What it does |
|---|---|
| `make help` | List all available targets |
| `make up` / `make down` | Build everything / remove everything |
| `make test` → `make image` | Image build only runs if tests pass |
| `git rev-parse --short HEAD` | Current commit ID, used as the image tag so every build is unique and traceable |
| `kind create cluster --config kind-config.yaml` | Cluster with port mappings |
| `helm install monitoring prometheus-community/kube-prometheus-stack` | Install the monitoring stack |
| `kubectl wait --for=condition=ready pod -l ... --timeout=2m` | Pause until pods are ready (scripts need this) |
| `locust -f locustfile.py` | Generate load and report throughput and latency percentiles |
| `set -euo pipefail` | In shell scripts: stop on the first error instead of carrying on broken |

### Required extras
- **README** with the demo flow and real screenshots
- **CI** running `make test` on every PR
- **RUNBOOK.md**: how to fix common failures (cluster won't start, image pull fails, HPA not scaling)
- **Clean teardown:** `docker ps -a`, `kubectl get all`, and the AWS account all empty after `make down`

### Why it matters for AI/GPU DevOps
This is the exact shape of my main project, with kind replaced by **EKS on AWS** and the sklearn model replaced by **vLLM on GPUs**. Being able to bring the whole platform up and down with one command, with tests, monitoring, and a runbook, is what senior platform engineers are hired for.

---

## The skipped and partial exercises

| Exercise | What it was | Why skipped |
|---|---|---|
| **04 Python env manager** | Build a CLI that manages Python versions and virtual environments | Python tool-building. I use `venv` and pre-built tools instead. |
| **05 Framework benchmark** | Compare PyTorch vs TensorFlow vs JAX, CPU vs GPU | Done the PyTorch part in Lesson 4 (warm-up, batching, quantization). The GPU comparison happens in the main project with vLLM. |
| **06 FastAPI template generator** | A tool that generates FastAPI project code | App development. Ex 08 covers what a production API needs. |
| **09 (advanced parts)** | Pact consumer-driven contracts | Good to know the idea; low priority for infra roles |

---

## Where each skill shows up in my main project

| Skill (exercise) | In the LLM platform on AWS |
|---|---|
| Docker (02) | vLLM container images, GPU base images, image size and caching |
| Kubernetes (03) | vLLM Deployment on GPU nodes, probes, rollouts, rollback |
| Cloud setup (07) | Terraform: VPC, EKS, S3 for model weights, IAM roles |
| Production serving (08) | API gateway: keys, rate limits, size limits; readiness for big models |
| Tests + CI (09) | GitHub Actions: lint, test, Trivy image scan, then deploy |
| One-command platform (10) | `terraform apply` + ArgoCD + Helm; `terraform destroy` to tear down |
| Monitoring (02, 08, 10) | Prometheus + Grafana + DCGM GPU metrics + vLLM metrics |
| Autoscaling (03, 10) | Karpenter for GPU nodes + KEDA on waiting requests |

---

*Part of my [AI Infrastructure learning log](../../../README.md). Exercises from the [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
