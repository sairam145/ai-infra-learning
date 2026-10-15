# Lesson 03: ML Infrastructure Basics (the ML Lifecycle)

> **In one sentence:** a machine learning model is never "done." It goes around a loop of **data → train → evaluate → deploy → monitor → retrain**, and infrastructure engineers build the systems that keep that loop running safely.

This folder has a small, working example of the **whole loop**: a spam detector you can train, test, version, serve as an API, monitor, retrain, and roll back. It's small enough to run on a laptop in minutes, but it follows the same structure real companies use.

---

## Why this matters

Most people think AI is about building a smart model. In real companies, building the model is maybe 10% of the work. The other 90% is:

- getting the right data to it,
- making sure a new version is actually *better* before users see it,
- serving it fast and reliably to millions of people,
- noticing when it quietly starts giving worse answers,
- and fixing it without downtime.

That 90% is **ML infrastructure**, and it's what this course and this repo are about.

---

## The ML lifecycle in plain words

```
 1. DATA ──► 2. TRAIN ──► 3. EVALUATE ──► 4. DEPLOY ──► 5. MONITOR ──► 6. RETRAIN ─┐
    ▲                                                                              │
    └──────────────────────────────────────────────────────────────────────────────┘
```

| # | Stage | What happens (plain words) | Real-life analogy | In this lab |
|---|---|---|---|---|
| 1 | **Data** | Collect examples, clean them, label them | Gathering ingredients | The list of messages in `train.py` |
| 2 | **Train** | The model studies the examples and learns patterns | A student studying | `model.fit(...)` |
| 3 | **Evaluate** | Test the model on examples it has **never seen** | The final exam | Accuracy, precision, recall |
| 4 | **Deploy** | Put the model behind an API so apps can use it | Opening the restaurant | `serve.py` with FastAPI |
| 5 | **Monitor** | Watch speed, errors, and what it's answering | A car dashboard | `/metrics` endpoint |
| 6 | **Retrain** | New data or worse results? Train a new version | Updating the menu | Add data, run `train.py` again |

---

## What I built

```
lesson-03/
├── train.py    # Stages 1–3: data → train → evaluate → save a versioned model
├── serve.py    # Stages 4–5: serve the newest model as an API + expose metrics
└── models/     # Mini "model registry": every version + its scores (not pushed to GitHub)
```

### `train.py`: data, train, evaluate, version
1. **Data:** 20+ example messages, each labeled `spam` or `ham` (ham = normal message).
2. **Split:** 70% for studying (training), 30% held back for the exam (testing).
3. **Train:** a simple text model (TF-IDF + Logistic Regression) learns which words point to spam.
4. **Evaluate:** grades the model on the 30% it never saw.
5. **Version:** saves the model with a timestamp name like `spam-v20261014-215245.joblib`, plus a `.json` file with its scores.

### `serve.py`: deploy and monitor
- Loads the **newest** model version from `models/`.
- `GET /health` → is the server alive, and **which version** is live?
- `POST /predict` → send a message, get back `spam` or `ham`.
- `GET /metrics/` → numbers a monitoring system (Prometheus) can collect.
- `GET /docs` → a free test page FastAPI generates in the browser.

---

## How to run it

```bash
cd ~/ai-infra-learning/modules/01-foundations/lesson-03
source ~/ai-infra-venv/bin/activate          # or: activate-ai
pip install scikit-learn joblib prometheus-client fastapi uvicorn

python train.py                    # train + evaluate + save a version
uvicorn serve:app --port 8000      # start the API (leave running)
```

In a second terminal:
```bash
curl localhost:8000/health
curl -X POST localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"Win a free prize now"}'
curl -X POST localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"See you at lunch"}'
curl -s localhost:8000/metrics/ | grep -E "^predictions_total|inference_seconds_count"
```

Or open **http://127.0.0.1:8000/docs** in a browser and click **Try it out**.

---

## What happened when I ran it (the real lesson)

1. **Version 1 worked.** "Win a free prize now" → `spam`, "See you at lunch" → `ham`.
2. **I added new spam examples and retrained.** Version 2 deployed, and `/health` showed the new version. Everything looked healthy.
3. **But version 2 got it wrong.** "Your package is held, pay the fee" → `ham`, a missed scam.
4. **Why:**
   - The dataset was tiny (22 messages), and the new examples probably landed in the 30% *test* split, so the model never studied them.
   - The test set was only ~7 messages, so both versions scored **67%**. The exam was too small to tell them apart.
5. **The fix:** **roll back** to the previous version (possible only because every version was saved), add more data, and add a **quality gate** that refuses to save a model scoring below a minimum.

**The takeaway:** a healthy server is not a good model. The API said "ok" the whole time while giving a wrong answer. This is the "silent failure" that makes ML infrastructure different from normal software.

---

## Key terms (plain words)

| Term | Plain meaning | Why it matters |
|---|---|---|
| **Model** | A file that turns input (a message) into an answer (spam/ham) | The thing we're serving |
| **Training** | The model learning from labeled examples | Bad data in, bad model out |
| **Test set** | Examples hidden during training, used only for grading | Without it, you can't know if the model really learned |
| **Accuracy** | How often it's right overall | 0.67 = right 2 out of 3 times |
| **Precision** | When it says "spam," how often is it really spam? | Low precision = good emails go to the spam folder |
| **Recall** | Of all real spam, how much did it catch? | Low recall = scams get through |
| **Model version** | A unique saved copy of each trained model | Lets you know what's live and roll back |
| **Model registry** | The library of all versions plus their scores (`models/` here; MLflow or S3 in real life) | The single source of truth for models |
| **Quality gate** | An automatic rule: "don't release a model below X score" | Stops bad models before users see them |
| **Rollback** | Switching back to the last good version | The 3am emergency fix |
| **System metric** | Is the *server* healthy? (speed, errors, CPU/GPU) | Catches crashes and slowness |
| **Model metric** | Are the *answers* good? (what it predicts, accuracy) | Catches silent quality problems |
| **Data drift** | Real-world inputs change from what the model trained on | Why models get worse over time |
| **Latency p95** | 95% of requests finish faster than this | Companies care about the slowest users |

