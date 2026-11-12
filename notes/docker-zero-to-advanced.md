# Docker — Zero to Advanced

**DOCKER**

**Zero to Advanced**

*Architecture to production — every concept, with examples and commands*

A deployment-focused guide. Every new term is explained the first time it appears, in plain words. Coding and hands-on steps are flagged clearly — and the focus throughout is on deploying, running, and operating containers, not on writing applications or models.

> HOW TO USE THIS GUIDE:  Read Parts 1–3 for the mental model. Part 4 is the daily work: run flags, networking, storage, Compose. Parts 5–6 are production and advanced: registries, optimisation, debugging, security, CI/CD, Buildx. Keep the cheat sheet in Part 7 (Section 25) open while you practise.

Who this is for: anyone starting Docker from zero who wants to reach production-level deployment skill — especially DevOps, Platform, SRE, and Cloud engineers moving into ML infrastructure, where Docker is the packaging layer under Kubernetes and model serving.

| **Part** | **What you will be able to do** |
| --- | --- |
| **1. Foundations** | Explain Docker, containers vs VMs, and the architecture |
| **2. Images & containers** | Pull, run, inspect, stop, and clean up with confidence |
| **3. Dockerfile & builds** | Write efficient Dockerfiles and build fast, small images |
| **4. Running systems** | Wire ports, env, networking, volumes, and Compose stacks |
| **5. Production** | Push to registries, secure, debug, limit, and ship via CI/CD |
| **6. Advanced & reference** | Multi-stage, Buildx, multi-arch, cheat sheet, practice roadmap |

# Part 1 — Foundations: what Docker is and how it works

## 1. The problem Docker solves

An application never runs alone. It needs a language runtime (the program that runs its code, such as Python or Node), libraries (ready-made code it borrows), config files, and the right versions of all of them. On a developer laptop those versions are one thing; on a server they are often another. The result is the oldest bug in software: 'it works on my machine.'

Docker fixes this by packaging the application together with its runtime, libraries, and config into one sealed unit called an image, and running that unit as a container. The same image runs identically on a laptop, a test server, and production — because everything it needs travels inside the package.

**The lunchbox idea (from your earlier lessons): **Docker is a lunchbox. It packs the dish with everything it needs, so it tastes the same in any kitchen. The recipe for packing the lunchbox is the Dockerfile. The packed lunchbox is the image. The lunchbox opened and being eaten from is the container.

- **Build once: **Write the recipe once (Dockerfile).

- **Ship the image: **Turn it into a sealed package (image) that never changes.

- **Run anywhere: **Open as many copies as you need, anywhere (containers).

## 2. Containers vs virtual machines

A virtual machine (VM) is a whole fake computer inside a real computer. It carries its own full operating system — its own kernel (the core of an operating system that talks to hardware). A container is lighter: it is an isolated process that shares the host machine's kernel, but has its own view of files, network, and processes.

|  | **Virtual machine** | **Container** |
| --- | --- | --- |
| **What is inside** | App + libraries + full guest OS | App + libraries only |
| **Size** | Gigabytes (GB) | Megabytes (MB) typically |
| **Start time** | Minutes | Seconds or less |
| **Isolation** | Very strong (separate OS) | Strong (namespaces + cgroups) |
| **Performance** | Extra layer = some overhead | Near-native |
| **Best for** | Different OS, strongest isolation | Same OS, many copies, fast scaling |

Plain version: a VM is renting a whole separate house. A container is renting a locked room in a large house — much faster to move into, much cheaper, and you can fit many more rooms, while the house's plumbing (the kernel) is shared.

## 3. Key words — explained once, used everywhere

| **Term** | **Plain meaning** |
| --- | --- |
| **Image** | Read-only template — the packed lunchbox. Never changes once built. |
| **Container** | A running (or stopped) instance of an image — the opened lunchbox. |
| **Dockerfile** | Text recipe that describes how to build an image, step by step. |
| **Registry** | A warehouse / app store for images. Docker Hub is the public one. |
| **Repository** | A named collection of image versions, e.g. nginx, python, myapp. |
| **Tag** | A label for a version, e.g. :1.27, :3.12-slim, :latest. |
| **Volume** | Storage that lives outside a container, so data survives deletion. |
| **Network** | How containers talk to each other and to the outside world. |
| **Compose** | A tool that runs a whole multi-container app from one YAML file. |
| **Orchestrator** | A manager for many containers across machines — Kubernetes, Swarm. |

## 4. Docker architecture — who does what

Docker uses a client–server design. You type commands into the client; a background service called the daemon does the actual work; a registry stores images.

- **Docker client (docker): **The command-line tool you type into. It never builds or runs anything itself — it asks the daemon.

- **Docker daemon (dockerd): **The background engine service that builds images, creates containers, manages networks and volumes, and talks to registries. If the daemon is not running, every docker command fails.

