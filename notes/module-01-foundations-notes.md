# Module 1 — AI Infra Learning Notes (Foundations)

**AI INFRA LEARNING NOTES**

**Explained Simply, From Zero**

Module 1, Lesson 1: What Is ML Infrastructure?

*No background needed. Every idea starts with a daily-life story.
Read it once, slowly — it is written so you do not have to read it again and again.*

# How to read this document — read once, remember it

This book assumes you know nothing about AI. Truly nothing. If a hard word appears, it is explained in simple words the moment it appears, with an example from daily life — a restaurant, a school, a hospital, a shop.

Each section follows the same pattern, and the pattern is what makes it stick:

```
1. A small story from daily life.
2. The real idea, in simple words.
3. The one line to carry in your head, marked as “One line to remember.”
```

At the end you get three gifts: a one-page cheat sheet (the whole lesson on one page), a word dictionary (every hard word in one simple line), and interview questions where every answer is written twice — first how to understand it, then the exact simple words you can say in an interview.

```
Golden rule: Do not memorise definitions. Remember the stories. In an interview, if you forget the definition, tell the story in your own words — that answer scores better than a memorised line anyway.
```

# Part 0 — Start from absolute zero: 6 basics

Forget AI for two minutes. Learn these 6 simple ideas first. Everything in this whole course is built from only these 6.

## Basic 1: A normal computer program follows fixed rules

A normal program is like a recipe card. “If the water boils, add pasta. Wait 10 minutes.” The computer does exactly what the card says, nothing more, nothing less. A calculator, a billing app, a website login page — all are recipe cards. If a situation is not written on the card, the program cannot handle it.

```
One line to remember: A normal program = fixed rules written by a human.
```

## Basic 2: Data is just information

Data means information in any form — photos, names, prices, voice recordings, a list of what you bought last month. Your phone gallery is data. Your bank statement is data. That is all the word means. Whenever you see the word “data” in this book, read it as “information.”

```
One line to remember: Data = information. Nothing more scary than that.
```

## Basic 3: AI learns the rules by itself, from examples

Now the big difference. Writing rules for “is this photo a cat?” is almost impossible — cats look different in every photo. So instead of writing rules, we show the computer lakhs of photos and say: “These are cats. These are dogs. You find the pattern.” Slowly, the computer finds the pattern by itself. A program that learns patterns from examples, instead of following hand-written rules, is what people call Artificial Intelligence (AI), and more exactly, Machine Learning (ML) — “machine learning” simply means “the machine learns.”

```
One line to remember: Normal program: human writes the rules. AI program: machine learns the rules from examples.
```

## Basic 4: A “model” is the trained brain — saved as a file

When the machine finishes learning, what it learned is saved as one big file. That file is called a model. Think of it like a student after studying: the knowledge is now inside the student’s head. The model is that “head” — a file that carries the knowledge. A famous model you have heard of is the one inside ChatGPT. Small models are the size of a movie file. Big ones are bigger than 100 movies together.

```
One line to remember: Model = the learned knowledge, saved as a file. Like a trained brain in a box.
```

## Basic 5: Training is studying. Inference is answering in the exam

These are the two most important words in this whole field, so learn them as a student story. Training is the study time: the machine looks at example after example and slowly learns — this takes hours or days and needs very powerful computers. Inference is the exam hall: a real user asks a real question, and the trained model gives an answer in a second or two. Studying happens once in a while. Answering happens millions of times a day.

When you type a question into ChatGPT, that is inference. Somewhere, a model that was trained long ago is answering you, live.

```
One line to remember: Training = studying (slow, once in a while). Inference = answering live questions (fast, all day).
```

## Basic 6: A GPU is a very fast worker for this kind of maths

Your normal computer chip (a CPU) is like one brilliant worker who does one job at a time, very cleverly. Learning and answering for AI needs crores of tiny, simple maths steps done at the same time. For that, we use a different chip called a GPU — think of it as ten thousand simple workers doing tiny jobs together. GPUs were first made for video games (smooth graphics need the same kind of maths), and AI simply borrowed them. They are powerful — and expensive. Remember the expense; it comes back again and again in this lesson.

```
One line to remember: CPU = one brilliant worker. GPU = ten thousand workers together. AI needs the crowd — and the crowd costs money.
```

That is all of Part 0. You now know: programs, data, AI, model, training, inference, GPU. Hold these 7 words and Lesson 1 becomes easy.

# Lesson 1 — What is ML infrastructure?

## 1. The restaurant story — the whole lesson in one story

Imagine a world-famous chef. She cooks one magical dish. But a chef alone is not a restaurant. For people to actually eat her food, you also need: a kitchen with working stoves, people who bring fresh vegetables every morning, waiters who take orders and serve fast, someone watching that the food quality never drops, and a manager who fixes things the moment something breaks. Without all of that, the chef’s talent feeds nobody.

Now replace the words. The chef is the model — the trained brain. The restaurant is ML infrastructure — everything around the model that lets real people use it, every day, without failure. ML infrastructure means: the computers (with GPUs) the model runs on, the system that brings it fresh data, the service that takes a user’s question and returns the model’s answer in seconds, the watchman-system that checks the answers are still good, and the safe method to replace an old model with a better new one without shutting down.

A data scientist’s model sitting in a file is like the chef sitting at home. Talented — and feeding nobody. Infrastructure is what turns talent into a business.

```
One line to remember: Model = chef. ML infrastructure = the whole restaurant around the chef.
```

## A small real example — cat or dog?

A company trains a model that looks at a photo and says “cat” or “dog.” Training is done. Now, to make it a real product in a phone app, someone must build all of this — and that someone is the ML infrastructure engineer:

- a live service: the phone sends a photo, the answer comes back in under a second;

- strong computers with GPUs, so thousands of people can use it at the same time;

- a flow that keeps bringing new photos, so the model can study again and improve;

- a watchman that notices if answers start going wrong;

- a safe switch to a new, better model — without the app ever going down.

Remove any one piece and there is no product. There is only a science experiment.

## 2. Three people, three jobs — who does what

In the restaurant, three different people matter. Mixing up their jobs is the most common confusion for beginners, so fix it now:

| **Person** | **In the restaurant** | **In the AI world — real job** |
| --- | --- | --- |
| Data Scientist | The chef who invents the dish | Experiments with data and teaches the model. Job ends with: “Here is a trained model that works in my tests.” |
| ML Engineer | The chef who makes the dish cookable in a real kitchen | Cleans up the model’s code so it is neat, tested, and ready to run in the real world. |
| ML Infrastructure Engineer — THIS IS YOU | The person who builds and runs the whole restaurant | Builds and runs everything around the model — the computers, the serving system, the watching system — so millions can use it daily. |

In a small company, one person may do all three jobs. In a big company they are separate, because the restaurant side alone is a full-time job. Notice something important: the infrastructure job uses the same daily skills as a DevOps or SRE job — servers, cloud, automation, watching systems. Only the “dish” is new.

```
One line to remember: Scientist invents it. ML engineer polishes it. You run it for the whole world.
```

## 3. Your 7 jobs — said in the simplest possible words

```
1. Serve it: Put the model live. Take the trained file and place it on real computers, open to real users, who can ask it questions through the internet. (The technical word for users asking and the model answering is “serving.”)
2. Bring the data: Build the roads that carry information to the model — both old information for studying, and live information for answering. These automated roads are called data pipelines; a pipeline is simply a fixed, automatic path that data travels on.
3. Watch everything: Keep an eye on two things at once: is the system alive and fast — and are the answers still correct? Normal IT only watches the first. You watch both.
4. Save money and time: GPUs cost a lot. Arrange things so the same work finishes faster and cheaper — right computer size, no idle machines, no waste.
5. Automate the steps: Studying, testing, and launching a model should happen by pressing a button, not by a human doing 40 careful steps by hand. You build that button-system.
6. Arrange the computers: Decide which computers and GPUs do which work, and share them fairly between teams — like a manager allotting tables in a busy restaurant.
7. Talk to everyone: The scientists speak “accuracy and experiments.” The business speaks “money and deadlines.” You stand in the middle and translate, both ways.
One line to remember: Six jobs are technical. The seventh — talking and translating — is the one that makes the other six useful.
```

## 4. Why this work is hard — 5 problems, 5 small stories

Problem 1 — The world changes, so the model becomes outdated.

A student studied only 2019 questions. In the 2026 exam, the topics have changed — the student’s answers slowly become wrong, even though the student did nothing wrong. A model is the same. It learned from old data. The world moves — new products, new words, new fraud tricks — and the model’s answers quietly get worse. So models must study again and again (this is called retraining), and every version must be kept safely, like old exam papers, so you can go back if a new version is worse.

Problem 2 — Bad data fails silently.

If a program’s code breaks, it crashes loudly — everyone sees. But if the data going into a model becomes bad — say, a shop’s prices start arriving in the wrong format — nothing crashes. The model simply starts learning and answering wrongly, quietly. That is why we must check data quality and always know exactly which data created which model. That record is called data lineage — in simple words, “which ingredients made this dish.”

Problem 3 — The computers are very expensive.

Training a big model can keep many GPUs busy for days. Serving one can need GPUs running day and night. One careless choice — a machine too big, left running idle — is not a small mistake. It is a very large electricity-style bill at the end of the month.

Problem 4 — The crowd is huge.

A hit product may need lakhs of answers every second, each answer in a fraction of a second. One waiter cannot serve a stadium. The system must grow and shrink with the crowd, automatically.

Problem 5 — The most dangerous failure makes no sound.

A normal website either opens or it does not — failure is visible. A model can be fully “up”, fast, no errors — and still be giving worse and worse answers, because the world drifted away from what it studied. This slow, silent spoiling is called model drift, or model degradation. Catching it needs a watchman that checks answer quality, not just server health.

```
One line to remember: In normal IT, green lights mean “all good.” In ML, green lights can hide a model that is quietly going wrong. Always ask: are the answers still good?
```

## 5. The normal IT job vs this job — same base, three extra things

If you already know DevOps, good news: you are not starting a new career. You are adding three extra things to a career you already have. This table is the whole difference:

| **Normal IT / DevOps job** | **ML infrastructure job (this course)** |
| --- | --- |
| You launch apps that stay the same until a human changes them | You launch models that slowly get outdated on their own |
| You mainly check: is it up? is it fast? | You also check: are the answers still correct and fair? |
| You keep versions of code only | You keep versions of code + data + models — all three |
| More users = more servers | More users = more servers, AND huge training work to look after |
| You watch CPU, memory, errors | You watch all that, PLUS answer quality and drift |

```
One line to remember: ML infrastructure = DevOps + data versions + model versions + answer-quality watching + GPU computers.
```

## 6. The life of a model — a circle, not a line

A model’s life goes around in a circle, forever. Walk the circle once, slowly:

```
1. Step 1 — DATA: Collect information — photos, records, text — the raw material. Clean it and check it; a mistake caught here costs almost nothing, the same mistake found later costs a fortune. Save each version with a name or number, so you always know which data is which.
2. Step 2 — TRAINING (studying): The model studies the data. Scientists try many ways of teaching and note down what they tried. Then the model is tested on data it has never seen — like a practice exam — to check how it will do in real life. Models that pass are stored safely in a model registry — in simple words, a proper cupboard where every model version sits with its name, its exam marks, and a label: “testing”, “live”, or “old/retired.”
3. Step 3 — LIVE (serving + watching): The approved model goes live. Users ask, the model answers (inference). And now the watchman starts: is it fast? is it up? — and are the answers still good?
4. Step 4 — FEEDBACK (the circle closes): The watchman reports what real life looks like. If answers are slipping — because the world changed — the model goes back to Step 1 and studies fresh data again. Then the circle repeats. There is no finish line, and that is normal.
One line to remember: Training is not the end of the story. It is roughly the middle. Most of a model’s life — and most of its cost and risk — is in living, being watched, and studying again.
```

## 7. MLOps — the idea with the scary name

You will hear the word MLOps everywhere. It is only this: a fixed, repeatable system for running the circle in Section 6, so nothing depends on one person’s memory or luck. ML + Operations — running machine learning properly, as a daily operation, the same way every time.

Why does it need a system? Because three things change at three different speeds. Code changes when a developer changes it. Data changes every minute. Models change every time they study again. If nobody coordinates those three, they keep breaking each other. MLOps is the coordination.

MLOps stands on 3 legs — if any one leg is missing, the stool falls:

- **People — **the scientists, the engineers, and you must actually work together, with clear hand-overs — not throw work over a wall.

- **Process — **the same steps, in the same order, every time — studying, testing, launching — like a pilot’s checklist, so results can be repeated and checked.

- **Platform — **the automatic systems that carry the steps — the pipelines, the model cupboard, the serving system, the watchman. Tools live here.

```
One line to remember: Buying tools gives you only the third leg. Tools alone are not MLOps. People + Process + Platform — all three, or it falls.
```

## 8. Three real stories — why big companies care

Notice the pattern in all three stories: none of them is “they built a smarter model.” Every one is “their restaurant was better run.” (Stories and figures are as given in the lesson.)

- **Netflix — **over 200 million users ask “what should I watch?” and the answer must come in under a tenth of a second. Answer: many copies of the model serving in parallel, plus smart caching — remembering common answers instead of cooking them fresh every time.

- **Uber — **prices, arrival times, and driver matching must happen live, in cities across the whole world, at the same moment. Answer: Uber built its own full platform, called Michelangelo, that handles studying, launching, and watching all models in one place.

- **OpenAI / ChatGPT — **models with billions of “connections” inside, answering people across the whole planet. Answer: fully custom infrastructure for serving, heavily optimised, with cost watched like a hawk — because at that size, serving can cost crores every month.

Good infrastructure gives a business four things: speed (models reach users sooner), reliability (quality is caught before users suffer), scale (the crowd can grow without the system falling), and savings (expensive GPUs are not wasted).

## 9. The tools map — do not panic, learn families first

This lesson names many tools. Do not try to learn them all now — nobody does. Learn what family each tool belongs to, the way you learn “this shop sells medicines” before learning every medicine’s name.

| **Family — what job it does** | **Tools you will meet** |
| --- | --- |
| Running apps at scale | Docker (packing an app in a box), Kubernetes (running lakhs of boxes), Terraform (writing down your cloud setup as code), Helm |
| Teaching and running models | PyTorch, TensorFlow, Hugging Face |
| Managing the ML circle | MLflow (experiment notes + model cupboard), Airflow (scheduling pipelines), DVC (versions for data), Kubeflow (ML on Kubernetes) |
| Renting computers (cloud) | AWS, Google Cloud, Azure — each also sells ready-made ML services |
| Watching systems | Prometheus, Grafana (graphs and alerts — same as normal IT) |
| Serving models live | vLLM (the popular one for big language models), TensorFlow Serving, TorchServe, FastAPI |
| GPU and big training | CUDA (talking to GPUs), Ray (spreading work across many machines) |

