# Module 2 — AWS & Terraform: DevOps Interview Notes

**MODULE 2  •  CLOUD COMPUTING — REDEFINED**

**AWS & Terraform**

DevOps Interview Notes — Complete

AWS completely. Terraform completely. Nothing else.
Every service explained the DevOps way: what it is, when to use it,
how it fails, how you secure it, how you monitor it —
and how you build it in Terraform and defend it in an interview.

> How this book is different: This is not a cloud survey. GCP, Azure and multi-cloud from the original Module 2 are deliberately out. Depth on AWS + Terraform is what DevOps, Platform, SRE and Cloud Engineer interviews in the US actually test. If you can explain it here and build the labs in Part E, you can claim it on a résumé.

> Separate document: Module 1 (68 pages, Lessons 1–8 + Docker) is untouched and stays separate, exactly as requested. This is the Module 2 book.

| **Part** | **What it covers** | **Interview payoff** |
| --- | --- | --- |
| A — AWS | IAM, VPC, compute, storage, databases, containers, serverless, observability, security, HA & cost | You can design and troubleshoot a real AWS account |
| B — Terraform | Workflow, state, backends, variables, modules, loops, lifecycle, import, testing, team working | You can write, review and safely change production IaC |
| C — Together | Production 3-tier stack in Terraform, end to end | You have one deep story to walk an interviewer through |
| D — Interview system | 20 core Q&A, scenarios, troubleshooting, system design, cheat sheets | You can say it out loud, under pressure |
| E — Practicals | Ordered labs with proof steps | No claim without evidence |

*A note on honesty: service limits, prices and console screens change. The concepts, trade-offs and Terraform patterns in this book are the durable part. Before an interview, check any exact limit or price you plan to quote on the official AWS documentation for that service.*

# How to use this book — and the DevOps mindset

An interviewer does not hire a list of services. They hire judgement: can you keep a system up, secure, and affordable, and can you change it without breaking it? Every chapter in this book is therefore built in the same six beats.

- Plain words first. What is it, in one sentence a non-expert would understand?

- Use it when / do not use it when. Every AWS service has a neighbour that looks similar. Choosing between them is the interview.

- How it fails. Timeouts, throttling, a full disk, a bad deploy, a single Availability Zone going down. DevOps is failure work.

- How you secure it. Least-privilege Identity and Access Management (IAM), encryption, private networking, no secrets in code.

- How you watch it. Logs, metrics, traces, alarms — and what you do when the alarm fires at 3 a.m.

- How you build it in Terraform. If you cannot code it, review it and roll it back, you do not operate it — you click it. Clicking does not scale and does not survive an audit.

> One line to remember: AWS is the vocabulary, Terraform is the grammar, DevOps is the judgement about what to build, how to change it safely, and how you know it is healthy.

## The roadmap — in interview order

| **Order** | **Topic** | **Why this order** |
| --- | --- | --- |
| 1 | IAM & accounts | Nothing is safe or even reachable without identity |
| 2 | VPC networking | Every later service lives inside — or outside — a VPC |
| 3 | Compute: EC2, ASG, ALB | The classic workload shape interviews start from |
| 4 | Storage & databases | State is harder than compute; data loss is unforgivable |
| 5 | Containers & serverless | ECS, EKS, Lambda — the modern workload shapes |
| 6 | Messaging & events | SQS, SNS, EventBridge decouple systems so one failure does not cascade |
| 7 | Observability & security | CloudWatch, CloudTrail, Config, KMS, WAF, Secrets Manager |
| 8 | Terraform, completely | Now rebuild everything above as code, safely, as a team |
| 9 | The capstone stack | One production architecture, explained end to end |

## Your experience is an asset — use it correctly

You bring production DevOps and site reliability experience on AWS and Azure, Kubernetes certification (Certified Kubernetes Administrator, CKA), and infrastructure work at scale. In interviews, anchor each answer in that shape: the problem, the constraint, what you chose, what broke or could break, and how you verified it. Never invent a metric, a scale figure or a tool you did not use. If you have not run a service in production, say so plainly and give your design reasoning instead — interviewers trust that distinction and punish bluffing faster than any knowledge gap.

# Part A — AWS with a DevOps mindset

## A1. AWS foundations — regions, accounts and shared responsibility

Amazon Web Services (AWS) is rented computing in data centres around the world, paid by use, controlled through an Application Programming Interface (API) — which is exactly why Terraform can manage it. Three ideas organise everything else.

- **Regions and Availability Zones. **A Region is a geographic cluster (for example us-east-1, Northern Virginia). An Availability Zone (AZ) is one or more physically separate data centres inside a Region, with independent power and networking. Design rule:

spread production across at least two, preferably three AZs. A single AZ is a single point of failure, however good the instance is.

- **Shared responsibility. **AWS secures the cloud itself — buildings, hardware, the hypervisor, the managed-service plumbing. You secure what you put in it — IAM, network rules, patching on EC2, data, encryption choices. Every security interview answer should name which side of that line the control sits on.

- **Accounts are the real blast-radius boundary. **Use separate AWS accounts for production, staging and development, grouped under AWS Organizations, with Service Control Policies (SCPs) as guardrails. One account for everything means one leaked credential or one runaway experiment can reach production data.

> DevOps mindset: Choose a Region for latency to users, service availability, data-residency law and cost — in that order of honesty. 'We used us-east-1 because the tutorial did' is not an answer. 'Closest Region that had every service we needed, with a second Region for disaster recovery' is.

## A2. IAM — the most important service in AWS

IAM decides who or what can do what, on which resource, under which conditions. Almost every AWS security incident is an IAM mistake, and almost every senior interview probes it early.

| **Concept** | **Plain meaning** | **Rule** |
| --- | --- | --- |
| User | A person (or long-lived app identity) | Humans use SSO + MFA; apps do not use users |
| Group | A bundle of users | Attach policies to groups, not individuals |
| Role | A temporary identity you assume | The default for EC2, Lambda, ECS, EKS and CI/CD |
| Policy | A JSON list of Allow/Deny statements | Least privilege: only the actions and resources needed |
| Permission boundary | A ceiling on what a role can ever get | Use in delegated-admin and multi-team accounts |

A policy statement has Effect (Allow or Deny), Action (for example s3:GetObject), Resource (an Amazon Resource Name, ARN) and optionally Condition (source IP, Multi-Factor Authentication (MFA), tags, time). Evaluation logic matters and is asked verbatim: an explicit Deny always wins; otherwise there must be an explicit Allow; if neither applies, the request is implicitly denied. Identity policies, resource policies, SCPs, permission boundaries and session policies are all evaluated together — the effective permission is the intersection, with any explicit Deny cutting through everything.