- **Docker Engine / Desktop: **Docker Desktop bundles client + daemon + a small Linux VM. On Windows and Mac, containers are Linux containers, so Desktop runs a lightweight Linux VM underneath — this is normal and invisible in daily use.

- **Registry: **Where images are pushed (uploaded) and pulled (downloaded). Public: Docker Hub. Cloud: Amazon ECR, Google Artifact Registry, Azure ACR. Private/self-hosted: Harbor, Nexus.

**Architecture in one picture**

```
You  ->  docker CLI  ->  Docker daemon  ->  images / containers / volumes / networks
                              |
                              +-->  Registry (Docker Hub / ECR / ACR)  [push / pull]
```

### Under the hood: namespaces and cgroups

Docker is not magic. It uses two Linux kernel features:

- **Namespaces — isolation of what you can see: **Give a container its private view: its own process list, network, filesystem mount points, hostname, and user IDs. The container thinks it is alone on the machine.

- **cgroups — limits on what you can use: **Short for control groups. They limit and measure how much CPU, memory, and I/O a container may use, so one container cannot eat the whole machine.

There is also the layered filesystem (OverlayFS): image layers are stacked read-only, and each container adds one thin writable layer on top. That is why containers start instantly and share disk space for common layers.

## 5. Install Docker and verify it properly

> DEPLOYMENT PRACTICE — flagged:  Installation and verification below are hands-on deployment steps for your laptop. Nothing here is model-writing or app development.

**Check what you already have**

```
docker --version
docker compose version
docker info
```

**Verify the daemon can actually run a container**

```
docker run hello-world
```

That tiny image downloads, starts, prints a confirmation, and exits. It proves three things at once: the client works, the daemon works, and you can reach a registry. On Linux, add your user to the docker group to avoid typing sudo for every command, then log out and back in:

**Linux — run Docker without sudo (then log out/in)**

```
sudo usermod -aG docker $USER
docker ps
```

> NOTE:  Membership in the docker group is effectively root-level access to the host. On shared or production machines, treat it that way.

# Part 2 — Images and containers: the daily core

## 6. Images — layers, tags, and digests

Every Dockerfile instruction creates a layer — a saved snapshot of what changed in that step. Layers are cached and shared: ten images built on python:3.12-slim store that base only once on disk.

- **Tag: **A human-readable label such as latest, 1.27, or 3.12-slim. Tags can be moved to a different image — latest is just a label, not a guarantee of newest or best.

- **Digest: **A fingerprint of the exact image content, written as sha256:... If the digest matches, the bits are identical. Pin by digest in production for reproducibility.

- **slim / alpine: **A variant suffix meaning the image was stripped down — fewer tools, smaller size. alpine is even smaller (musl-based). Use slim/alpine for running; use full images when you need build tools.

**Image commands you will use daily**

```
docker images                      # list local images
docker pull nginx:1.27             # download an image
docker pull nginx@sha256:<digest>  # download exact image by digest
docker inspect nginx:1.27          # full details as JSON
docker history nginx:1.27          # layer-by-layer build history
docker tag myapp:1.0 myapp:latest  # add another tag
docker rmi nginx:1.27              # remove a local image
docker image prune                 # remove dangling (untagged) images
```

## 7. Containers — lifecycle and core commands

A container goes through a simple lifecycle: created → running → paused/stopped → removed. A container that has finished its job does not disappear automatically unless you ask — stopped containers still sit on disk and show in docker ps -a.

**The lifecycle in commands**

```
docker create nginx:1.27     # create but do not start
docker start <name-or-id>    # start a created/stopped container
docker run nginx:1.27        # create + start in one step
docker pause <name>          # freeze all processes
docker unpause <name>        # resume
docker stop <name>           # graceful stop (SIGTERM, then SIGKILL after timeout)
docker kill <name>           # immediate stop (SIGKILL)
docker restart <name>        # stop + start
docker rm <name>             # delete a stopped container
docker rm -f <name>          # force-delete a running container
```

**Seeing and inspecting containers**

```
docker ps                    # running containers only
docker ps -a                 # all containers, including stopped
docker logs <name>           # what the container printed
docker logs -f --tail 100 <name>   # follow last 100 lines
docker exec -it <name> sh    # open a shell inside a running container
docker inspect <name>        # full config/state as JSON
docker stats                 # live CPU / memory / network per container
docker top <name>            # processes inside the container
```

**docker run is the most important command in Docker. **Everything in Part 4 — ports, environment variables, volumes, names, limits — is a flag on docker run or its Compose equivalent.

**Your first real container**

```
# Run nginx in the background, name it web, publish port 8080 -> 80
docker run -d --name web -p 8080:80 nginx:1.27

# Test it
curl http://localhost:8080

# Look inside, then clean up
docker logs web
docker exec -it web sh
docker stop web && docker rm web
```

