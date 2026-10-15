#!/bin/bash
echo "=== Environment check ==="
python --version
python -c "import torch; print('PyTorch', torch.__version__)" || echo "❌ PyTorch"
python -c "import fastapi; print('FastAPI', fastapi.__version__)" || echo "❌ FastAPI"
git --version
docker --version && (docker ps >/dev/null 2>&1 && echo "✅ Docker running" || echo "⚠️ Start Docker Desktop")
kubectl version --client 2>/dev/null | head -1 || echo "❌ kubectl"
helm version --short || echo "❌ helm"
minikube version --short || echo "❌ minikube"
aws --version || echo "❌ aws"
terraform -version | head -1 || echo "❌ terraform"
aws sts get-caller-identity >/dev/null 2>&1 && echo "✅ AWS connected" || echo "❌ AWS not connected"
echo "=== Done ==="
