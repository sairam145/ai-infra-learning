# Lesson 07: Docker Basics for ML Infrastructure

> **In one sentence:** Docker packs an app and everything it needs into a **container** that runs the same on my laptop, a server, or Kubernetes, and every AI model in production runs this way.

---

## The problem Docker solves
"It works on my machine." Different Python versions, missing libraries, different CUDA versions. ML makes this worse: PyTorch, CUDA, drivers, and model files all have to match. Docker freezes the whole setup into one package.

## The analogy: a meal-kit box

| Docker word | Meaning |
|---|---|
| **Dockerfile** | The recipe card: instructions to pack the box |
| **Image** | The sealed, packed box on the shelf |
| **Container** | The box opened and the meal cooking (an image *running*) |
| **Layer** | Each recipe step adds one layer; unchanged layers are reused (cache) |
| **Registry** | The warehouse boxes ship from: Docker Hub, **AWS ECR** |
| **Volume** | A storage locker outside the box that survives when the box is thrown away |

### Containers vs. virtual machines
| | Virtual machine | Container |
|---|---|---|
| Contains | A whole operating system | Just the app + its libraries (shares the host's kernel) |
| Size | GBs | MBs to GBs |
| Starts in | Minutes | Seconds |
| Analogy | A whole house | An apartment in a shared building |

---

## A good ML Dockerfile, explained

```dockerfile
# ---- Stage 1: build (has compilers and tools) ----
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .                          # shopping list FIRST (caching)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: runtime (small, clean) ----
FROM python:3.12-slim
WORKDIR /app
RUN useradd -m appuser                           # a normal user, not admin (-m creates a home folder)
COPY --from=builder /install /usr/local          # copy only the installed packages
COPY --chown=appuser:appuser src/ ./src/         # code LAST: changes most often
ENV PYTHONUNBUFFERED=1                           # print logs immediately
USER appuser                                     # run as the normal user
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Best practices, and why

| ✅ Do | ❌ Don't | Why |
|---|---|---|
| Copy requirements before code | `COPY . .` first | Code changes then skip the slow install (cached) |
| Multi-stage builds | Ship build tools in the final image | Smaller, safer image |
| Pin versions (`python:3.12-slim`, `torch==X`) | Use `latest` | Same build every time |
| Run as a non-root user | Run as root | Limits damage if hacked |
| Clean up in the **same** `RUN` line | Clean up in a later line | Deleting in a later layer doesn't shrink the image |
| Use `.dockerignore` (venv, .git, models) | Send everything to the build | Faster builds, no secrets or junk inside |
| **CPU-only PyTorch** when there's no GPU | Default PyTorch (includes GBs of CUDA libs) | **The biggest size win for ML images** |

---

## Key commands

### Images
| Command | What it does |
|---|---|
| `docker build -t ml-app:v1 .` | Build an image from the Dockerfile here |
| `docker build -f Dockerfile.gpu -t ml-app:gpu .` | Use a different Dockerfile |
| `docker build --no-cache -t ml-app:v1 .` | Rebuild from scratch |
| `docker images` | List images and sizes |
| `docker history ml-app:v1` | Size of each layer: *what made it big?* |
| `docker tag ml-app:v1 <repo>:v1` | Give an image another name (needed before pushing) |
| `docker push <repo>:v1` / `docker pull <repo>:v1` | Upload / download from a registry |
| `docker rmi ml-app:v1` | Delete an image |

### Containers
| Command | What it does |
|---|---|
| `docker run --rm -p 8000:8000 ml-app:v1` | Run; laptop port 8000 → container port 8000; delete when stopped |
| `docker run -d --name api ml-app:v1` | Run in the background with a name |
| `docker run -e LOG_LEVEL=debug ...` | Pass an environment variable |
| `docker run -v $(pwd)/models:/app/models:ro ...` | Mount a host folder read-only (big model files stay outside the image) |
| `docker run --memory=4g --cpus=2 ...` | Limit resources |
| `docker run --restart unless-stopped ...` | Restart automatically if it crashes |
| `docker ps` / `docker ps -a` | Running / all containers |
| `docker logs -f api` | Follow output live |
| `docker exec -it api bash` | Shell inside a running container |
| `docker inspect api` | Every detail (IP, mounts, env) |
| `docker stats` | Live CPU / memory per container |
| `docker stop api` / `docker rm api` | Stop / remove |

### Compose (several containers together)
| Command | What it does |
|---|---|
| `docker compose up -d` | Start everything in `docker-compose.yml` |
| `docker compose up -d --build` | Rebuild, then start |
| `docker compose logs -f ml-api` | Follow one service |
| `docker compose ps` | What's running |
| `docker compose down` | Stop and remove it all |

Containers on the same Compose network reach each other **by service name**, e.g., `redis:6379`.

### Clean-up
| Command | What it does |
|---|---|
| `docker system df` | How much disk Docker is using |
| `docker system prune` | Remove stopped containers, unused networks, dangling images |
| `docker volume prune` | Remove unused volumes (deletes their data) |

---

## Docker with GPUs

| Step | Command / detail |
|---|---|
| Host needs | NVIDIA driver + **NVIDIA Container Toolkit** |
| Test GPU access | `docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi` |
| One specific GPU | `docker run --gpus '"device=0"' ...` |
| GPU base images | `nvidia/cuda:<version>-runtime-ubuntu22.04` (or `-devel` if compiling) |
| LLM serving image | `vllm/vllm-openai` (`docker run --gpus all -p 8000:8000 vllm/vllm-openai --model <model>`) |

On Kubernetes, the NVIDIA GPU Operator installs the toolkit for you, and pods request `nvidia.com/gpu: 1`.

---

## Pushing to AWS ECR

```bash
aws ecr create-repository --repository-name ml-app
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag ml-app:v1 <account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-app:v1
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-app:v1
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `permission denied ... docker.sock` | User not in the docker group (Linux) | `sudo usermod -aG docker $USER`, log out and in |
| Container exits immediately | App crashed on start | `docker logs <container>` |
| `port is already allocated` | Something else uses the port | Stop it, or use `-p 8001:8000` |
| `no space left on device` | Old images and containers | `docker system prune` |
| Huge image | Default PyTorch with CUDA, no multi-stage, no `.dockerignore` | CPU-only PyTorch, multi-stage, `.dockerignore` |
| Slow rebuilds | Code copied before requirements | Copy requirements first |
| Healthcheck always failing | `curl`/`requests` not in a slim image | Use Python's built-in `urllib` |

---

## Why it matters for AI/GPU DevOps
GPU images are often **10–20 GB**. Image size decides how fast new pods start, which decides how fast the platform can scale when traffic spikes. vLLM, the GPU Operator, DCGM exporter, and every model server I'll run are containers.

---

## Self-check
1. Image vs. container?
2. Why copy `requirements.txt` before the code?
3. Two reasons for multi-stage builds?
4. What's the single biggest size win for an ML image without a GPU?
5. What does `--gpus all` need on the host?

<details>
<summary>Answers</summary>

1. Image = the packed box (template). Container = a running copy of it.
2. So code changes reuse the cached dependency layer and rebuilds take seconds.
3. Smaller images (no build tools) and a smaller attack surface.
4. Installing CPU-only PyTorch instead of the default CUDA build.
5. An NVIDIA driver plus the NVIDIA Container Toolkit.

</details>

---

*Part of my [AI Infrastructure learning log](../../../README.md). Course: [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