## 8. Cleaning up — disk fills up fast

Images, stopped containers, unused networks, and build cache accumulate silently. On a busy laptop this can reach tens of gigabytes.

**Cleanup commands — safe to destructive**

```
docker system df                 # how much disk Docker is using
docker container prune           # remove stopped containers
docker image prune               # remove dangling images
docker volume prune              # remove unused volumes (careful: data!)
docker builder prune             # clear build cache
docker system prune              # all of the above except volumes
docker system prune -a --volumes # EVERYTHING unused — destructive, read twice
```

> WARNING:  docker system prune -a --volumes deletes images you may need to re-download and volumes that may hold the only copy of data. Never run it on a machine whose volumes you have not checked.

# Part 3 — Dockerfile and building images

## 9. The Dockerfile — every instruction that matters

A Dockerfile is a plain text file named Dockerfile (no extension). Each line is an instruction. Instructions run top to bottom, and each one creates a layer — so put things that change rarely at the top and things that change often (your code) near the bottom, to reuse the cache.

| **Instruction** | **What it does — plain words** |
| --- | --- |
| **FROM** | Sets the base image to start from. Always the first line. |
| **WORKDIR** | Sets the working folder inside the image for later commands. |
| **COPY** | Copies files from your computer (build context) into the image. |
| **ADD** | Like COPY plus auto-extracts tar files and can fetch URLs. Prefer COPY. |
| **RUN** | Runs a command at build time and saves the result as a layer. |
| **CMD** | The default command when a container starts. Overridable at run time. |
| **ENTRYPOINT** | The fixed starting command; CMD becomes its arguments. |
| **ENV** | Sets environment variables baked into the image. |
| **ARG** | Build-time variable, passed with --build-arg. Not present at run time. |
| **EXPOSE** | Documents which port the app listens on. Does not publish it. |
| **USER** | Which user the container runs as. Set a non-root user. |
| **VOLUME** | Declares a mount point for persistent / anonymous volume storage. |
| **HEALTHCHECK** | Command Docker runs to decide if the container is healthy. |
| **LABEL** | Adds metadata (maintainer, version) as key=value pairs. |
| **SHELL** | Changes the shell used for RUN commands. |

**Example 1 — a complete, commented Dockerfile (Python / FastAPI serving app)**

```
# Base image: official Python, slim variant
FROM python:3.12-slim

# Work inside /app in the image
WORKDIR /app

# Copy requirements FIRST so dependency layer is cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code (changes often, so it is last)
COPY . .

# Run as a non-root user (security)
RUN useradd -m appuser
USER appuser

# Document the port and define a healthcheck
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Default start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**CMD vs ENTRYPOINT, in one breath: **CMD is the whole default command and is fully replaced if you pass arguments to docker run. ENTRYPOINT is fixed — anything you pass is added as arguments to it. Images for tools (e.g. a CLI) use ENTRYPOINT; service images usually use CMD, or ENTRYPOINT + CMD together.

**Example 2 — Node.js app**

```
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

**Example 3 — static website on nginx**

```
FROM nginx:1.27-alpine
COPY ./site /usr/share/nginx/html
EXPOSE 80
```

### Exec form vs shell form

Prefer the exec (JSON array) form — CMD ["uvicorn", "main:app"] — because the app receives stop signals directly and shuts down cleanly. The shell form — CMD uvicorn main:app — runs via /bin/sh -c, which can swallow signals and cause slow or forced shutdowns.

## 10. Building images — cache, context, and .dockerignore

**Build commands**

```
docker build -t myapp:1.0 .              # build, tag myapp:1.0, context = current folder
docker build -t myapp:1.0 -f Dockerfile.prod .   # use a different Dockerfile
docker build --no-cache -t myapp:1.0 .   # ignore cache, rebuild every layer
docker build --build-arg VERSION=1.0 -t myapp:1.0 .  # pass a build-time ARG
```

- **Build context: **Everything in the folder you point docker build at is sent to the daemon before building. A folder containing node_modules, .git, datasets, or venvs can be gigabytes — slow builds and bloated context.

- **.dockerignore: **A file that lists what NOT to send, exactly like .gitignore. Every real project needs one.

**A solid .dockerignore**

```
.git
__pycache__
*.pyc
.venv
node_modules
.env
*.md
.pytest_cache
data/
models/*.bin   # large files: mount at run time instead of baking in
```

- **Layer cache rule: **If an instruction and everything before it are unchanged, Docker reuses the cached layer instead of re-running it. That is why COPY requirements.txt + RUN pip install comes before COPY . . — code changes daily, dependencies rarely.

> DEPLOYMENT PRACTICE — flagged:  Writing a Dockerfile for a serving app, building it, and optimising its cache and size are deployment work. They are in the parked laptop practice roadmap in Section 27.

### Build arguments and secrets — do not bake secrets in