If you come from DevOps, the first, fourth, and fifth families are already your home. The truly new families are: ML frameworks, the ML-circle tools, serving for big language models, and GPU computing.

## 10. Where this field is going, and the job ladder

Five directions, in simple words (as stated in the lesson — directions to trust, exact numbers are the lesson’s own):

```
1. LLM infrastructure is the hot skill: Serving big language models (LLMs — models like the one inside ChatGPT) is becoming the most wanted skill. It needs special serving tools, and something called RAG: instead of the model answering only from its study-memory, we first search your company’s documents and hand the right pages to the model, so it answers from facts. The documents are stored in a special “similarity-finding” store called a vector database.
2. Many clouds, not one: Companies rent computers from 2–3 cloud companies instead of one, to avoid being trapped and to pick the cheapest place for each job.
3. Cost and “Green AI”: Watching the GPU bill like a household budget (this practice is called FinOps), and preferring smaller models when they answer just as well — cheaper and greener.
4. Fair and safe AI: Infrastructure must also help check that models treat people fairly, explain their answers, and protect private data — laws now demand it.
5. One platform for the whole company: Instead of every team struggling with scattered tools, companies build one internal platform — one simple “restaurant counter” where scientists help themselves, and the rules are followed automatically.
```

The job ladder, by what you actually do (salary ranges below are the US ranges printed in the lesson itself — a snapshot from the lesson, not a promise):

| **Level** | **What you really do** | **Salary in the lesson** |
| --- | --- | --- |
| AI Infrastructure Engineer | Run systems others designed; launch models; watch them | $107k–$230k |
| Senior AI Infra Engineer | Design the systems; make them faster and cheaper; guide juniors | $150k–$280k |
| AI Infrastructure Architect | Decide the whole company’s ML platform and standards | $165k–$350k |
| Senior Architect (executive) | Connect those decisions to the company’s big strategy | $200k–$500k+ |

Read the ladder by freedom, not title: first you run systems → then you design systems → then you decide which systems the company should even have.

```
Remember: The lesson reports these roles grew over 400% in three years, with the biggest shortage at senior levels and for LLM skills. Direction: demand is highest exactly where this course is heading.
```

# 11. One-page cheat sheet — the whole lesson on one page

If you read nothing else before an interview, read only this page, slowly, twice.

- **Model: **A model is a trained brain saved as a file. Alone, it does nothing.

- **ML infrastructure: **Everything around the model that lets real people use it daily — computers, serving, data flow, watching, safe upgrades. You are the restaurant builder; the scientist is the chef.

- **Training vs inference: **Studying = training (slow, now and then). Answering live = inference (fast, all day).

- **GPU: **One brilliant worker (CPU) vs ten thousand workers together (GPU). AI needs the crowd; the crowd is expensive.

- **Your 7 jobs: **Put it live. Bring data. Watch system AND answers. Save money. Automate. Arrange computers. Talk to everyone.

- **5 hard problems: **Models get outdated (world changes). Bad data fails silently. GPUs are costly. Crowds are huge. Failures hide — a model can be up, fast, and wrong.

- **Vs normal IT: **DevOps + data versions + model versions + answer-quality watching + GPUs.

- **The circle of life: **Data → Training → Live → Watch → study again. A circle, forever.

- **MLOps: **A repeatable system for that circle. Three legs: People, Process, Platform. Tools alone are not MLOps.

- **Netflix trick: **Serve common answers from memory (caching) + many parallel copies of the model.

- **Uber trick (Michelangelo): **One platform for studying, launching, and watching all models.

- **ChatGPT trick: **Custom, heavily optimised serving + watching cost like a hawk.

- **Hottest skill now: **LLM serving with vLLM, and RAG — search documents first, then let the model answer from facts.

# 12. Word dictionary — every hard word, one simple line

| **Word** | **Simple meaning + example** |
| --- | --- |
| Data | Information of any kind — photos, prices, records. |
| Model | The learned knowledge, saved as a file. “The trained brain.” |
| Training | The model studying examples and learning. Like exam preparation. |
| Inference | The trained model answering a real question, live. Like writing the exam. |
| Serving | Running a model live so users can ask it questions. |
| Data pipeline | An automatic road that carries data from one place to another. |
| Model registry | A cupboard of model versions, each with its marks and a label: testing / live / retired. |
| Data lineage | The record of which data created which model. “Which ingredients made this dish.” |
| Model drift / degradation | Answers slowly getting worse because the world changed after the model studied. |
| Retraining | Making the model study again, with fresh data. |
| MLOps | A fixed, repeatable system (People + Process + Platform) for running models properly. |
| GPU | A chip with thousands of small workers — needed for AI maths; expensive. |
| LLM | Large Language Model — a very big model trained on text, like the one inside ChatGPT. |
| RAG | Search the documents first, then let the model answer using those facts. |
| Vector database | A store that finds “similar meaning” items fast; RAG uses it to find the right pages. |
| A/B testing | Show the new model to some users, old model to others, compare honestly, then decide. |
| Caching | Remembering a common answer instead of cooking it fresh every time. |
| FinOps | Watching and controlling the cloud bill as a daily habit. |

# 13. Interview questions and answers — understand simply, answer confidently

Every answer is given twice. First, how to understand it — in story words. Second, the exact simple sentence you can say in the interview. Say it in your own style; do not memorise word by word.

**Q1. What does an ML infrastructure engineer actually do?**

**Understand it like this: **You run the restaurant around the chef. The scientist builds the model; you make sure the whole world can use it, every day, without it breaking or costing a fortune.

**Say this in the interview: ***"I build and run the systems that take a trained model to real users and keep it healthy there — deployment and serving, data pipelines, monitoring for both system health and answer quality, cost optimisation, automation, and GPU management, working closely with data scientists."*

**Q2. How is launching a model different from launching a normal app?**

**Understand it like this: **A normal launch sends one thing: code. A model launch sends three things that change at different times: code, data, and the model itself. So you must keep versions of all three, and keep checking answer quality after launch.

**Say this in the interview: ***"A normal deployment ships code. A model deployment ships code, data, and the model — three things changing independently. So I need versioning and rollback for all three, plus model-quality monitoring and a retraining path after release."*

**Q3. The model is doing worse in real life than in testing, but all dashboards are green. What is happening?**

**Understand it like this: **This is the silent failure. The restaurant is open, tables are full, no fire — but the food quality is slowly dropping and nobody tasted it. In AI words: the world changed (drift), so answers decayed while servers stayed healthy.

**Say this in the interview: ***"That pattern points to model drift, not a system failure — production data has moved away from the training data. I would compare live input data and quality metrics against the training baseline, check the data pipeline for changes, and if drift is confirmed, retrain on fresher data, validate, and redeploy."*

**Q4. Why is GPU cost such a big topic in this field?**

**Understand it like this: **Because the crowd of workers is rented by the hour. Leaving ten thousand workers sitting idle, or hiring a bigger crowd than needed, burns money every single hour.

**Say this in the interview: ***"Compute is the biggest cost in ML systems. Training can hold many GPUs for days and serving needs GPUs around the clock, so instance choice, utilisation, and efficiency directly decide whether the system is affordable. I treat cost as a design constraint, not an afterthought."*

**Q5. What is a model registry, and why do we need one?**

**Understand it like this: **It is the cupboard. Without it, model files lie everywhere with sticky notes, nobody knows which one is live, and going back to yesterday’s good version is a panic job.

**Say this in the interview: ***"Many versions exist at once — experiments, a staging candidate, the live model, and older versions kept for rollback. A registry like MLflow stores each version with its training data, metrics, and status, so any behaviour can be traced to an exact model and dataset, and rollback is safe and instant."*

**Q6. What is MLOps, in simple words?**

**Understand it like this: **It is the pilot’s checklist for the whole model circle — the same steps, in the same order, every time, carried by people working together and a platform that makes it automatic.

**Say this in the interview: ***"MLOps is the set of practices combining machine learning, DevOps, and data engineering to deploy and maintain ML systems reliably. It automates the full lifecycle — data, training, deployment, monitoring, retraining — and it stands on three pillars: People, Process, and Platform."*

**Q7. Walk me through the life of a model.**

**Understand it like this: **Tell the circle story: ingredients → studying → exam → go live → watchman → world changes → study again.

**Say this in the interview: ***"Data first: collection, cleaning, and versioning. Then training: experiments, validation on unseen data, and storing the approved model in a registry. Then deployment: go live, serve predictions, and monitor. Monitoring feeds back — when quality drops, we retrain on fresh data and the loop repeats. It is a loop, not a one-way pipeline."*

**Q8. When should a model be retrained?**

**Understand it like this: **When the watchman proves the answers are slipping — not just because a month passed. You send the student back to study when the world’s questions have changed, and you check the new version beats the old one before swapping.

**Say this in the interview: ***"When monitoring shows measured quality loss — usually from data drift — or when clearly better data or methods arrive. The trigger should be evidence, not the calendar alone, and the new model must be validated and compared against the current production model before release."*

**Q9. How do you launch a new model version safely?**

**Understand it like this: **Like changing a restaurant’s recipe: first taste it in the kitchen, then serve it to a few tables, watch their faces, and only then change the full menu. Keep yesterday’s recipe ready in hand.

**Say this in the interview: ***"Validate it offline first, then release gradually — A/B testing or a small canary share of live traffic — comparing quality and speed against the current version. If it wins, shift traffic fully; if it regresses, roll back instantly to the registered previous version."*

**Q10. How is watching an ML system different from watching a website?**

**Understand it like this: **For a website you check: is the shop open, is the queue moving? For ML you add one more check: is the food still tasty? That extra check exists because ML’s worst failure is silent.

**Say this in the interview: ***"A website is monitored for availability, latency, errors, and resource use. An ML system needs all of that plus model metrics — answer quality, data drift, and fairness — and data-quality checks on inputs, because the most dangerous ML failure is silent: correct-looking answers with decaying quality."*

**Q11. A product needs a million answers per second, very fast. What do you think about first?**

**Understand it like this: **A stadium crowd. One waiter is hopeless — you need many counters, pre-made popular items ready (caching), and the ability to open more counters the moment the crowd grows. And every extra counter costs GPU money.

**Say this in the interview: ***"Serving architecture and scale first: distributed serving with many model copies, caching of frequent predictions, efficient batching, and autoscaling GPU capacity — plus the cost of holding that capacity. I would also pin down the per-request latency budget, because it decides how much of the design is caching and placement versus raw compute."*

**Q12. Give a real example of ML infrastructure at big scale.**

**Understand it like this: **Use the Netflix or Uber story from Section 8. Stories are easy to remember and interviewers enjoy them more than definitions.

**Say this in the interview: ***"Netflix serves recommendations to over 200 million users in under 100 milliseconds using distributed model serving and advanced caching. Uber built its Michelangelo platform to handle training, deployment, and monitoring for real-time pricing and matching worldwide. In both cases, the infrastructure platform was the differentiator, not a single model."*

**Q13. What is an LLM, and why is it hard to serve?**

**Understand it like this: **An LLM is a giant text-brain — billions of internal connections — so the file is enormous and needs a crowd of GPU workers just to answer one question. Serving it is like running a restaurant where every single order needs the full kitchen.

**Say this in the interview: ***"An LLM is a model with billions of parameters, so it is very large in memory and expensive to run. Serving it needs GPU infrastructure, inference optimisation tools like vLLM or TensorRT-LLM, and strict cost management. RAG is often added — retrieving company documents at question time — so the model answers from facts instead of needing retraining for every new fact."*

**Q14. What are the three pillars of MLOps?**

**Understand it like this: **People, Process, Platform. If the interviewer asks “can we just buy tools?” — smile: tools are only one leg of a three-legged stool.

**Say this in the interview: ***"People — collaboration between data scientists, ML engineers, and infrastructure teams. Process — standardised, repeatable workflows for experiments, testing, and deployment. Platform — the automated tools that carry the lifecycle. Buying tools covers only the platform leg, which is why tool purchases alone never create MLOps."*

**Q15. Why should a DevOps or SRE engineer move into ML infrastructure?**

**Understand it like this: **Because you are not changing your house — you are adding one floor to it. Your old skills carry you most of the way; the new floor is small, specific, and exactly where the shortage is.

**Say this in the interview: ***"Most of the foundation transfers directly — containers, Kubernetes, cloud, infrastructure as code, CI/CD, and observability. The new layer is specific and learnable: data and model versioning, model-quality monitoring, the ML lifecycle, and GPU compute. That hybrid profile is where demand and shortages are strongest, especially for LLM infrastructure."*

# 14. Quick self-test — say the answers out loud

Do not write. Speak. If you can say each answer out loud in your own words, Lesson 1 is finished and you never need to re-read the lesson — only the cheat sheet in Section 11.

```
1. What is ML infrastructure? (Hint: the restaurant.)
2. What are the three main stages of a model’s life? (Hint: data, studying, going live — then the circle.)
3. What is MLOps, and why does it matter? (Hint: the checklist and the three legs.)
4. Name any three hard problems in this field. (Hint: old models, silent bad data, costly GPUs, huge crowds, hidden failures — pick three.)
5. Name some tools from the map. (Hint: pick one from each family — Docker/Kubernetes, MLflow, Prometheus/Grafana, vLLM.)
6. What jobs exist in this field? (Hint: run systems → design systems → decide systems.)
```

# 15. What is next

Lesson 2 is Environment Setup — getting your computer ready with Python, Git, Docker, and cloud tools, and checking each one works. Even if you already have these tools, do the checking part: a missing tool here becomes a confusing error five lessons later.

- **Done: **Module 1, Lesson 1 — Introduction to ML Infrastructure: understood from zero, in simple words, interview-ready.

- **Next: **Module 1, Lesson 2 — Environment Setup.

*Source for this chapter: Lesson 01, “Introduction to ML Infrastructure,” and the Module 01 overview in the ai-infra-engineer-learning curriculum — https://github.com/ai-infra-curriculum/ai-infra-engineer-learning*

**MODULE 1 — CONTINUED**

**Lessons 2 to 6, and Docker in Depth**

The chapters below continue exactly where Lesson 1 ended. Same rule as before: story first, technical word second, and a “One line to remember” at the end of every idea. Your focus rule applies throughout: deployment only. You do not write models and you do not do development work. Every coding or hands-on step is flagged, and every deployment practice is called out the moment it appears.

# Lesson 2 — Environment Setup: your toolbox, checked and ready