- **Roles over keys. **Prefer roles with short-lived credentials from the Security Token Service (STS) over long-lived access keys. If a key must exist, rotate it, scope it, and monitor it with CloudTrail.

- **One role per workload. **EC2 gets an instance profile, Lambda and ECS tasks get execution/task roles, GitHub Actions gets an OpenID Connect (OIDC) role — no stored AWS keys in the CI system at all.

- **Separate deploy from data access. **Split duties: a role that can deploy infrastructure should not automatically be able to read production database contents.

**Terraform — an IAM role EC2 can assume (pattern)**

```
resource "aws_iam_role" "app" {
  name = "${var.project}-${var.env}-app"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow", Action = "sts:AssumeRole"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}
resource "aws_iam_instance_profile" "app" {
  name = aws_iam_role.app.name
  role = aws_iam_role.app.name
}
```

> One line to remember: IAM answer formula: who (principal) + can do what (action) + on what (resource) + under what conditions — and explicit Deny always wins.

## A3. VPC networking — the chapter interviews are won and lost on

A Virtual Private Cloud (VPC) is your private network inside AWS. You choose its IP range (Classless Inter-Domain Routing, CIDR — for example 10.0.0.0/16, about 65,536 addresses), carve it into subnets, and control traffic with route tables, security groups and network access control lists (NACLs). If you understand this chapter deeply, half of all AWS troubleshooting becomes routine.

| **Subnet type** | **Route to internet?** | **What belongs there** |
| --- | --- | --- |
| Public | Yes — via Internet Gateway (IGW) | Load balancers, NAT gateways, bastions only |
| Private | Outbound only — via NAT Gateway | App servers, containers, workers — the default for compute |
| Isolated / data | No internet route at all | Databases, caches — reached only from the app tier |

- **Routing makes a subnet public. **Route tables decide where traffic goes. A subnet is 'public' only because its route table sends 0.0.0.0/0 to an IGW. There is no checkbox — routing is the definition.

- **Security groups. **Stateful, attached to an instance/task/load balancer, allow-rules only, evaluated as a set. Default denies inbound, allows outbound. This is your primary firewall.

- **NACLs. **Stateless, attached to a subnet, numbered allow AND deny rules evaluated in order, and you must allow ephemeral return ports. A blunt subnet-level guardrail — most teams keep NACLs permissive and do the real work in security groups, using NACL denies only for known-bad ranges.

- **Reference, do not hard-code. **Databases should never be public, and app security groups should reference the load balancer's security group — not a CIDR — so rules follow the resource, not an IP that can change.

### The rest of the network toolkit, in one pass

- **NAT Gateway. **One per AZ for production. It lets private subnets reach the internet outbound (patching, APIs) without being reachable inbound. It is AZ-scoped and costs money — a favourite cost question.

- **VPC endpoints. **Private AWS endpoints inside your VPC: interface endpoints (powered by PrivateLink, for most services) and gateway endpoints (free, for S3 and DynamoDB). They keep traffic off the public internet and cut NAT data charges.

- **Route 53. **Authoritative DNS. Public hosted zones for your domain, private zones for internal names like db.internal, plus alias records to load balancers and health-checked failover routing.

- **VPN and Direct Connect. **Managed site-to-site VPN or a dedicated private line into AWS, for office / data-centre connectivity. Direct Connect is consistent and private, but takes weeks to provision — VPN is the fast start.

- **Transit Gateway. **Connects many VPCs and VPNs through one hub instead of a mesh of peerings. VPC peering itself is point-to-point, non-transitive, and cannot overlap CIDRs.

- **VPC Flow Logs. **The full traffic log: source, destination, ports, bytes, accept/reject. Your first stop when 'it cannot connect' — after security groups.

> Troubleshooting mantra: 'Cannot connect' is checked in order: route table → NACL → security group → listener / target health → application. Walk the packet. Never guess at random layers.

> One line to remember: Public = route to an IGW. Private = route to NAT or no internet. Security groups are stateful; NACLs are stateless. That trio answers a surprising share of interview questions.

## A4. Compute — EC2, Auto Scaling and load balancing

Elastic Compute Cloud (EC2) is a virtual server: you pick an Amazon Machine Image (AMI), an instance type (CPU/RAM shape), storage, network and IAM role, and you own patching and scaling unless you automate them. Instance families in plain words: general purpose (balanced, the default), compute-optimised (CPU-heavy), memory-optimised (caches, in-memory work), storage-optimised (fast local NVMe), and accelerated (GPU).

| **Buying model** | **Use it for** | **Trap** |
| --- | --- | --- |
| On-Demand | Unpredictable, short, or first workloads | Most expensive per hour |
| Reserved / Savings Plans | Steady baseline you can commit to | You pay even if idle — commit conservatively |
| Spot | Batch, stateless workers, CI runners — interruptible | Can be reclaimed with 2 minutes' notice; never for stateful primaries |

- **Application Load Balancer (ALB). **A group of listeners forwarding to target groups. Layer-7 (HTTP/HTTPS) routing by host and path, WebSockets, and the default front door for web and API traffic.

- **Network Load Balancer (NLB). **Layer-4 (TCP/UDP), extreme performance, static IPs. For non-HTTP protocols and very high throughput.

- **Auto Scaling Group (ASG). **Replaces unhealthy instances and scales count between a minimum, desired and maximum based on alarms or schedules, across AZs. Always pair with a launch template (versioned — AMI, type, user data, security groups, IAM profile).

- **Scale on demand, not just CPU. **Target tracking on CPU is the interview baseline, but the honest production answer is scaling on a signal that represents demand — requests per target, queue depth, or a custom CloudWatch metric. CPU scaling a queue worker that is I/O-bound will disappoint you.

**First-boot scripting — user data (keep it small)**

```
#!/bin/bash
set -euo pipefail
dnf update -y
dnf install -y my-app
systemctl enable --now my-app
# Anything complex belongs in a baked AMI (Packer) or config
# management — not in a 200-line user-data script nobody tests.
```

> One line to remember: ALB thinks in HTTP, NLB thinks in packets. An ASG's job is not 'scaling' — it is self-healing across AZs, and scaling is the bonus.

## A5. Storage — S3, EBS and EFS, and never confusing them

| **Service** | **What it is** | **Use / avoid** |
| --- | --- | --- |
| S3 (Simple Storage Service) | Object storage: buckets, keys, unlimited scale, 11-nines durability design | Files, backups, static sites, data lakes, Terraform state. Not a filesystem or a database |
| EBS (Elastic Block Store) | Network disk attached to one EC2 instance (mostly) | Boot and data volumes. gp3 is the default; io2 for high-IOPS databases. Snapshot to S3 for backup |
| EFS (Elastic File System) | Shared NFS filesystem, many instances at once | Shared uploads, CMS, ML datasets. Costs more than EBS; not for Windows (use FSx) |