ARG values and anything copied into an image can be recovered by anyone who can pull the image. Never COPY a .env file, password, or API key into an image, and never pass real secrets as --build-arg (they show in docker history). For builds that need a secret (for example a private package index), use BuildKit secret mounts, which are available during that RUN step only and never saved in a layer:

**BuildKit secret mount (secret is never stored in the image)**

```
# syntax=docker/dockerfile:1
FROM python:3.12-slim
RUN --mount=type=secret,id=pip_index pip install -r requirements.txt
# build with: docker build --secret id=pip_index,env=PIP_INDEX_URL -t myapp:1.0 .
```

# Part 4 — Running real systems: ports, networking, storage, Compose

## 11. docker run in depth — the deployment flags

| **Flag** | **Meaning** |
| --- | --- |
| **-d** | Detached: run in background and print the container ID. |
| **-it** | Interactive + terminal: needed for shells and CLIs. |
| **--name** | Give a stable, human name instead of a random one. |
| **-p HOST:CONTAINER** | Publish a port: host port : container port. |
| **-e KEY=value** | Set an environment variable at run time. |
| **--env-file .env** | Load environment variables from a file. |
| **-v name:/path** | Mount a named volume at a path in the container. |
| **--mount / --bind** | Mount a host folder into the container (dev use). |
| **--network** | Which network the container joins. |
| **--restart** | Restart policy: no, on-failure, unless-stopped, always. |
| **--rm** | Delete the container automatically when it exits. |
| **--memory / --cpus** | Resource limits (see Section 17). |
| **--read-only** | Make the container filesystem read-only. |
| **--user** | Run as a specific user, overriding the image USER. |

**A production-shaped run command**

```
docker run -d \
  --name api \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file .env \
  -v app-data:/app/data \
  --memory 512m --cpus 1.0 \
  myapp:1.0
```

**EXPOSE vs -p — a classic confusion: **EXPOSE in a Dockerfile only documents the port. Nothing is reachable from your computer until you publish it with -p hostPort:containerPort (or -P to publish all exposed ports on random host ports).

### Environment variables and config

Config that changes between environments (URLs, keys, feature flags) belongs outside the image, injected at run time with -e or --env-file. Build one image; configure it per environment. Keep real secret files out of Git and out of images; on servers, prefer your platform's secret store.

### Restart policies — what happens when it crashes

| **Policy** | **Behaviour** |
| --- | --- |
| **no** | Never restart. The default. |
| **on-failure[:N]** | Restart only on non-zero exit, optionally at most N times. |
| **unless-stopped** | Always restart, except if you manually stopped it. |
| **always** | Always restart, including after a daemon/host reboot. |

For long-running services on a single host, unless-stopped is the usual choice. In Kubernetes, restart policy is handled by the orchestrator instead — do not stack both logics blindly.

## 12. Networking — how containers talk

A network driver decides how isolated a container is and who it can reach. Containers on the same custom network can reach each other by container/service name — Docker runs a built-in DNS (name lookup) server for them.

| **Driver** | **Plain meaning** | **Use when** |
| --- | --- | --- |
| **bridge (default)** | Private network on the host; ports published explicitly | Default single-host apps |
| **custom bridge** | Your own bridge network with name-based DNS | Multi-container apps on one host |
| **host** | Container shares the host network directly; no port mapping | Performance-critical, single service; Linux mainly |
| **none** | No networking at all | Batch jobs that must be fully isolated |
| **overlay** | Network spanning multiple hosts (Swarm) | Multi-host Swarm deployments |
| **macvlan** | Container gets its own LAN IP like a physical machine | Legacy apps expecting a real LAN address |

**Networking commands**

```
docker network ls
docker network create app-net
docker network inspect app-net
docker run -d --name db --network app-net postgres:16-alpine
docker run -d --name api --network app-net -p 8000:8000 myapp:1.0
# Inside api, the database is reachable at hostname: db
docker network connect app-net existing-container
docker network rm app-net
```

Port publishing recap: -p 8080:80 means 'my computer's port 8080 forwards to the container's port 80.' Only published ports are reachable from the host on bridge networks — everything else stays private between containers, which is exactly what you want for databases.

> RULE OF THUMB:  Publish only the front door (web / API). Never publish a database port to the public internet; let the app reach it over the private container network by name.

## 13. Storage — why data disappears, and how to keep it

A container's own writable layer disappears when the container is removed. Anything that must survive — database files, uploads, model weights downloaded at run time — must live outside that layer. There are three mount types:

| **Type** | **Where data lives** | **Best for** |
| --- | --- | --- |
| **Named volume** | Managed by Docker in its own storage area | Production data: databases, uploads |
| **Bind mount** | A specific folder on the host | Development: live code reload; explicit host paths |
| **tmpfs mount** | Memory only, never on disk | Temporary / sensitive scratch data |