Before a chef cooks, the kitchen must exist: stove, knives, gas, water. Lesson 2 is that check for this course — the tools on your computer, and proof that each one works. In your case this lesson was short, and honestly so: you confirmed every tool was already installed from your DevOps work, so the install walkthrough was skipped. What matters is knowing what each tool is for, and the one command that proves it works.

| **Tool** | **What it is for, in simple words** | **Proof it works** |
| --- | --- | --- |
| Python 3.11 | The language almost all ML tools are written in. Your serving apps will run on it. | python3 --version |
| Virtual environment (venv) | A private box for one project's Python libraries, so two projects never fight over versions. | python3 -m venv venv, then activate it |
| Git + GitHub | Version control for code — every change saved, nothing lost, work shared with a team. | git --version |
| Docker | Packs an app with everything it needs into one box that runs the same anywhere. Full chapter at the end of this document. | docker --version and docker run hello-world |
| kubectl, minikube, Helm | Kubernetes tools: kubectl gives orders, minikube runs a small Kubernetes on your laptop, Helm installs ready-made packages. | kubectl version --client |
| Cloud CLIs (aws, gcloud, az) | Talk to AWS, Google Cloud, and Azure from the terminal instead of clicking in a browser. | aws --version |
| VS Code | The editor where code and configuration files are written and fixed. | code --version |

Why the check matters: a missing tool here does not fail loudly today. It fails five lessons later, in the middle of something else, with a confusing error that has nothing to do with what you were learning. Ten minutes of checking now saves an hour of confusion later.

```
Deployment practice — flagged: No deployment practice in this lesson for you — the toolbox was already installed and verified on 2026-11-11. Nothing is parked from Lesson 2.
One line to remember: Check the toolbox before you cook — a missing tool fails later, in the middle of something else.
```

## Interview questions — Lesson 2

**Q1. Why use a virtual environment for every Python project?**

**Understand it like this: **Two restaurants sharing one spice shelf. One changes the salt, the other's food breaks. A venv gives each project its own shelf.

**Say this in the interview: ***"A virtual environment isolates each project's dependencies and versions, so projects cannot break each other and any environment can be recreated exactly from its requirements file."*

**Q2. How do you prove a fresh machine is ready for ML infrastructure work?**

**Understand it like this: **Do not trust that a tool is installed — run its version command and one tiny real task, like docker run hello-world.

**Say this in the interview: ***"I verify each tool with its version command and one smoke test: Python and pip inside a venv, git configured, Docker running a hello-world container, kubectl reaching a cluster, and the cloud CLI authenticated. Installation without a smoke test is an assumption, not a setup."*

# Lesson 3 — ML Infrastructure Basics: the model's life in six stages

Lesson 1 gave you a circle: data, training, serving, feedback. This lesson zooms into that circle and splits it into six stages, so you can see what infrastructure each stage needs. Same restaurant, now walking through it room by room.

```
1. Stage 1. Data — gather and clean the ingredients.
2. Stage 2. Training — teach the chef.
3. Stage 3. Evaluation — taste before serving.
4. Stage 4. Deployment — put it on the menu.
5. Stage 5. Monitoring — watch the kitchen and the food.
6. Stage 6. Retraining — teach again when the food gets worse. Then back to Stage 1, forever.
```

## Stage 1 — Data: gather and clean the ingredients

Raw data arrives from everywhere: databases, APIs, sensors, logs, user activity. Before anyone can teach with it, it must be collected, cleaned, checked, and labelled. Labelling means marking examples with the right answer — a tag on each photo saying “cat” or “dog” — so the model can learn from it. Every version of the data is saved, so any model can be traced back to the exact data that created it.

The infrastructure: object storage (S3-style warehouses) for the raw and cleaned data, pipelines that move and clean it on a schedule (Airflow is the common scheduler), and data-quality checks that refuse bad ingredients before they reach the kitchen.

```
One line to remember: No model is better than its ingredients — and bad ingredients fail silently.
```

## Stage 2 — Training: teach the chef

The model studies the prepared examples. This is the compute-heavy stage: GPU clusters, often for hours or days. Two ideas for scale: data parallelism splits the data across many machines (many ovens, same recipe), and model parallelism splits the model itself across machines when it is too big for one oven.

The infrastructure: GPU machines that can be rented and released on demand, experiment tracking (MLflow records every study session — which data, which settings, what score), and checkpoints — saved progress points, so a crashed or interrupted training run resumes instead of starting over.

```
One line to remember: Training is studying: slow, expensive, and done once in a while — with every session recorded.
```

## Stage 3 — Evaluation: taste before serving

A model that scores well on the data it studied proves nothing — it may have memorised the answers. So it is tested on data it has never seen. That unseen-data test is the real exam.

| **Job type** | **Scores that matter** | **In simple words** |
| --- | --- | --- |
| Sorting into groups (spam or not, cat or dog) | Accuracy, Precision, Recall, F1, Confusion matrix | Accuracy: how often right overall. Precision: when it says spam, how often is it really spam? Recall: of all real spam, how much did it catch? F1: one number balancing precision and recall. Confusion matrix: a four-box table showing exactly where it goes wrong. |
| Guessing a number (price, delivery time) | MAE, MSE, RMSE | Three ways of measuring how far off the guesses are, on average. RMSE punishes big misses the hardest. |
| Ranking (recommendations, search) | Ranking quality scores | Did the best items land at the top of the list, where people actually look? |

Your job at this stage is not choosing the score — that is the data scientist's call. Your job is that the exam is fair and repeatable: same unseen test data, same scoring code, every time, with the result recorded next to the model version.

```
One line to remember: Never serve food nobody tasted — and taste it on dishes the chef has never seen.
```

## Stage 4 — Deployment: put it on the menu

The tasted, approved model goes live. Deployment means packaging the model so it can serve answers — usually inside a container, behind an API — registering it in a model registry (the menu book: every version, its score, and whether it is approved, staging, or live), and releasing it with a strategy that can be undone. The three strategies are covered fully in Lesson 6: blue-green, canary, and shadow.

```
Deployment practice — flagged: Deployment is your stage. Packaging, registry, release strategy, and rollback are infrastructure work — no model writing involved.
One line to remember: A deployment you cannot undo is not a deployment — it is a gamble.
```

## Stage 5 — Monitoring: watch the kitchen AND the food

A normal app needs one kind of watching: is the server up, fast, and error-free? A model needs two kinds, and this is the single most repeated idea in the whole course.

- **The kitchen — system metrics. **Request rate (orders per second), latency, error rate, CPU/GPU, memory. Latency is read as p50, p95, p99: p50 is the middle customer — half waited less; p95 means 95 of 100 waited less; p99 is the worst 1 in 100. Averages hide suffering; p99 shows it.

- **The food — model metrics. **Prediction distribution (are the answers shifting — “yes” was 30% of answers, now 70%?), confidence (how sure the model sounds), and drift (live inputs or answers moving away from what training expected).

Tooling: Prometheus collects the numbers, Grafana draws the dashboards, and alerts fire when either dashboard turns bad — including when every server light is green but the answers are decaying.

```
One line to remember: Green server lights can hide a model that is quietly going wrong. Watch the answers, not just the machines.
```

## Stage 6 — Retraining: teach again when the food gets worse

Monitoring tells you when the model has gone stale. Retraining teaches it again on fresher data. Triggers come in three kinds: on a schedule (weekly, monthly), on drift (the watchman sees answers decaying), and on new data (a new product line, a new market). The new model still passes through evaluation and a safe deployment — retraining never skips the tasting.

```
One line to remember: The circle never ends: watch, retrain, taste, deploy — forever.
```

## Five hard problems, and the standard fixes

| **Problem** | **Why it is hard** | **Standard fixes** |
| --- | --- | --- |
| Too much data, arriving too fast | Data never stops growing, and daily batches arrive too late for live decisions | Distributed storage (S3, HDFS), stream processing (Kafka, Flink) for data as it arrives, efficient formats (Parquet, ORC) |
| Training needs enormous compute | One model can need many GPUs for days | GPU clusters, distributed training, cloud elasticity, spot instances for cheap spare capacity |
| Versioning three things at once | Code, data, and model all change — and they must match | Git for code, data versioning, a model registry tying all three together |
| Serving must be fast | Users will not wait; the latency budget is milliseconds | Batching, caching, quantization, the right serving framework (Lesson 6) |
| Failures hide | The worst ML failure is silent — wrong answers, no crash | Two-dashboard monitoring: system metrics plus model metrics and drift detection |

## Five mistakes to avoid (anti-patterns)

```
1. Manual deployments — 40 careful hand steps will eventually be done wrong. Automate.
2. No model versioning — if you cannot say which model answered, you cannot roll back or investigate.
3. Training in production — studying and serving fight over the same machines; both lose.
4. Ignoring data quality — bad ingredients in, confident wrong answers out, silently.
5. No monitoring — flying blind in the one system whose failures make no noise.
```

## One full story — a recommendation system

A shopping app recommends products. Data stage: clicks and purchases flow in continuously and are cleaned nightly and in streams. Training: the model re-studies recent behaviour on GPUs. Evaluation: it must beat the current live model's score on unseen recent data. Deployment: canary release to 5% of users. Monitoring: click-through rate is the food metric; latency and errors are the kitchen metrics. Retraining: weekly on schedule, and immediately when drift is detected after a big sale event changes buying patterns. Every stage you just read, working as one circle.

```
One line to remember: Six stages, one circle: data, training, tasting, deployment, watching, retraining.
```

## Interview questions — Lesson 3

**Q1. Walk me through the ML lifecycle.**

**Understand it like this: **The restaurant circle, in six rooms: ingredients, teaching, tasting, menu, watching, teaching again.

**Say this in the interview: ***"Six stages: data collection and preparation, training, evaluation on unseen data, deployment, monitoring, and retraining — and then the cycle repeats. Infrastructure supports every stage, and the cycle never ends because the world keeps changing under the model."*

**Q2. How is monitoring an ML system different from monitoring a normal application?**

**Understand it like this: **A normal app needs a watchman for the kitchen. An ML system needs a second watchman for the food itself.

**Say this in the interview: ***"A normal application is monitored for availability, latency, errors, and resource use. An ML system needs all of that plus model metrics — prediction distribution, confidence, and data and model drift — because its most dangerous failure is silent: the service stays up and fast while answer quality decays."*

**Q3. What is model drift, and what do you do about it?**

**Understand it like this: **The student studied 2019 questions; the 2026 exam changed. Nothing broke — the world moved.

**Say this in the interview: ***"Drift is the gradual decay of model quality as live data moves away from training data. I detect it by monitoring input distributions and prediction quality against training baselines, and I respond with retraining on fresher data, followed by evaluation and a safe, reversible deployment."*

**Q4. Why version data and models, not just code?**

**Understand it like this: **Because the answer a user got came from a specific model, trained on specific data, by specific code. Lose any one of the three and you cannot reproduce or undo anything.

**Say this in the interview: ***"Reproducibility and rollback need all three: Git versions the code, data versioning records the exact dataset, and a model registry ties each model version to the data and code that produced it, with its evaluation score and approval state."*

**Q5. Name three anti-patterns in ML infrastructure.**

**Understand it like this: **Hand steps, no versions, and studying in the dining room.

**Say this in the interview: ***"Manual deployments, missing model versioning, and training in production — plus ignoring data quality and running without monitoring. Each one removes either repeatability, reversibility, or visibility, which are the three things production ML cannot survive without."*

## Self-test — Lesson 3 (say the answers out loud)

```
1. Name the six stages of the ML lifecycle, in order.
2. What is the difference between precision and recall?
3. What do p50, p95, and p99 latency mean, and why not just use the average?
4. What are the three kinds of retraining trigger?
5. Why must evaluation use data the model has never seen?
```

# Lesson 4 — ML Frameworks: the two kitchens models are built in

This lesson is written for you, not for a data scientist. You do not need to train models. You need to deploy them, fix them when they break, make them fast, and talk to the people who built them. A framework is the set of ready-made tools a model is built with — a cookbook with pre-made sauces and doughs, instead of everything from scratch. Nearly everything in ML is built on one of two frameworks.

|  | **PyTorch** | **TensorFlow** |
| --- | --- | --- |
| Made by | Meta (Facebook), 2016 | Google, 2015 |
| Style | Dynamic graph — the model is built step by step while it runs, like cooking while tasting and adjusting | Static graph by default — the full recipe is written first, then executed; newer versions also allow eager, step-by-step running |
| Loved for | Flexibility, easy debugging, research; about 70% of research papers; home of NLP and large language models (LLMs) | Production scale, mobile and edge, enterprise stability |
| Ecosystem | Hugging Face (ready-made models), PyTorch Lightning (simpler training), TorchServe (official serving) | TF Hub (ready-made models), TF Lite (phones and edge), TF Serving (production serving), TensorFlow.js (browsers) |
| Multiple GPUs | Manual — one model per GPU, you route requests yourself | Built in — MirroredStrategy spreads one model across GPUs |

```
One line to remember: PyTorch cooks while tasting; TensorFlow writes the full recipe first. Both produce a model file — and the file is where your job starts.
```

## Saving a model — recipe plus weights

A trained model is two things: the architecture (the recipe — how the layers are arranged) and the weights (the learned settings — how much of each spice). PyTorch offers two ways to save:

- **Whole model. **Save everything together. Easier, but clumsy: bigger, fragile across PyTorch versions. Fine for experiments, not for production.

- **State dict. **Save only the weights — the standard in production. About half the size and travels better between versions. The catch: to load it, you must first rebuild the recipe from code, then pour the weights in.

TensorFlow's production format is SavedModel: a folder holding the graph, the weights, and the settings, saved under a version number such as serving_model/1/. That version number matters — TF Serving can hold several versions at once and switch between them, which is how safe rollouts work.

## The three traps that break serving

Trap 1 — forgetting eval mode.

This is the classic silent bug. In training mode, some layers behave randomly on purpose (dropout switches parts off so the model learns robustly) and some keep re-computing their settings (batch normalisation). If you serve in training mode, the same question can get different answers and accuracy drops — with no error anywhere. The fix is one line before inference: model.eval().

Trap 2 — computing gradients during inference.

During training, the framework records every step so it can learn backwards from mistakes. During serving, nobody is learning — but if recording stays on, it eats memory and slows everything down. Wrap inference in torch.no_grad() to switch the recording off.

Trap 3 — device mismatch.

“Expected tensor on cuda:0 but got tensor on cpu.” The model sits on the GPU and the input sits on the CPU. Data and model must live on the same device. Move the input to the model's device before inference, and move the answer back to the CPU afterwards if other code needs it.

```
One line to remember: Serving checklist from these three traps: eval mode on, gradients off, input on the model's device.
```