### S3 in depth — because it appears in every interview

- **Secure by default. **Block Public Access on, bucket policies scoped, IAM on top, and default encryption enabled. A public bucket is a career event.

- **Storage classes & lifecycle. **Intelligent-Tiering or lifecycle rules move ageing objects to cheaper classes (Standard → Infrequent Access → Glacier Instant / Flexible / Deep Archive). Retrieval time and minimum-duration charges are the trade-off you must name.

- **Versioning & Object Lock. **Overwrite/delete protection and audit history — and with Object Lock, WORM retention for compliance and ransomware defence. Versioning is not a backup by itself: a compromised credential can delete versions too.

- **Replication. **Same-Region for backup, Cross-Region for disaster recovery and residency. Replication does not retro-copy existing objects without a batch job.

- **Static hosting + CloudFront. **Serve static sites and single-page apps directly, usually behind CloudFront (the content delivery network, CDN) with Origin Access Control so the bucket itself stays private.

## A6. Databases — choose by access pattern, not by fashion

| **Service** | **Type** | **Pick it when** |
| --- | --- | --- |
| RDS (Relational Database Service) | Managed SQL — PostgreSQL, MySQL, etc. | You need relations, joins and transactions. Multi-AZ for HA; read replicas for read scale |
| Aurora | AWS-built, MySQL/PostgreSQL-compatible SQL | You need RDS behaviour with faster failover and storage that grows automatically |
| DynamoDB | Serverless NoSQL key-value / document | Massive, predictable key-based access. Design the partition key first — a bad key cannot be fixed later |
| ElastiCache (Redis / Memcached) | Managed in-memory cache | Session data, leaderboards, hot reads. It is a cache — never the only copy of truth |
| Redshift / Athena | Warehouse / query-in-place on S3 | Analytics. Athena is serverless SQL over S3 — ideal for logs and data-lake queries |

- **High availability is not backup. **Multi-AZ on RDS is synchronous standby in another AZ with automatic failover — it is a high-availability feature, not a read-scaling or backup feature. Backups and snapshots are separate, and you must test restoring them.

- **DynamoDB capacity. **DynamoDB on-demand suits spiky or unknown traffic; provisioned with auto scaling suits steady traffic and is cheaper when you can predict it. Hot partitions — one key taking most traffic — are the classic design failure.

- **Database security baseline. **Put the database in isolated subnets, allow only the app security group, require encrypted connections, rotate credentials through Secrets Manager, and take credentials out of Terraform variables and CI logs entirely.

> One line to remember: RDS Multi-AZ answers 'the AZ died'. Backups answer 'we deleted or corrupted the data'. Replicas answer 'too many reads'. Three different problems, three different tools.

## A7. Containers — ECS and EKS, honestly compared

|  | **ECS (Elastic Container Service)** | **EKS (Elastic Kubernetes Service)** |
| --- | --- | --- |
| Mental model | AWS-native container orchestrator | Managed Kubernetes control plane |
| Best when | You want the simplest path on AWS | You need Kubernetes portability, ecosystem, or have CKA-level skills |
| You manage | Task definitions, services, capacity | Node groups / Fargate, add-ons, upgrades, Kubernetes RBAC + IAM |
| Scaling | Service auto scaling on metrics | HPA, Cluster Autoscaler / Karpenter, VPA |

On either platform the vocabulary is the same: an image in Elastic Container Registry (ECR), a task/pod definition (image, CPU/RAM, ports, env, secrets, logs), a service that keeps N copies alive behind a load balancer, and a deployment strategy. Use Fargate when you want no nodes to patch; use EC2 capacity when you need specific instances, GPUs, or the lowest cost at steady scale. Scan ECR images, pin images by digest or immutable tag — never float on 'latest' in production — and send container logs to CloudWatch Logs (or your aggregator) from day one.

> Interview trap: 'Why Kubernetes?' is only answered well with a workload reason — complex scheduling, a large microservice fleet, portability, or team standardisation. For a three-container app, ECS on Fargate is usually the more honest, cheaper answer. Seniority is knowing when NOT to use EKS.

## A8. Serverless and events — Lambda, queues and decoupling

- **Lambda. **Code that runs in response to an event, billed per request and duration, scaling automatically, with a 15-minute maximum run. Perfect for APIs (with API Gateway), file processing, scheduled jobs and glue. Watch for cold starts, VPC latency, concurrency limits and cost surprises from chatty loops. Provisioned concurrency is the paid cold-start fix.

- **API Gateway. **The front door for Lambda and HTTP backends: throttling, authorisers, request validation, stages. It is also a common cost and latency layer — cache and validate there, not in code.

- **SQS (Simple Queue Service). **A durable queue. Producers send, consumers poll, visibility timeout hides a message while it is processed, dead-letter queues (DLQs) collect poison messages after N retries. This is how you survive a downstream outage without losing work.

- **SNS (Simple Notification Service). **Publish/subscribe fan-out to many subscribers (queues, Lambdas, email). SNS notifies; SQS buffers. The classic pairing is SNS → multiple SQS queues, one per consumer, so each consumer retries independently.

- **EventBridge & Step Functions. **A managed event bus with rules and targets, plus Scheduler for cron-like jobs. Step Functions orchestrate multi-step workflows with retries, waits and human approval as visible state machines — prefer them over a Lambda calling a Lambda calling a Lambda.

> One line to remember: Queues turn a hard failure into a delay. If losing the request is unacceptable, put a queue in front of it and a DLQ behind the consumer — and alarm on the DLQ, or it is just a quieter way to lose work.

## A9. Observability — you cannot operate what you cannot see

| **Signal** | **AWS tool** | **Question it answers** |
| --- | --- | --- |
| Metrics & alarms | CloudWatch Metrics + Alarms | Is it slow, saturated or erroring — right now? |
| Logs | CloudWatch Logs + Logs Insights | What exactly happened, for this request / instance? |
| Traces | X-Ray (and OpenTelemetry) | Where in the chain of services was time spent? |
| API audit trail | CloudTrail | Who called which AWS API, when, from where? |
| Config history | AWS Config | What did this resource look like yesterday? Is it still compliant? |
| Health & posture | Health Dashboard, Trusted Advisor, Security Hub, GuardDuty | What is AWS telling me about risk, threat and waste? |

The DevOps baseline for every production workload: dashboards for the four golden signals (latency, traffic, errors, saturation), alarms that are actionable and routed to a human with a runbook link, structured JSON logs with a correlation/request ID, log retention set deliberately (never 'forever by default' — cost), and CloudTrail in every account, delivered to a central, protected log account that application admins cannot alter.