**Volumes in commands**

```
docker volume create app-data
docker volume ls
docker volume inspect app-data
docker run -d --name db -v app-data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=example postgres:16-alpine
# Bind mount (development): host folder -> container folder
docker run -d -p 8000:8000 -v $(pwd):/app myapp:1.0
# Read-only mount: add :ro
docker run -v $(pwd)/config:/app/config:ro myapp:1.0
docker volume rm app-data   # deletes the data — be certain first
```

## 14. Docker Compose — a whole app in one file

Running five containers with five long docker run commands is error-prone. Compose describes the whole system — services, networks, volumes, ports, environment — in one file called compose.yaml, and starts it with one command. When people say 'a service' in Compose, they mean one container role (api, db, cache) that Compose can run one or more copies of.

**Example — full stack: API + PostgreSQL + Redis**

```
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://app:secret@db:5432/appdb
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=appdb
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 3s
      retries: 10
  cache:
    image: redis:7-alpine
volumes:
  db-data:
```

| **Compose key** | **What it controls** |
| --- | --- |
| **build / image** | Build from a Dockerfile, or use a ready image. |
| **ports** | Published ports, same HOST:CONTAINER format. |
| **environment / env_file** | Run-time config injected into the container. |
| **volumes** | Named volumes and bind mounts. |
| **depends_on** | Start order; with condition: service_healthy, waits for health. |
| **healthcheck** | How to test that the service is actually ready, not just started. |
| **restart** | Restart policy, same values as docker run. |
| **profiles** | Optional services started only when their profile is named. |
| **deploy.replicas** | Number of copies (mainly honoured by Swarm). |
| **networks** | Custom networks; Compose creates a default one per project. |

**Compose commands**

```
docker compose up -d          # build if needed + start in background
docker compose ps             # status of project services
docker compose logs -f api    # follow logs of one service
docker compose exec api sh    # shell into a running service
docker compose build          # rebuild images
docker compose pull           # pull newer images
docker compose down           # stop and remove containers + network
docker compose down -v        # also delete volumes (DATA LOSS)
docker compose config         # validate and print the merged config
```

**depends_on does not mean 'ready': **by itself it only controls start order. A database container can be 'started' seconds before it accepts connections. Always pair it with a healthcheck and condition: service_healthy, as in the example above.

> DEPLOYMENT PRACTICE — flagged:  Bringing up this three-service stack with Compose, breaking it, and recovering it is a core deployment exercise in the Section 27 roadmap.

# Part 5 — Production: registries, optimisation, debugging, security

## 15. Registries — sharing and deploying images

An image on your laptop helps no one else. You push it to a registry; servers pull it. The image name encodes the address: [registry-host]/[account-or-project]/[repository]:[tag]. An image with no host prefix lives on Docker Hub.

**Push and pull workflow**

```
docker login                          # Docker Hub (or: docker login ghcr.io / your ECR/ACR)
docker tag myapp:1.0 yourname/myapp:1.0
docker tag myapp:1.0 yourname/myapp:latest
docker push yourname/myapp:1.0
docker push yourname/myapp:latest
# On the server:
docker pull yourname/myapp:1.0
docker run -d -p 8000:8000 yourname/myapp:1.0
```

| **Registry** | **Notes** |
| --- | --- |
| **Docker Hub** | Public default; rate limits apply; private repos available. |
| **GitHub Container Registry (ghcr.io)** | Good fit when code already lives on GitHub. |
| **Amazon ECR / Google Artifact Registry / Azure ACR** | Cloud-native, IAM-integrated, same-region pulls are fast/cheap. |
| **Harbor / Nexus (self-hosted)** | For air-gapped or compliance-driven environments. |

Tagging strategy that works in production: tag every build with an immutable version (semantic version or Git commit SHA, e.g. myapp:1.4.2 or myapp:a1b2c3d), move latest only as a convenience, and deploy by version or digest — never by latest alone, because you cannot tell later what actually ran.

## 16. Smaller, faster images — multi-stage builds and friends

A build environment is fat: compilers, package managers, caches, source code. The running app needs only a fraction of it. A multi-stage build uses several FROM blocks: stage 1 builds, the final stage copies only the finished artefact into a clean, small base. Everything else is thrown away.

**Example — multi-stage build (Go binary, final image is tiny)**

```
# Stage 1: build
FROM golang:1.23-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/server .

# Stage 2: run — only the binary, on a minimal base
FROM alpine:3.20
RUN adduser -D appuser
USER appuser
COPY --from=builder /out/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

**Example — multi-stage for Python serving (builder installs, runtime serves)**

```
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
USER 10001
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- **Size habits: **Start from slim/alpine; install with --no-cache-dir (pip) or clean package caches in the same RUN layer.

- **One-layer rule: **Combine related RUN commands with && so temporary files are deleted in the same layer that created them — deleting in a later layer does not shrink the image.