## Making a model smaller and faster

- **TorchScript. **Compile the model into a form that runs without the original Python code. 10 to 30% faster inference. Saved as a .pt file, loaded with one line. You can also combine it with quantization.

- **Quantization — use simpler numbers. **A model's weights are precise 32-bit decimal numbers. Quantization rounds them to 8-bit whole numbers: the model gets 4 times smaller and 2 to 4 times faster, and loses less than 1% accuracy in most cases — too small for users to notice. It is a deployment decision, made by you, and it is never shipped blind: measure the quantized model on the same test data first, and ship only if the score holds.

| **Model** | **Original size** | **After quantization** |
| --- | --- | --- |
| ResNet-50 | 98 MB | 25 MB |
| BERT | 440 MB | 110 MB |
| GPT-2 small | 548 MB | 137 MB |

- **ONNX — the universal format. **One format every framework can convert to. Build in PyTorch or TensorFlow, convert to ONNX, serve with ONNX Runtime. Your serving stack stops caring which framework built the model — and it is often faster than serving with the original framework. For an infrastructure engineer this is the cleanest setup: one serving system, any model.

- **Warm-up — preheat the oven. **The first inference a model ever runs is 10 to 100 times slower than normal — code compiling, GPU kernels initialising, memory allocating. Run about ten dummy inferences at startup, before measuring latency or opening to real traffic. Skip it and your latency numbers are lies, and your first real customers get the slow answer.

## The four errors you will actually see

| **Error** | **What it means** | **Fixes, in order** |
| --- | --- | --- |
| Out of memory (OOM) — “CUDA out of memory” | The model plus the batch does not fit on the GPU | Smaller batch size; empty the GPU cache; mixed precision (FP16 — half-size numbers, half the memory); gradient checkpointing during training |
| Slow first inference | A cold start — nothing is compiled or initialised yet | Warm up with dummy inferences at startup |
| Shape mismatch | The model expects an exact input shape — for example 1 image, 3 colour channels, 224 by 224 pixels — and got something else | Check and enforce the input shape before sending |
| CPU vs GPU mismatch | Model on GPU, input on CPU (or the reverse) | Move the input to the model's device |

## Choosing between the frameworks

- **Pick PyTorch when: **The work is NLP or LLMs, the environment is research-heavy, you need flexibility and debuggability, or you are deploying Python-first.

- **Pick TensorFlow when: **You need mobile or edge (TF Lite), large-scale production serving (TF Serving), enterprise stability, Google Cloud integration, or JavaScript deployment (TensorFlow.js).

- **When you do not want to choose: **Convert to ONNX and serve with ONNX Runtime — one serving system for models from either framework.

```
Deployment practice — flagged: No model-building practice in this lesson for you. The deployment-relevant skills are the saving formats, eval mode, warm-up, quantization, ONNX conversion, and the four errors — all of which appear again when you run the parked serving practice from Lessons 5 and 6.
One line to remember: Eval mode on, warm it up, batch the questions, and quantize when you need it small and fast.
```

## Interview questions — Lesson 4 (the lesson's seven self-test questions)

**Q1. What is the difference between PyTorch and TensorFlow's computation graphs?**

**Understand it like this: **PyTorch is cooking while tasting — the dish is built step by step as it runs. TensorFlow traditionally writes the full recipe first, then cooks it exactly as written.

**Say this in the interview: ***"PyTorch uses a dynamic graph, built at runtime, which makes it flexible and easy to debug. TensorFlow was built around a static graph defined before execution, which suits optimisation and large-scale deployment; modern TensorFlow also supports eager execution. For infrastructure, the practical effect is in how models are exported and served."*

**Q2. Why must you call model.eval() before inference?**

**Understand it like this: **Because in training mode the chef cooks randomly on purpose — fine for learning, wrong for serving a customer.

**Say this in the interview: ***"Training mode enables behaviours like dropout and training-style batch normalisation, which make predictions non-deterministic and less accurate. Calling model.eval() switches those layers to inference behaviour, so the same input gives the same, correct output every time."*

**Q3. What are the two ways to save PyTorch models, and when do you use each?**

**Understand it like this: **Save the whole kitchen, or save only the learned spice amounts and rebuild the kitchen from its plan.

**Say this in the interview: ***"You can save the entire model, which is simple but larger and brittle across versions, or save the state dict — just the weights — which is the production standard: smaller and portable, but loading requires recreating the architecture in code first, then loading the weights into it."*

**Q4. What is TorchScript, and how does it improve inference?**

**Understand it like this: **Turning a handwritten recipe into a printed, optimised one that any kitchen can follow without the original cook.

**Say this in the interview: ***"TorchScript compiles a PyTorch model into a serialised form that runs without the original Python code. That removes Python overhead and allows graph optimisations, typically giving 10 to 30 percent faster inference, and the compiled model can be served from non-Python environments."*

**Q5. What is ONNX, and why is it useful for infrastructure?**

**Understand it like this: **One suitcase every airline accepts. Pack the model once, and any serving system can carry it.

**Say this in the interview: ***"ONNX is a framework-neutral model format. Models from PyTorch, TensorFlow, and others convert into it, and ONNX Runtime serves them — often faster than the native frameworks. For infrastructure it means one standard serving stack regardless of which framework each team trained with."*

**Q6. How do you warm up a model, and why is it necessary?**

**Understand it like this: **Preheat the oven before the first customer orders — ten dummy dishes, thrown away.

**Say this in the interview: ***"At startup I run roughly ten dummy inferences before opening traffic or measuring latency. The first inference is 10 to 100 times slower because of compilation, GPU kernel initialisation, and memory allocation; warm-up absorbs that cost so real users and latency measurements never see it."*

**Q7. What is the difference between batch inference and single inference?**

**Understand it like this: **Answering questions one by one, or collecting a page of questions and answering them together.

**Say this in the interview: ***"Single inference processes one request at a time, which under-uses the GPU. Batch inference groups requests — for example 32 at a time, or whatever arrives within a short wait window — and processes them together, typically giving 3 to 10 times the throughput at a small latency cost per request."*

# Lesson 5 — Cloud Computing for ML: rented computers, GPU prices, and the bill

Cloud computing in one line: renting computers over the internet instead of buying them. Five traits make it cloud and not just someone else's computer: you get a server in a minute with no purchase order; you can reach it from anywhere; thousands of customers share the same giant data centres; you can grow or shrink fast; and you pay only for what you use, like an electricity meter.

## The service models — the pizza version

| **Model** | **In simple words** | **Examples** |
| --- | --- | --- |
| On-premises | You own the building and the ovens. You cook, clean, and fix everything. | Your own data centre |
| IaaS — Infrastructure as a Service | You rent the kitchen and the ovens, bring ingredients, and cook. The most common model for ML infrastructure, because you keep full control of the compute. | Amazon EC2, Google Compute Engine, Azure VMs |
| PaaS — Platform as a Service | The kitchen comes stocked and the platform handles the boring parts; you bring the dish. | Elastic Beanstalk, App Engine |
| SaaS — Software as a Service | Someone else cooked it. You just eat. | Gmail, Salesforce, Dropbox |

For ML work, the other main option besides raw IaaS is a managed ML platform — SageMaker (AWS), Vertex AI (GCP), Azure ML. Think of it as an all-in-one ML kitchen: data, training, serving, and monitoring under one roof, instead of you bolting together twenty separate services.

## The big three

| **Provider** | **Market share (lesson figures)** | **Known for** | **ML services** |
| --- | --- | --- | --- |
| AWS | About 32% | Oldest (2006), most services, biggest community and documentation, 30+ regions | SageMaker, Bedrock |
| Azure | About 23% | The enterprise favourite — Active Directory, Office 365, hybrid cloud | Azure ML, Azure OpenAI |
| GCP | About 11% | The ML innovator — built on Google's own ML infrastructure, makes its own ML chips (TPUs), created Kubernetes, best managed Kubernetes (GKE) | Vertex AI |

## GPU machines and what they cost

Cloud machines come in families: general purpose (the all-rounder, good for API servers), compute-optimised (batch number-crunching), memory-optimised (models needing huge RAM), GPU machines (training and fast serving), and TPUs (Google-only chips built just for ML). Lesson prices, per hour, roughly:

| **Machine** | **GPU** | **Rough cost per hour** |
| --- | --- | --- |
| g5.xlarge (AWS) | 1 x A10G | About $1 — the cheapest way to get a GPU |
| p3.2xlarge (AWS) | 1 x V100 | About $3 |
| a2-highgpu-1g (GCP) | 1 x A100 | About $3.50 |
| p4d.24xlarge (AWS) | 8 x A100 | About $32 — that is $768 a day, which is why nobody leaves GPU machines idling |

## The three kinds of storage

| **Kind** | **Simple picture** | **Rough price** | **Best for** |
| --- | --- | --- | --- |
| Object storage (S3, Cloud Storage, Blob) | A giant warehouse | About $0.023 per GB per month | Datasets, models, logs — where ML data lives |
| Block storage (EBS, Persistent Disk) | A hard drive attached to one machine | About $0.10 per GB per month | Databases and application data needing fast, low-delay access |
| File storage (EFS, Filestore) | A shared folder many machines open at once | About $0.30 per GB per month | Training data several machines need simultaneously |

Storage also has classes: hot (instant access, costs more), cool (instant but cheaper, for things rarely opened), and archive (hours to retrieve, costs pennies — long-term backups).

## Networking — and the hidden cost trap

A VPC is your private network inside the cloud; subnets are rooms inside it; security groups are the firewall rules — who may knock on which door; a load balancer spreads traffic across machines; a CDN copies content close to users so it loads fast.

The trap most people learn the hard way: moving data costs money. Inside the same region it is free or nearly free. Between regions it is roughly $0.01 to $0.02 per GB. Out to the internet it is roughly $0.05 to $0.09 per GB — and this egress charge can quietly exceed the machine bill for a chatty, cross-region design.

## Where the money goes, and five ways to keep it small

The lesson's example monthly bill is $8,300: compute $5,000 (60%), storage $1,000, data transfer $800, load balancers $500, managed Kubernetes $500, monitoring $300. The machines are the bill; everything else is rounding.

```
1. Right-size. Do not rent a big machine just in case. The lesson's example: serving on 2 CPUs and 4 GB of RAM costs about $50 a month; the same job on 8 CPUs and 32 GB costs $200 — for the same answers.
2. Spot instances. Rent spare capacity at up to 90% off — but the cloud can take the machine back with short notice. Perfect for batch jobs, dev environments, and training that saves checkpoints. Never for live serving.
3. Turn things off. Dev environments do not need to run at 3 AM. Shut down at 6 PM, start at 8 AM on weekdays.
4. Reserved instances. Commit for 1 year and save 30 to 40%; 3 years, 50 to 60%. Good for always-on production serving; bad for bursty training.
5. Watch the bill. Budget alerts at 50%, 80%, and 100% of budget. Tools: AWS Cost Explorer, GCP Cost Management, Azure Cost Management, and Kubecost for cost per Kubernetes workload.
```

## Safety rules, short version

- **Security: **IAM roles, not access keys. MFA on. Security groups locked down. Data encrypted. Credentials never committed to Git. Root account never used for daily work.

- **Reliability: **Multiple availability zones, health checks, auto-scaling, backups, and a disaster recovery plan.

- **Performance: **A region close to your users, a CDN, caching, and the right machine size.

## Which cloud to learn

The lesson's advice: start with GCP (simplest pricing, best Kubernetes, $300 free credit for 90 days, strongest ML focus), then AWS (most job postings, biggest ecosystem; 12 months of free tier), then Azure (enterprise Microsoft shops; $200 credit for 30 days). For you the honest version is shorter: you already know AWS and Azure, so GCP's ML side — Vertex AI, TPUs, GKE — is the new part.

```
Deployment practice — flagged: Lesson 5's exercise — deploying a FastAPI app to a cloud VM — is deployment practice. It is parked for when you are at your laptop, together with the Lesson 6 serving build. No model writing is involved in either.
One line to remember: Compute is the bill — right-size it, rent spare capacity for batch work, and never let a GPU idle.
```

## Interview questions — Lesson 5 (the lesson's seven self-test questions)

**Q1. What are the cloud service models, and how do they differ?**

**Understand it like this: **Pizza. Make it all yourself, rent a kitchen, rent a stocked kitchen, or order a finished pizza.

**Say this in the interview: ***"On-premises means owning everything. IaaS rents raw infrastructure — virtual machines, storage, networking — with full control, which is the most common base for ML infrastructure. PaaS adds a managed platform so you only bring the application. SaaS is a finished product you simply use."*

**Q2. What are the key differences between AWS, GCP, and Azure?**

**Understand it like this: **The biggest shop, the ML inventor, and the enterprise favourite.

**Say this in the interview: ***"AWS is the oldest and largest, with the widest service catalogue — SageMaker and Bedrock for ML. GCP is the ML innovator: TPUs, Vertex AI, and the best managed Kubernetes in GKE. Azure is the enterprise and hybrid-cloud favourite, with Azure ML and Azure OpenAI, and the deepest Microsoft integration."*

**Q3. What is a GPU instance, and when would you use it?**

**Understand it like this: **A rented machine carrying the ten-thousand-worker chip from Part 0.

**Say this in the interview: ***"A GPU instance is a cloud machine with one or more GPUs attached. I use it for training, which needs massive parallel computation, and for latency-sensitive or high-throughput inference. Because it is the most expensive compute, I right-size it and never leave it idle."*

**Q4. What is the difference between object storage (S3) and block storage (EBS)?**

**Understand it like this: **A warehouse versus the hard drive bolted into one machine.

**Say this in the interview: ***"Object storage is an effectively unlimited, cheap warehouse for datasets, models, and logs, accessed over an API. Block storage is a fast, low-latency disk attached to a single instance, suited to databases and application data. ML data lives in object storage; block storage serves the machines."*

**Q5. How can you reduce cloud costs by 90% for batch workloads?**

**Understand it like this: **Rent the spare ovens the cloud is about to throw away.

**Say this in the interview: ***"Use spot or preemptible instances, which rent spare capacity at up to 90 percent discount. Batch workloads tolerate interruption when they are checkpointed and restartable, which serving workloads are not — so spot is for batch and training, never for live serving."*

**Q6. What is a spot or preemptible instance, and when should you use it?**

**Understand it like this: **Same machine, steep discount, one condition: the cloud can take it back with short notice.

**Say this in the interview: ***"It is spare cloud capacity sold cheap with an interruption warning. I use it for batch processing, dev environments, and checkpointed training. I never use it for production serving, where an interruption is an outage."*

**Q7. What are the main cost components in cloud ML infrastructure?**