> Alarm quality: An alarm with no action is noise. Every alarm should answer: what is the user impact, what is the first check, and who owns it? Page on symptoms users feel (error rate, latency, queue age), alert on causes second.

## A10. Security services — the supporting cast interviewers expect

- **KMS (Key Management Service). **Create, rotate and use encryption keys. Every S3 bucket, EBS volume, RDS instance and Secrets Manager secret should name its key strategy. Customer-managed keys give you rotation control, key policies and the ability to disable a key as an emergency brake.

- **Secrets Manager. **Stores and auto-rotates database passwords and API keys. Applications fetch at runtime via IAM — secrets never live in code, images, Terraform state in plain sight, or chat messages.

- **WAF (Web Application Firewall). **A managed firewall in front of ALB / API Gateway / CloudFront: rate limits, managed rule groups, geo and IP rules. It reduces noise; it does not fix a broken application.

- **ACM (Certificate Manager). **The certificate authority for TLS everywhere: free public certs for ALB/CloudFront/API Gateway, auto-renewed. No excuse for expired or self-signed certs on AWS load balancers.

- **GuardDuty, Security Hub & Inspector. **Threat detection over CloudTrail, DNS and flow logs; central findings and compliance checks; vulnerability scanning for EC2, ECR and Lambda.

## A11. Delivery on AWS — CI/CD the DevOps way

Whether the pipeline is GitHub Actions, GitLab CI, Jenkins or AWS CodePipeline / CodeBuild / CodeDeploy, the shape interviewers want is constant: build and test once, produce one immutable artifact (AMI, container image or zip), promote that same artifact through environments, deploy with a reversible strategy (rolling, blue/green or canary), run smoke tests, and roll back automatically on alarm. The pipeline assumes an IAM role via OIDC — no long-lived keys stored in the CI tool — and it deploys Terraform with a plan that a human (or a protected-branch rule) approves before apply in production.

- **Blue/green. **Two identical environments; traffic shifts after health checks; rollback is a traffic shift back, measured in seconds.

- **Canary. **A small percentage of traffic gets the new version first; metrics decide whether it grows or dies. The safest choice for high-traffic services.

- **Rolling. **Instances/pods are replaced in batches. Simple, but rollback is another rollout — slowest to reverse.

## A12. High availability, disaster recovery and cost — the senior layer

| **DR strategy** | **RPO / RTO shape** | **Cost** |
| --- | --- | --- |
| Backup & restore | Hours / hours | Lowest — backups in another Region |
| Pilot light | Minutes–hours / hours | Low — core data replicated, compute stood up on failover |
| Warm standby | Seconds–minutes / minutes | Medium — scaled-down copy always running |
| Multi-site active/active | Near zero / near zero | Highest — and the hardest to build correctly |

Recovery Point Objective (RPO) is how much data you can afford to lose, in time. Recovery Time Objective (RTO) is how long you can afford to be down. Never quote a strategy without both numbers, and never claim a DR plan you have not restored in a test. For cost: tag everything (owner, project, environment), review with Cost Explorer and budgets with alerts, right-size from CloudWatch data (not guesses), use Savings Plans for the steady baseline and Spot for interruptible work, lifecycle S3 aggressively, delete unattached EBS volumes and idle load balancers, and treat NAT Gateway data processing and CloudWatch Logs retention as the two surprise line items they reliably are.

> One line to remember: Availability is AZs, durability is backups and replication, and affordability is a design input — not a bill you discover at the end of the month.

# Part B — Terraform, completely

Terraform is HashiCorp's infrastructure-as-code tool: you declare the infrastructure you want in HashiCorp Configuration Language (HCL), and Terraform works out — through a provider that talks to a cloud API — what to create, change or destroy to get there. The provider for this book is AWS. Everything in Part A can be built by clicking; Terraform is how a DevOps engineer builds it the same way, fifty times, in three environments, with a reviewable diff and a rollback story.

## B1. The workflow — init, plan, apply, and why plan is sacred

| **Command** | **What it really does** | **Interview point** |
| --- | --- | --- |
| terraform init | Downloads providers/modules, configures the backend | Run in CI every time; commit the lock file (.terraform.lock.hcl) |
| terraform fmt / validate | Formats code / checks syntax and schema | Fail the pipeline on either — cheap, early |
| terraform plan | Reads state, refreshes reality, diffs desired vs actual, prints the change plan | The plan is the review artifact. No plan, no apply |
| terraform apply | Executes the approved plan, updates state | Apply the saved plan file in production, not a fresh re-plan |
| terraform destroy | Plans the removal of everything state manages | Guard it: protected branches, approvals, never in an unreviewed pipeline |
| terraform output / show / state | Reads results / inspects state | State is sensitive — treat commands on it as production access |

**The pipeline shape every interviewer recognises**

```
# PR:  fmt -> validate -> plan  (plan posted to the PR, human reviews)
# Merge to main (staging): apply the saved plan
# Production: apply the SAME saved plan, behind an approval gate
terraform init -input=false
terraform plan -out=tfplan
terraform apply tfplan        # apply exactly what was reviewed
```

> Declarative, not imperative: You do not write steps ('create a VPC, then a subnet'). You declare the end state, and Terraform builds the dependency graph — it knows the subnet needs the VPC first because the code references it. That graph is also why a rename or a careless replace can destroy and recreate a resource: the graph, not malice.

## B2. State — the single most important Terraform concept

State (terraform.tfstate) is Terraform's record of what it manages: each resource in code mapped to a real ID in AWS, plus attributes. Without state, Terraform cannot diff, update or destroy correctly — it would create duplicates on every run. Three rules follow, and they are non-negotiable in production.

- **Never local in a team. **Local state on a laptop means one person, no locking, and a lost laptop is lost infrastructure control. Production state lives in S3, encrypted, versioned, with access logged.

- **Always lock. **When two applies run at once they can corrupt state or double-create. S3 state with DynamoDB locking (the classic pattern) — or the backend's native lock — serialises applies. Newer Terraform / S3 configurations add native S3 locking; name the pattern you use and why locking matters, not just the service.

- **State is sensitive data. **State contains secrets in plain text — database passwords it set, generated keys. Restrict the bucket, encrypt it (KMS), version it (recovery from a bad write), and never print it in CI logs or commit it to git. Ever.

**Terraform — remote state on S3 with locking (backend block)**

```
terraform {
  backend "s3" {
    bucket       = "mycompany-tfstate-prod"
    key          = "apps/web/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    dynamodb_table = "terraform-locks"
    kms_key_id   = "alias/terraform-state"
  }
}
# Bootstrap problem: the bucket/table must exist BEFORE init.
# Create them once with a tiny bootstrap config (or manually),
# then never manage the state bucket from the state inside it.
```