- **Distroless: **Google's minimal bases with almost nothing inside — not even a shell. Extremely small and secure, but harder to debug (no sh to exec into). A deliberate trade-off.

- **ML note: **For ML serving: keep large model weights out of the image where possible — download from object storage at startup or mount them — so image pulls stay fast and deploys stay cheap.

## 17. Resource limits, logging, and health

Without limits, one container can consume all CPU or memory and starve everything else on the host — the exact problem cgroups exist to prevent.

**Limits on docker run**

```
docker run -d --memory 512m --memory-swap 512m --cpus 1.0 --pids-limit 200 myapp:1.0
# --memory: hard RAM cap   --cpus: CPU quota   --pids-limit: max processes (fork-bomb guard)
```

A container killed for exceeding its memory cap exits with code 137 and status OOMKilled — check with docker inspect. That signature (137 = 128 + SIGKILL) is one of the most useful numbers in container debugging.

### Logging

By default Docker captures everything a container writes to stdout/stderr with the json-file logging driver. In production, set rotation so logs cannot fill the disk, and ship logs to your platform's aggregator (the ELK / cloud logging stack from your monitoring lessons).

**Log rotation (daemon.json or per-container)**

```
docker run -d --log-opt max-size=10m --log-opt max-file=3 myapp:1.0
docker logs --since 1h --until 30m <name>   # time-windowed logs
```

### Healthchecks

A running container is not necessarily a working container — the process can be up while the app is stuck. A HEALTHCHECK (in the Dockerfile or Compose) runs a probe inside the container; Docker marks it starting → healthy / unhealthy. Orchestrators and Compose depends_on use that status to route traffic and order startups. Pair health endpoints (/health) in serving apps with Docker healthchecks — this is the same pattern you will use for model serving in Kubernetes later.

## 18. Debugging and troubleshooting — the incident toolkit

| **Symptom** | **First commands** | **What you are looking for** |
| --- | --- | --- |
| **Container exits immediately** | docker ps -a; docker logs <name> | Exit code + the app's own error message |
| **Exit code 137** | docker inspect <name> | OOMKilled: true — raise --memory or fix a leak |
| **Port already in use** | docker ps; change host port | Another container/process owns the host port |
| **Cannot reach the app** | docker port <name>; curl -v localhost:<port> | Was the port actually published? App listening on 0.0.0.0? |
| **App works locally, not in container** | docker exec -it <name> sh; env; ls | Missing env var, wrong WORKDIR, file not copied |
| **Image is huge** | docker history <image>; docker images | A layer copying data, caches, or build tools |
| **Build uses stale code** | docker build --no-cache; check .dockerignore | Cache hit on COPY, or file excluded from context |
| **Container cannot reach DB** | docker network inspect; ping by name | Containers on different networks; use service name, not localhost |

**The five commands that solve most incidents**

```
docker ps -a                  # what exists and its status / exit code
docker logs --tail 200 <name> # what it said before it died
docker inspect <name>         # config, mounts, networks, OOMKilled
docker exec -it <name> sh     # go inside and look (if it stays up)
docker stats                  # is it starved or leaking resources?
```

**localhost trap: **inside a container, localhost means the container itself — not your laptop, and not another container. Containers reach each other by name on a shared network (db, cache, api). Half of all beginner networking bugs are this one word.

Also remember bind address: an app listening only on 127.0.0.1 inside its container cannot be reached through a published port. Serving apps must listen on 0.0.0.0 inside the container — that is why the uvicorn examples in this guide use --host 0.0.0.0.

## 19. Security — the non-negotiables

- **Never run as root: **Default root inside a container is root on the image's filesystem and makes escapes and accidents far worse. Create a user in the Dockerfile and set USER, or pass --user.

- **Pin images: **Pin base images by version (and digest for production). An unpinned FROM python can silently change under you.

- **Smaller image, smaller risk: **Every tool in the image is attack surface. Slim/distroless bases and multi-stage builds are security controls, not just size tricks.

- **Drop capabilities: **Containers start with a default capability set. Drop everything and add back only what is needed; combine with --read-only where the app allows.

- **Secrets outside images: **Inject at run time (env file with tight permissions, orchestrator secrets, cloud secret managers). Never in Dockerfiles, layers, or Git.

- **Scan every image: **Scan images in CI for known vulnerabilities in the base image and dependencies; rebuild on a patched base when findings are critical.

- **Patch and protect the daemon: **Keep the Docker daemon and base images updated; never expose the daemon's TCP socket publicly without TLS — it is unauthenticated root access.

**A hardened run, putting it together**

```
docker run -d --name api \
  --user 10001 --read-only --cap-drop ALL \
  --memory 512m --cpus 1.0 --pids-limit 200 \
  -p 8000:8000 myapp:1.0@sha256:<digest>
```

## 20. Docker in CI/CD and production