**Understand it like this: **The machines are the bill — roughly 60 percent in the lesson's example. The rest is storage, data movement, and the supporting services.

**Say this in the interview: ***"Compute dominates — about 60 percent of the example $8,300 monthly bill — followed by storage, data transfer including egress, load balancing, managed Kubernetes, and monitoring. Cost work starts with compute: right-sizing, spot for batch, reservations for steady serving, and shutting down idle GPUs."*

# Lesson 6 — Model Serving Basics: your home ground

Serving is the step where the model leaves the lab and meets real people. The flow is simple: a question comes in, you clean it up (preprocessing), the model answers it (inference), you format the answer nicely (post-processing), and the answer goes back. That whole flow is your job — this is a deployment lesson from start to finish.

## Training vs serving — opposite worlds

|  | **Training** | **Serving** |
| --- | --- | --- |
| Takes | Hours or days | Milliseconds |
| Works on | Millions of examples at once | One question at a time |
| Optimises for | Accuracy — the most answers right | Latency and throughput — fast answers, many per second |
| Failure | Can fail and retry quietly | Must work first time, in front of a real user |
| Runs | Temporarily — machines released when done | All the time — and the bill never stops |

## What serving has to deliver

- **Speed — latency budgets. **Search ranking under 50 ms; ad serving under 20 ms (the ad must load before the page does); fraud detection under 100 ms; chatbots under 500 ms (a person is waiting). Relaxed batch budgets: spam filtering under 5 s, recommendations under 1 s, image processing under 2 s.

- **Volume — throughput. **Small app 10 requests per second; medium 100; large 1,000; massive scale 10,000 or more.

- **Uptime — availability. **99% uptime is 3.65 days down per year. 99.9% is about 8.76 hours. 99.99% is 52 minutes. 99.999% is 5 minutes. Each extra nine costs real engineering.

- **Features. **Versioning (several model versions live at once), A/B testing (some users get the new model, some the old), monitoring and logging of every prediction, batching, caching, and a fallback — a backup answer or a graceful error instead of a crash.

- **Operations. **Easy deployment, quick rollback, scaling with traffic spikes, cost efficiency, security, and observability — you must be able to see what the system is doing.

```
One line to remember: Training is a sprint for accuracy; serving is a marathon for speed, volume, and uptime.
```

## The four ways to serve a model

| **Approach** | **In simple words** | **Use it when** | **Watch out for** |
| --- | --- | --- | --- |
| 1. Embedded | The model lives inside the app's own code; a Flask app loads it at startup and answers directly | Prototypes, simple apps, low traffic — never real production | Updating the model restarts the whole app; no separate scaling; no versioning |
| 2. Model as a service | The model is its own service (usually FastAPI), called over HTTP or gRPC; one model service feeds many apps | Several apps share one model, or model and app scale on different schedules | Every request pays a network trip; more infrastructure; needs load balancing |
| 3. Serving frameworks | A professional kitchen built for this: TorchServe (PyTorch), TensorFlow Serving (Google), ONNX Runtime (any ONNX model) | Real production deployments | A learning curve; less flexible than your own code; mostly framework-specific. In return: versioning, batching, metrics, and a management API built in |
| 4. Cloud ML platforms | A fully managed restaurant: SageMaker, Vertex AI, Azure ML run it for you | You want it managed, have the budget, and need it deployed fast | Vendor lock-in, higher cost, less control, framework limits |

```
One line to remember: Prototype embedded, grow into a microservice, go to production with a serving framework or a managed platform.
```

## Five ways to make serving faster

```
1. Batch inference. Collect questions and answer them together — 3 to 10 times the throughput. Two knobs: batch size (for example 32) and max wait time (for example 50 ms). Send when the batch is full or the wait runs out, whichever comes first, so one lonely question never waits forever.
2. Quantization. Shrink the numbers from 32-bit to 8-bit (Lesson 4): 4 times smaller, 2 to 4 times faster, under 1% accuracy lost. A serving decision, made by you.
3. Caching. If the same question keeps coming back, remember the answer instead of computing it again. Best when the model is expensive, the possible questions are limited, and reads far outnumber writes.
4. Warm-up. Run about ten dummy inferences at startup, before the first real customer (Lesson 4).
5. Async processing. Do not let one slow step block the others: read uploads asynchronously and run inference in a separate thread pool, so the server keeps answering while heavy work proceeds. FastAPI's async endpoints exist for exactly this.
```

## Three ways to roll out a new model safely

| **Strategy** | **How it works** | **Strength** | **Cost** |
| --- | --- | --- | --- |
| Blue-green | Two identical environments. New version goes to green, gets tested, all traffic flips at once; blue stays ready for instant rollback | Zero downtime, instant rollback | Double resources during the deploy; the switch is all-or-nothing |
| Canary | 5% of traffic to the new version, then 50%, then everyone | Errors appear early and hurt almost nobody | Slower rollout; needs traffic-routing logic and close monitoring |
| Shadow | Every request goes to the old version as usual, and a copy also goes to the new one — whose answers are never shown | Zero user risk, real-traffic comparison | Double compute; cannot catch problems that only appear when users react to the new answers |

```
One line to remember: Batch the questions, shrink the model, cache the repeats, warm it up — and never swap the whole menu in one go.
```

## What to monitor — the lesson's example numbers

- **The kitchen. **Latency p50 45 ms, p95 120 ms, p99 300 ms; throughput 150 requests per second; CPU 65%, memory 3.2 GB, GPU 80%; uptime 99.95%; error rate 0.05%.

- **The food. **Prediction distribution — class 0 at 35%, class 1 at 45%, class 2 at 20%; if those proportions suddenly shift, something changed. Confidence: average 0.87, plus a count of low-confidence predictions (below 0.5) — a rising count means the model is getting unsure. Plus drift: the input's average and spread versus what you expected.

Wiring: Prometheus collects a counter of predictions by model version and status (success or error), a histogram of latency, and a histogram of confidence scores, exposed on a /metrics endpoint that Prometheus scrapes. Every prediction records its outcome, and latency is recorded in a finally block so failures count in the dashboards too.

## The complete serving solution — what the lesson builds

- **Load once. **The model loads once, at startup — never per request. Loading takes seconds; a request has milliseconds. It is warmed up with ten dummy inferences immediately.

- **/health endpoint. **Answers “healthy” and whether the model is loaded. This is what Kubernetes probes hit to decide if the pod is alive.

- **/predict endpoint. **Six steps in order: check the input is actually an image (reject with a 400 error if not), read it, clean it up, run the model under torch.no_grad(), format the answer as class plus confidence plus time taken, and count success or error in Prometheus.

- **Honest failures. **Errors return a 500 with a log line — and the latency is still recorded.

- **/metrics endpoint. **Mounted on the app for Prometheus, and the service runs with uvicorn on port 8000.

```
Deployment practice — flagged: This complete serving solution is deployment practice — the second parked build, alongside the Lesson 5 cloud VM deployment. When you are at your laptop we build this exact service, run it, hit it with real requests, and watch the metrics. No model writing: the model file is given; everything else is serving.
One line to remember: Serving is a marathon — load once, warm it up, answer fast, watch two dashboards, and always have a way back.
```

## Interview questions — Lesson 6 (the lesson's seven self-test questions)

**Q1. What is the difference between training and serving workloads?**

**Understand it like this: **Studying versus the exam hall — except the exam never ends and every answer has a time limit.

**Say this in the interview: ***"Training is a batch workload: hours or days, millions of examples, optimised for accuracy, and it can fail and retry. Serving is a live workload: milliseconds per request, one question at a time, optimised for latency and throughput, and it must succeed first time in front of a user, around the clock."*

**Q2. What are the pros and cons of embedded models versus microservices?**

**Understand it like this: **The chef inside your restaurant versus a separate kitchen any restaurant can order from.

**Say this in the interview: ***"Embedded is simple and avoids network latency, but the model cannot scale, update, or version independently of the app. A model microservice scales and updates independently and can serve many applications, at the cost of network latency, extra infrastructure, and load balancing."*

**Q3. How does batch inference improve throughput?**

**Understand it like this: **One trip carrying 32 orders beats 32 trips carrying one.

**Say this in the interview: ***"GPUs are massively parallel, so processing one request wastes most of their capacity. Batching groups requests — up to a batch size or a short wait limit — and processes them together, typically improving throughput 3 to 10 times, at a small, controlled latency cost."*

**Q4. What is quantization, and what are its benefits?**

**Understand it like this: **Rounding precise prices to whole numbers: the customer never notices, the till runs much faster.

**Say this in the interview: ***"Quantization converts model weights from 32-bit floats to 8-bit integers. The model becomes about 4 times smaller and inference 2 to 4 times faster, with under 1 percent accuracy loss in most cases — which means cheaper hardware, faster loading, and models that fit on edge devices. I always validate accuracy on test data before shipping a quantized model."*

**Q5. What is the difference between blue-green and canary deployments?**

**Understand it like this: **Blue-green flips the whole restaurant at once with the old one standing by. Canary sends the first few tables to the new kitchen and watches them eat.

**Say this in the interview: ***"Blue-green runs two full environments and switches all traffic at once, giving instant rollback but an all-or-nothing change. Canary shifts traffic gradually — 5 percent, then 50, then all — so problems surface early with a small blast radius, at the cost of a slower rollout and more routing and monitoring work."*

**Q6. What metrics should you monitor for model serving?**

**Understand it like this: **Two dashboards, as always: the kitchen and the food.

**Say this in the interview: ***"System metrics: latency at p50, p95, and p99, throughput, error rate, CPU, GPU, and memory, and uptime. Model metrics: prediction distribution, confidence scores including the low-confidence count, and input and output drift. Either dashboard can fail while the other stays green, so both are mandatory."*

**Q7. When would you use TorchServe versus a simple FastAPI service?**

**Understand it like this: **A hand-built counter versus a professional kitchen with the systems already installed.

**Say this in the interview: ***"A simple FastAPI service suits a single model, low traffic, or a quick deployment I fully control. TorchServe is the choice for production: multiple models and versions, built-in batching, Prometheus metrics, and a management API for loading and unloading models without restarts."*

**Docker — Zero to Advanced**

This chapter collects the full Docker deep-dive taught after Lesson 6: every concept from architecture to production, with examples and commands, in the same plain words. Two scope decisions you made are honoured here: volumes and networks are covered briefly, because you will go deep on the same concepts in Kubernetes (PersistentVolumes and Claims for storage; Services and Ingress for networking) — and Docker Compose and Swarm are noted only to be set aside, because in companies Kubernetes does that job. The Docker workflow that matters in production is the one you named: write the Dockerfile, build the image, push it to the registry.

# What Docker is, and the problem it solves

Every developer knows this sentence: “But it works on my machine!” Code runs perfectly on a laptop and breaks on the server, because the server has a different operating system version, a different Python version, a missing library, a different setting. The app works — the environment around it does not match.

Docker fixes this by packing the app together with everything it needs — code, language version, libraries, settings — into one sealed box called a container. The box runs the same on a laptop, on a server, on AWS, anywhere. The environment travels with the app. Think of moving house: without Docker you move each item separately and hope the new house matches; with Docker you move the whole house — walls, wiring, furniture — and it works exactly as before.

## The architecture — four pieces, plus two

| **Piece** | **In simple words** |
| --- | --- |
| Docker client | You, typing commands — docker run, docker build, docker ps. The client does not do the work; it sends orders. |
| Docker daemon | The engine running in the background. It receives orders and does the real work: building images, running containers, managing networks and storage. |
| Image | A read-only blueprint: a snapshot of an operating system plus your app plus everything it needs. Build once, run a hundred times. |
| Container | A running image — the house built from the blueprint. Alive, isolated, and gone when removed unless its data was saved elsewhere. One image becomes many containers. |
| Dockerfile | The recipe: a text file of step-by-step instructions for building the image. |
| Registry | The warehouse where images are stored and shared. Docker Hub is the public one — an app store for images. You pull images down and push your own up. |

Containers versus virtual machines, in one breath: a virtual machine runs a whole second operating system, so it is heavy and slow to start. A container shares the host's kernel and carries only the app and its libraries, so it is light and starts in seconds.

```
docker run hello-world
```

What happens behind that one command: the client sends the order to the daemon; the daemon checks for the hello-world image locally, does not find it, and pulls it from Docker Hub; it creates a container from the image and runs it; the container prints its message and exits. A container that finishes its job exits — that is normal, not an error.

```
docker --version   # is Docker installed, which version
docker images      # which blueprints are on this machine
docker ps          # which containers are running right now
docker ps -a       # all containers, including stopped ones
```

```
One line to remember: An image is the blueprint, a container is the house, and the daemon is the builder.
```

# The Dockerfile — the recipe, instruction by instruction

A plain text file called Dockerfile. Each line is one instruction, and each instruction adds one layer to the image. Layers stack, and Docker caches them: change only the last line and Docker reuses every earlier layer instead of rebuilding. That is why order matters — things that rarely change (installing libraries) go early; things that change daily (your code) go last.

| **Instruction** | **What it does, in simple words** |
| --- | --- |
| FROM | The foundation — every image starts from a base image. FROM python:3.11-slim starts from a small Linux with Python 3.11 installed. |
| WORKDIR | The working folder inside the container — like cd /app. Every later command runs from there. |
| COPY | Copy files from your machine into the image. COPY requirements.txt . copies the file into the working folder. |
| RUN | Run a command while building the image — for example installing libraries. Happens once, at build time, not at every start. |
| ENV | Set an environment variable inside the container. It survives into the running container. |
| ARG | A variable used only while building, such as a version number. It does not survive into the running container — that is the difference from ENV. |
| EXPOSE | A note on the blueprint saying which port the app listens on. It documents the port; it does not open it. The real opening is -p at run time. |
| CMD | The default command when the container starts. A default — it can be overridden at run time. |
| ENTRYPOINT | The fixed command. If CMD is a suggestion, ENTRYPOINT is the rule; when both exist, CMD's words become ENTRYPOINT's arguments. |
| USER | Which user runs the app. Containers run as root by default — a security risk — so production images switch to a limited user. |
| HEALTHCHECK | How Docker checks the app is alive, for example by calling its /health endpoint. |