- **Drift. **Someone changed a resource in the console; the next plan shows the diff and either reverts it (apply) or you accept it into code. Drift is information — a recurring drift pattern means your code is not the real source of truth, and that is a process bug.

- **Import. **terraform import (or import blocks in newer versions) maps an existing AWS resource into state so Terraform can manage it. You still must write matching configuration — import brings it under management, it does not generate good code for you.

> One line to remember: Code says what should exist. State says what Terraform believes exists. The AWS API says what actually exists. A plan is the three-way conversation between them.

## B3. Language essentials — variables, outputs, locals, data sources

| **Block** | **Purpose** | **Good practice** |
| --- | --- | --- |
| variable | An input to the config | Type it, describe it, validate it, default only when a default is safe |
| output | A value the config publishes | Mark secrets sensitive = true; outputs are how modules talk |
| locals | Named, computed values inside the config | Build names/tags once: local.name = "${var.project}-${var.env}"  |
| data | Read an existing thing (AMI, AZs, caller identity, SSM parameter) | Prefer data sources over hard-coded IDs that differ per account/Region |
| resource | A thing Terraform creates and manages | One responsibility per resource; reference, never copy-paste IDs |

**Variables with validation — fail fast, in the plan**

```
variable "environment" {
  type        = string
  description = "Deployment environment"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging or prod."
  }
}
variable "db_password" {
  type      = string
  sensitive = true   # still in state — see B2. Never commit a tfvars with it.
}
data "aws_availability_zones" "available" { state = "available" }
data "aws_ami" "app" {
  most_recent = true
  owners      = ["self"]
  filter { name = "tag:Role" values = ["app"] }
}
locals {
  name = "${var.project}-${var.environment}"
  tags = { Project = var.project, Environment = var.environment, ManagedBy = "terraform" }
}
```

- **Variable files. **terraform.tfvars and *.auto.tfvars hold environment values; secrets come from the CI secret store or environment variables (TF_VAR_…), never from a committed tfvars file. .gitignore covers state, plans, crash logs and secret tfvars from the first commit.

## B4. Reuse — count, for_each, conditionals and modules

| **Tool** | **Use it for** | **Watch out** |
| --- | --- | --- |
| count | N identical things, toggled features (count = var.enable ? 1 : 0) | Removing a middle item re-indexes and can recreate later items |
| for_each | Sets/maps of named things — subnets per AZ, users, buckets | Stable keys = stable resources. The production default over count |
| Dynamic blocks | Repeated nested blocks (security-group rules, listeners) | Powerful but hard to read — use sparingly, comment generously |

- **Modules are the product. **A module is a reusable package of resources with inputs and outputs — a VPC module, an 'app service' module — versioned in git or a registry and consumed the same way in every environment. The golden rule: a module does one coherent job, exposes the few knobs callers truly need, and hides everything else. Copy-pasting a VPC block into five repos is not reuse; it is five future incidents.

**for_each over AZs — subnets that survive change**

```
resource "aws_subnet" "private" {
  for_each          = { for i, az in data.aws_availability_zones.available.names : az => i }
  vpc_id            = aws_vpc.main.id
  availability_zone = each.key
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, 10 + each.value)
  tags = merge(local.tags, { Name = "${local.name}-private-${each.key}", Tier = "private" })
}
```

## B5. Safe change — lifecycle, moves, replaces and the dangerous commands

- **lifecycle { … } **create_before_destroy (new before old dies — zero-downtime replaces), prevent_destroy (refuse to destroy this — databases, state buckets), ignore_changes (let an external system own an attribute, e.g. ASG desired count under auto scaling).

- **Refactoring without downtime. **moved blocks declare 'this resource is now that resource' so a refactor renames in state instead of destroying and recreating. removed / import blocks do the same for giving up or adopting resources, as code, in review.

- **Replace and state surgery. **terraform plan -replace=… (modern taint) forces one resource's recreation with a visible plan. terraform state rm / mv are surgery: powerful, occasionally necessary, always after a state backup and never as a first resort.

- **Partial applies. **If apply fails halfway, state records what did succeed. Fix the cause, re-plan, re-apply — Terraform converges. Do not hand-edit state JSON unless you have exhausted every other option and taken a backup first.

> The destroy question: Interviewers love asking how you stop Terraform destroying a production database. Layered answer: prevent_destroy on the resource, deletion protection on the RDS instance itself, a separate state for data vs app (see B6), approval gates on prod applies, and backups tested by restore. No single switch is the answer.

## B6. Structuring real projects — environments, layering and teams

**A layout that scales past one engineer**

```
infra/
  bootstrap/          # state bucket + lock table (applied once)
  modules/
    vpc/  app-service/  rds-postgres/    # versioned, tested, documented
  live/
    dev/     vpc/  app/  data/          # small states, one per layer
    staging/ vpc/  app/  data/
    prod/    vpc/  app/  data/          # prod app state cannot destroy prod data
# Rules: small states (blast radius + speed), one backend key per state,
# environments differ by tfvars — never by forked code,
# providers and modules pinned to versions, lock file committed.
```

- **Pin everything. **Provider and module versions are pinned, the lock file is committed, and upgrades are deliberate pull requests with a plan reviewed — not a surprise on a Monday apply.

- **Terraform in CI/CD. **A pull request runs fmt, validate and plan; the plan is posted for review; apply happens on merge, from the saved plan, with OIDC credentials; production adds an approval and a restricted branch. Terraform Cloud / an Atlantis-style runner are valid answers for where this runs.

- **Testing and policy. **terraform validate and fmt in CI, tflint for lint rules, Checkov/tfsec-style scanning for security policy (public S3, open security groups, unencrypted volumes), and native terraform test / policy-as-code (Sentinel / Open Policy Agent) for guardrails in larger organisations.

> One line to remember: Small states, pinned versions, reviewed plans, saved-plan applies, OIDC credentials. That sentence is a complete senior answer to 'how does your team run Terraform?'

## B7. Terraform + AWS patterns you must be fluent in

| **Pattern** | **What Terraform wires together** | **Gotcha** |
| --- | --- | --- |
| VPC foundation | VPC, subnets per AZ (for_each), IGW, NAT per AZ, route tables, endpoints, flow logs | Single NAT for prod = single point of failure and cross-AZ traffic charges |
| Front door | ACM cert → ALB (HTTPS listener, HTTP→HTTPS redirect) → target group → ASG / ECS service | Health-check path must be a real, cheap endpoint like /health |
| Secrets without secrets in code | Secrets Manager secret (value set outside Terraform) → IAM policy → ECS task / Lambda env reference | If Terraform sets the secret value, it lands in state |
| State backend | S3 (versioned, encrypted, public access blocked) + lock table — built by bootstrap | Chicken-and-egg: bootstrap cannot use the backend it creates |
| Logs by default | Log group with retention + the resource pointed at it, in the same change | No retention set = an unbounded bill in six months |