The production pattern is a straight line: commit → CI builds the image once → scan and test the image → push to the registry with an immutable tag → deploy that exact tag everywhere. The image that passed testing is byte-for-byte the image that runs in production — that identity is Docker's core production promise.

**CI-shaped flow (any CI system)**

```
docker build -t registry.example.com/myapp:${GIT_SHA} .
docker push registry.example.com/myapp:${GIT_SHA}
# Deploy step pulls and runs that exact tag — never rebuilds on the server
```

- **Promote, don't rebuild: **Deploy by immutable tag/digest; promote the same image dev → staging → prod.

- **One concern per container: **One process per container; logs to stdout; config from environment. These are the container-era form of the twelve-factor app rules.

- **Rollout: **Blue-green and canary (from your serving lessons) become image-tag swaps: run the new tag beside the old, shift traffic, roll back by re-running the old tag.

- **When Docker alone is not enough: **Docker alone runs containers on one host. Across many hosts you need an orchestrator: Docker Swarm (built-in, simple) or Kubernetes (the industry standard, and the platform the rest of your course builds on). Docker is the packaging skill; Kubernetes is the fleet-management skill.

# Part 6 — Advanced Docker

## 21. BuildKit and Buildx — the modern builder

BuildKit is Docker's current build engine (default in modern Docker). It builds independent steps in parallel, has better caching (including cache mounts that reuse pip/npm caches between builds without storing them in layers), supports secret mounts (Section 10), and can use remote cache in a registry so CI builds reuse your laptop's cache and vice versa.

**Cache mounts and registry cache**

```
# In a Dockerfile: reuse the pip download cache between builds
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Build with cache stored in a registry
docker buildx build --cache-to type=registry,ref=yourname/myapp:cache --cache-from type=registry,ref=yourname/myapp:cache -t yourname/myapp:1.0 .
```

Buildx is the CLI front-end for BuildKit's advanced features — most importantly multi-platform builds.

## 22. Multi-platform images — one tag, many CPUs

Your laptop may be ARM (Apple Silicon) while cloud servers are x86 (amd64) — different CPU families need different binaries. A multi-platform image (a manifest list) lets one tag, e.g. myapp:1.0, contain both variants; Docker automatically pulls the right one for the machine. Running the wrong architecture is slow (emulation) or fails outright.

**Build and push a multi-platform image**

```
docker buildx create --name multi --use   # create a multi-platform builder (once)
docker buildx build --platform linux/amd64,linux/arm64 -t yourname/myapp:1.0 --push .
```

## 23. Contexts, Swarm mode, and other advanced pieces

- **Contexts: **A context is a saved connection to a Docker daemon — your local one, or a remote server over SSH/TCP. docker context use switches where every command runs. Powerful and dangerous: always check your current context before destructive commands.

- **Swarm mode (docker swarm init, docker service, docker stack): **Docker's built-in orchestrator: turn Docker hosts into a cluster, declare services with replicas, and get rolling updates and overlay networking. Far simpler than Kubernetes, far less capable. Worth knowing it exists; the industry's centre of gravity is Kubernetes.

- **Plugins and templates: **Re-usable image templates and daemon extensions (for example volume drivers for cloud storage, network drivers). Mostly encountered when a platform team hands you a standard setup.

- **Offline transfer — docker save / docker load: **Images can be saved to a tar file and loaded elsewhere with no registry at all — used in air-gapped (no-internet) environments.

**Offline transfer and contexts**

```
docker save myapp:1.0 -o myapp-1.0.tar
docker load -i myapp-1.0.tar
docker context ls
docker context use default
```

## 24. Docker and ML infrastructure — where this fits your path

For AI infrastructure, Docker is the packaging layer under everything else in your course. Models are served from containers (your Lesson 6 FastAPI serving app becomes an image, then a Kubernetes Deployment). Training jobs run as containers on GPU machines — the image carries the CUDA libraries and framework versions, which is exactly the 'works on my machine' problem at its most expensive. Three ML-specific habits:

- **GPU access: **GPU containers need the NVIDIA Container Toolkit on the host and --gpus all at run time; the image must match CUDA versions to the driver.

**Run a GPU container**