```
# A real example — a FastAPI app
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Notice the order: requirements are copied and installed before the code. Code changes every day; the library list rarely does. Docker reuses the cached install layer and rebuilds only the last step.

```
docker build -t my-app:1.0 .                      # build, name it my-app, version 1.0
docker run -d -p 8000:8000 --name my-app my-app:1.0
```

In that run command: -d is detached (runs in the background), -p 8000:8000 maps your machine's port 8000 to the container's port 8000 — that is the door being opened — and --name gives the container a human name.

```
One line to remember: Each Dockerfile line is a cached layer — stable stuff first, changing stuff last.
```

# The container lifecycle — commands you will actually use

```
docker run -d --name web nginx   # create + start, in background
docker ps                        # running containers
docker stop web                  # stop gently — gives the app time to shut down
docker start web                 # start it again
docker restart web               # stop + start in one go
docker rm web                    # remove it (must be stopped first)
docker rm -f web                 # force remove — stop and remove together
```

| **Run flag** | **What it does** |
| --- | --- |
| -d | Detached — run in the background. |
| -it | Interactive with a terminal: -i keeps input open, -t gives a proper terminal. docker run -it ubuntu bash drops you into a shell. |
| --name | A human name instead of a random one. |
| -p 8080:80 | Map ports — host first, container second. |
| -e KEY=value | Set an environment variable. |
| -v mydata:/data | Attach storage (brief section below; depth comes in Kubernetes). |
| --rm | Delete the container automatically when it stops. Perfect for one-off jobs and tests. |
| --restart unless-stopped | Restart after a crash or a machine reboot. Policies: no (default), always, unless-stopped, on-failure (with optional max retries, e.g. on-failure:5). |
| --memory 512m --cpus 1 | Limits. Without a fence, one container can eat the whole machine. |

## Looking inside, and managing images

```
docker logs web              # what the container printed
docker logs -f web           # follow live, like tail -f
docker logs --tail 50 web    # last 50 lines only
docker exec -it web sh       # open a shell inside — knock and walk in
docker inspect web           # everything Docker knows, as JSON
docker stats                 # live CPU and memory for all containers
docker top web               # processes running inside it
```

docker exec is your best debugging friend: the app misbehaves, you step inside, look around, check files, and test the network from the container's own point of view.

```
docker images                          # blueprints on this machine
docker pull python:3.11                # download an image from a registry
docker push myname/my-app:1.0          # upload your image to a registry
docker tag my-app:1.0 my-app:latest    # give an image another name or tag
docker rmi my-app:1.0                  # delete an image
docker history my-app:1.0              # every layer and its size
docker save my-app:1.0 -o app.tar      # export an image to a file
docker load -i app.tar                 # import it on another machine, no registry needed
```

Cleaning up — Docker eats disk quietly. Stopped containers, unused images, and old volumes pile up. Check with docker system df; clean with docker system prune (add -a to also remove images no container uses, and --volumes for unused volumes). docker image prune, docker container prune, and docker volume prune clean one kind at a time.

```
# The whole lifecycle in 60 seconds
docker run -d --name demo -p 8080:80 nginx
docker ps                        # see it running
curl http://localhost:8080       # it answers
docker exec -it demo sh          # step inside, look around, type exit to leave
docker logs demo                 # see the requests
docker stop demo && docker rm demo   # stop, remove, gone
```

```
One line to remember: Containers are cheap and disposable — stop, remove, rebuild without fear. The image is the truth; the container is just a running copy.
```

# Volumes and networks — the short version (depth comes in Kubernetes)

A container is disposable: delete it and everything inside is gone, so data must live outside it, in a volume — storage Docker attaches to the container, like plugging an external hard drive into a laptop. Three kinds: named volumes (Docker manages them; the recommended way for real data such as databases — create with docker volume create mydata, attach with -v mydata:/data, and the data survives container removal); bind mounts (a folder on your machine mapped in — best for development, because edits appear inside instantly with no rebuild); and tmpfs (memory only, vanishes on stop — fast, and good for temporary data and secrets you never want on disk). The newer --mount syntax says the same thing more explicitly, and anonymous volumes (a bare -v /data with no name) are best avoided because their random names make them hard to find later.

```
docker volume ls
docker volume inspect mydata
docker volume rm mydata
docker volume prune
```

Networks: containers on the same network talk by container name — Docker has built-in DNS, so your app connects to postgres:5432 instead of memorising an IP. Drivers in one line each: bridge (the default — a private network on one machine; create your own, because custom bridge networks get name-based DNS and the default one does not); host (shares the machine's network — fastest, no isolation, ports can clash); none (no network at all); overlay (containers on different machines acting as one network — Swarm territory); macvlan (the container gets its own address on the physical network and looks like a separate real machine).

```
docker network create mynet
docker run -d --name db --network mynet -v pgdata:/var/lib/postgresql/data postgres
docker run -d --name api --network mynet -p 8000:8000 my-app
docker network ls
docker network inspect mynet
docker network connect mynet web
docker network disconnect mynet web
docker network prune
```

In that example the app reaches the database at db:5432 — by name, no IP — and if both containers are deleted, the pgdata volume still holds the data. Per your decision, this stays shallow here: in Kubernetes you will use the same ideas every day as PersistentVolumes and PersistentVolumeClaims for storage, and Services and Ingress for networking.

```
One line to remember: Containers are disposable, data is not — volumes save the data, networks let containers find each other by name.
```

# Multi-stage builds — build fat, ship thin

The problem: a normal Dockerfile keeps everything it used to build the app. A Go program may need a 1 GB build environment to produce a 20 MB binary — and the final image carries all 1 GB. Python has the same shape: compilers, build caches, tools needed for five minutes. Bigger image, slower pulls, slower deploys, and more tools inside means more places for vulnerabilities to hide.

The fix: build in stages. One Dockerfile, several FROM lines. Stage 1 is the builder — full toolchain, compile everything. Stage 2 is the final image — a slim base, copying over only the finished artifact. The build tools never ship.

```
# Stage 1: build
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp .
```

```
# Stage 2: run
FROM alpine:3.19
COPY --from=builder /app/myapp /usr/local/bin/myapp
CMD ["myapp"]
```

Result: about a 20 MB image instead of 1 GB. The COPY --from=builder line is the whole trick — it reaches into the first stage and takes only the finished binary. The same idea in Python: stage 1 installs dependencies and builds wheels; stage 2 is python:3.11-slim and copies only the installed packages and your code. You can also build just one stage for debugging: docker build --target builder -t myapp:debug .

Three wins: smaller images (faster pulls and deploys), smaller attack surface (fewer tools inside), and no source code or build secrets in the final image.

```
One line to remember: Build fat, ship thin.
```

# Registries — version control for images

Docker Hub is the public registry. In companies it is usually ECR on AWS, Artifact Registry on GCP, ACR on Azure, or self-hosted Harbor. This is the workflow you identified as the one that matters in companies — Dockerfile, build, push — and the registry is the version control for images: tags are the versions, like Git tags for code.

```
docker login
docker build -t my-app:1.0 .
docker tag my-app:1.0 myname/my-app:1.0
docker push myname/my-app:1.0
```

Tags versus digests — the part that bites people. A tag is a human label (1.0, latest) and it can move: latest today can point to a different image than latest last month. A digest is the fingerprint (sha256:…) — it never changes and always points to the exact same image. In production, pin by digest or by an immutable version tag. Never deploy latest to production: you cannot tell which version is actually running, and rollback becomes guesswork.

A tagging strategy that works: semantic versions (1.2.3) for releases, plus the Git commit SHA as a tag (my-app:abc1234) so every image traces back to the exact code that built it. Keep latest for development only.

## Production habits, short version

- Run as a non-root user (USER in the Dockerfile).

- Use slim, Alpine, or distroless base images, and pin base image versions.

- Keep a .dockerignore so junk never enters the build context.

- Never bake secrets into an image — pass them at build time with BuildKit secret mounts, or at run time as environment variables.

- Scan images for vulnerabilities (Trivy, Docker Scout).

- Set memory and CPU limits on every container.

# Docker for ML — the GPU part

A container does not see the GPU by default. The host needs the NVIDIA Container Toolkit installed, then you hand the GPU to the container with a flag:

```
docker run --gpus all my-model-image              # all GPUs
docker run --gpus '"device=0,1"' my-model-image   # only GPU 0 and 1
docker run --gpus all nvidia/cuda:12.0-base-ubuntu22.04 nvidia-smi   # check: if it lists your GPU, the plumbing is right
```

For the base image, start from NVIDIA's CUDA images (for example nvidia/cuda:12.0-runtime-ubuntu22.04) — they carry the GPU libraries. Do not install CUDA by hand.

The model-weights question.

Model files are gigabytes, and there are three ways to handle them. Bake them into the image: simple and self-contained, but every weight change means rebuilding and pushing a giant image. Mount them from a volume: fast startup, weights managed separately from code. Or download them at startup from S3: an entrypoint step pulls the right version when the container starts. For serving that changes versions often, volume or download beats baking.

# Troubleshooting — the problems you will actually hit

| **Problem** | **Likely cause** | **Fix** |
| --- | --- | --- |
| “Cannot connect to the Docker daemon” | The engine is not running | Start Docker Desktop, or systemctl start docker |
| “Port is already allocated” | Something else owns that host port | Change your -p mapping, or stop the other container |
| “No space left on device” | Docker ate the disk — old images, containers, volumes | docker system df to see; docker system prune to clean |
| Pull fails with “unauthorized” | Not logged in, or wrong registry credentials | docker login and check the credentials |
| Container exits immediately | A container lives only as long as its main process — the app probably crashed on startup | Read docker logs |
| Slow builds | Layer cache misses | Check Dockerfile order and .dockerignore; use BuildKit |
| Container killed (OOM) | It hit its memory limit | Raise --memory or fix the leak; docker stats shows who is eating RAM |

# Interview rapid-fire — Docker (speakable answers)

**Q1. Image vs container?**

**Understand it like this: **Blueprint versus the running house.

**Say this in the interview: ***"An image is a read-only template containing the application and its environment. A container is a running instance of an image — isolated, with its own filesystem view, network, and process space. One image can run as many containers."*

**Q2. What is a Dockerfile?**

**Understand it like this: **The recipe — and every line is a cached layer.

**Say this in the interview: ***"A Dockerfile is a text file of instructions for building an image. Each instruction creates a cached layer, so builds reuse unchanged layers; that is why stable steps like dependency installation go before frequently changing application code."*

**Q3. Containers vs virtual machines?**

**Understand it like this: **VMs carry a whole second operating system; containers share the host's kernel.

**Say this in the interview: ***"Containers share the host kernel and package only the app and its libraries, so they are lighter and start in seconds. Virtual machines virtualise hardware and run a full guest OS, giving stronger isolation at much higher overhead."*

**Q4. How do you keep data after a container is removed?**

**Understand it like this: **Plug the storage in from outside — a volume.

**Say this in the interview: ***"With a volume: storage managed by Docker and mounted into the container, independent of the container's lifecycle. Named volumes are the production choice for data such as databases; bind mounts map a host folder, mainly for development."*

**Q5. How do containers find each other?**

**Understand it like this: **Same network, by name — Docker's built-in DNS does the rest.

**Say this in the interview: ***"Containers on the same user-defined network resolve each other by container name through Docker's embedded DNS, so services connect to a stable name like db:5432 instead of a changing IP address."*

**Q6. What is a multi-stage build?**

**Understand it like this: **Build fat, ship thin.

**Say this in the interview: ***"A Dockerfile with multiple FROM stages: a builder stage with the full toolchain produces the artifact, and the final stage starts from a slim base and copies only that artifact. The result is a much smaller image with a smaller attack surface and no build tools or secrets inside."*

**Q7. Why not deploy latest?**

**Understand it like this: **Because the tag moves — you would not know what is running.

**Say this in the interview: ***"latest is a mutable label that can point to different images at different times. Production deployments should pin an immutable version tag or the image digest, so the running version is known exactly and rollback is deterministic."*

**Q8. A container exits right away — why?**

**Understand it like this: **Its main process ended. The container's life is its main process's life.

**Say this in the interview: ***"A container runs only while its main process runs. If it exits immediately, the process failed or completed — I check docker logs for the startup error, which is usually a bad command, a missing file, or a configuration problem."*

**Q9. How do you give a container a GPU?**

**Understand it like this: **Install the bridge once, then hand the GPU over with a flag.

**Say this in the interview: ***"The host needs the NVIDIA Container Toolkit; then the container is started with --gpus all, or a device selection such as device=0,1. I verify with nvidia-smi inside a CUDA base image before trusting the setup."*

**Q10. How do you shrink an image?**

**Understand it like this: **Slim base, multi-stage build, clean caches, ignore the junk.

**Say this in the interview: ***"Use a slim or distroless base image, a multi-stage build so only the artifact ships, a .dockerignore to keep the build context clean, and clean package caches in the same RUN layer that created them."*

# Deployment-only practice roadmap — Docker (all flagged, all parked until your laptop session)

Every step below is deployment practice. None of it involves writing a model. The model file is always given; your work is packaging, shipping, running, and proving it runs.

```
1. Stage 1. Containerise the Lesson 6 serving app: write its Dockerfile (Lesson 6 service, uvicorn on port 8000), build the image, run it locally, and hit /health and /predict.
2. Stage 2. Prove the lifecycle by hand: logs, exec inside, stats, stop, remove, rebuild — until the commands are muscle memory.
3. Stage 3. Convert the Dockerfile to a multi-stage build and measure the image size before and after with docker images and docker history.
4. Stage 4. Add the production habits: non-root USER, .dockerignore, pinned base image, a Trivy scan, and memory and CPU limits at run time.
5. Stage 5. Tag with a semantic version plus the Git commit SHA, push to a registry (ECR, Artifact Registry, ACR, or Docker Hub), then pull and run that exact image on a clean machine or VM — the Lesson 5 cloud deployment, completed.
6. Stage 6. Run the same image with --gpus all on a GPU machine, verify with nvidia-smi inside the container, and serve the model from an NVIDIA CUDA base image.
7. Stage 7. Deliberately break and fix it: occupy the port, exhaust the disk with images, start with a wrong command — and clear each failure using the troubleshooting table above.
```

# Combined cheat sheet — Lessons 2 to 6 and Docker, on one page

- Lesson 2: check the toolbox before you cook — Python and venv, Git, Docker, kubectl and Helm, cloud CLIs, each proven by a version command and one smoke test.

- Lesson 3: six stages, one circle — data, training, evaluation, deployment, monitoring, retraining. Watch the kitchen and the food.

- Lesson 4: eval mode on, gradients off, input on the model's device. State dict for production; TorchScript compiles; quantization shrinks 4x; ONNX unifies; warm up first.

- Lesson 5: compute is about 60% of the bill. Right-size, spot for batch (up to 90% off, never for serving), reservations for steady serving, alerts at 50/80/100%. Egress is the sneaky charge.

- Lesson 6: load once, warm up, batch, cache, quantize. Blue-green flips, canary creeps, shadow copies. Two dashboards, always.

- Docker: image is the blueprint, container is the house. Stable layers first. Build fat, ship thin. Pin by digest, never latest. The company workflow is Dockerfile, build, push.

# New words from Lessons 2 to 6 and Docker — one simple line each

| **Word** | **Simple meaning** |
| --- | --- |
| State dict | Only the learned weights of a model, saved without the recipe — the production way to save in PyTorch |
| SavedModel | TensorFlow's production save format: a versioned folder with graph, weights, and settings |
| Eval mode | The serving setting (model.eval()) that switches off training-only behaviour like dropout |
| Quantization | Rounding a model's 32-bit numbers to 8-bit: 4x smaller, 2–4x faster, under 1% accuracy lost |
| ONNX | The universal model format any framework can convert to, served by ONNX Runtime |
| Warm-up | Running dummy inferences at startup so the slow first inference never hits a real user |
| Drift | Live data or answers slowly moving away from what the model trained on — quality decays silently |
| p95 / p99 latency | The wait time that 95% / 99% of users beat — shows the suffering the average hides |
| IaaS / PaaS / SaaS | Rent the kitchen / rent a stocked kitchen / order the finished meal |
| Spot instance | Spare cloud capacity at up to 90% off that can be taken back on short notice |
| Egress | The charge for data leaving the cloud — the bill that sneaks up on you |
| Canary deployment | Releasing to a small slice of traffic first — 5%, then 50%, then everyone |
| Shadow deployment | Sending a copy of live traffic to a new version whose answers are never shown |
| Image / Container | The blueprint / the running house built from it |
| Layer | One Dockerfile instruction's contribution to an image — cached and reused when unchanged |
| Registry | The warehouse and version control for images — Docker Hub, ECR, Artifact Registry, ACR, Harbor |
| Digest | An image's unchanging fingerprint (sha256:…) — pin production to it, not to a moving tag |
| Multi-stage build | Building in a fat stage and shipping only the finished artifact in a thin final image |

# What is next

Module 1 has one lesson left: Lesson 8 — API Development. After that, the parked deployment practice (Lessons 5 and 6 builds, then the seven Docker stages above) turns this document from reading into proof.

- **Done: **Module 1, Lessons 1 to 6 — plus the Docker deep-dive: understood from zero, in simple words, interview-ready.

- **Next: **Module 1, Lesson 8 — API Development.

*Sources for these chapters: Lessons 02 to 07 of Module 01 in the ai-infra-engineer-learning curriculum, as taught in this course — https://github.com/ai-infra-curriculum/ai-infra-engineer-learning*

**MODULE 1 - LESSON 8 (THE LAST LESSON OF MODULE 1)**

**Lesson 8 - API Development: the waiter between the world and your model**

This lesson is special for you: building an API is deployment work. A model sitting in a file does nothing for anyone. The API is what puts it on the internet so real users can use it. Same rule as always in this book: story first, technical word second, and a line to remember at the end of every idea.

# Part 1 - What is an API, really?

Remember the restaurant from Lesson 1: the model is the chef, the infrastructure is the restaurant. An API is the waiter. A customer - a user, an app, another system - never walks into the kitchen and talks to the chef directly. They talk to the waiter, in a fixed format: one photo of a cat, please. The waiter carries it to the kitchen, the chef cooks, the waiter brings the answer back. That fixed format is the whole idea.

API stands for Application Programming Interface. In plain words it means: the agreed way one program talks to another program. A menu with fixed dishes and fixed prices. You cannot order off-menu - and that is a feature, not a bug. It keeps both sides sane.

## The 6 jobs of an ML API

```
1. Takes input in - a photo, some text, a row of numbers.
2. Runs the model on it - that is inference, the exam, from Lesson 1.
3. Returns the prediction - that is a tabby cat, 87% sure.
4. Handles errors gracefully - bad photo, wrong format, model down - and says so politely instead of crashing.
5. Scales - handles many customers at once without falling over.
6. Watches itself - logs and metrics, so you know it is healthy. That is the Lesson 6 dashboard idea, built into the API itself.
```

## Why FastAPI wins for ML

| **Framework** | **Speed** | **Async** | **Auto docs** | **Type safety** |
| --- | --- | --- | --- | --- |
| FastAPI | Fastest class | Yes | Yes - free | Yes |
| Flask | Slower | No | Manual | No |
| Django | Slower | No | Good | No |
| Tornado | Fast | Yes | Manual | No |

- **Fast. **One of the quickest Python frameworks - every millisecond of latency is money.

- **Async. **It can juggle many customers at once instead of serving them strictly one by one. Part 4 unpacks this properly.

- **Free documentation. **Visit /docs and you get a web page where anyone can try the API in their browser. No separate documentation to write and keep updated.

- **Type safety. **It checks the order form before the kitchen sees it. Wrong type or missing field, and the customer gets a polite no immediately instead of a crash later.

```
One line to remember: An API is the waiter between the world and your model - fixed menu, polite errors, many customers at once.
Deployment practice - flagged: This entire lesson is deployment practice. The hands-on build - writing the API and running it - is the parked practice from Lesson 6, now with the full code. When you are at your laptop, we build it for real.
```

# Part 2 - Your first API, line by line

An API needs two things: the code that defines it, and a server that runs it. FastAPI is the code - the recipe for the waiter. Uvicorn is the server - the actual waiter on duty, standing at the door, taking orders. You write the menu with FastAPI; you open the restaurant with Uvicorn.

## Hello world, in 6 lines

```
from fastapi import FastAPI
```

```
app = FastAPI()
```

```
@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