## B8. Terraform troubleshooting — the failure catalogue

| **Symptom** | **Likely cause** | **Fix** |
| --- | --- | --- |
| State lock error | A crashed / still-running apply holds the lock | Check who is applying first; force-unlock only when certain no apply is live |
| Plan wants to recreate everything | State lost, backend mis-pointed, or a key attribute (AMI, AZ, name) changed | Stop. Do not apply. Restore state / fix the reference; use moved blocks for refactors |
| Provider / auth errors | Wrong profile, expired SSO, CI role missing a permission | aws sts get-caller-identity — prove which identity Terraform is acting as |
| Cycle error | Two resources reference each other directly | Break the cycle with a separate resource (e.g. standalone security-group rule) |
| Diff that never clears | Provider bug, an AWS-side default, or ignore_changes candidate | Read the attribute; pin the value in code or ignore it deliberately, with a comment |
| Slow plans on huge state | State too large / too many resources per state | Split states by layer/environment (B6); use -target only as emergency surgery, never routine |

> One line to remember: Never apply a plan you do not understand. A surprising destroy in the plan is a stop sign, not a detail.

# Part C — Together: a production 3-tier stack in Terraform

This is the architecture to walk an interviewer through, slowly. It uses only Part A services and only Part B techniques, and every layer can be defended: why it exists, what happens when it fails, and how it is observed.

| **Tier / layer** | **AWS pieces** | **Terraform notes** |
| --- | --- | --- |
| Edge | Route 53 → CloudFront (optional) → WAF → ALB with ACM TLS | Cert validated by DNS records Terraform also manages |
| Web / app | ASG or ECS Fargate service in private subnets across 3 AZs, target-tracking scaling, /health health checks | Launch template / task definition versioned; desired count ignored in lifecycle when an external scaler owns it |
| Data | RDS PostgreSQL Multi-AZ in isolated subnets, automated backups, Secrets Manager credentials; ElastiCache only if a measured hot-read problem exists | prevent_destroy + deletion protection; its own state (data/) separate from the app state |
| Async (when needed) | SQS + DLQ for background work, EventBridge Scheduler for cron, SNS for alerts fan-out | Alarm on DLQ depth and oldest-message age — in the same PR as the queue |
| Observe | CloudWatch log groups with retention, golden-signal dashboard, alarms → SNS → on-call; CloudTrail + Config in the account baseline | Dashboards and alarms are code too — if it is not in Terraform, it will rot |

**Reading the stack top-down in an interview (the 60-second version)**

```
# "Users hit Route 53, which points at an ALB in public subnets
#  across three AZs, TLS from ACM, WAF in front. The ALB forwards
#  to an auto-scaled app tier in private subnets. The app reads its
#  database password from Secrets Manager at boot, talks to RDS
#  PostgreSQL — Multi-AZ, isolated subnets, app security group
#  only — and puts background jobs on SQS with a DLQ. Everything is
#  Terraform: VPC, app and data in three separate states, remote
#  state on S3 with locking, plans reviewed on the PR. CloudWatch
#  alarms page on error rate and queue age, not on raw CPU."
```

### Change story — how a release moves through this stack

1. Developer merges application code. CI builds one immutable image, pushes to ECR with the commit SHA as the tag, and scans it.

1. A second PR bumps the image tag in Terraform. The plan shows exactly one change: the task definition / launch template version.

1. Staging applies the saved plan, smoke tests run, alarms are watched. Production repeats with the same artifact and the same plan shape, behind an approval.

1. Rollback is re-applying the previous tag — minutes, rehearsed, and boring. Boring rollbacks are the goal.

> If asked 'what would you improve next?': Name one measured thing — canary deploys, a second Region warm standby, Karpenter on EKS, or cost work on NAT/logs — and the metric that tells you it mattered. A roadmap tied to evidence beats a shopping list of services.

# Part D — The interview system

Read each answer once for understanding, then practise saying it out loud in your own words. The 'Say this' line is a starting shape, not a script to memorise word for word — interviewers hear memorised scripts instantly.

## D1. AWS interview Q&A

**Q: Security group vs NACL — what is the difference?**

Security groups are stateful, instance-level, allow-only; return traffic is automatic. NACLs are stateless, subnet-level, numbered allow/deny rules; you must open ephemeral ports for replies. Most designs do the real work in security groups and keep NACLs as a coarse guardrail.

```
Say this in the interview: “Security groups are the firewall on the door; NACLs are the fence around the plot — and the fence makes you open the gate in both directions.”
```

**Q: How do you make a private EC2 instance reachable for admin access?**

Do not open SSH to the internet and do not add a public IP. Use AWS Systems Manager Session Manager through the instance role — audited, no inbound ports, no bastion to patch. A bastion in a public subnet is the older answer; name it only as the fallback.

```
Say this in the interview: “Session Manager — no open port, no key file floating around, and every session is in CloudTrail.”
```

**Q: S3 bucket is returning 403. How do you debug it?**

In order: is there an explicit Deny (bucket policy, SCP, permission boundary)? Does the identity policy actually allow this bucket/prefix? Is Block Public Access or an ACL interfering? Is it a KMS-encrypted object and the caller lacks kms:Decrypt? Check CloudTrail for the denied call and the exact principal.

```
Say this in the interview: “403 means identity, resource policy, or the KMS key said no — I find which one in CloudTrail instead of guessing.”
```

**Q: When do you choose DynamoDB over RDS?**

When the access pattern is known, key-based, and needs very high, predictable scale with single-digit-millisecond reads — carts, sessions, lookups. If you need joins, ad-hoc queries or complex transactions across entities, that is relational work: RDS/Aurora.

```
Say this in the interview: “DynamoDB rewards a known access pattern and punishes an unknown one. RDS forgives. I choose based on the queries, not the hype.”
```

**Q: Multi-AZ vs read replica on RDS?**

Multi-AZ is a synchronous standby for failover only — you cannot read from it and it does not help a slow query. Read replicas are asynchronous copies you can read from, for scaling reads, with replication lag you must handle.

```
Say this in the interview: “Multi-AZ keeps you up. Replicas keep you fast. Different purchases.”
```

**Q: ALB or NLB?**

