# Lesson 01: Introduction to ML Infrastructure

> **In one sentence:** data scientists build the model; ML infrastructure engineers build everything that makes it useful to real users: fast, reliable, and affordable.

---

## The core idea

**The model is a chef. Infrastructure is the restaurant.**
A brilliant chef alone feeds nobody. You need a kitchen, ordering, delivery, health inspections, and someone watching costs. ML infrastructure is the restaurant around the model.

ML infrastructure = the systems, tools, and practices that let models be **built, deployed, and kept running in production**.

---

## What the job actually involves

| Responsibility | Plain meaning |
|---|---|
| Deploy models | Put trained models behind an API that apps can call |
| Build data pipelines | Get the right data to the model for training and answering |
| Monitor | Watch speed, uptime, **and whether the answers are still good** |
| Optimize cost and speed | Get the most out of every expensive GPU |
| Automate | Training, testing, deploying with no manual steps |
| Manage compute | GPUs and clusters of machines |
| Partner with data scientists | Turn their needs into working systems |

**In one line:** keep models fast, reliable, and affordable in production.

---

## Why it's harder than normal DevOps

| Challenge | What it means |
|---|---|
| **Models change** | They get retrained and replaced, unlike an app that stays the same |
| **Data decides quality** | Bad or changed data quietly makes a model worse |
| **GPUs are expensive** | Wasted GPU time is the biggest bill in AI |
| **Scale is huge** | Some systems answer millions of requests per second |
| **Failures are silent** | The server stays up while the answers slowly get worse. Nothing crashes, so nothing alerts. |

### Normal infrastructure vs. ML infrastructure

| Area | Normal infrastructure | ML infrastructure |
|---|---|---|
| What you deploy | An app that stays the same | A model that keeps changing |
| Quality checks | Uptime and speed | Plus model quality and data quality |
| Versioning | Code in Git | Code + data + models |
| Scaling | Based on traffic | Traffic + heavy training jobs |
| Monitoring | CPU, memory, requests | Plus accuracy, drift, bias |
| Tools | Docker, Kubernetes, CI/CD | Same, plus MLflow, Airflow, GPU tooling |

**Good news for DevOps engineers:** it's the same foundation (Docker, Kubernetes, CI/CD, Terraform, monitoring) with ML-specific layers on top.

---

## MLOps in plain words

**MLOps** = Machine Learning + DevOps + Data Engineering. Practices that get models into production reliably and keep them improving.

It's a **loop**, not a straight line:
```
Data → Training → Deployment → Feedback → (back to Data)
```

**Three pillars:**
| Pillar | Meaning |
|---|---|
| People | Data scientists, ML engineers, and infra teams working as one team |
| Process | Agreed, repeatable steps for experimenting, testing, deploying |
| **Platform** | Automated infrastructure that runs the whole lifecycle. **This is my part.** |

---

## Real-world examples

| Company | Problem | Infrastructure answer |
|---|---|---|
| Netflix | Recommendations for 200M+ users in under 100 ms | Distributed model serving + heavy caching |
| Uber | Real-time pricing, ETAs, driver matching in every city | Michelangelo, an in-house ML platform |
| OpenAI | Serving models with billions of parameters to millions of people | Custom inference infrastructure + model optimization |

---

## Trends shaping the field

1. **LLM infrastructure:** serving large models efficiently (vLLM, RAG, vector databases). At scale it can cost $1M+/month, so optimization matters.
2. **Multi-cloud:** most enterprises use more than one cloud provider.
3. **Cost and green AI:** FinOps, smaller models, less wasted compute.
4. **Responsible AI:** bias checks, explainability, privacy, laws like the EU AI Act.
5. **Platform engineering:** self-service internal platforms instead of one-off tools.

---

## What makes a great ML infra engineer

| Technical | Soft skills | Mindset |
|---|---|---|
| Strong Python, some Go and Bash | Work well with data scientists | Reliable beats "just working" |
| Systems thinking at scale | Explain tech to any audience | Every choice has a cost |
| Deep skill in one cloud | Solve new problems creatively | Make data scientists faster |
| Debugging production issues | Keep learning as tools change | Test, monitor, document |
| Automate everything as code | Sweat the small config details | Always keep improving |

**How to learn it:** 60% hands-on, 40% theory. Type the code, break things on purpose, write down every error and fix, push everything to GitHub.

---

## Note on the course material
The lesson quotes "400%+ growth in AI infrastructure roles" without a source, so I left it out. Its salary ranges are the course's own estimates; treat them as rough guides.

---

## Self-check

1. What is ML infrastructure, and how is it different from normal infrastructure?
2. What are the main phases of the ML lifecycle?
3. What is MLOps, and why does it matter?
4. Name three challenges unique to ML infrastructure.
5. Why is "failures are silent" the scariest challenge?

<details>
<summary>Answers</summary>

1. The systems that run models in production. It adds changing models, data/model versioning, and quality monitoring on top of normal DevOps.
2. Data → Training → Deployment → Monitoring/Feedback, in a loop.
3. Practices combining ML, DevOps, and data engineering so models reach production reliably and keep improving.
4. Changing models, data quality, GPU cost, huge scale, silent failures.
5. Because the server keeps running and reports healthy while the answers get worse, so normal alerts never fire.

</details>

---

*Part of my [AI Infrastructure learning log](../../../README.md). Course: [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*