```
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

- **Model weights: **Keep weights in object storage or a mounted volume, not baked into the image, unless the model is small and immutable — image size is pull time on every node.

- **Version pinning: **Pin framework + CUDA + Python versions together in the Dockerfile; that pinned combination is the reproducibility guarantee for serving.

# Part 7 — Reference: cheat sheet, practice, self-test

## 25. Command cheat sheet

| **Task** | **Command** |
| --- | --- |
| **Version / info** | docker --version  \|  docker info |
| **Run (background, named, port)** | docker run -d --name web -p 8080:80 nginx:1.27 |
| **List containers** | docker ps  \|  docker ps -a |
| **Logs (follow)** | docker logs -f <name> |
| **Shell inside** | docker exec -it <name> sh |
| **Stop / start / remove** | docker stop <name>  \|  docker start <name>  \|  docker rm <name> |
| **List / pull / remove images** | docker images  \|  docker pull <img>  \|  docker rmi <img> |
| **Build** | docker build -t myapp:1.0 . |
| **Tag / push** | docker tag myapp:1.0 user/myapp:1.0  \|  docker push user/myapp:1.0 |
| **Volumes** | docker volume create data  \|  docker volume ls |
| **Networks** | docker network create app-net  \|  docker network ls |
| **Inspect anything** | docker inspect <name-or-id> |
| **Live resource use** | docker stats |
| **Disk use / cleanup** | docker system df  \|  docker system prune |
| **Compose up / down** | docker compose up -d  \|  docker compose down |
| **Compose logs / shell** | docker compose logs -f api  \|  docker compose exec api sh |

## 26. Best practices — the whole guide on one page

1. Use official, pinned, slim base images; rebuild regularly for patches.

1. Copy dependency files first, code last — protect the layer cache.

1. Always write a .dockerignore; keep the build context small.

1. One process per container; log to stdout/stderr; configure via environment.

1. Run as a non-root USER; drop capabilities; use --read-only where possible.

1. Never bake secrets into an image — inject them at run time.

1. Persist data in named volumes; never trust the container writable layer.

1. Publish only the ports that must be public; keep databases on private networks.

1. Set memory/CPU limits and a restart policy for every long-running service.

1. Add a HEALTHCHECK and a /health endpoint to every service image.

1. Tag builds immutably (version or Git SHA); deploy by tag/digest, never latest alone.

1. Use multi-stage builds; measure image size with docker history.

1. Scan images in CI; promote the same image through every environment.

## 27. Practice roadmap — deployment only, for your laptop

> DEPLOYMENT PRACTICE — flagged, per your rule:  Every stage below is deployment / operations practice. No model-writing, no application development. Stages are ordered; do not skip Stage 2 — it is where most real understanding forms.

| **Stage** | **Exercise** | **You prove it by** |
| --- | --- | --- |
| **1. Basics** | Run nginx and hello-world; ps, logs, exec, stop, rm | Serving a page on localhost:8080 and cleaning up fully |
| **2. Dockerfile** | Containerise the Lesson 6 FastAPI serving app; add .dockerignore, non-root USER, HEALTHCHECK | docker build + run; /health and /metrics responding |
| **3. Optimise** | Shrink that image: slim base, cache order, multi-stage | Before/after docker images + docker history comparison |
| **4. Compose** | Bring up API + Postgres + Redis stack from Section 14 | docker compose up; API reaches db by name; data survives down/up in the volume |
| **5. Operate** | Kill the API, OOM it with a low --memory, read exit 137, fix limits, follow logs | Explaining each failure from ps/inspect/logs evidence |
| **6. Ship** | Push a SHA-tagged image to a registry; pull and run it 'on a server' (second context or a cloud VM — the parked Lesson 5 exercise) | Same digest running in both places |
| **7. GPU (when available)** | Run the nvidia/cuda container with --gpus all | nvidia-smi output from inside the container |

## 28. Glossary — quick lookup

| **Term** | **Meaning** |
| --- | --- |
| **Build context** | Files sent to the daemon for a build (controlled by .dockerignore). |
| **BuildKit / Buildx** | Modern build engine / its CLI for advanced and multi-platform builds. |
| **cgroups** | Kernel feature limiting CPU/memory/IO per container. |
| **Daemon (dockerd)** | Background service that builds and runs containers. |
| **Digest** | Immutable sha256 fingerprint of an image's exact content. |
| **Layer** | One saved step of an image; cached, shared, stacked via OverlayFS. |
| **Namespace** | Kernel feature giving a container its private view of the system. |
| **Overlay network** | Multi-host container network (Swarm). |
| **Registry / Repository** | Where images live / a named collection of image versions. |
| **Volume** | Docker-managed storage that outlives containers. |

## 29. Test yourself

1. What is the difference between an image and a container?

2. Why does a container start in seconds while a VM takes minutes?

3. What do namespaces and cgroups each do?

4. Why does COPY requirements.txt come before COPY . . in a Dockerfile?

5. EXPOSE 8000 is in the Dockerfile — why can you still not reach the app?

6. Your API cannot reach its database and the code uses localhost. What is wrong?

7. A container keeps disappearing along with its data. What should the data have been on?

8. What does exit code 137 tell you, and what do you check next?

9. Why is deploying :latest risky, and what should you deploy instead?

10. What does a multi-stage build throw away, and why does that matter for security?

*If you can answer all ten in your own words, you have the mental model. The rest is practice — and on your deployment-only path, that practice is exactly the roadmap in Section 27.*

**— End of guide —**