ALB when the traffic is HTTP/HTTPS and you want host/path routing, auth and WAF. NLB when you need TCP/UDP, static IPs, or extreme connection rates. Most web APIs start on an ALB.

```
Say this in the interview: “If I need to read the HTTP request to route it, ALB. If I just need to move packets very fast, NLB.”
```

**Q: How do you stop a Lambda / app from being overwhelmed by a traffic spike?**

Put buffering in front (SQS for work, API Gateway throttling/caching for APIs), set sane concurrency/pool limits downstream — especially database connections — and scale on queue depth. Protect the database first; it is usually the scarcest resource.

```
Say this in the interview: “The app tier scales easily. The database does not. I design the spike protection around the database.”
```

**Q: What does CloudTrail not tell you?**

CloudTrail records API/management activity — who did what to the infrastructure. It does not record data-plane content: what was inside an S3 object read is not there (though S3 data events can be enabled), and it will not tell you what happened inside your application. That is application logging.

```
Say this in the interview: “CloudTrail is the security camera on the doors, not a recording of every conversation inside.”
```

**Q: How do you cut this AWS bill by 20%?**

Measure first with Cost Explorer by tag. Usual findings: over-sized instances (right-size from CloudWatch), idle resources (unattached volumes, old snapshots, idle LBs), no S3 lifecycle, NAT and log-retention waste, and no Savings Plans on the steady baseline. Commit last, after the waste is gone, or you commit to waste.

```
Say this in the interview: “Waste first, rightsizing second, commitments last — in that order, or you lock in the waste.”
```

**Q: Design a highly available web app on AWS.**

Three AZs; ALB in public subnets; auto-scaled stateless app in private subnets; RDS Multi-AZ in isolated subnets; static assets on S3 behind CloudFront; secrets in Secrets Manager; queues for async work; CloudWatch alarms on user symptoms; everything in Terraform with separate data state. Then name the residual risks: Region failure (DR strategy by RPO/RTO) and bad deploys (canary + rollback).

```
Say this in the interview: “Stateless app, stateful data protected, no single AZ anywhere, and a deploy I can reverse in minutes.”
```

## D2. Terraform interview Q&A

**Q: What is Terraform state, and why is it sensitive?**

State maps code to real resource IDs and stores attribute values — including secrets Terraform set. Losing it loses management control; leaking it leaks credentials. Hence remote, encrypted, versioned, locked, access-restricted state.

```
Say this in the interview: “State is both the map and a secrets file. I store it like both.”
```

**Q: How does your team avoid two people applying at once?**

Remote backend with state locking (S3 + DynamoDB lock in the classic pattern), plus process: applies run from CI on merge, not from laptops, so there is exactly one apply path to lock.

```
Say this in the interview: “Locking in the backend, and one apply path through CI — technology and process, both.”
```

**Q: A plan wants to destroy and recreate a production resource after your refactor. What do you do?**

Stop — do not apply. It is almost always a rename or a structural move. Add a moved block so Terraform renames it in state, re-plan, and confirm the destroy is gone. If a replace is genuinely required, schedule it, use create_before_destroy where supported, and say so in the PR.

```
Say this in the interview: “A surprise destroy is a stop sign. moved blocks exist precisely for that refactor.”
```

**Q: count or for_each?**

for_each for anything named or long-lived — stable keys mean removing one item does not shift the others. count only for truly identical, fungible copies or on/off feature flags.

```
Say this in the interview: “for_each by default. count re-indexes, and re-indexing a production subnet is a bad afternoon.”
```

**Q: How do you handle secrets in Terraform?**

Terraform should reference secrets, not contain them: create the Secrets Manager container, set the value outside Terraform (console, CLI, or the application bootstrap), and grant the workload's role access. Where Terraform must generate a secret, mark it sensitive, keep it out of logs, and accept and state plainly that it lives in state — which is why state is locked down.

```
Say this in the interview: “If Terraform knows the secret, state knows the secret. I design so Terraform mostly does not need to.”
```

**Q: How do you structure Terraform for dev, staging and prod?**

Same modules, same code, different tfvars and different state keys/backends per environment. Never fork the code per environment — forked code drifts, and staging stops predicting production.

```
Say this in the interview: “One codebase, three variable files, three states. Staging must be production's rehearsal, not its cousin.”
```

**Q: What is a module and when do you write one?**

A reusable, versioned bundle of resources with inputs and outputs. Write one when a pattern repeats (VPC, standard app service) or when a bundle has one clear owner. Keep its inputs few and its job singular.

```
Say this in the interview: “A module is a product with an interface. If callers need twenty variables, the abstraction is leaking.”
```

**Q: How do you adopt existing click-built infrastructure?**

Write configuration matching reality, use import blocks to bring resources into state, plan until the plan is empty or explainable, then manage normally. Do it in small batches, low-risk resources first, state backed up before each batch.

```
Say this in the interview: “Import in small batches, and I do not move on until the plan is clean.”
```

**Q: Terraform vs CloudFormation?**

CloudFormation is AWS-native, no separate state file to manage, and integrates with AWS release timing; Terraform is multi-cloud, has a stronger module ecosystem and, for most engineers, a cleaner language and plan experience. The honest answer is team standardisation — one IaC tool, done well, beats two done casually.

```
Say this in the interview: “I work in Terraform, and I can read CloudFormation — but a team should standardise on one.”
```

**Q: Your apply failed halfway. Now what?**

Read the error, fix the root cause (usually a permission, a quota, or a conflicting manual change), then re-plan and re-apply. State already records the resources that succeeded, so Terraform converges from where it stopped. No panic deletes.

```
Say this in the interview: “A half-applied plan is resumable by design. Fix the cause, re-plan, converge.”
```

## D3. Scenario and troubleshooting questions — think out loud

Scenario questions are scored on method, not on jumping to the answer. Use this order every time: clarify impact and scope, check what changed, look at the evidence (metrics, logs, CloudTrail, flow logs), form one hypothesis, test it, fix, then prevent recurrence. Say the steps out loud even when you already suspect the cause.

| **Scenario** | **First evidence** | **Likely causes, in order** |
| --- | --- | --- |
| Site down after a deploy | ALB target health, app logs, the deploy diff | Bad image/config, health-check path broken, security-group or listener change in the same release |
| EC2 cannot reach the internet (private subnet) | Route table, NAT health, flow logs | No NAT route, NAT in a subnet without IGW route, NACL blocking ephemeral returns |
| Terraform plan shows changes nobody made | git log on code, CloudTrail on the resource | Console drift, an AWS-side default changed, someone else's pipeline applied |
| Database slow, app healthy | RDS Performance Insights, connection count, slow-query log | Connection exhaustion, a missing index after a data change, storage IOPS ceiling — before blaming the app |
| Bill jumped 40% this month | Cost Explorer by service and tag, day by day | Forgotten load test resources, log retention, NAT data, a new always-on GPU instance — find the day it started first |
| SQS messages piling up | Queue age/depth, consumer error logs, DLQ depth | Consumer crashing on a poison message, downstream (DB) saturated, visibility timeout shorter than processing time |

