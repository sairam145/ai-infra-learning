# Lesson 02: Development Environment Setup

> **In one sentence:** install and verify every tool the course needs, so the rest of the work is building, not fighting the laptop.

---

## How my setup works (Windows)

I work **inside Ubuntu (WSL2)**. Only two things run on the Windows side:

```
Windows
├── Docker Desktop   ← the Docker engine; Ubuntu borrows it via WSL Integration
├── VS Code          ← the editor; connects into Ubuntu with the WSL extension
└── WSL2: Ubuntu 24.04   ← where everything else lives and runs
    ├── Python 3.12 + venv (~/ai-infra-venv)
    ├── Git + SSH key for GitHub
    ├── kubectl, Helm, minikube
    ├── AWS CLI, Terraform
    └── ~/ai-infra-learning   ← this repo
```

---

## What each tool is for

| Tool | Version | Plain meaning |
|---|---|---|
| **Python** | 3.12.3 | The language most AI tools are written in |
| **Virtual environment** | `~/ai-infra-venv` | A separate box for this project's packages, so projects can't break each other |
| **PyTorch** | 2.14.1 | The ML framework (runs on CPU here: `GPU: False` is expected on a laptop) |
| Transformers, FastAPI, uvicorn, pytest | current | Load models, build APIs, run tests |
| **Git + GitHub (SSH)** | 2.43 | Save every version of my work and publish it as a portfolio |
| **Docker** | 29.0.1 | Pack apps into containers that run the same everywhere |
| **kubectl** | 1.37.1 | The remote control for any Kubernetes cluster |
| **Helm** | 3.22.0 | App store for Kubernetes: install complex software with one command |
| **minikube** | 1.39.0 | A small practice Kubernetes cluster on my laptop |
| **AWS CLI** | 2.38.1 | Control my AWS account from the terminal (IAM user, region `us-east-1`) |
| **Terraform** | 1.16.6 | Create cloud infrastructure from code |
| **VS Code + WSL extension** | — | Edit Ubuntu files directly from Windows |

---

## Check everything in one command

```bash
cd ~/ai-infra-learning
./verify-setup.sh
```
Every line should show a version number or ✅. The script also prints "AWS connected" **without** showing any account details.

---

## Daily workflow

```bash
cd ~/ai-infra-learning
activate-ai          # shortcut for: source ~/ai-infra-venv/bin/activate
code .               # open VS Code (terminal inside it: Ctrl + `)
# ... build ...
git add . && git commit -m "message" && git push
```

## Local Kubernetes

```bash
minikube start --driver=docker --memory=4096   # first run 3–5 min; wait for "Done!"
kubectl get nodes                              # minikube   Ready
minikube stop                                  # free RAM when finished
```

---

## Install commands (Ubuntu / WSL2), for a fresh machine

```bash
# Basics
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential curl wget unzip git python3-venv python3-pip

# Python environment
python3 -m venv ~/ai-infra-venv && source ~/ai-infra-venv/bin/activate
pip install --upgrade pip
pip install torch transformers fastapi uvicorn requests pyyaml python-dotenv pytest
echo 'alias activate-ai="source ~/ai-infra-venv/bin/activate"' >> ~/.bashrc

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -m 0755 kubectl /usr/local/bin/kubectl && rm kubectl

# Helm
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
unzip -q awscliv2.zip && sudo ./aws/install && rm -rf aws awscliv2.zip

# Terraform
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform

# Git + GitHub SSH key
git config --global user.name "Sai Ram N."
git config --global user.email "<github-email>"
git config --global init.defaultBranch main
ssh-keygen -t ed25519 -C "<github-email>"     # Enter through the prompts
cat ~/.ssh/id_ed25519.pub                      # paste into GitHub → Settings → SSH keys
ssh -T git@github.com                          # "Hi <user>! You've successfully authenticated"
```

**Docker on WSL:** install Docker Desktop on Windows, then **Settings → Resources → WSL Integration → turn on Ubuntu → Apply & Restart**. Don't install a second Docker inside Ubuntu.

---

## Lessons learned the hard way

### Security
- **AWS secret keys go into the terminal only.** Never into chat, screenshots, GitHub, or videos. A leaked key can be abused within hours (often for crypto mining) and run up thousands of dollars.
- **If a key leaks:** IAM → Users → *user* → Security credentials → **Deactivate → Delete** the key, then create a new one. Then check Billing and EC2 for anything unexpected.
- Run `clear` after `aws configure`, **before** copying any terminal output.
- `chmod 600 ~/.aws/credentials` keeps the key file private to me.
- Use an **IAM user**, never the root account's keys.
- The `.gitignore` blocks `.env`, `.aws/`, `*.tfstate`, and model files from ever being committed.

### Setup gotchas
| Problem | Cause | Fix |
|---|---|---|
| `docker: command not found` in Ubuntu | Docker Desktop not connected to WSL | Turn on WSL Integration for Ubuntu, then reopen the terminal |
| `minikube` half-created, `kubectl` "connection refused" | Pressed Ctrl+C during the first `minikube start` | `minikube delete`, then start again and wait for "Done!" |
| AWS SSL error for `sts.yes.amazonaws.com` | Typed `yes` at the region prompt | Re-run `aws configure` with `us-east-1` and `json` |
| `-bash: your-username: No such file` | Typed the `< >` placeholder brackets | `< >` means "replace this"; type the value without brackets |
| Slow files, permission errors | Project stored under `/mnt/c/` | Keep projects in Ubuntu's home `~/` |
| Interactive prompt filled with the wrong text | Pasted several commands at once | Paste interactive or slow commands one at a time |

---

## Exercise 01: done

- [x] Verification script all green
- [x] PyTorch imports and runs
- [x] `docker run hello-world` works
- [x] Repo created and pushed to GitHub over SSH

---

*Part of my [AI Infrastructure learning log](../../../README.md). Course: [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