---

## Safe ways to release a new model

| Strategy | How it works | Analogy |
|---|---|---|
| **Blue-green** | Run old and new side by side, then switch all traffic at once. Switch back if it breaks. | Two stages; flip the spotlight |
| **Canary** | Give the new model to 5% of users first, watch, then increase | Let a few customers taste-test first |
| **Shadow** | The new model sees real requests, but users still get the old model's answers | A trainee cooks alongside the chef; nobody eats the trainee's food |

A canary rollout would have caught my version-2 mistake while only a few users saw it.

---

## Mistakes to avoid

| Mistake | What goes wrong | Fix |
|---|---|---|
| Manual deployments | Slow, error-prone, can't repeat | Automate with CI/CD |
| No model versions | Can't roll back or explain results | Save every version with its scores |
| Training on production servers | Training steals resources from live users | Separate training from serving |
| Ignoring data quality | Garbage in, garbage out, silently | Validate data before training |
| No monitoring | You never find out the model got worse | Track system **and** model metrics |

---

## The tools in this lesson, plainly

**★ = core for AI/GPU DevOps**, ◐ = know it and use it a little, ○ = just recognize the name

| Stage | Tool | What it does | Need |
|---|---|---|---|
| Data | **S3 / GCS / Azure Blob** | Cloud file storage for datasets and models | ★ |
| Data | Airflow | Runs multi-step jobs on a schedule, in order | ◐ |
| Data | Kafka / Flink | Moves and processes live data streams | ○ |
| Data | Spark / Dask | Splits huge data jobs across many machines | ○ |
| Data | DVC / Delta Lake | Version control for datasets | ◐ |
| Data | Great Expectations | Automatic data quality checks | ○ |
| Data | Parquet | Compressed table format, much smaller and faster than CSV | ◐ |
| Train | **GPU clusters** | Many GPU machines working together | ★ |
| Train | **Kubernetes** | Schedules containers onto machines, including GPUs | ★ |
| Train | **Spot instances** | Spare cloud machines at 60–90% off; can be taken back | ★ |
| Train | MLflow / W&B / TensorBoard | Track experiments and store model versions | ◐ |
| Evaluate | scikit-learn metrics | Accuracy, precision, recall | ◐ |
| Evaluate | SHAP / LIME / Fairlearn | Explain decisions, check fairness | ○ |
| Deploy | **FastAPI** | Python framework to put a model behind an API | ★ |
| Deploy | **vLLM** | The serving engine for large language models | ★★ |
| Deploy | TorchServe / TF Serving | Older servers for classic models | ○ |
| Deploy | **Load balancer / API gateway** | Spread traffic; handle keys and rate limits | ★ |
| Monitor | **Prometheus + Grafana** | Collect numbers + show dashboards and alerts | ★ |
| Monitor | ELK / Jaeger | Search logs / trace a request across services | ◐ |
| Retrain | **CI/CD** (GitHub Actions, Jenkins) | Automatic test and deploy | ★ |
| Optimize | **Quantization** | Shrink a model so it's smaller and faster | ★ |

---

## From this lab to a real company

| This lab | Real enterprise version |
|---|---|
| A list of messages in code | Data lake on S3 + Airflow pipelines |
| `python train.py` on a laptop | Training jobs on GPU clusters, tracked in MLflow |
| `models/` folder | Model registry (MLflow, S3) |
| `if accuracy < 0.8: block` | Automated evaluation gate in CI/CD |
| `uvicorn serve:app` | vLLM / model server in Kubernetes behind a load balancer |
| `/metrics` page | Prometheus scraping + Grafana dashboards + alerts |
| Ctrl+C and restart with a new version | Canary rollout through ArgoCD |
| Renaming a bad model file | One-click rollback to the previous version |

**One correction to the course material:** the lesson lists a 7B LLM as needing "28 GB+." That's for **training**. To **serve** it: ~14 GB at FP16, or ~4–5 GB at 4-bit.

---

## Self-check

1. What are the six stages of the ML lifecycle?
2. Why should every model version be saved?
3. What's the difference between a system metric and a model metric?
4. Blue-green vs. canary vs. shadow: what's the difference?
5. What is data drift, and why does it matter?
6. Why did version 2 deploy "healthy" but still answer wrong?

<details>
<summary>Answers</summary>

1. Data → Train → Evaluate → Deploy → Monitor → Retrain (and loop).
2. To know exactly what's live, compare versions, and roll back when a new one is worse.
3. System = is the server healthy (speed, errors). Model = are the answers good (predictions, accuracy).
4. Blue-green switches everyone at once. Canary releases to a small group first. Shadow runs the new model silently without users seeing its answers.
5. Real-world input changes away from the training data, so the model slowly gets worse.
6. Server health doesn't measure answer quality. The model had too little data, and the test set was too small to catch the problem.

</details>

---

*Part of my [AI Infrastructure learning log](../../../README.md). Course material from the [AI Infrastructure Engineer curriculum](https://github.com/ai-infra-curriculum/ai-infra-engineer-learning) (MIT license).*