## D4. System-design prompts you can now answer

- Design a URL shortener / file-upload service / image-processing pipeline on AWS — stateless API, S3 for objects, DynamoDB or RDS by access pattern, SQS for async processing, CloudFront for delivery.

- Design CI/CD for a 20-engineer team — trunk-based flow, immutable artifacts, OIDC into AWS, Terraform plans on PRs, canary deploys, automatic rollback on alarm.

- Design logging for 50 microservices — structured JSON, correlation IDs, CloudWatch (or a central aggregator), retention by value, alarms on symptoms, and a cost ceiling you can defend.

- Design for a Region outage — RPO/RTO first, then data replication, then traffic failover with Route 53 health checks, then the game-day that proves it.

## D5. One-page AWS cheat sheet

| **Need** | **Reach for** | **Need** | **Reach for** |
| --- | --- | --- | --- |
| Private app server | EC2/ECS in private subnet | Secrets | Secrets Manager |
| Public front door | ALB + ACM + WAF | Encryption keys | KMS |
| Files / objects | S3 (+ CloudFront) | Audit who did it | CloudTrail |
| Shared filesystem | EFS | Config history | AWS Config |
| SQL database | RDS / Aurora | Queue / buffer | SQS (+ DLQ) |
| Key-value at scale | DynamoDB | Fan-out notify | SNS |
| Cache | ElastiCache (Redis) | Events / cron | EventBridge |
| Run code on event | Lambda (≤15 min) | Workflow | Step Functions |
| Containers, simple | ECS Fargate | DNS | Route 53 |
| Containers, Kubernetes | EKS | Logs/metrics/alarms | CloudWatch |

## D6. One-page Terraform cheat sheet

| **Job** | **Command / pattern** |
| --- | --- |
| Start a project | terraform init  (commit .terraform.lock.hcl) |
| See the change | terraform plan -out=tfplan |
| Ship the reviewed change | terraform apply tfplan |
| Format / validate | terraform fmt -check  •  terraform validate |
| Adopt a resource | import block + matching config, plan to zero |
| Refactor safely | moved block — never let a rename become a destroy |
| Force one recreation | terraform plan -replace=<address> |
| Inspect reality | terraform state list  •  terraform show |
| Feature on/off | count = var.enabled ? 1 : 0 |
| Many named things | for_each over a map with stable keys |
| Never do | Hand-edit state JSON; apply an unreviewed plan; commit state or secret tfvars |

## D7. Self-test — cover the answers and say them out loud

1. SG vs NACL, from memory, in under 30 seconds.

1. Draw the 3-tier VPC (subnets, routes, gateways) on a blank page.

1. Explain state, locking and the bootstrap problem without notes.

1. count vs for_each — and the re-indexing failure story.

1. Walk the capstone stack top-down in 60 seconds (Part C).

1. A plan wants to destroy your database. Your exact next three actions.

1. Multi-AZ vs replica vs backup — three sentences, no mixing.

1. How OIDC removes stored AWS keys from CI/CD.

1. Your bill jumped 40%. Your first three clicks.

1. Why ECS Fargate over EKS for a small service — argue both sides.

# Part E — Practicals to finish before interviews (laptop work)

Do these in order. Each lab has a proof step — if you cannot show the proof, the lab is not finished. Use a personal AWS account with billing alerts set first, the AWS free tier where it applies, and destroy everything at the end of each lab unless the lab says to keep it. Parked means parked: these do not block reading ahead, but no résumé claim comes from an unfinished lab.

| **#** | **Lab** | **Proof** |
| --- | --- | --- |
| 0 | Account safety: MFA on root, IAM Identity Center user, billing alarm, budget alert | Screenshot/log of the budget alarm existing before any resource does |
| 1 | IAM by hand, then in Terraform: one role, one scoped policy, one instance profile | Deny test: an action outside the policy fails, and CloudTrail shows it |
| 2 | VPC from scratch in Terraform: 2–3 AZs, public/private/isolated subnets, IGW, NAT, endpoints, flow logs | A private instance reaches S3 via the gateway endpoint with no NAT traffic |
| 3 | ALB + ASG web tier serving a /health page, TLS via ACM | Kill one instance — the service stays up and the ASG replaces it |
| 4 | S3 done properly: private bucket, versioning, lifecycle to Glacier, replication or backup | Restore a deleted, versioned object; show the lifecycle rule |
| 5 | RDS PostgreSQL Multi-AZ wired to the app via Secrets Manager | Failover test timed; app reconnects; no password anywhere in the repo |
| 6 | Remote state: bootstrap bucket + lock, migrate a project to S3 backend | Two simultaneous applies — the second is blocked by the lock |
| 7 | Refactor drill: rename a resource with a moved block; import one console-made resource | Plan after each operation shows zero destroys |
| 8 | Containers: push an image to ECR, run it on ECS Fargate behind the ALB | Roll a new image tag via Terraform; roll back by re-applying the old tag |
| 9 | Events: S3 upload → SQS → Lambda, with a DLQ and alarms | A poison message lands in the DLQ and the alarm fires |
| 10 | Capstone: assemble Parts C's full stack from your modules; run a canary-style change and a restore test | A 60-second spoken walkthrough + a restore log you could show an interviewer |

> Interview rule that follows from these labs: After Labs 0–10 you may honestly say 'I have built this' about every core topic in this book. Until a lab is done, the honest phrasing is 'I have designed this and I am building it' — interviewers respect the distinction, and it protects you in deep follow-ups.

## What is deliberately not in this book

GCP, Azure deep-dives, multi-cloud strategy and managed ML services from the original Module 2 outline are out of scope by your decision: AWS and Terraform, completely, is the Module 2 you asked for. Your Azure knowledge remains on your résumé from experience; this book simply does not duplicate it. Kubernetes operations, CI/CD tooling depth, and observability platforms return in their own later modules, where they belong.

## Closing — the Module 2 standard

Module 2 is complete when three things are true: you can draw and defend the capstone architecture from a blank page, you can write and safely change the Terraform that builds it, and you can answer the self-test in D7 out loud without notes. The concepts are now in front of you. The labs in Part E turn them into stories, and stories — specific, honest, and yours — are what interviews are actually won on.

> One line to remember: Explain the service. Build it in Terraform. Say how it fails and how you would know. That is the whole method — for this module, and for every interview after it.