Read it in plain words. Line 1: bring in the FastAPI toolbox. Line 3: create the app - open a restaurant. Line 5: @app.get("/") is a decorator - a sticky note on the next function that says: when someone asks for the front door (/), run this function. GET is the simplest kind of request: give me something. The function answers with a small package like {"message": "Hello World"}. That package format is called JSON - just text shaped like a labelled box, the standard way programs hand data to each other.

You start it with one command: uvicorn app:app --reload. That means: run the app object from the file app.py, and --reload means restart automatically when the code changes while you are practising. The API now lives at http://localhost:8000/ - localhost means this computer, and 8000 is the port, the door number.

**The free menu. **Go to http://localhost:8000/docs and FastAPI has already built a web page listing every dish, with a Try it button for each. No documentation to write. This page is called Swagger UI - remember it as the free menu. A second, prettier version lives at /redoc. Same menu, different layout.

## The health check

Every real API has a /health endpoint - a tiny function that answers {"status": "healthy"}. It is the waiter saying: yes, I am awake. Kubernetes uses exactly this for its liveness probes (Lesson 6): if /health stops answering, Kubernetes restarts the container. Two lines of code, and it is how the whole system knows you are alive.

## Three ways a customer orders

- **Path parameter - **The choice is baked into the address itself. /models/resnet18 means: tell me about the model named resnet18. The name is part of the road you are walking on.

- **Query parameter - **Extra notes stuck on the end after a question mark. /predict?model=resnet50&top_k=10 means: predict, using model resnet50, and give me the top 10 answers. The & separates the notes. top_k just means: how many best answers do you want back.

- **Request body (POST) - **When the order is too big or too private for the address bar, the customer puts it in an envelope. POST is the request type for: here, take this. The envelope in FastAPI is described with a Pydantic model - a form with labelled blanks. Pydantic is the bouncer: it checks the form before the kitchen sees it. Wrong type, missing field, or number out of range, and the customer gets a polite 422 error - your form is wrong, here is exactly what is wrong - before anything bad can happen.

**File upload. **Photos do not fit in an address bar or a text form. FastAPI handles them with UploadFile: the customer attaches the file like an email attachment, and your code reads it with await file.read(). The await is a promise: I will wait for the file to finish arriving - without freezing the whole restaurant. That is the async idea peeking in; Part 4 explains it properly.

```
One line to remember: FastAPI writes the menu, Uvicorn runs the restaurant, and every order arrives one of three ways - in the address, after a ?, or in an envelope.
```

# Part 3 - The complete prediction API: a real one, with a model inside

This is the heart of the lesson. The full example is an image-classification API: a customer uploads a photo of a cat, the API answers: tabby cat, 87% sure. The model is ResNet-18 - a famous pre-trained image model, the same one from Lesson 4. You do not train it here; you download it ready-made and serve it. That is deployment.

## Load once, serve forever

The single most important rule in this whole lesson: the model is loaded once, when the server starts, and then kept in memory for every request after. The lesson does this with a startup event - code that runs one time when Uvicorn opens the restaurant, before the first customer arrives. It picks the device (GPU if there is one, CPU if not), loads ResNet-18, sets it to eval mode (the Lesson 4 trap - forgetting eval() gives silently wrong answers), and prepares the image recipe: resize to 256, crop the middle 224 pixels, convert to numbers, normalise them.

Why once? Loading a model takes seconds and gigabytes. If you loaded it fresh for every photo, each customer would wait seconds and your server would melt. Load once, answer thousands of times. This is the exact same rule from Lesson 6 - load once at startup, plus warm-up - now you see the real code for it.

## The three endpoints

- **/ - **The front door. Answers with the service name, version, and a list of the other doors. A polite receptionist.

- **/health - **The health check from Part 2, but smarter now: it also reports whether the model is actually loaded (model_loaded: true) and which device it is on. Kubernetes reads this. If the model failed to load, this door says so.

- **/predict - **The real work. A POST: the customer uploads an image file and optionally says top_k=3 (give me the 3 best guesses). The function runs six steps - exactly the serving flow from Lesson 6: validate the file type, read the photo, preprocess it, run inference, pick the top answers, and return them with a confidence number and the time taken in milliseconds.

A real answer looks like this: tabby cat 0.87, egyptian cat 0.09, tiger cat 0.03, model resnet18, inference time 45.23 ms. The three numbers add up to roughly 1 - they are probabilities, the model's way of saying how sure it is.

## Errors, politely

| **Status code** | **Plain meaning** | **When you see it** |
| --- | --- | --- |
| 400 | Your fault, politely | The customer sent a file that is not a JPEG or PNG. Answer: Invalid file type. The request was bad. |
| 422 | Your form is wrong | Pydantic rejected the input before your code ran - wrong type, missing field, or value out of range. |
| 500 | My fault, sorry | Something broke on the server side. The error is written to the log; the customer gets a clean internal server error, not a crash dump. |
| 503 | Not ready yet | The model has not finished loading and a customer knocked early. Answer: service is starting up, please try again. |
| 429 | Too many orders | Rate limit exceeded - see Part 4. Slow down and try again in a moment. |

That graceful failure is the difference between a demo and a production system: the production one never crashes in the customer's face.

## Pydantic, the bouncer, in full

Part 2 introduced the form-checker. Here it grows up. The request model declares: top_k must be between 1 and 10 (ge=1, le=10 - greater-or-equal, less-or-equal), threshold between 0 and 1, the image URL must start with http:// or https://, and the model name must be one of exactly three allowed models (resnet18, resnet50, mobilenet_v2). Break any rule and FastAPI refuses the order before your code ever runs, with a message pointing at the exact broken field. You write the rules once, in plain declarations, and never write if-checks for them again.

```
One line to remember: Load the model once at startup, answer every request from memory, and never let a bad input or a crash reach the customer raw.
```

# Part 4 - Making it production-ready: async, background work, metrics, versions, limits, and how it really runs

Parts 1 to 3 built a working API. A working API is a demo. This part is what turns the demo into something a company can trust with real customers: it stays fast when many people arrive at once, it does its paperwork after answering instead of before, it reports its own health in numbers, it can change without breaking old customers, it refuses abuse politely, and it runs under a proper manager in production. Every one of these is deployment work - this is your job description, written as code.

## Async - one waiter who never stands still

Start with a picture. A synchronous waiter takes one table's order, walks to the kitchen, and stands there doing nothing until the food is ready. Only then does he serve the next table. If cooking takes ten seconds, every other customer waits, even though the waiter himself is free. That is a synchronous (sync) endpoint: one request blocks the worker until it fully finishes.

An asynchronous (async) waiter takes the order, hands it to the kitchen, and immediately goes to serve other tables while the food cooks. When the dish is ready, he comes back for it. In FastAPI you get this waiter by writing async def instead of def, and by writing await at each waiting point - await file.read() means: while this file is arriving, go and serve someone else; come back when it is here.

| **Style** | **What happens while waiting** | **Best for** |
| --- | --- | --- |
| Sync (def) | The worker is blocked - nobody else is served | Quick CPU work that finishes immediately |
| Async (async def + await) | The worker serves other requests during every wait | Reading uploads, calling databases or other services - any waiting on input/output |

One honest catch, and it matters for ML: inference itself is heavy maths, not waiting. Running it inside the async function would still block the waiter - the kitchen work happens in his hands. So the lesson hands CPU-bound work to a thread pool: loop.run_in_executor(None, model.predict, contents). In plain words: give the heavy parcel to a helper worker, keep the waiter free to greet customers, and await the result. Rule of thumb: waiting work goes async; heavy maths goes to a thread pool (or, at real scale, to a dedicated serving process - Lesson 6).

```
One line to remember: Async does not make the cooking faster. It stops the waiter from standing idle while the cooking happens.
```

## Background tasks - answer first, paperwork after

Some work must happen for every prediction, but the customer does not need to wait for it: writing the prediction to a log, saving it to a database, sending a metric. FastAPI's BackgroundTasks lets you attach that work to the response: the answer goes back to the customer immediately, and the paperwork runs right after, in the same process.

```
from fastapi import BackgroundTasks
```

```
def log_prediction(image_id: str, prediction: str):
    logger.info(f"Image {image_id}: predicted {prediction}")
```

```
@app.post("/predict")
async def predict(file: UploadFile = File(...),
                  background_tasks: BackgroundTasks):
    result = await run_inference(file)
    background_tasks.add_task(log_prediction,
        image_id=file.filename, prediction=result["class"])
    return result   # sent now; the logging runs just after
```

Keep background tasks small and non-critical - logging, metrics, a notification. Anything the business cannot afford to lose (billing, a database write that must succeed) belongs in a proper job queue, not in a background task that dies silently if the server restarts.

```
One line to remember: If the customer does not need to wait for it, do not make them wait for it - but never hide critical work in a background task.
```

## Monitoring - the API reports its own numbers

Lesson 6 said: watch two dashboards. This is where the numbers come from. The API exposes a /metrics endpoint, and Prometheus (the collector from Lessons 1 and 6) scrapes it on a schedule. The lesson defines three Prometheus instruments, and each one answers a different question:

| **Instrument** | **What it counts or measures** | **Question it answers** |
| --- | --- | --- |
| Counter - ml_predictions_total, labelled by model and status (success / error) | Predictions, split into successes and errors - a counter only ever goes up | How much traffic, and how much of it is failing? |
| Histogram - ml_prediction_latency_seconds, labelled by model | How long predictions take, spread across time buckets - this is what p50 / p95 / p99 are calculated from | How fast are we, including the worst 1 in 100? |
| Histogram - ml_prediction_confidence, labelled by model | The confidence scores the model gives its answers | Is the model getting unsure? (The food dashboard, not the kitchen.) |

The wiring matters as much as the instruments: record success inside the try, record error inside the except, and record latency in a finally block - so failures are timed too, not just successes. A dashboard built only from successful requests is a dashboard that lies exactly when things break.

Alongside metrics, the lesson uses structured logging: every log line is a small JSON package with a timestamp, a level (INFO, ERROR), the message, and a request_id when there is one. Plain text logs are fine for a human reading one server. JSON logs are what machines search when there are fifty servers and one customer complaint to trace.

```
One line to remember: Metrics tell you something is wrong; structured logs tell you what. You need both, and latency gets recorded even - especially - when the request fails.
```

## API versioning - change the menu without starving the regulars

Your API will change. A better model arrives, a new feature appears - say, asking the model to also return its internal numbers (return_embeddings). If you change the existing doors, every old app that uses them breaks on the same morning. So you do not change the doors. You build a new wing: /v1 keeps working exactly as before, /v2 serves the new behaviour, and customers migrate when they are ready.

In FastAPI this is done with an APIRouter - a mini-menu with its own prefix. v1_router carries prefix /v1, v2_router carries /v2, and the app includes both routers. Version 2 in the lesson adds a model choice (default resnet50) and the return_embeddings flag, while version 1 stays untouched for existing clients.

```
v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")
app.include_router(v1_router)
app.include_router(v2_router)
# POST /v1/predict  - the original behaviour, unchanged
# POST /v2/predict  - new model default + return_embeddings
```

```
One line to remember: Never break an old customer to serve a new feature. Add a version; retire the old one only when nobody is left using it.
```

## Rate limiting - the polite bouncer at the door

Without a limit, one runaway script - or one attacker - can place ten thousand orders a minute and starve every real customer. A rate limit is a simple rule: this many requests, per customer, per time window. The lesson's version allows 100 requests per 60 seconds per IP address. Cross the line and the answer is status 429 - Too Many Requests - with a message saying what the limit is.

The lesson's limiter keeps a list of recent request times per IP address in memory, throws away entries older than the window, and counts what is left. That is fine for one server and for learning. The lesson is explicit about production: use Redis - a shared memory store - instead, because with four servers each keeping its own list, a customer quietly gets four times the limit.

```
One line to remember: A rate limit protects your real customers from your loudest one. In production the counting must be shared (Redis), or the limit is fiction.
```

## The documentation, finished properly

Part 2's free menu can be customised: the lesson replaces the auto-generated OpenAPI description with a proper one - what the API does, its features, the rate limits, and a contact. This sounds cosmetic; it is not. The /docs page is the contract every other team builds against. If the limits and behaviour are not written there, they will be discovered in production, the hard way.

## How it actually runs in production - workers and Gunicorn

In development you ran: uvicorn app:app --reload. Reload - restart on every code change - is a practice tool, never a production setting. Production runs look like this:

```
# Production, Uvicorn alone:
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4 \
  --limit-concurrency 1000 --timeout-keep-alive 5
```

```
# Production, Gunicorn managing Uvicorn workers:
gunicorn app:app --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 --timeout 120
```

- **--host 0.0.0.0 - **0.0.0.0 means: listen on every network door of this machine, not just localhost. Without it, nobody outside the machine can reach the API.

- **--workers 4 - **A worker is a full separate copy of your app process, with its own waiter. Four workers means four requests can truly proceed in parallel on four CPU cores. One worker is one queue, however async it is.

- **--limit-concurrency / --timeout-keep-alive - **A ceiling on simultaneous connections, and how long an idle connection is kept open. Guardrails, set deliberately instead of inherited by accident.

- **Gunicorn - **Gunicorn is the manager: it starts the workers, watches them, restarts any that die, and spreads requests across them. Uvicorn workers do the actual serving. Manager plus waiters - that is the whole picture.

**Watch out: **One ML-specific warning that the raw commands hide: every worker loads its own copy of the model at startup. Four workers serving a 2 GB model need roughly 8 GB of GPU (or RAM) just for the copies, before a single request arrives. Worker count is a capacity decision and a memory bill at the same time - size it, do not copy-paste it.

```
One line to remember: Development is one waiter with auto-restart. Production is a manager (Gunicorn), several waiters (workers) - and every waiter carries a full copy of the model in memory.
Deployment practice - flagged: Lesson 8's build - the complete prediction API from Part 3, run the production way - is deployment practice, and it completes parked practice from Lesson 6. Parked until your laptop session, together with the Lesson 5 cloud VM deployment and the Docker stages. No model writing anywhere in it: the model is downloaded ready-made; everything else is serving.
```

That closes Module 1. You now hold the full foundation: what ML infrastructure is, the toolbox, the model's six-stage life, the two frameworks, the cloud and its bill, serving, Docker, and the API that ties serving to real users.

# Interview questions - Lesson 8

The first seven are the lesson's own self-check questions. The last four come straight from Parts 1 to 4 of this chapter - the questions a serving interview actually opens with.

**Q1. What are the advantages of FastAPI over Flask for ML serving?**

**Understand it like this: **Flask is a single waiter who writes his own menu and never checks the order form. FastAPI is the fast waiter with a printed menu and a bouncer.

**Say this in the interview: ***"FastAPI is significantly faster, supports async endpoints natively so one worker can handle many concurrent requests, generates interactive documentation automatically with Swagger UI, and validates requests through Pydantic type checking - so malformed input is rejected before it reaches the model. Flask needs extensions or manual code for each of those."*

**Q2. How does Pydantic help with input validation?**

**Understand it like this: **Pydantic is the bouncer with a checklist: every field, its type, and its allowed range, checked before the kitchen ever sees the order.

**Say this in the interview: ***"I declare a request model with fields, types, and constraints - for example top_k between 1 and 10, a threshold between 0 and 1, an allow-list of model names. FastAPI validates every incoming request against it automatically and returns a 422 with the exact broken field if validation fails, so my endpoint code only ever sees clean input and I write no manual if-checks."*

**Q3. What is the difference between sync and async endpoints?**

**Understand it like this: **Sync is the waiter who stands at the kitchen counter until the dish is ready. Async is the waiter who serves three other tables while it cooks.

**Say this in the interview: ***"A sync endpoint blocks its worker for the whole request, including every wait. An async endpoint uses await at waiting points - reading an upload, calling a database - so the worker serves other requests during the wait. For CPU-bound work like inference, async alone does not help; I offload that to a thread pool with run_in_executor, or to a dedicated serving process."*

**Q4. How do you handle file uploads in FastAPI?**

**Understand it like this: **Photos arrive as attachments, not as text in a form.

**Say this in the interview: ***"I declare the parameter as UploadFile with File(...), read it asynchronously with await file.read(), validate the content type, decode it, preprocess it, and run inference. I also enforce size and type limits so a wrong or hostile file is rejected with a 400 before it costs any compute."*

**Q5. What metrics should you track for an ML API?**

**Understand it like this: **The same two dashboards as Lesson 6 - the API is simply where the numbers are born.

**Say this in the interview: ***"A counter of predictions labelled by model and status, so traffic and error rate are visible per version; a latency histogram, which gives p50, p95, and p99; and a histogram of prediction confidence, which is the model-quality signal - a falling confidence trend warns of drift while every server metric is still green. I record latency in a finally block so failed requests are timed too."*

**Q6. How do you implement API versioning?**

**Understand it like this: **You do not repaint the old doors. You build a new wing and let the regulars move when they are ready.

**Say this in the interview: ***"With APIRouters per version: a v1 router with prefix /v1 keeps the original behaviour untouched, a v2 router with prefix /v2 carries new parameters and features, and the app includes both. Existing clients keep working, new clients opt into v2, and v1 is retired only when its traffic reaches zero."*

**Q7. What is the difference between Uvicorn and Gunicorn?**

**Understand it like this: **Uvicorn is the waiter. Gunicorn is the manager who hires four waiters, watches them, and replaces any who fall over.

**Say this in the interview: ***"Uvicorn is the ASGI server that actually runs a FastAPI app - it is the serving process itself. Gunicorn is a process manager: in production I run Gunicorn with Uvicorn worker class, so Gunicorn spawns, supervises, and restarts multiple Uvicorn workers and spreads traffic across them. Development is Uvicorn alone with --reload; production is workers under supervision, with no reload."*

**Q8. Why do you load the model once at startup instead of per request?**

**Understand it like this: **You would not hire and train a new chef for every single order.

**Say this in the interview: ***"Loading takes seconds and gigabytes of memory; a request budget is milliseconds. Loading per request would multiply latency and exhaust memory under any real traffic. I load once in a startup event, set eval mode, warm the model up with dummy inferences, keep it in memory, and have /health report model_loaded so orchestration knows the truth."*

**Q9. What do status codes 400, 422, 429, 500, and 503 each tell you?**

**Understand it like this: **Each number says whose problem it is and what to do next - the politest debugging tool the API gives you.

**Say this in the interview: ***"400: the request itself is bad, for example an unsupported file type. 422: validation failed - a field is missing, mistyped, or out of range. 429: the client exceeded the rate limit. 500: the server failed - I log it and return a clean error, never a stack trace. 503: the service is not ready, typically because the model is still loading."*

**Q10. How do you protect an ML API from being overwhelmed?**

**Understand it like this: **A bouncer with a clicker at the door, plus enough waiters inside - and honesty about what each layer does.

**Say this in the interview: ***"Rate limiting per client - the lesson uses 100 requests per 60 seconds per IP, counted in Redis in production so the limit holds across servers - plus concurrency limits at the server, multiple workers, autoscaling at the platform level, and caching for repeated requests. Rate limiting is the first line, not the whole defence."*

**Q11. Your API is in production. A new model version needs a new request field. Walk me through the release.**

**Understand it like this: **New wing, old wing untouched, customers migrate on their own schedule - the deployment strategies from Lesson 6 applied to the API itself.

**Say this in the interview: ***"I ship it as /v2: a new router, the new field added to the Pydantic model with a safe default where possible, /v1 unchanged for existing clients. The new model itself rolls out behind the endpoint with a canary or shadow strategy, metrics compared per version, and the docs updated so the contract is public. v1 is retired only after its traffic is zero."*

# Self-test - Lesson 8 (say the answers out loud)

```
1. What is an API, in the restaurant picture? What are its 6 jobs?
2. FastAPI writes the menu; what runs the restaurant? What command starts it, and where is the free menu?
3. Name the three ways a request carries data, with an example of each.
4. Why load once at startup? What else must the startup step do? (Hint: device, eval, image recipe.)
5. A customer sends a .gif file. Which status code, and whose fault is it? The model is still loading and a request arrives - which code now?
6. Sync versus async in one waiter sentence. Where does heavy inference go, and why?
7. Name the three Prometheus instruments in this lesson and the question each one answers.
8. Why Redis for rate limiting in production? What status code says the limit was crossed?
9. Four workers, 2 GB model - how much memory just for model copies? Why does that number belong in a deployment decision?
```

# Lesson 8 cheat sheet - on one page

- API = the waiter: fixed menu, polite errors, many customers at once. FastAPI defines it; Uvicorn serves it; Gunicorn manages Uvicorn workers in production.

- Three doors on every real ML API: / (receptionist), /health (alive + model_loaded + device - what Kubernetes probes read), /predict (the work).

- Orders arrive three ways: path (in the address), query (after the ?), body (the POST envelope, checked by Pydantic - the bouncer; failure = 422).

- Load once at startup: pick device, load model, eval(), prepare preprocessing, warm up. Never load per request.

- Status codes: 400 bad request, 422 form wrong, 429 too many requests, 500 server fault (log it, answer clean), 503 model not ready.

- Async for waiting (await), thread pool for heavy maths (run_in_executor). BackgroundTasks for paperwork after the answer - never for critical work.

- Metrics: predictions counter (model, status), latency histogram (p50/p95/p99 - recorded in finally), confidence histogram (the food dashboard). Plus JSON structured logs with request_id.

- Version with routers: /v1 untouched, /v2 new. Rate limit per client (lesson: 100 per 60s); count in Redis when there is more than one server.

- Workers are parallel copies of the app - and each one carries a full copy of the model. Worker count = parallelism AND memory bill.

# New words from Lesson 8 - one simple line each

| **Word** | **Simple meaning** |
| --- | --- |
| API / endpoint | The agreed way programs talk / one specific door of that API, like /predict |
| JSON | Text shaped like a labelled box - the standard package programs hand each other |
| Decorator | A sticky note (@app.get) that connects a function to a door and a request type |
| GET / POST | Give me something / here, take this - the two request types you will use daily |
| Path / query parameter | A choice inside the address itself / extra notes after the ? in the address |
| Pydantic | The bouncer: a declared form that validates every request before your code runs |
| Swagger UI (/docs) | The free interactive menu FastAPI generates - try every endpoint from the browser |
| Async / await | Juggling other customers while waiting / the exact point where the waiter may step away |
| Thread pool (run_in_executor) | Helper workers who take heavy maths off the async waiter's hands |
| Background task | Paperwork that runs just after the answer is sent - logging, metrics, notifications |
| Rate limiting (429) | A per-customer order cap per time window; crossing it answers Too Many Requests |
| APIRouter / versioning | A mini-menu with a prefix (/v1, /v2) / running old and new menus side by side |
| Worker | One full copy of the app process serving in parallel - with its own copy of the model |
| Structured logging | Log lines as JSON packages (timestamp, level, message, request_id) that machines can search |

# What is next

Module 1 is complete: all eight lessons, plus the Docker deep-dive. Per the track plan, the deep path continues with Module 5 (skim), then Module 6 (MLOps), Module 7 (GPU computing), Module 10 in depth (LLM infrastructure), and Project 3 - the LLM Deployment Platform - as the capstone. The parked deployment practice is ready whenever you are at your laptop: the Lesson 5 cloud VM deployment, the Lesson 6 + Lesson 8 serving API build, and the seven Docker stages.

- **Done: **Module 1, Lessons 1 to 8 - plus the Docker deep-dive: understood from zero, in simple words, interview-ready.

- **Next: **Module 5 (skim), on the way to Modules 6, 7, and 10 and Project 3.

*Source for this chapter: Lesson 08, API Development for ML Services, in the ai-infra-engineer-learning curriculum - https://github.com/ai-infra-curriculum/ai-infra-engineer-learning*
