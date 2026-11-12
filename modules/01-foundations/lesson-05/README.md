# Lesson 05: Cloud Computing for ML Infrastructure

> **In one sentence:** the cloud lets me rent computers, storage, and GPUs by the hour instead of buying them, and my job is to use them **securely, reliably, and without wasting money.**

---

## What the cloud is, plainly

Renting instead of buying. Like using a car-rental service instead of owning a fleet: pick the car you need, pay by the hour, return it when done.

**Five things that make it "cloud":**
| Feature | Plain meaning |
|---|---|
| Self-service | Create machines yourself in minutes, no ticket to IT |
| Network access | Reach it from anywhere |
| Shared pool | Many customers share huge data centers |
| Elastic | Scale up for a spike, scale down after |
| Pay per use | You're billed for what you actually use (and for what you forget to turn off) |

### Service models: how much you manage

| Model | You manage | Provider manages | Analogy | Examples |
|---|---|---|---|---|
| **IaaS** | OS, runtime, app, data | Hardware, network | Renting an empty kitchen | EC2, Compute Engine |
| **PaaS** | App and data | Everything below | Renting a kitchen with staff | Elastic Beanstalk, Cloud Run |
| **SaaS** | Just your usage | Everything | Ordering food | Gmail, Slack |
| **ML platforms** | Model and data | Training/serving infra | A meal-kit service | SageMaker, Vertex AI, Azure ML |

**For GPU DevOps I mostly work at the IaaS + Kubernetes layer:** EC2 GPU instances under EKS, built with Terraform.

---

## The big three, side by side

| Need | AWS | Google Cloud | Azure |
|---|---|---|---|
| Virtual machines | EC2 | Compute Engine | Virtual Machines |
| GPU machines | G / P instances (e.g., g4dn T4, g5 A10G, p5 H100) | A2 / G2 / A3 | NC / ND series |
| Managed Kubernetes | **EKS** | GKE | AKS |
| Object storage | **S3** | Cloud Storage | Blob Storage |
| Container registry | **ECR** | Artifact Registry | ACR |
| ML platform | SageMaker | Vertex AI | Azure ML |
| Serverless | Lambda | Cloud Functions / Cloud Run | Functions |
| Identity | **IAM** | IAM | Entra ID + RBAC |
| Private network | **VPC** | VPC | VNet |

**I focus on AWS.** It has the biggest market share and the most job postings, and it's what my project runs on.

---

## The three building blocks for ML

### 1. Compute
| Type | Use |
|---|---|
| CPU instances | APIs, small models, preprocessing |
| **GPU instances** | Training and serving deep learning models and LLMs |
| Serverless | Small, bursty tasks; not for big models |
| Managed Kubernetes | Running many containers at scale, including GPU pods |

### 2. Storage
| Type | Plain meaning | ML use |
|---|---|---|
| **Object (S3)** | Unlimited file warehouse | Datasets, model weights, artifacts |
| Block (EBS) | A hard drive attached to one machine | OS disk, fast local cache for model files |
| File (EFS) | A shared drive many machines mount | Shared model cache across pods |
| Databases | Structured data | Metadata, features, results |

### 3. Networking
| Piece | Plain meaning |
|---|---|
| **VPC** | My private network in the cloud |
| Public subnet | Faces the internet (load balancers) |
| Private subnet | Hidden from the internet (servers, GPU nodes) |
| NAT gateway | Lets private servers reach out (e.g., download models) without being reachable |
| Security group | Firewall rules: which ports, from where |
| Load balancer | Spreads traffic across servers |

---

## Cost management (the part that saves real money)

| Strategy | Saving | Use it for | Watch out |
|---|---|---|---|
| **Right-size** | 50%+ | Everything: start small, measure, then scale | Over-provisioning "just in case" |
| **Spot instances** | Up to ~90% | Batch jobs, training with checkpoints, dev | Can be taken back: **AWS gives a 2-minute warning** (GCP: 30 seconds) |
| **Reserved / Savings Plans** | ~30–60% (1–3 year commitment) | Always-on production serving | Locks you in |
| **Auto-shutdown** | Varies | Dev environments: off at night and weekends | Forgetting it |
| **Delete unused resources** | Varies | Old volumes, snapshots, idle load balancers, NAT gateways | "Zombie" resources quietly billing |
| **Storage lifecycle rules** | Varies | Move old files to cheaper storage tiers | — |
| **Budget alerts** | — | Alert at 50% / 80% / 100% of budget | Not setting them |

**My rule for the GPU project:** the cluster costs about $0.80/hour. Run `terraform destroy` at the end of every session.

---

## Security and reliability best practices

**Security**
- ✅ Use **IAM roles** for machines and pods, not long-lived access keys
- ✅ MFA on root and admin accounts; never use root for daily work
- ✅ Security groups open only what's needed
- ✅ Encrypt data at rest and in transit
- ✅ Private subnets for servers, databases, and GPU nodes
- ✅ Rotate credentials
- ❌ Never commit credentials to Git
- ❌ No public S3 buckets with sensitive data

**Reliability**
- Spread across multiple availability zones (separate data centers in a region)
- Health checks, auto-scaling, managed services where possible
- Backups and a recovery plan

---

## Key commands (AWS)

| Command | What it does |
|---|---|
| `aws configure` | Set up CLI credentials and default region |
| `aws sts get-caller-identity` | "Who am I logged in as?" |
| `aws ec2 describe-instances` | List my machines |
| `aws ec2 describe-instance-types --filters "Name=instance-type,Values=g4dn.*"` | See GPU instance specs |
| `aws ec2 run-instances ...` | Launch a machine |
| `aws ec2 stop-instances` / `terminate-instances --instance-ids i-...` | Stop (keep disk) / delete for good |
| `aws s3 mb s3://my-bucket` | Make a bucket |
| `aws s3 cp model.bin s3://my-bucket/models/` | Upload a file |
| `aws s3 ls s3://my-bucket/` | List files |
| `aws service-quotas get-service-quota --service-code ec2 --quota-code L-DB2E81BA` | Check my GPU (G and VT) vCPU quota |
| `aws ce get-cost-and-usage ...` | Pull cost data from Cost Explorer |

---

## Why it matters for AI/GPU DevOps
- **GPUs are the most expensive line item.** A forgotten H100 node can cost thousands per month.
- **GPU quotas start at zero** on new AWS accounts and are **per region**. Requesting them is step one of any GPU project.
- Model weights live in **S3**, images in **ECR**, GPU nodes in **private subnets** behind a **NAT gateway**. That's the exact layout of my EKS platform.

---

## Self-check
1. IaaS vs. PaaS vs. SaaS, in one line each?
2. Which AWS services store model weights, store container images, and run Kubernetes?
3. When are spot instances a good idea, and when not?
4. Why put GPU nodes in a private subnet?
5. Name three ways cloud bills get out of control.

<details>
<summary>Answers</summary>

1. IaaS: rent machines, manage the OS up. PaaS: just deploy the app. SaaS: just use the software.
2. S3, ECR, EKS.
3. Good for interruptible work (batch, checkpointed training, dev). Not for serving that must stay up, unless you have spare capacity to absorb the 2-minute takeback.
4. So they can't be reached from the internet. They reach out through a NAT gateway.
5. Over-sized instances, forgotten resources (idle GPUs, NAT gateways, volumes), no budget alerts.

</details>

---

*Part of my [AI Infrastructure learning log](../../../README.md). Course: [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
