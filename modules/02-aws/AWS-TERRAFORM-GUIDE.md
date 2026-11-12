# AWS + Terraform: Lesson-by-Lesson Guide

> **What this is:** Module 2 of my learning log: AWS for DevOps and AI infrastructure, one lesson at a time. Every lesson explains the concept in plain words, then builds it three ways: **console** (to see it), **CLI** (to script it), and **Terraform** (how companies actually do it).
>
> **Companion reference:** [Terraform: Zero to Advanced](TERRAFORM-ZERO-TO-ADVANCED.md) covers every Terraform concept in depth. This guide shows Terraform *in use*; that one explains it.
>
> **Interview notes:** [Module 2 AWS & Terraform notes](../../notes/module-02-aws-terraform-notes.md)

---

## Contents

| # | Lesson | Builds | Cost while running |
|---|---|---|---|
| 01 | [Account, billing & IAM](#lesson-01-account-billing--iam) | Read-only role, budget | Free |
| 02 | [VPC networking](#lesson-02-vpc-networking) | VPC, public/private subnets, routes, NAT, endpoint | Free without NAT; **NAT ≈ $0.045/h** |
| 03 | [EC2](#lesson-03-ec2) | Web server with SSM access | Free tier (t3.micro) |
| 04 | [Load balancing & auto scaling](#lesson-04-load-balancing--auto-scaling) | ALB + Auto Scaling Group | **ALB ≈ $0.023/h** + instances |
| 05 | [Storage: S3, EBS, EFS](#lesson-05-storage-s3-ebs-efs) | Secure versioned bucket with lifecycle | Cents |
| 06 | [Containers: ECR & ECS](#lesson-06-containers-ecr--ecs-fargate) | Image registry + Fargate service | **≈ $0.012/h** (smallest Fargate task) |
| 07 | [EKS](#lesson-07-eks) | Kubernetes cluster + node group + Pod Identity | **≈ $0.25/h** (control plane + nodes + NAT) |
| 08 | [Observability](#lesson-08-observability-cloudwatch--cloudtrail) | Alarms, log metrics, dashboard, CloudTrail | Mostly free tier |
| 09 | [Security & secrets](#lesson-09-security--secrets) | KMS key, secret, least-privilege reader role | ≈ $1/month per key + $0.40/secret |
| 10 | [DNS, TLS & CDN](#lesson-10-dns-tls--cdn) | Route 53 + ACM + CloudFront site | $0.50/month per hosted zone |
| 11 | [Infrastructure as Code](#lesson-11-infrastructure-as-code) | Remote state, CloudFormation basics | Cents |
| 12 | [CI/CD on AWS](#lesson-12-cicd-on-aws) | GitHub Actions → ECR → ECS via OIDC | Free (GitHub minutes) |
| 13 | [Serverless & data](#lesson-13-serverless--data) | SQS → Lambda → DynamoDB | Free tier |
| 14 | [Reliability & DR](#lesson-14-reliability--disaster-recovery) | AWS Backup plan, S3 cross-region replication | Cents |
| 15 | [Cost & FinOps](#lesson-15-cost--finops) | Budgets, anomaly detection, cost tags | Free |
| 16 | [AWS for ML](#lesson-16-aws-for-ml) | GPU instances, SageMaker, Bedrock: when to use what | Depends |

---

## How each lesson works

1. **Why it matters**: the problem it solves
2. **Concepts in plain words**: an analogy and the key terms
3. **Architecture**: a picture of what you'll build
4. **Cost**: what bills by the hour, *before* you create it
5. **Console**: click through once to see it
6. **CLI**: the commands
7. **Terraform**: complete, working code
8. **Verify**: prove it works
9. **Clean up**: delete what costs money
10. **Gotchas and interview questions**

### Folder layout in this repo
```
modules/02-aws/
├── AWS-TERRAFORM-GUIDE.md            ← this file
├── TERRAFORM-ZERO-TO-ADVANCED.md     ← Terraform reference
├── lesson-01-iam/terraform/
├── lesson-02-vpc/terraform/
├── lesson-03-ec2/terraform/
└── ...
```

### The standard `versions.tf` (copy into every lesson's `terraform/` folder)
```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      ManagedBy = "terraform"
      Project   = "ai-infra-learning"
      Lesson    = "change-me"       # e.g. "02-vpc": makes cleanup and cost tracking easy
    }
  }
}

variable "region" {
  type    = string
  default = "us-east-1"
}
```
When a lesson needs another provider (`random`, `archive`), add it under `required_providers`.

### The routine for every lesson
```bash
cd ~/ai-infra-learning/modules/02-aws/lesson-NN-name/terraform
terraform init
terraform fmt && terraform validate
terraform plan -out=tfplan     # READ IT
terraform apply tfplan
# ... verify ...
terraform destroy              # when done (unless the lesson says keep)
```

### Safety rules for the whole module
- **Read the cost line of each lesson before applying.**
- **Destroy at the end of every session** unless a lesson says to keep something.
- Find anything left behind: **Tag Editor** in the console (Resource Groups → Tag Editor → all regions → tag `ManagedBy = terraform`), or:
  ```bash
  aws resourcegroupstaggingapi get-resources --tag-filters Key=ManagedBy,Values=terraform \
    --query "ResourceTagMappingList[].ResourceARN" --output table
  ```
- Your budgets (Lesson 01) email you if spend starts.

---
# Lesson 01: Account, billing & IAM

## Why it matters
Everything in AWS starts with two questions: **who can do what** (IAM) and **how much will this cost** (billing). Get IAM wrong and you get breached; get billing wrong and you get a surprise bill. Both happen to beginners and to big companies.

## Concepts in plain words

**The analogy: an office building**

| AWS | Office building | Meaning |
|---|---|---|
| **Root user** | The owner's master key | Can do everything, including closing the account. Protect it with MFA; use it almost never. |
| **IAM user** | An employee badge | Long-term identity with a password and/or access keys |
| **IAM group** | A department | Attach permissions once; members inherit them |
| **IAM role** | A visitor pass for a job | **Temporary** credentials anyone *allowed* can "wear." No permanent keys. |
| **Policy** | The rulebook | JSON: which actions, on which resources, under which conditions |
| **MFA** | Badge + PIN | Second factor |
| **ARN** | A street address | Unique ID of any AWS thing: `arn:aws:iam::111122223333:role/lab-readonly` |

### Roles beat keys
Access keys are permanent: leak one and it works until someone deletes it. Role credentials **expire** (1 hour by default). In real companies **machines, pods, Lambda functions, and CI pipelines all use roles**:

| Who needs access | How they get it |
|---|---|
| EC2 instance | **Instance profile** (a role attached to the instance) |
| EKS pod | **IRSA** or **EKS Pod Identity** (role per Kubernetes service account) |
| ECS task | **Task role** |
| Lambda | **Execution role** |
| GitHub Actions | **OIDC** role (no stored keys) |
| Humans | **IAM Identity Center (SSO)** → permission sets (roles) |

### Anatomy of a policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadModels",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::acme-models", "arn:aws:s3:::acme-models/*"],
      "Condition": { "Bool": { "aws:SecureTransport": "true" } }
    }
  ]
}
```
| Field | Meaning |
|---|---|
| `Effect` | `Allow` or `Deny` |
| `Action` | API calls, `service:Action` (wildcards allowed: `s3:Get*`) |
| `Resource` | Which things (ARNs). Buckets and objects need **both** forms: `bucket` and `bucket/*` |
| `Condition` | Only when… (from an IP, with MFA, over HTTPS, with a tag…) |
| `Principal` | **Who**: only in resource-based and trust policies |

### How AWS decides allow vs. deny
1. **Default deny.** Nothing is allowed unless something allows it.
2. An **explicit Deny** anywhere → **denied**, no matter what allows it.
3. Otherwise an **Allow** → allowed, as long as every guardrail (SCP, permission boundary, session policy) also allows it.

### Policy types

| Type | Attached to | Purpose |
|---|---|---|
| **Identity-based** | User, group, role | What this identity can do |
| **Resource-based** | Bucket, KMS key, SQS queue, Lambda | Who can use this resource (has a `Principal`) |
| **Trust policy** | A role | Who may **assume** (wear) the role |
| **Permission boundary** | User or role | The *maximum* permissions it can ever have (used when delegating IAM to developers) |
| **SCP** (Service Control Policy) | AWS Organizations account/OU | Account-wide guardrail, e.g., "nobody can leave us-east-1" or "nobody can disable CloudTrail" |
| **Session policy** | A single assume-role session | Narrows permissions for that session only |

**AWS managed vs. customer managed vs. inline:** AWS managed policies (`ReadOnlyAccess`) are maintained by AWS. Customer managed policies are yours and reusable. Inline policies are embedded in one identity (avoid; hard to audit).

### Multi-account basics (what companies run)
```
AWS Organization (management account: billing only)
├── Security OU   → log-archive account, security-tooling account
├── Workloads OU  → dev account, staging account, prod account
└── Sandbox OU    → personal experiment accounts
SCPs on each OU; IAM Identity Center for all human logins
```
**Control Tower** sets this up with best-practice guardrails.

## Cost
Free. IAM, Organizations, Identity Center, and budgets cost nothing.

## Console
1. **Root MFA:** account name → Security credentials → Assign MFA device.
2. **Budgets:** Billing → Budgets → Create → Monthly cost budget ($50) + Zero spend budget.
3. **IAM:** Users, Roles, Policies. Open `ReadOnlyAccess` → **Policy** tab to read real AWS JSON.
4. **Policy simulator:** IAM → Policies → any policy → **Simulate**: test "would this action be allowed?" without doing it.

## CLI
```bash
aws sts get-caller-identity                                   # who am I
aws iam list-users --query "Users[].UserName"
aws iam list-roles --query "Roles[?starts_with(RoleName,'lab')].RoleName"
aws iam list-attached-role-policies --role-name lab-readonly
aws iam get-role --role-name lab-readonly --query "Role.AssumeRolePolicyDocument"

# Assume a role manually (what profiles do for you)
aws sts assume-role --role-arn arn:aws:iam::<account-id>:role/lab-readonly --role-session-name test

# Would this be allowed? (no changes made)
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<account-id>:role/lab-readonly \
  --action-names s3:CreateBucket s3:ListAllMyBuckets \
  --query "EvaluationResults[].[EvalActionName,EvalDecision]" --output table
```

## Terraform
**`main.tf`**: the read-only role (built in this lesson) plus a budget as code:
```hcl
data "aws_caller_identity" "current" {}

# WHO may wear the role
data "aws_iam_policy_document" "trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
  }
}

resource "aws_iam_role" "lab_readonly" {
  name                 = "lab-readonly"
  assume_role_policy   = data.aws_iam_policy_document.trust.json
  max_session_duration = 3600
}

# WHAT the role may do
resource "aws_iam_role_policy_attachment" "readonly" {
  role       = aws_iam_role.lab_readonly.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}

# A custom least-privilege policy: read one bucket only
data "aws_iam_policy_document" "read_models" {
  statement {
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::acme-models"]
  }
  statement {
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::acme-models/*"]
  }
}

resource "aws_iam_policy" "read_models" {
  name   = "read-models"
  policy = data.aws_iam_policy_document.read_models.json
}

# Budget as code
variable "alert_email" {
  type = string
}

resource "aws_budgets_budget" "monthly" {
  name         = "monthly-50-terraform"
  budget_type  = "COST"
  limit_amount = "50"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.alert_email]
  }
}

output "role_arn" {
  value = aws_iam_role.lab_readonly.arn
}
```
Run with `terraform apply -var="alert_email=you@example.com"`. You already created a budget in the console, so this one is practice; delete one of them afterwards to avoid duplicate emails.

## Verify
```bash
# ~/.aws/config
# [profile lab-readonly]
# role_arn = arn:aws:iam::<account-id>:role/lab-readonly
# source_profile = default

aws sts get-caller-identity --profile lab-readonly           # assumed-role/lab-readonly/...
aws s3 ls --profile lab-readonly                              # works
aws s3 mb s3://lab-test-$RANDOM --profile lab-readonly        # AccessDenied ✅
```
Console: **Switch role** → account ID + `lab-readonly` → try to create a bucket → denied.
Audit: **CloudTrail → Event history → `CreateRole`** shows who created it.

## Clean up
Keep `lab-readonly` (free, reused later). Remove the practice budget with `terraform destroy -target=aws_budgets_budget.monthly`, or keep it and delete the console one.

## Gotchas
- `arn:aws:iam::<account>:root` in a trust policy means **"this account"** (any identity in it with permission), not the root user.
- S3 needs two resource ARNs: the bucket (for `ListBucket`) and `bucket/*` (for objects). Missing one is the #1 S3 permission bug.
- Policy changes can take a few seconds to apply everywhere (eventual consistency).
- IAM is global: no region.
- IAM users can't see billing pages until root enables **"IAM user and role access to Billing information."**

## Interview questions
1. **User vs. role?** A user has permanent credentials; a role is assumed for temporary credentials. Use roles for machines, CI, and cross-account access.
2. **How does an EC2 instance get AWS permissions?** An instance profile wrapping a role; the SDK gets temporary credentials from the instance metadata service.
3. **Explicit deny vs. allow?** An explicit deny always wins.
4. **What's an SCP?** An Organizations guardrail that limits what accounts can do; it grants nothing by itself.
5. **How would you give developers access to 20 accounts?** IAM Identity Center with SSO from the company IdP, with permission sets per role assigned per account. No IAM users.
6. **What's least privilege?** Only the actions and resources required, scoped with conditions; start narrow and widen as needed (CloudTrail and IAM Access Analyzer help generate policies from real usage).

---

# Lesson 02: VPC networking

## Why it matters
Every server, database, container, and GPU node lives in a network. Networking is **the** topic AWS interviews are won or lost on, and most "it can't connect" problems at work are network problems.

## Concepts in plain words

**The analogy: a gated community**

| AWS | Gated community | Meaning |
|---|---|---|
| **VPC** | The whole community, behind a wall | Your private network, e.g. `10.0.0.0/16` (65,536 addresses) |
| **Subnet** | A street | A slice of the VPC in **one** Availability Zone, e.g. `10.0.1.0/24` (256 addresses; AWS keeps 5) |
| **Availability Zone (AZ)** | A separate neighbourhood | A separate data center in the region. Spread across ≥2 for resilience |
| **Internet Gateway (IGW)** | The main gate | Two-way door between the VPC and the internet |
| **Public subnet** | A street with a gate route | Its route table sends `0.0.0.0/0` → IGW |
| **Private subnet** | An inner street, no gate | No direct internet route; can't be reached from outside |
| **NAT Gateway** | A one-way exit door | Lets private servers reach **out** (updates, model downloads); nothing can come **in** |
| **Route table** | Street signs | "Traffic to X goes via Y" |
| **Security group (SG)** | A guard at each house door | **Stateful** firewall on each resource; **allow rules only**; replies automatically allowed |
| **Network ACL (NACL)** | A checkpoint at each street entrance | **Stateless** subnet firewall; allow **and** deny; numbered rules; replies need their own rule |
| **VPC endpoint** | A private tunnel to an AWS service | Reach S3, ECR, and others without the internet or a NAT |
| **Elastic IP** | A permanent street address | A fixed public IPv4 address |

### CIDR in one minute
`10.0.0.0/16`: the `/16` means the first 16 bits are fixed, so 2^(32−16) = **65,536** addresses.
| CIDR | Addresses | Typical use |
|---|---|---|
| `/16` | 65,536 | A VPC |
| `/20` | 4,096 | A big subnet (EKS pods use many IPs) |
| `/24` | 256 (251 usable in AWS) | A normal subnet |
| `/28` | 16 (11 usable) | Smallest AWS subnet |
| `/32` | 1 | One exact IP in a rule |
| `0.0.0.0/0` | Everything | "The internet" |

`cidrsubnet("10.0.0.0/16", 8, 3)` → `10.0.3.0/24` (add 8 bits, take subnet #3).

### Security group vs. NACL

| | Security group | NACL |
|---|---|---|
| Applies to | A resource (an ENI) | A whole subnet |
| State | **Stateful** (replies allowed automatically) | **Stateless** (replies need rules, including ephemeral ports 1024–65535) |
| Rules | Allow only | Allow and deny, evaluated by number |
| Can reference | **Other security groups** ("allow from the ALB's SG") | CIDRs only |
| Used for | Almost everything | Coarse subnet-level blocks |

**Best practice:** reference security groups, not IPs. "The app SG allows port 8000 **from the ALB SG**" keeps working when IPs change.

### The standard 3-tier layout
```
                         Internet
                            │
                    ┌───────┴────────┐
                    │ Internet GW    │
┌───────────────────┴────────────────┴───────────────────┐
│ VPC 10.0.0.0/16                                         │
│   AZ a                          AZ b                    │
│  ┌──────────────────┐         ┌──────────────────┐      │
│  │ public 10.0.0.0/24│        │ public 10.0.1.0/24│      │  ALB, NAT GW
│  │  NAT GW           │        │                   │      │
│  └────────┬──────────┘        └────────┬──────────┘      │
│  ┌────────┴──────────┐        ┌────────┴──────────┐      │
│  │private 10.0.10.0/24│       │private 10.0.11.0/24│     │  apps, EKS/GPU nodes
│  └───────────────────┘        └───────────────────┘      │
│  (data subnets: databases, no internet route at all)     │
│           S3 gateway endpoint (free) ──► S3               │
└──────────────────────────────────────────────────────────┘
```

### VPC endpoints

| Type | For | Cost |
|---|---|---|
| **Gateway** | **S3 and DynamoDB** only; added to route tables | **Free** |
| **Interface** (PrivateLink) | Most other services (ECR, STS, SSM, Secrets Manager, CloudWatch…) | ≈ $0.01/h per AZ + data |

For EKS/GPU nodes in private subnets: the **S3 gateway endpoint** saves NAT data charges when pulling model weights from S3. ECR/STS interface endpoints allow fully private clusters.

### Connecting VPCs
| Option | Use |
|---|---|
| **VPC peering** | Two VPCs, simple, not transitive |
| **Transit Gateway** | Hub connecting many VPCs and on-premises networks |
| **PrivateLink** | Expose one service privately to other VPCs/accounts |
| **Site-to-Site VPN / Direct Connect** | On-premises ↔ AWS |

## Cost
- VPC, subnets, route tables, IGW, security groups, S3 gateway endpoint: **free**
- **NAT Gateway: ≈ $0.045/hour (~$32/month) + $0.045/GB processed.** That's why the Terraform below makes it optional (`enable_nat = false` by default).
- **Public IPv4 addresses: ≈ $0.005/hour each** (including Elastic IPs and the NAT's IP).
- Interface endpoints: ≈ $0.01/hour per AZ each.

## Console
VPC → **Create VPC** → choose **"VPC and more"**. The preview diagram shows subnets, route tables, and gateways connected. It's the best way to *see* the architecture. Look, then cancel; we'll build it with Terraform.

## CLI
```bash
aws ec2 describe-vpcs --query "Vpcs[].[VpcId,CidrBlock,IsDefault]" --output table
aws ec2 describe-subnets --filters Name=vpc-id,Values=<vpc-id> \
  --query "Subnets[].[SubnetId,AvailabilityZone,CidrBlock,MapPublicIpOnLaunch]" --output table
aws ec2 describe-route-tables --filters Name=vpc-id,Values=<vpc-id> \
  --query "RouteTables[].Routes[].[DestinationCidrBlock,GatewayId,NatGatewayId]" --output table
aws ec2 describe-security-groups --filters Name=vpc-id,Values=<vpc-id> \
  --query "SecurityGroups[].[GroupId,GroupName]" --output table
aws ec2 describe-availability-zones --query "AvailabilityZones[].ZoneName"
```

## Terraform
**`variables.tf`**
```hcl
variable "name" {
  type    = string
  default = "lesson02"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "az_count" {
  type    = number
  default = 2
}

variable "enable_nat" {
  description = "NAT gateway costs ~$32/month; keep false unless needed"
  type        = bool
  default     = false
}
```

**`main.tf`**
```hcl
data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  azs = slice(data.aws_availability_zones.available.names, 0, var.az_count)
  # { "us-east-1a" = 0, "us-east-1b" = 1 }
  az_index = { for i, az in local.azs : az => i }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = { Name = var.name }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.name}-igw" }
}

# ---------- public subnets: 10.0.0.0/24, 10.0.1.0/24 ----------
resource "aws_subnet" "public" {
  for_each                = local.az_index
  vpc_id                  = aws_vpc.main.id
  availability_zone       = each.key
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, each.value)
  map_public_ip_on_launch = true
  tags = {
    Name                     = "${var.name}-public-${each.key}"
    Tier                     = "public"
    "kubernetes.io/role/elb" = "1"          # lets EKS place internet load balancers here
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = { Name = "${var.name}-public-rt" }
}

resource "aws_route_table_association" "public" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

# ---------- private subnets: 10.0.10.0/24, 10.0.11.0/24 ----------
resource "aws_subnet" "private" {
  for_each          = local.az_index
  vpc_id            = aws_vpc.main.id
  availability_zone = each.key
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, each.value + 10)
  tags = {
    Name                              = "${var.name}-private-${each.key}"
    Tier                              = "private"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.name}-private-rt" }
}

resource "aws_route_table_association" "private" {
  for_each       = aws_subnet.private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}

# ---------- optional NAT (one, in the first public subnet) ----------
resource "aws_eip" "nat" {
  count  = var.enable_nat ? 1 : 0
  domain = "vpc"
  tags   = { Name = "${var.name}-nat-eip" }
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat ? 1 : 0
  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[local.azs[0]].id
  tags          = { Name = "${var.name}-nat" }
  depends_on    = [aws_internet_gateway.main]
}

resource "aws_route" "private_default" {
  count                  = var.enable_nat ? 1 : 0
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main[0].id
}

# ---------- free S3 gateway endpoint ----------
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private.id]
  tags              = { Name = "${var.name}-s3-endpoint" }
}

# ---------- security groups: ALB → app ----------
resource "aws_security_group" "alb" {
  name        = "${var.name}-alb"
  description = "Public load balancer"
  vpc_id      = aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "alb_all" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_security_group" "app" {
  name        = "${var.name}-app"
  description = "App servers: only reachable from the ALB"
  vpc_id      = aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "app_from_alb" {
  security_group_id            = aws_security_group.app.id
  referenced_security_group_id = aws_security_group.alb.id     # SG-to-SG reference
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "app_all" {
  security_group_id = aws_security_group.app.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}
```

**`outputs.tf`**
```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = [for s in aws_subnet.public : s.id]
}

output "private_subnet_ids" {
  value = [for s in aws_subnet.private : s.id]
}

output "app_security_group_id" {
  value = aws_security_group.app.id
}
```

## Verify
```bash
terraform output
aws ec2 describe-route-tables --filters Name=vpc-id,Values=$(terraform output -raw vpc_id) \
  --query "RouteTables[].[Tags[?Key=='Name']|[0].Value, Routes[].DestinationCidrBlock]" --output json
```
Console: **VPC → Your VPCs → lesson02 → Resource map** shows the subnets, route tables, gateway, and endpoint as a diagram. Check that public subnets route `0.0.0.0/0` to the IGW and private subnets don't.

Try `terraform apply -var="enable_nat=true"`, look at the private route table (now `0.0.0.0/0 → nat-…`), then apply with `false` again **to stop the NAT charge**.

## Clean up
`terraform destroy`. Free without NAT, but destroy anyway to practise.

## Gotchas
- **NAT gateways cost money every hour**, even idle. They're the #1 surprise bill for learners.
- One NAT in one AZ is a single point of failure. Production uses **one NAT per AZ**.
- A subnet is "public" only because of its **route table**, not its name.
- An instance in a public subnet still needs a **public IP** to be reachable.
- Security group changes apply immediately; NACL mistakes can silently drop return traffic (remember ephemeral ports).
- Plan CIDRs up front: VPCs that will be peered **must not overlap**. EKS pods consume many IPs; use large subnets (`/20` or bigger) for clusters.
- `DependencyViolation` on destroy usually means something else (a load balancer or ENI) is still in the VPC.

## Interview questions
1. **Public vs. private subnet?** Public has a route to an internet gateway; private doesn't (outbound only via NAT).
2. **Security group vs. NACL?** SG: stateful, resource-level, allow-only, can reference other SGs. NACL: stateless, subnet-level, allow and deny, numbered.
3. **How do private instances download updates?** Through a NAT gateway in a public subnet, or VPC endpoints for AWS services.
4. **How do you reduce NAT costs for S3-heavy workloads (like model weights)?** An S3 gateway endpoint: free, and traffic stays on the AWS network.
5. **Design a highly available VPC.** At least 2–3 AZs; public, private, and data subnets in each; NAT per AZ; endpoints for AWS services; SG-to-SG rules; flow logs.
6. **An instance can't reach the internet. How do you troubleshoot?** Check in order: route table (IGW/NAT route), public IP (if public), security group egress, NACL inbound/outbound including ephemeral ports, the NAT's own subnet route, DNS settings. **VPC Reachability Analyzer** checks this automatically.

---

# Lesson 03: EC2

## Why it matters
EC2 is AWS's virtual machines, the base layer under EKS nodes, GPU servers, and most of AWS. Knowing instance types, AMIs, user data, roles, and storage is required for every DevOps role.

## Concepts in plain words

**The analogy: renting a car**
- **Instance type** = the car model (size, engine)
- **AMI** = the car's factory setup (OS and installed software)
- **User data** = the first-start checklist
- **EBS volume** = the trunk (persistent storage)
- **Instance profile** = the car's toll tag (permissions)
- **Security group** = who's allowed to get in

### Instance type names
`g5.2xlarge` → family **g** (GPU), generation **5**, size **2xlarge**. Letters after the generation add details: `g` = Graviton/ARM (`t4g`), `d` = local NVMe disk (`g4dn`), `n` = extra networking.

| Family | Built for | Examples |
|---|---|---|
| **t** | Burstable, cheap, small workloads | `t3.micro`, `t3.medium` |
| **m** | General purpose | `m7i.large` |
| **c** | Compute (CPU) heavy | `c7i.xlarge` |
| **r** | Memory heavy | `r7i.large` |
| **g** | GPU, inference and graphics | `g4dn` (T4 16 GB), `g5` (A10G 24 GB), `g6` (L4 24 GB), `g6e` (L40S 48 GB) |
| **p** | GPU, big training and inference | `p4d` (8× A100), `p5` (8× H100) |
| **inf / trn** | AWS Inferentia / Trainium chips | `inf2`, `trn1` |

### Pricing models

| Model | Discount | Catch | Use for |
|---|---|---|---|
| **On-Demand** | — | Most expensive | Unpredictable or short workloads |
| **Spot** | up to ~90% | AWS can reclaim with a **2-minute** warning | Batch jobs, CI, stateless or interruptible work |
| **Savings Plans** | up to ~72% | 1- or 3-year spend commitment | Steady baseline usage |
| **Reserved Instances** | up to ~72% | Commitment to specific instance types | Older model; Savings Plans are more flexible |
| **Capacity Reservations / Capacity Blocks for ML** | none (pay for reserved capacity) | Guarantees GPUs are available | Scarce GPU capacity for training or launches |

### Key pieces

| Piece | Meaning |
|---|---|
| **AMI** | Machine image. Look it up with a data source; never hard-code IDs (they differ per region) |
| **User data** | Script run once on first boot |
| **IMDS** | Instance metadata service at `169.254.169.254`. Require **IMDSv2** (token-based); it blocks a class of attacks |
| **Instance profile** | The container that attaches an IAM role to an instance |
| **EBS** | Network disk. Use `gp3`. It survives stop/start; deleted on terminate by default |
| **Instance store** | Local NVMe on `d` types: very fast, **erased on stop** (good for scratch or model cache) |
| **Key pair** | SSH key. **Modern practice: no SSH at all, use SSM Session Manager** |
| **SSM Session Manager** | A shell in the browser or CLI through IAM. No open port 22, no keys, every session logged |
| **Stop vs. terminate** | Stop: off, disk kept, no compute charge. Terminate: deleted |

## Cost
`t3.micro`/`t4g.micro` are free-tier eligible. Other costs: the EBS volume (~$0.08/GB-month) and a public IPv4 (≈$0.005/h). **GPU instances are not free:** `g4dn.xlarge` ≈ $0.53/h, and you need the GPU quota first.

## Console
EC2 → **Launch instance**: walk through name, AMI, type, key pair (choose "Proceed without"), network, security group, storage, and **Advanced details** (IAM instance profile, user data, metadata version = V2 only). This screen lists every EC2 concept in one place.

## CLI
```bash
# Latest Amazon Linux 2023 AMI (public SSM parameter)
aws ssm get-parameter --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --query Parameter.Value --output text

aws ec2 describe-instances --query \
  "Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key=='Name']|[0].Value]" --output table

aws ec2 describe-instance-types --instance-types g4dn.xlarge g5.xlarge \
  --query "InstanceTypes[].[InstanceType,VCpuInfo.DefaultVCpus,MemoryInfo.SizeInMiB,GpuInfo.Gpus[0].Name,GpuInfo.Gpus[0].MemoryInfo.SizeInMiB]" --output table

aws ec2 describe-spot-price-history --instance-types g4dn.xlarge --product-descriptions "Linux/UNIX" \
  --max-items 5 --query "SpotPriceHistory[].[AvailabilityZone,SpotPrice]" --output table

aws ec2 stop-instances --instance-ids i-xxxx
aws ec2 start-instances --instance-ids i-xxxx
aws ec2 terminate-instances --instance-ids i-xxxx

# Shell without SSH (needs the Session Manager plugin installed locally)
aws ssm start-session --target i-xxxx
```
Install the Session Manager plugin on Ubuntu:
```bash
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o ssm.deb
sudo dpkg -i ssm.deb && rm ssm.deb
```

## Terraform
Uses the **default VPC** so the lesson stands alone.

**`main.tf`**
```hcl
data "aws_vpc" "default" {
  default = true
}

# One subnet in AZ "a" (some AZs, like us-east-1e, lack newer instance types)
data "aws_subnets" "az_a" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "availability-zone"
    values = ["${var.region}a"]
  }
}

data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# ----- IAM role so SSM Session Manager works (no SSH needed) -----
data "aws_iam_policy_document" "ec2_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "web" {
  name               = "lesson03-web"
  assume_role_policy = data.aws_iam_policy_document.ec2_trust.json
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.web.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "web" {
  name = "lesson03-web"
  role = aws_iam_role.web.name
}

# ----- security group: HTTP in, everything out, NO port 22 -----
resource "aws_security_group" "web" {
  name        = "lesson03-web"
  description = "HTTP from anywhere"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_ingress_rule" "http" {
  security_group_id = aws_security_group.web.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.web.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# ----- the instance -----
resource "aws_instance" "web" {
  ami                         = data.aws_ssm_parameter.al2023.value
  instance_type               = "t3.micro"
  subnet_id                   = data.aws_subnets.az_a.ids[0]
  vpc_security_group_ids      = [aws_security_group.web.id]
  iam_instance_profile        = aws_iam_instance_profile.web.name
  associate_public_ip_address = true

  metadata_options {
    http_tokens = "required"            # IMDSv2 only
  }

  root_block_device {
    volume_type = "gp3"
    volume_size = 8
    encrypted   = true
  }

  user_data = <<-EOF
    #!/bin/bash
    dnf install -y nginx
    TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
    ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
    echo "<h1>Hello from $ID</h1>" > /usr/share/nginx/html/index.html
    systemctl enable --now nginx
  EOF
  user_data_replace_on_change = true      # editing user data recreates the instance

  tags = { Name = "lesson03-web" }
}

output "public_url" {
  value = "http://${aws_instance.web.public_ip}"
}

output "instance_id" {
  value = aws_instance.web.id
}
```

## Verify
```bash
curl $(terraform output -raw public_url)            # <h1>Hello from i-...</h1> (allow ~1 min to boot)
aws ssm start-session --target $(terraform output -raw instance_id)
#   inside: sudo systemctl status nginx; curl -s localhost; exit
```
Console: **EC2 → Instances → lesson03-web → Connect → Session Manager**: a shell in the browser with no SSH key.

## Clean up
`terraform destroy`

## Gotchas
- User data runs **once**, as root, at first boot. Logs: `/var/log/cloud-init-output.log`.
- Changing user data doesn't affect a running instance unless `user_data_replace_on_change = true` (which recreates it).
- A stopped instance still bills for EBS and its public IPv4.
- The public IP changes on stop/start; use an Elastic IP or (better) a load balancer.
- AMI IDs are per region; look them up.
- GPU instances need the **G and VT quota**, an NVIDIA driver AMI (Deep Learning AMI, or the EKS GPU AMI), and enough capacity in the AZ (`InsufficientInstanceCapacity` happens; try another AZ).

## Interview questions
1. **How do you give an instance access to S3 without keys?** An IAM role through an instance profile.
2. **How do you access instances without SSH?** SSM Session Manager: IAM-controlled, no open ports, logged.
3. **Spot vs. On-Demand vs. Savings Plans?** Spot is cheapest but interruptible; Savings Plans are commitment discounts for baseline usage; On-Demand is flexible but full price.
4. **What's IMDSv2 and why require it?** Token-based metadata access that blocks SSRF-style credential theft.
5. **EBS vs. instance store?** EBS is a persistent network disk; instance store is local, very fast, and erased on stop.
6. **An instance is "running" but the website doesn't load. Steps?** Security group inbound rule, public IP/route, NACL, whether the service is listening (`ss -ltnp` via SSM), user data logs, OS firewall.

---
# Lesson 04: Load balancing & auto scaling

## Why it matters
One server is one failure away from an outage. Real services run **several copies behind a load balancer**, with **auto scaling** adding and removing copies as traffic changes. It's the same pattern Kubernetes uses for pods, and how inference fleets scale.

## Concepts in plain words

**The analogy: a restaurant host and on-call staff**
- **Load balancer** = the host, seating each guest at a free table
- **Target group** = the list of tables (servers) the host can use
- **Health check** = the host checking a table is ready before seating anyone
- **Auto Scaling Group** = the manager calling in staff when busy and sending them home when quiet
- **Launch template** = the job description each new staff member is hired from

### Load balancer types

| Type | Layer | Routes by | Use for |
|---|---|---|---|
| **ALB** (Application) | 7 (HTTP/HTTPS) | Path (`/api`), host (`api.site.com`), headers | Web apps, APIs, model endpoints, gRPC |
| **NLB** (Network) | 4 (TCP/UDP/TLS) | IP and port; ultra-low latency, static IPs | Non-HTTP, extreme throughput, PrivateLink |
| **GWLB** (Gateway) | 3 | Transparent to firewall appliances | Security appliances |
| CLB (Classic) | 4/7 | Legacy | Don't use for new work |

### ALB building blocks
```
Client ──► ALB (public subnets, ALB SG: 80/443 from internet)
            └─ Listener :80/:443 ── rules (path/host) ──► Target group (health check /health)
                                                           ├─ instance in AZ a (app SG: from ALB SG only)
                                                           └─ instance in AZ b
```

### Auto Scaling Group pieces

| Piece | Meaning |
|---|---|
| **Launch template** | AMI, instance type, security groups, user data, IAM profile, versioned |
| **min / desired / max** | Never fewer than min, never more than max, aim for desired |
| **Health check type `ELB`** | Replace instances the load balancer marks unhealthy (not just dead ones) |
| **Grace period** | Seconds to wait after launch before health checks count |
| **Scaling policies** | **Target tracking** ("keep average CPU at 50%"), step, scheduled, predictive |
| **Instance refresh** | Rolling replacement when the launch template changes: zero-downtime deploys |
| **Mixed instances policy** | Combine on-demand and spot, several instance types |

**For inference:** CPU% is a poor signal for GPU or model servers. Scale on **request count per target**, **queue depth**, or custom metrics (e.g., waiting requests from vLLM). On Kubernetes, that's KEDA.

## Cost
- **ALB ≈ $0.0225/hour (~$16/month) + LCU usage.** It bills even with zero traffic.
- 2× `t3.micro` (free tier covers 750 hours/month total, so 2 instances ≈ 15 days)
- **Destroy at the end of the session.**

## Console
EC2 → **Load Balancers**: open one and look at the **Listeners** and **Resource map** tabs. EC2 → **Auto Scaling Groups**: the **Activity** tab shows launches and terminations with reasons.

## CLI
```bash
aws elbv2 describe-load-balancers --query "LoadBalancers[].[LoadBalancerName,DNSName,State.Code]" --output table
aws elbv2 describe-target-health --target-group-arn <tg-arn> \
  --query "TargetHealthDescriptions[].[Target.Id,TargetHealth.State,TargetHealth.Reason]" --output table
aws autoscaling describe-auto-scaling-groups --query "AutoScalingGroups[].[AutoScalingGroupName,MinSize,DesiredCapacity,MaxSize]" --output table
aws autoscaling describe-scaling-activities --auto-scaling-group-name <asg> --max-items 5
aws autoscaling set-desired-capacity --auto-scaling-group-name <asg> --desired-capacity 3
aws autoscaling start-instance-refresh --auto-scaling-group-name <asg>
```

## Terraform
**`main.tf`** (default VPC, two AZs)
```hcl
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "two_azs" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "availability-zone"
    values = ["${var.region}a", "${var.region}b"]
  }
}

data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# ---------- security groups ----------
resource "aws_security_group" "alb" {
  name   = "lesson04-alb"
  vpc_id = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "alb_out" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_security_group" "app" {
  name   = "lesson04-app"
  vpc_id = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_ingress_rule" "app_from_alb" {
  security_group_id            = aws_security_group.app.id
  referenced_security_group_id = aws_security_group.alb.id
  from_port                    = 80
  to_port                      = 80
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "app_out" {
  security_group_id = aws_security_group.app.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# ---------- launch template ----------
resource "aws_launch_template" "app" {
  name_prefix            = "lesson04-"
  image_id               = data.aws_ssm_parameter.al2023.value
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.app.id]

  metadata_options {
    http_tokens = "required"
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    dnf install -y nginx
    TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
    ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
    AZ=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone)
    echo "<h1>$ID in $AZ</h1>" > /usr/share/nginx/html/index.html
    systemctl enable --now nginx
  EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags          = { Name = "lesson04-app" }
  }
}

# ---------- load balancer ----------
resource "aws_lb" "app" {
  name               = "lesson04-alb"
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.two_azs.ids
}

resource "aws_lb_target_group" "app" {
  name                 = "lesson04-tg"
  port                 = 80
  protocol             = "HTTP"
  vpc_id               = data.aws_vpc.default.id
  deregistration_delay = 30           # seconds to drain in-flight requests

  health_check {
    path                = "/"
    matcher             = "200"
    interval            = 15
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# ---------- auto scaling group ----------
resource "aws_autoscaling_group" "app" {
  name_prefix               = "lesson04-"
  min_size                  = 2
  desired_capacity          = 2
  max_size                  = 4
  vpc_zone_identifier       = data.aws_subnets.two_azs.ids
  target_group_arns         = [aws_lb_target_group.app.arn]
  health_check_type         = "ELB"
  health_check_grace_period = 120

  launch_template {
    id      = aws_launch_template.app.id
    version = aws_launch_template.app.latest_version
  }

  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
    }
  }

  tag {
    key                 = "Name"
    value               = "lesson04-app"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "cpu50" {
  name                   = "cpu-target-50"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 50
  }
}

output "url" {
  value = "http://${aws_lb.app.dns_name}"
}
```

## Verify
```bash
URL=$(terraform output -raw url)
for i in $(seq 6); do curl -s $URL; echo; done     # alternates between 2 instance IDs / AZs
```
**Self-healing test:** terminate one instance in the console, watch the target group mark it unhealthy, and watch the ASG launch a replacement (ASG → Activity tab).
**Rolling deploy test:** change the `<h1>` text in user data → `terraform apply` → a new template version triggers an **instance refresh**: instances are replaced gradually, with no downtime.

## Clean up
`terraform destroy`. **The ALB bills hourly.**

## Gotchas
- ALBs need subnets in **at least 2 AZs**.
- Targets show `unhealthy` until the app is up. Health check path, port, and security group rules are the usual culprits.
- `health_check_type = "EC2"` (the default) only replaces *dead* instances; `"ELB"` also replaces ones failing the app health check.
- Set `deregistration_delay` low for fast deploys, high enough to finish long requests (LLM streaming requests can take minutes).
- Don't put `desired_capacity` under Terraform's control *and* let scaling policies change it, or they fight; consider `lifecycle { ignore_changes = [desired_capacity] }`.

## Interview questions
1. **ALB vs. NLB?** ALB is layer-7 HTTP routing (paths, hosts, headers); NLB is layer-4 TCP/UDP with very low latency, static IPs, and huge throughput.
2. **How does an ASG know to replace an instance?** Health checks: EC2 status, or the ELB target health when the type is `ELB`.
3. **How do you deploy a new version with zero downtime on EC2?** New launch template version + instance refresh (rolling), or blue/green with two target groups.
4. **What metric would you scale an inference fleet on?** Requests per target, queue depth, or latency, not CPU.
5. **What does connection draining (deregistration delay) do?** Lets in-flight requests finish before an instance leaves the target group.

---

# Lesson 05: Storage (S3, EBS, EFS)

## Why it matters
Models, datasets, logs, backups, Terraform state, and container layers all live in storage. Picking the wrong type is slow, expensive, or both. **S3 appears in almost every AWS interview.**

## Concepts in plain words

| Type | Analogy | What it is | Use for |
|---|---|---|---|
| **S3** (object) | An infinite warehouse with labeled boxes | Files ("objects") in buckets, over HTTPS | Model weights, datasets, backups, logs, static sites, Terraform state |
| **EBS** (block) | A hard drive plugged into one computer | A network disk attached to **one** instance (mostly) in **one** AZ | OS disks, databases, fast local model cache |
| **EFS** (file) | A shared network drive | NFS file system many instances or pods mount at once, across AZs | Shared model cache across pods, shared home directories |
| **FSx for Lustre** | A race-car file system | High-performance parallel file system, linked to S3 | Large-scale GPU training data |
| **Instance store** | A scratch pad | Local NVMe on some instance types; erased on stop | Temporary cache, scratch space |

### S3 essentials

| Feature | Meaning |
|---|---|
| **Bucket** | A container with a **globally unique** name, living in one region |
| **Key** | The object's full "path," e.g. `models/llama/v3/model.safetensors` (folders are just name prefixes) |
| **Durability** | 99.999999999% ("11 nines") |
| **Block Public Access** | Account- and bucket-level switch that overrides any public grant. **Keep it on.** |
| **Encryption** | On by default (SSE-S3). SSE-KMS gives key-level control and an audit trail |
| **Versioning** | Keeps every version; protects against deletes and overwrites |
| **Lifecycle rules** | Move to cheaper classes or delete after N days |
| **Bucket policy** | Resource-based policy: who can access this bucket |
| **Presigned URL** | Temporary link to one object, no AWS login needed |
| **Replication** | Copy objects to another bucket or region automatically (Lesson 14) |
| **Object Lock** | Write-once-read-many (compliance, ransomware protection) |
| **Event notifications** | Trigger Lambda/SQS/EventBridge on upload |

### S3 storage classes

| Class | For | Notes |
|---|---|---|
| **Standard** | Frequently used | Default |
| **Intelligent-Tiering** | Unknown access patterns | Moves objects between tiers automatically |
| **Standard-IA** / **One Zone-IA** | Infrequent access | Cheaper storage, retrieval fee, 30-day minimum |
| **Glacier Instant / Flexible / Deep Archive** | Archives | Cheapest; retrieval takes milliseconds to hours |
| **Express One Zone** | Ultra-low latency | Single AZ, very fast (ML training data) |

### EBS volume types

| Type | Use |
|---|---|
| **gp3** | Default general SSD. Set IOPS and throughput independently of size |
| **io2** | Databases needing guaranteed high IOPS |
| **st1 / sc1** | Throughput or cold HDD, for big sequential reads |

EBS snapshots are stored in S3 (incremental). Copy them across regions for DR.

## Cost
- S3 Standard ≈ $0.023/GB-month plus requests. Lesson data is cents.
- **Versioning keeps old versions, and they're billed.** Use lifecycle rules to expire them.
- EBS gp3 ≈ $0.08/GB-month, **billed even when the instance is stopped**.
- EFS ≈ $0.30/GB-month (Standard).

## Console
S3 → **Create bucket**: every section on that page is a concept above (Object Ownership, Block Public Access, Versioning, Encryption). Inside a bucket: the **Management** tab (lifecycle, replication) and the **Permissions** tab (bucket policy).

## CLI
```bash
B=lesson05-$(aws sts get-caller-identity --query Account --output text)
aws s3 mb s3://$B
echo "hello v1" > note.txt && aws s3 cp note.txt s3://$B/notes/note.txt
aws s3 ls s3://$B --recursive --human-readable
aws s3 sync ./models s3://$B/models/            # upload a folder (only changes)
aws s3 presign s3://$B/notes/note.txt --expires-in 300    # 5-minute link
aws s3api get-bucket-versioning --bucket $B
aws s3api list-object-versions --bucket $B --prefix notes/
aws s3api get-public-access-block --bucket $B
aws s3 rm s3://$B --recursive && aws s3 rb s3://$B
```
| `aws s3` (high level) | `aws s3api` (low level) |
|---|---|
| `cp`, `mv`, `sync`, `ls`, `rm`, `mb`, `rb`, `presign` | Every S3 API call: versioning, policies, lifecycle, ACLs |

**Big model files:** `aws s3 cp` uses multipart uploads automatically. Pulling multi-GB weights is faster with `s5cmd` or more concurrency (`aws configure set default.s3.max_concurrent_requests 32`).

## Terraform
**`main.tf`**: a production-style "model artifacts" bucket
```hcl
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "models" {
  bucket        = "lesson05-models-${data.aws_caller_identity.current.account_id}"
  force_destroy = true             # learning only: lets destroy delete a non-empty bucket
}

resource "aws_s3_bucket_public_access_block" "models" {
  bucket                  = aws_s3_bucket.models.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "models" {
  bucket = aws_s3_bucket.models.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "models" {
  bucket = aws_s3_bucket.models.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"       # AWS-managed KMS key; use kms_master_key_id for your own
    }
    bucket_key_enabled = true         # far fewer KMS calls = cheaper
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "models" {
  bucket = aws_s3_bucket.models.id

  rule {
    id     = "old-versions"
    status = "Enabled"
    filter {}                         # whole bucket
    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }
    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }

  rule {
    id     = "abort-incomplete-uploads"
    status = "Enabled"
    filter {}
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  depends_on = [aws_s3_bucket_versioning.models]
}

# Deny any request not using HTTPS
data "aws_iam_policy_document" "tls_only" {
  statement {
    sid     = "DenyInsecureTransport"
    effect  = "Deny"
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.models.arn,
      "${aws_s3_bucket.models.arn}/*",
    ]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "models" {
  bucket     = aws_s3_bucket.models.id
  policy     = data.aws_iam_policy_document.tls_only.json
  depends_on = [aws_s3_bucket_public_access_block.models]
}

output "bucket" {
  value = aws_s3_bucket.models.bucket
}
```
**Why so many resources for one bucket?** Since AWS provider v4, each S3 feature is its own resource. That's more code, but each setting can be changed independently and cleanly.

## Verify
```bash
B=$(terraform output -raw bucket)
echo v1 > m.txt && aws s3 cp m.txt s3://$B/m.txt
echo v2 > m.txt && aws s3 cp m.txt s3://$B/m.txt
aws s3api list-object-versions --bucket $B --prefix m.txt --query "Versions[].[VersionId,IsLatest]" --output table
aws s3 rm s3://$B/m.txt                       # "delete" just adds a delete marker
aws s3api list-object-versions --bucket $B --prefix m.txt --query "DeleteMarkers[].VersionId"
# restore: delete the delete marker
aws s3api delete-object --bucket $B --key m.txt --version-id <delete-marker-id>
aws s3 cp s3://$B/m.txt -                     # v2 is back
```

## Clean up
`terraform destroy` (works on a non-empty bucket because of `force_destroy`; never set that on real data).

## Gotchas
- Bucket names are **global**: add the account ID or a random suffix.
- Deleting a versioned object only adds a **delete marker**; old versions still cost money.
- "Folders" don't exist; they're key prefixes.
- **S3 request rate:** about 3,500 writes and 5,500 reads per second **per prefix**. Spread hot data across prefixes.
- The public-access-block account setting overrides bucket settings.
- An EBS volume can only attach to instances **in the same AZ**; move it across AZs with a snapshot.

## Interview questions
1. **S3 vs. EBS vs. EFS?** Object storage over HTTP for any number of clients; block disk for one instance in one AZ; shared NFS across instances and AZs.
2. **How do you secure an S3 bucket?** Block Public Access, encryption (KMS), a bucket policy denying non-TLS, least-privilege IAM, versioning, access logging/CloudTrail data events, VPC endpoint policies.
3. **How do you give a user temporary access to one file?** A presigned URL.
4. **How do you cut S3 costs?** Lifecycle rules, Intelligent-Tiering, expiring old versions and incomplete multipart uploads, S3 Storage Lens to find waste.
5. **How would you store and serve 50 GB of model weights to GPU nodes?** S3 (versioned) as the source of truth; nodes pull through an S3 gateway endpoint; cache on local NVMe or EFS/FSx so restarts don't re-download.

---

# Lesson 06: Containers (ECR & ECS Fargate)

## Why it matters
Containers are how modern apps and model servers ship. **ECR** stores images. **ECS** runs containers without Kubernetes; with **Fargate** there are no servers to manage. Many companies run ECS, and it's the gentlest step before EKS.

## Concepts in plain words

| Term | Meaning | Kubernetes equivalent |
|---|---|---|
| **ECR** | Private container image registry | (Docker Hub / any registry) |
| **ECS cluster** | A logical group of running services | Cluster |
| **Task definition** | Blueprint: image, CPU, memory, ports, env vars, roles, logs | Pod spec |
| **Task** | A running copy of a task definition | Pod |
| **Service** | Keeps N tasks running, replaces failed ones, registers with a load balancer | Deployment + Service |
| **Fargate** | AWS runs the servers; you pay per task CPU/memory | (serverless nodes) |
| **EC2 launch type** | You provide EC2 instances (needed for **GPUs** on ECS) | Node group |
| **Task execution role** | Lets **ECS** pull the image and write logs | kubelet's credentials |
| **Task role** | Lets **your app** call AWS (S3, SQS…) | IRSA / Pod Identity |

### ECS vs. EKS

| | ECS | EKS |
|---|---|---|
| Complexity | Low | Higher |
| Portability | AWS only | Kubernetes anywhere |
| Ecosystem | AWS-native | Huge (Helm, operators, KEDA, vLLM charts, GPU Operator) |
| Control plane cost | Free | ≈ $0.10/hour |
| GPU inference at scale | Possible (EC2 launch type) | **The industry default** |

## Cost
- ECR: 500 MB free/month on the free tier, then ≈ $0.10/GB-month.
- **Fargate: ≈ $0.04/vCPU-hour + $0.0044/GB-hour.** The smallest task (0.25 vCPU, 0.5 GB) ≈ $0.012/hour.
- The public IPv4 on the task ≈ $0.005/hour.

## Console
ECS → **Clusters** → a service → the **Tasks** tab and **Logs** tab. ECR → a repository → image **scan results** (vulnerabilities).

## CLI: build and push an image to ECR
```bash
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1
REPO=$ACCOUNT.dkr.ecr.$REGION.amazonaws.com/lesson06-app

aws ecr get-login-password --region $REGION | \
  docker login --username AWS --password-stdin $ACCOUNT.dkr.ecr.$REGION.amazonaws.com

docker build -t lesson06-app:v1 .
docker tag lesson06-app:v1 $REPO:v1
docker push $REPO:v1

aws ecr describe-images --repository-name lesson06-app --query "imageDetails[].[imageTags[0],imageSizeInBytes]" --output table
aws ecr describe-image-scan-findings --repository-name lesson06-app --image-id imageTag=v1 \
  --query "imageScanFindings.findingSeverityCounts"
```
ECS operations:
```bash
aws ecs list-services --cluster lesson06
aws ecs describe-services --cluster lesson06 --services web --query "services[0].[status,runningCount,desiredCount]"
aws ecs update-service --cluster lesson06 --service web --force-new-deployment   # redeploy
aws ecs execute-command --cluster lesson06 --task <task-id> --container web --interactive --command "/bin/sh"  # needs enable_execute_command
```

## Terraform
Runs the public `nginx` image first, so it works without pushing anything. Swap in your ECR image afterwards.

**`main.tf`**
```hcl
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# ---------- ECR ----------
resource "aws_ecr_repository" "app" {
  name                 = "lesson06-app"
  image_tag_mutability = "IMMUTABLE"        # a tag can't be overwritten: v1 is always v1
  force_delete         = true               # learning only

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep only the last 10 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 10
      }
      action = { type = "expire" }
    }]
  })
}

# ---------- ECS ----------
resource "aws_ecs_cluster" "main" {
  name = "lesson06"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_cloudwatch_log_group" "web" {
  name              = "/ecs/lesson06-web"
  retention_in_days = 7
}

data "aws_iam_policy_document" "ecs_tasks_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# Execution role: ECS uses it to pull images and write logs
resource "aws_iam_role" "execution" {
  name               = "lesson06-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_trust.json
}

resource "aws_iam_role_policy_attachment" "execution" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Task role: the app's own AWS permissions (empty here; add S3/SQS as needed)
resource "aws_iam_role" "task" {
  name               = "lesson06-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_trust.json
}

resource "aws_ecs_task_definition" "web" {
  family                   = "lesson06-web"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"            # 0.25 vCPU
  memory                   = "512"            # MiB
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  container_definitions = jsonencode([{
    name         = "web"
    image        = "public.ecr.aws/nginx/nginx:stable"   # later: "${aws_ecr_repository.app.repository_url}:v1"
    essential    = true
    portMappings = [{ containerPort = 80, protocol = "tcp" }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.web.name
        awslogs-region        = var.region
        awslogs-stream-prefix = "web"
      }
    }
  }])
}

resource "aws_security_group" "web" {
  name   = "lesson06-web"
  vpc_id = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_ingress_rule" "http" {
  security_group_id = aws_security_group.web.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.web.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_ecs_service" "web" {
  name                   = "web"
  cluster                = aws_ecs_cluster.main.id
  task_definition        = aws_ecs_task_definition.web.arn
  desired_count          = 1
  launch_type            = "FARGATE"
  enable_execute_command = true

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.web.id]
    assign_public_ip = true             # default VPC public subnets; production: private subnets + ALB
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true                     # failed deploy → automatic rollback
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}
```
`enable_execute_command` (ECS Exec) also needs `ssmmessages` permissions on the **task role** to actually work. Add them if you want shell access to tasks.

## Verify
```bash
TASK=$(aws ecs list-tasks --cluster lesson06 --service-name web --query "taskArns[0]" --output text)
ENI=$(aws ecs describe-tasks --cluster lesson06 --tasks $TASK \
  --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text)
IP=$(aws ec2 describe-network-interfaces --network-interface-ids $ENI \
  --query "NetworkInterfaces[0].Association.PublicIp" --output text)
curl -s http://$IP | head -5                 # nginx welcome page
aws logs tail /ecs/lesson06-web --follow
```
**Next step:** push your own image (CLI section), change `image` to `"${aws_ecr_repository.app.repository_url}:v1"`, apply, and watch ECS roll out the new task.

## Clean up
`terraform destroy`

## Gotchas
- `CannotPullContainerError`: the execution role lacks ECR permissions, the task has no route to ECR (private subnet with no NAT/endpoints), or the tag doesn't exist.
- `awsvpc` mode gives each task its own network interface and security group.
- `IMMUTABLE` tags stop "who overwrote `latest`?" incidents. Deploy by unique tag (git SHA).
- Fargate doesn't support GPUs; use the ECS EC2 launch type or EKS for GPUs.
- Production layout: tasks in private subnets, an ALB in public subnets, and ECR/S3/Logs VPC endpoints instead of a NAT.

## Interview questions
1. **Task role vs. execution role?** Execution role: ECS pulls images and writes logs. Task role: the application's own AWS permissions.
2. **Fargate vs. EC2 launch type?** Fargate is serverless (no instances, per-task billing); EC2 gives control, GPUs, and cheaper scale with Savings Plans or Spot.
3. **ECS vs. EKS: how do you choose?** ECS for simplicity and AWS-only teams; EKS for Kubernetes portability, the ecosystem, and GPU/ML platforms.
4. **How do you roll back a bad ECS deploy?** Deployment circuit breaker with rollback, or update the service to the previous task definition revision.
5. **Why immutable image tags?** Reproducibility and auditability: the same tag always means the same image.

---

# Lesson 07: EKS

## Why it matters
**EKS is where GPU inference platforms run.** It's AWS-managed Kubernetes, and it's the foundation of the main project (vLLM on GPU node pools).

## Concepts in plain words

| Piece | Meaning | Who manages it |
|---|---|---|
| **Control plane** | Kubernetes API server, etcd, scheduler | **AWS** (multi-AZ, ≈ $0.10/hour) |
| **Data plane** | Worker nodes running your pods | You (or AWS with Fargate/Auto Mode) |
| **Managed node group** | ASG of EC2 nodes that EKS creates, updates, and drains for you | Shared |
| **Karpenter** | Smart autoscaler that launches the *right* instance type for pending pods, fast | You install it |
| **EKS Auto Mode** | AWS manages nodes, scaling, networking add-ons | AWS |
| **Fargate profile** | Pods without nodes (no GPUs, no DaemonSets) | AWS |
| **Add-ons** | `vpc-cni` (pod IPs from the VPC), `coredns`, `kube-proxy`, `eks-pod-identity-agent`, EBS CSI driver | AWS-maintained, you enable them |
| **Access entries** | Which IAM identities can use `kubectl`, with which Kubernetes permissions | You |
| **IRSA / Pod Identity** | IAM role per Kubernetes service account, so pods get AWS permissions | You |

### Networking that surprises people
- With the **VPC CNI**, every pod gets a **real VPC IP address**. Big clusters need big subnets.
- Load balancers: install the **AWS Load Balancer Controller**; a Kubernetes `Service` of type `LoadBalancer` creates an NLB, and an `Ingress` creates an ALB. Subnets need the `kubernetes.io/role/elb` (public) or `internal-elb` (private) tags (Lesson 02 added them).

### Pod permissions: Pod Identity (newer) vs. IRSA (older, still common)

| | EKS Pod Identity | IRSA |
|---|---|---|
| Setup | Pod Identity agent add-on + an association | OIDC provider + annotated service account |
| Role trust policy | `pods.eks.amazonaws.com` (same for every cluster) | Cluster-specific OIDC provider |
| Reuse a role across clusters | Easy | Trust policy per cluster |

### GPU nodes on EKS
- AMI type `AL2023_x86_64_NVIDIA`: NVIDIA drivers preinstalled
- **Taint** GPU nodes (`nvidia.com/gpu=true:NoSchedule`) so only GPU pods land there
- **NVIDIA device plugin / GPU Operator** makes `nvidia.com/gpu` visible to Kubernetes
- Pods request `resources.limits["nvidia.com/gpu"]: 1`
- **Karpenter** scales GPU nodes to zero when idle (the biggest cost lever)

## Cost
**Control plane ≈ $0.10/hour + 2× t3.medium nodes ≈ $0.083/hour + NAT ≈ $0.045/hour ≈ $0.23/hour (~$5.50/day).** Destroy after every session. GPU node groups add ≈ $0.53/hour per `g4dn.xlarge`.

## Console
EKS → cluster → **Compute** (node groups), **Add-ons**, **Access** (access entries), **Resources** (pods and deployments visible right in the console).

## CLI
```bash
aws eks list-clusters
aws eks describe-cluster --name lesson07 --query "cluster.[status,version,endpoint]"
aws eks update-kubeconfig --region us-east-1 --name lesson07     # point kubectl at it
aws eks list-nodegroups --cluster-name lesson07
aws eks list-addons --cluster-name lesson07
aws eks list-access-entries --cluster-name lesson07

kubectl get nodes -o wide
kubectl get pods -A
kubectl describe node <node> | grep -A6 Allocatable
```

## Terraform
Uses the community modules (the industry standard). **Check each module's README for its current major version**; v21 of the EKS module renamed several inputs from v20.

**`main.tf`**
```hcl
data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  name = "lesson07"
  azs  = slice(data.aws_availability_zones.available.names, 0, 2)
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"

  name = local.name
  cidr = "10.0.0.0/16"
  azs  = local.azs

  private_subnets = ["10.0.0.0/20", "10.0.16.0/20"]      # big: pods use VPC IPs
  public_subnets  = ["10.0.100.0/24", "10.0.101.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true                             # learning: one NAT

  public_subnet_tags  = { "kubernetes.io/role/elb" = "1" }
  private_subnet_tags = { "kubernetes.io/role/internal-elb" = "1" }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = local.name
  kubernetes_version = "1.33"

  endpoint_public_access                   = true      # learning; production: private + VPN/bastion
  enable_cluster_creator_admin_permissions = true      # you get kubectl admin

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  addons = {
    vpc-cni                = { before_compute = true }
    eks-pod-identity-agent = { before_compute = true }
    coredns                = {}
    kube-proxy             = {}
  }

  eks_managed_node_groups = {
    general = {
      ami_type       = "AL2023_x86_64_STANDARD"
      instance_types = ["t3.medium"]
      min_size       = 1
      max_size       = 3
      desired_size   = 2
    }

    # GPU pool: uncomment once the G-instance quota is approved
    # gpu = {
    #   ami_type       = "AL2023_x86_64_NVIDIA"
    #   instance_types = ["g4dn.xlarge"]
    #   min_size       = 0
    #   max_size       = 1
    #   desired_size   = 1
    #   labels         = { workload = "gpu" }
    #   taints = {
    #     gpu = { key = "nvidia.com/gpu", value = "true", effect = "NO_SCHEDULE" }
    #   }
    # }
  }
}

# ---------- Pod Identity: a pod that can read S3 ----------
data "aws_iam_policy_document" "pod_trust" {
  statement {
    actions = ["sts:AssumeRole", "sts:TagSession"]
    principals {
      type        = "Service"
      identifiers = ["pods.eks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "s3_reader" {
  name               = "lesson07-s3-reader"
  assume_role_policy = data.aws_iam_policy_document.pod_trust.json
}

resource "aws_iam_role_policy_attachment" "s3_reader" {
  role       = aws_iam_role.s3_reader.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_eks_pod_identity_association" "s3_reader" {
  cluster_name    = module.eks.cluster_name
  namespace       = "default"
  service_account = "s3-reader"
  role_arn        = aws_iam_role.s3_reader.arn
}

output "configure_kubectl" {
  value = "aws eks update-kubeconfig --region ${var.region} --name ${module.eks.cluster_name}"
}
```
Apply takes **~15–20 minutes** (the control plane is slow to create).

## Verify
```bash
$(terraform output -raw configure_kubectl)
kubectl get nodes                                   # 2 Ready nodes

# Pod Identity test: a pod using the s3-reader service account
kubectl create serviceaccount s3-reader
kubectl run awscli --image=amazon/aws-cli --overrides='{"spec":{"serviceAccountName":"s3-reader"}}' \
  --restart=Never --command -- aws s3 ls
kubectl logs awscli                                 # lists your buckets: the pod got AWS permissions with no keys
kubectl delete pod awscli
```

## Clean up
```bash
kubectl get svc -A | grep LoadBalancer        # any load balancers Kubernetes created?
kubectl delete svc -n <namespace> <name>        # delete each one listed
terraform destroy                                    # ~10–15 minutes
```
**Delete Kubernetes-created load balancers first**, or the VPC destroy fails with `DependencyViolation`.

## Gotchas
- `kubectl` says "Unauthorized" → your IAM identity has no **access entry**; `enable_cluster_creator_admin_permissions` covers the creator only.
- Pods `Pending` with "Too many pods" → the node's IP/ENI limit. Use larger instances or prefix delegation.
- Upgrades: control plane first (one minor version at a time), then add-ons, then nodes.
- Load balancers and EBS volumes created **by Kubernetes** aren't in Terraform state; clean them up first.
- GPU node group stuck creating → quota, AZ capacity, or the instance type not offered in that AZ.

## Interview questions
1. **What does AWS manage in EKS, and what do you?** AWS: the control plane. You: nodes (unless Fargate/Auto Mode), add-ons, networking, IAM, workloads, upgrades.
2. **How do pods get AWS permissions?** Pod Identity or IRSA, mapping a service account to an IAM role, never node-wide credentials or keys.
3. **How do you keep normal pods off expensive GPU nodes?** Taint GPU nodes; give GPU pods a matching toleration plus a node selector/affinity.
4. **Managed node groups vs. Karpenter?** Node groups are fixed ASGs per instance type; Karpenter launches right-sized instances directly for pending pods, consolidates, and scales to zero.
5. **Why do EKS clusters run out of IPs?** The VPC CNI gives every pod a VPC IP. Plan large subnets, use prefix delegation, or custom networking.
6. **How do you upgrade EKS safely?** Check deprecated APIs → control plane +1 minor → add-ons → node groups (rolling) → verify, ideally on a staging cluster first.

---
# Lesson 08: Observability (CloudWatch & CloudTrail)

## Why it matters
You can't run what you can't see. Observability answers three questions: **is it working** (metrics and alarms), **what happened** (logs), and **who did it** (audit trail). On-call DevOps work is mostly this.

## Concepts in plain words

| Service | Analogy | What it does |
|---|---|---|
| **CloudWatch Metrics** | The car dashboard | Numbers over time: CPU, requests, latency, queue length, custom metrics |
| **CloudWatch Alarms** | The warning lights | Trigger when a metric crosses a threshold for N periods → SNS, auto scaling, actions |
| **CloudWatch Logs** | The ship's log | Log groups (per app) → log streams (per instance/task); search with **Logs Insights** |
| **Metric filters** | A highlighter on the log | Turn log lines (e.g., "ERROR") into a metric you can alarm on |
| **Dashboards** | A wall of screens | Graphs of key metrics in one place |
| **SNS** | A loudspeaker | Sends alarm messages to email, SMS, Slack (via Chatbot), PagerDuty, Lambda |
| **CloudTrail** | Security camera footage | Records **every API call**: who, what, when, from where |
| **X-Ray / Application Signals** | Package tracking | Traces one request through many services |
| **Container Insights** | Kubernetes/ECS dashboards | Pod, node, and task metrics |
| **Amazon Managed Prometheus / Grafana** | Hosted Prometheus and Grafana | Kubernetes-native metrics (what GPU platforms use) |

### Metrics vocabulary
- **Namespace** (`AWS/EC2`), **metric** (`CPUUtilization`), **dimensions** (`InstanceId=i-…`)
- **Statistic:** Average, Sum, Maximum, p95/p99
- **Period:** the bucket size (60s, 300s)
- **Basic monitoring** = 5-minute EC2 metrics (free); detailed = 1-minute (paid)
- **EC2 doesn't report memory or disk usage by default.** Install the **CloudWatch agent**.

### Alarm states
`OK` → `ALARM` → `INSUFFICIENT_DATA`. Configure *how many* periods breach before alarming (e.g., 3 of 5) to avoid flapping.

### What to alarm on (the "golden signals")
| Signal | Example metric |
|---|---|
| **Latency** | ALB `TargetResponseTime` p95 |
| **Traffic** | `RequestCount` |
| **Errors** | `HTTPCode_Target_5XX_Count` |
| **Saturation** | CPU, memory, GPU utilization, queue depth |

Alarm on **symptoms users feel** (errors, latency), not just causes (CPU).

### CloudTrail basics
- **Event history:** last 90 days of management events, free, always on
- **Trail:** delivers events to S3 (and optionally CloudWatch Logs) for long-term retention and alerting. The first trail's management events are free.
- **Data events** (S3 object reads/writes, Lambda invokes): opt-in, paid
- **Organization trail:** one trail for every account in the org

## Cost
Most of this lesson fits the free tier: 10 alarms, 3 dashboards, 5 GB of log ingestion, and 1 free trail of management events. Logs storage is cheap, but **set retention**; never-expiring logs are a classic slow leak.

## Console
CloudWatch → **All metrics** (browse namespaces), **Alarms**, **Logs → Log groups**, **Logs Insights**. CloudTrail → **Event history** (filter by user, event name, resource).

## CLI
```bash
aws cloudwatch list-metrics --namespace AWS/EC2 --metric-name CPUUtilization --max-items 5
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxx --start-time $(date -u -d '-1 hour' +%FT%TZ) \
  --end-time $(date -u +%FT%TZ) --period 300 --statistics Average
aws cloudwatch describe-alarms --state-value ALARM
aws cloudwatch set-alarm-state --alarm-name lesson08-errors --state-value ALARM --state-reason "test"  # test notifications

aws logs describe-log-groups --query "logGroups[].[logGroupName,retentionInDays]" --output table
aws logs tail /lesson08/app --follow --since 10m
aws logs filter-log-events --log-group-name /lesson08/app --filter-pattern "ERROR"

aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=CreateRole --max-results 5 \
  --query "Events[].[EventTime,Username,EventName]" --output table
```
**Logs Insights query** (console → Logs Insights, pick the log group):
```
fields @timestamp, @message
| filter @message like /ERROR/
| stats count(*) as errors by bin(5m)
| sort @timestamp desc
```

## Terraform
**`main.tf`**: log group → metric filter → alarm → email; a dashboard; a CloudTrail trail.
```hcl
variable "alert_email" {
  type = string
}

data "aws_caller_identity" "current" {}

# ---------- alerting channel ----------
resource "aws_sns_topic" "alerts" {
  name = "lesson08-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email         # you must click the confirmation email
}

# ---------- logs → metric → alarm ----------
resource "aws_cloudwatch_log_group" "app" {
  name              = "/lesson08/app"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_metric_filter" "errors" {
  name           = "app-errors"
  log_group_name = aws_cloudwatch_log_group.app.name
  pattern        = "ERROR"

  metric_transformation {
    name          = "AppErrors"
    namespace     = "Lesson08"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "errors" {
  alarm_name          = "lesson08-errors"
  alarm_description   = "More than 5 ERROR lines in 5 minutes"
  namespace           = "Lesson08"
  metric_name         = "AppErrors"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 5
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  ok_actions          = [aws_sns_topic.alerts.arn]
}

# ---------- dashboard ----------
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "lesson08"
  dashboard_body = jsonencode({
    widgets = [{
      type   = "metric"
      x      = 0
      y      = 0
      width  = 12
      height = 6
      properties = {
        title   = "App errors"
        region  = var.region
        stat    = "Sum"
        period  = 300
        metrics = [["Lesson08", "AppErrors"]]
      }
    }]
  })
}

# ---------- CloudTrail → S3 ----------
resource "aws_s3_bucket" "trail" {
  bucket        = "lesson08-trail-${data.aws_caller_identity.current.account_id}"
  force_destroy = true
}

data "aws_iam_policy_document" "trail_bucket" {
  statement {
    sid       = "AclCheck"
    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.trail.arn]
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
  }
  statement {
    sid       = "Write"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trail.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"]
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
  }
}

resource "aws_s3_bucket_policy" "trail" {
  bucket = aws_s3_bucket.trail.id
  policy = data.aws_iam_policy_document.trail_bucket.json
}

resource "aws_cloudtrail" "main" {
  name                          = "lesson08-trail"
  s3_bucket_name                = aws_s3_bucket.trail.id
  is_multi_region_trail         = true
  include_global_service_events = true        # IAM events
  enable_log_file_validation    = true        # detect tampering
  depends_on                    = [aws_s3_bucket_policy.trail]
}
```

## Verify
```bash
# 1. Confirm the SNS email subscription (check your inbox)
# 2. Push fake ERROR logs
aws logs create-log-stream --log-group-name /lesson08/app --log-stream-name test
for i in $(seq 7); do
  aws logs put-log-events --log-group-name /lesson08/app --log-stream-name test \
    --log-events timestamp=$(date +%s%3N),message="ERROR something broke $i"
done
# 3. Within ~5 minutes the alarm goes to ALARM and you get an email
aws cloudwatch describe-alarms --alarm-names lesson08-errors --query "MetricAlarms[0].StateValue"
# 4. CloudTrail delivers files to S3 within ~15 minutes
aws s3 ls s3://lesson08-trail-$(aws sts get-caller-identity --query Account --output text)/AWSLogs/ --recursive | head
```

## Clean up
`terraform destroy`. If you already have a trail you want long-term, keep one; don't create duplicates (extra trails of management events cost money).

## Gotchas
- **Logs default to "never expire."** Always set `retention_in_days`.
- An SNS email subscription does nothing until it's **confirmed**.
- `treat_missing_data` matters: for error counts, missing data usually means "no errors" (`notBreaching`).
- Memory, disk, and GPU metrics need an agent: CloudWatch agent, or **DCGM exporter** for GPUs on Kubernetes.
- CloudTrail is regional unless `is_multi_region_trail = true`; IAM events are "global service events."

## Interview questions
1. **How do you get memory metrics from EC2?** The CloudWatch agent (or Prometheus node exporter).
2. **Someone deleted a security group rule in prod. How do you find out who?** CloudTrail: filter by event name (`RevokeSecurityGroupIngress`) and resource.
3. **What would you alarm on for an API?** p95/p99 latency, 5xx error rate, request rate anomalies, saturation (CPU/GPU/queue), with SNS to on-call.
4. **How do you avoid alert fatigue?** Alarm on user-facing symptoms, require multiple breaching periods, use composite alarms, route by severity, and delete noisy alarms.
5. **Logs → metrics?** Metric filters (or embedded metric format) turn log patterns into metrics you can alarm on.

---

# Lesson 09: Security & secrets

## Why it matters
Leaked secrets and misconfigurations cause most cloud breaches. You've already had leaked access keys, and this lesson is the professional answer: **encryption keys, secret storage, and detection**.

## Concepts in plain words

| Service | Analogy | What it does |
|---|---|---|
| **KMS** | A bank vault that holds the master keys | Creates and controls encryption keys; keys never leave KMS; every use is logged in CloudTrail |
| **Secrets Manager** | A safe for passwords | Stores secrets (DB passwords, API keys, Hugging Face tokens), encrypted with KMS, **automatic rotation** |
| **SSM Parameter Store** | A labeled filing cabinet | Config values and `SecureString` secrets; free standard tier; no built-in rotation |
| **IAM Access Analyzer** | An auditor | Finds resources shared outside the account; generates least-privilege policies from usage |
| **GuardDuty** | A burglar alarm | Threat detection from CloudTrail, VPC flow logs, DNS (e.g., crypto mining, leaked-key use) |
| **Security Hub** | The security dashboard | Collects findings and checks against standards (CIS, AWS Foundational Best Practices) |
| **Inspector** | A vulnerability scanner | Scans EC2, ECR images, and Lambda for CVEs |
| **WAF** | A bouncer for web traffic | Blocks SQL injection, bad bots, rate abuse at ALB/CloudFront/API Gateway |
| **Shield** | DDoS protection | Standard is automatic and free; Advanced is paid |
| **Macie** | A data detective | Finds sensitive data (PII) in S3 |

### KMS key types
| Type | Example | Control |
|---|---|---|
| **AWS owned** | Default S3 encryption | None; invisible |
| **AWS managed** | `aws/s3`, `aws/secretsmanager` | Can see, can't manage policy |
| **Customer managed** | Your own key | Full control: key policy, rotation, deletion, cross-account sharing (≈ $1/month) |

**Envelope encryption:** KMS encrypts a small *data key*; the data key encrypts the actual data. Large data never goes to KMS.

### Secrets Manager vs. Parameter Store

| | Secrets Manager | Parameter Store |
|---|---|---|
| Cost | $0.40/secret/month + API calls | Standard tier free |
| Rotation | ✅ Built in (RDS, custom Lambda) | ❌ |
| Max size | 64 KB | 4 KB (standard) |
| Cross-account | ✅ Resource policies | Limited |
| Use for | Passwords, tokens, keys | Config values, feature flags, small secrets |

### How an app should get a secret
```
App (EC2 / ECS task / EKS pod) → its IAM role → secretsmanager:GetSecretValue + kms:Decrypt → secret
```
**Never** bake secrets into images, environment files in Git, or Terraform code. On EKS, the **External Secrets Operator** or the **Secrets Store CSI driver** syncs secrets into pods.

## Cost
Customer-managed KMS key ≈ $1/month (prorated; scheduled deletion takes 7–30 days). Secret ≈ $0.40/month. **GuardDuty and Security Hub have 30-day free trials, then bill.** Disable them after the lesson unless you want to keep them.

## Console
KMS → **Customer managed keys** → **Key policy** tab. Secrets Manager → a secret → **Retrieve secret value** (and the CloudTrail event that action creates). GuardDuty → **Findings** → **Generate sample findings** to see what alerts look like.

## CLI
```bash
aws kms list-aliases --query "Aliases[?starts_with(AliasName,'alias/lesson')]"
aws kms encrypt --key-id alias/lesson09 --plaintext fileb://<(echo -n "hello") --query CiphertextBlob --output text > ct.b64
aws kms decrypt --ciphertext-blob fileb://<(base64 -d ct.b64) --query Plaintext --output text | base64 -d

aws secretsmanager list-secrets --query "SecretList[].Name"
aws secretsmanager get-secret-value --secret-id lesson09/hf-token --query SecretString --output text
aws secretsmanager put-secret-value --secret-id lesson09/hf-token --secret-string "new-value"

aws ssm put-parameter --name /lesson09/model_name --type String --value "llama-3-8b"
aws ssm put-parameter --name /lesson09/db_pass --type SecureString --value "s3cr3t" --overwrite
aws ssm get-parameter --name /lesson09/db_pass --with-decryption --query Parameter.Value --output text

aws guardduty list-detectors
aws accessanalyzer list-analyzers
```
**Never paste secret values into chat, tickets, or screenshots.** The commands above print them to your terminal only.

## Terraform
**`main.tf`**: a KMS key, a secret whose value **never lands in Terraform state**, and a least-privilege reader role.
```hcl
# needs: random provider (~> 3.7) in required_providers, Terraform >= 1.11

data "aws_caller_identity" "current" {}

# ---------- customer managed KMS key ----------
resource "aws_kms_key" "main" {
  description             = "lesson09 app secrets"
  enable_key_rotation     = true
  deletion_window_in_days = 7
}

resource "aws_kms_alias" "main" {
  name          = "alias/lesson09"
  target_key_id = aws_kms_key.main.key_id
}

# ---------- secret (value generated ephemerally: never stored in state) ----------
ephemeral "random_password" "token" {
  length  = 32
  special = false
}

resource "aws_secretsmanager_secret" "hf_token" {
  name                    = "lesson09/hf-token"
  kms_key_id              = aws_kms_key.main.arn
  recovery_window_in_days = 0                  # learning: delete immediately on destroy
}

resource "aws_secretsmanager_secret_version" "hf_token" {
  secret_id                = aws_secretsmanager_secret.hf_token.id
  secret_string_wo         = ephemeral.random_password.token.result
  secret_string_wo_version = 1                 # bump to write a new value
}

# ---------- plain config value ----------
resource "aws_ssm_parameter" "model_name" {
  name  = "/lesson09/model_name"
  type  = "String"
  value = "llama-3-8b"
}

# ---------- a role that can read ONLY this secret ----------
data "aws_iam_policy_document" "ec2_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "read_secret" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [aws_secretsmanager_secret.hf_token.arn]
  }
  statement {
    actions   = ["kms:Decrypt"]
    resources = [aws_kms_key.main.arn]
  }
  statement {
    actions   = ["ssm:GetParameter"]
    resources = [aws_ssm_parameter.model_name.arn]
  }
}

resource "aws_iam_role" "app" {
  name               = "lesson09-app"
  assume_role_policy = data.aws_iam_policy_document.ec2_trust.json
}

resource "aws_iam_role_policy" "read_secret" {
  name   = "read-lesson09-secret"
  role   = aws_iam_role.app.id
  policy = data.aws_iam_policy_document.read_secret.json
}

# ---------- detection (30-day free trial, then paid) ----------
variable "enable_guardduty" {
  type    = bool
  default = false
}

resource "aws_guardduty_detector" "main" {
  count  = var.enable_guardduty ? 1 : 0
  enable = true
}

resource "aws_accessanalyzer_analyzer" "account" {
  analyzer_name = "lesson09-analyzer"
  type          = "ACCOUNT"                    # free for external-access findings
}
```

## Verify
```bash
terraform state show aws_secretsmanager_secret_version.hf_token | grep -i secret_string
#   → no plaintext value: write-only arguments aren't stored in state ✅
aws secretsmanager get-secret-value --secret-id lesson09/hf-token --query SecretString --output text | wc -c
#   → 33 (32 characters + newline): the value exists in AWS
aws iam simulate-principal-policy --policy-source-arn $(aws iam get-role --role-name lesson09-app --query Role.Arn --output text) \
  --action-names secretsmanager:GetSecretValue secretsmanager:DeleteSecret \
  --resource-arns $(aws secretsmanager describe-secret --secret-id lesson09/hf-token --query ARN --output text) \
  --query "EvaluationResults[].[EvalActionName,EvalDecision]" --output table
#   → GetSecretValue allowed, DeleteSecret implicitDeny ✅
```

## Clean up
`terraform destroy`. The KMS key enters a 7-day pending-deletion period (prorated cost); `recovery_window_in_days = 0` deletes the secret immediately. If you enabled GuardDuty, the destroy disables it.

## Gotchas
- `sensitive = true` hides values in output, **not in state**. Use write-only arguments, ephemeral values, or let AWS generate secrets.
- Secrets Manager's default **7–30 day recovery window** means re-creating a secret with the same name fails until it's purged (`aws secretsmanager delete-secret --force-delete-without-recovery`).
- KMS key policies are **resource policies**. If the key policy doesn't allow the account, even admins can't use the key.
- Rotation only helps if apps re-read the secret instead of caching it forever.

## Interview questions
1. **How do apps on AWS get secrets securely?** IAM role → Secrets Manager / Parameter Store at runtime, KMS-encrypted, least privilege to specific ARNs, rotation enabled.
2. **Secrets Manager vs. Parameter Store?** Rotation, cross-account, and size vs. a free tier and simple config.
3. **An access key leaked on GitHub. What do you do?** Deactivate/delete it immediately, check CloudTrail for what it did, revoke sessions, rotate related credentials, check billing for abuse (crypto mining), then fix the cause (use roles/OIDC, add secret scanning).
4. **What's envelope encryption?** KMS encrypts a data key; the data key encrypts the data. It's fast and scales.
5. **How do you keep secrets out of Terraform state?** AWS-generated secrets (e.g., `manage_master_user_password`), write-only arguments, ephemeral resources, and treating state as sensitive.

---

# Lesson 10: DNS, TLS & CDN

## Why it matters
Users reach services by **name** over **HTTPS**, often through a **CDN**. Every public model API, website, or dashboard needs DNS, a certificate, and usually CloudFront.

## Concepts in plain words

| Service | Analogy | What it does |
|---|---|---|
| **Route 53** | The phone book | DNS: turns `api.example.com` into an address. Also domain registration and health checks |
| **Hosted zone** | One phone-book page | All records for one domain |
| **ACM** | A notary | Free public TLS certificates, auto-renewed |
| **CloudFront** | Local branch offices | CDN: caches content at 400+ edge locations near users; HTTPS, WAF, DDoS protection |

### DNS records

| Record | Points to | Example |
|---|---|---|
| `A` / `AAAA` | IPv4 / IPv6 address | `api → 54.1.2.3` |
| `CNAME` | Another name (not allowed at the domain apex) | `www → example.com` |
| **Alias** (Route 53 only) | An AWS resource (ALB, CloudFront, S3), works at the apex, free queries | `example.com → d123.cloudfront.net` |
| `MX` / `TXT` / `NS` | Mail / verification text / name servers | — |

### Routing policies
Simple, **weighted** (canary: 90/10), **latency-based** (nearest region), **failover** (primary/secondary with health checks), geolocation, multivalue.

### Certificates (ACM)
- **DNS validation:** ACM gives you a CNAME record to create; once it exists, the certificate is issued and **auto-renews forever**.
- **CloudFront certificates must be in `us-east-1`**, whatever region the rest of the app is in.
- ALB certificates must be in the ALB's region.

### CloudFront in front of S3 (static site / model artifacts)
- The bucket stays **private**. **Origin Access Control (OAC)** lets only CloudFront read it.
- Users get HTTPS, caching, and compression at the edge.

## Cost
- **Hosted zone: $0.50/month**, plus queries (alias queries to AWS resources are free).
- ACM public certificates: free.
- CloudFront: generous free tier (1 TB/month of transfer).
- **You need a domain you own**, either registered in Route 53 (from ~$13/year for `.com`) or elsewhere with its name servers pointed at Route 53.

## Console
Route 53 → **Hosted zones** → a zone → records. ACM (switch to **us-east-1**) → **Request certificate**. CloudFront → **Distributions** → **Origins** and **Behaviors**.

## CLI
```bash
aws route53 list-hosted-zones --query "HostedZones[].[Name,Id]" --output table
aws route53 list-resource-record-sets --hosted-zone-id Z123 --query "ResourceRecordSets[].[Name,Type]" --output table
dig +short api.example.com
dig NS example.com +short                     # which name servers answer for the domain
aws acm list-certificates --region us-east-1 --query "CertificateSummaryList[].[DomainName,Status]" --output table
aws cloudfront list-distributions --query "DistributionList.Items[].[Id,DomainName,Status]" --output table
aws cloudfront create-invalidation --distribution-id E123 --paths "/*"    # clear the cache after deploys
```

## Terraform
A private S3 bucket → CloudFront (OAC, HTTPS) → `site.<your-domain>`. Assumes the hosted zone already exists in Route 53.

**`main.tf`**
```hcl
variable "domain" {
  description = "A domain whose hosted zone is in Route 53, e.g. example.com"
  type        = string
}

locals {
  site = "site.${var.domain}"
}

data "aws_caller_identity" "current" {}

data "aws_route53_zone" "main" {
  name = var.domain
}

# CloudFront certificates must be in us-east-1
provider "aws" {
  alias  = "use1"
  region = "us-east-1"
}

# ---------- private bucket with the site ----------
resource "aws_s3_bucket" "site" {
  bucket        = "lesson10-site-${data.aws_caller_identity.current.account_id}"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "site" {
  bucket                  = aws_s3_bucket.site.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.site.id
  key          = "index.html"
  content      = "<h1>Served by CloudFront from a private S3 bucket</h1>"
  content_type = "text/html"
}

# ---------- certificate with DNS validation ----------
resource "aws_acm_certificate" "site" {
  provider          = aws.use1
  domain_name       = local.site
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for o in aws_acm_certificate.site.domain_validation_options : o.domain_name => o
  }
  zone_id = data.aws_route53_zone.main.zone_id
  name    = each.value.resource_record_name
  type    = each.value.resource_record_type
  records = [each.value.resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "site" {
  provider                = aws.use1
  certificate_arn         = aws_acm_certificate.site.arn
  validation_record_fqdns = [for r in aws_route53_record.cert_validation : r.fqdn]
}

# ---------- CloudFront with Origin Access Control ----------
resource "aws_cloudfront_origin_access_control" "site" {
  name                              = "lesson10-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "site" {
  enabled             = true
  default_root_object = "index.html"
  aliases             = [local.site]
  price_class         = "PriceClass_100"        # US/Europe edges only: cheapest

  origin {
    domain_name              = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id                = "s3-site"
    origin_access_control_id = aws_cloudfront_origin_access_control.site.id
  }

  default_cache_behavior {
    target_origin_id       = "s3-site"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6"   # AWS managed "CachingOptimized"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.site.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}

# Only this distribution may read the bucket
data "aws_iam_policy_document" "site_bucket" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.site.arn}/*"]
    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.site.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "site" {
  bucket     = aws_s3_bucket.site.id
  policy     = data.aws_iam_policy_document.site_bucket.json
  depends_on = [aws_s3_bucket_public_access_block.site]
}

# ---------- DNS name → CloudFront ----------
resource "aws_route53_record" "site" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.site
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.site.domain_name
    zone_id                = aws_cloudfront_distribution.site.hosted_zone_id
    evaluate_target_health = false
  }
}

output "url" {
  value = "https://${local.site}"
}
```
Apply with `terraform apply -var="domain=yourdomain.com"`. CloudFront takes **5–15 minutes** to deploy.

## Verify
```bash
curl -I $(terraform output -raw url)            # HTTP/2 200; run twice: x-cache goes Miss → Hit from cloudfront
aws s3api get-object --bucket lesson10-site-<account-id> --key index.html /dev/stdout  # works for you (IAM)
curl -I https://lesson10-site-<account-id>.s3.amazonaws.com/index.html               # 403: bucket is private ✅
```

## Clean up
`terraform destroy` (CloudFront takes ~10–15 minutes to disable and delete). The hosted zone stays; it wasn't created here.

## Gotchas
- **CloudFront + ACM = us-east-1**, always.
- DNS changes can take time to propagate (TTL). Low TTLs before migrations, higher afterwards.
- `CNAME` isn't allowed at the apex (`example.com`); use a Route 53 **alias**.
- After deploying new files, **invalidate** the CloudFront cache or use versioned file names.
- If the domain is registered elsewhere, its **NS records** must point to the Route 53 hosted zone's name servers.

## Interview questions
1. **Alias vs. CNAME?** Alias is Route 53-specific, points at AWS resources, works at the apex, and alias queries to AWS resources are free.
2. **How do you serve a private S3 bucket publicly over HTTPS?** CloudFront with Origin Access Control, a bucket policy allowing only that distribution, ACM certificate in us-east-1.
3. **How would you do a canary release with DNS?** Route 53 weighted records (e.g., 95/5), shifting weights gradually, plus health checks.
4. **Multi-region failover?** Route 53 failover or latency routing with health checks across regional endpoints.
5. **Why put CloudFront in front of an API?** TLS at the edge, caching, WAF, DDoS protection, fewer cross-region round trips.

---
# Lesson 11: Infrastructure as Code

## Why it matters
Every lesson so far used Terraform with **local state**. Real teams need **shared, locked, versioned state**. You'll also meet **CloudFormation** in AWS-heavy companies and in AWS certification exams, so you need to read it comfortably.

## Concepts in plain words
The full Terraform reference is in [TERRAFORM-ZERO-TO-ADVANCED.md](TERRAFORM-ZERO-TO-ADVANCED.md). This lesson covers the AWS side:

| Topic | Plain meaning |
|---|---|
| **Remote state** | Terraform's memory stored in S3 instead of on the laptop: shared, versioned, encrypted, locked |
| **State locking** | Only one `apply` at a time (S3 native lockfile in Terraform ≥ 1.10; DynamoDB in older setups) |
| **CloudFormation (CFN)** | AWS's own IaC: YAML/JSON templates → **stacks** |
| **Change set** | CloudFormation's version of `terraform plan` |
| **Drift detection** | Find manual changes made outside IaC |
| **CDK** | Write CloudFormation in TypeScript/Python, compiled to templates |

### Terraform vs. CloudFormation

| | Terraform | CloudFormation |
|---|---|---|
| Clouds | Any (plus SaaS: GitHub, Datadog…) | AWS only |
| State | You manage (S3) | AWS manages it for you |
| Preview | `terraform plan` | Change sets |
| Rollback on failure | No automatic rollback | **Automatic rollback** |
| New AWS features | Usually days to weeks after launch | Often on day one |
| Language | HCL | YAML/JSON (+ CDK) |
| Industry usage | Most DevOps job posts | AWS-centric shops, AWS-native tools (SAM, Control Tower) |

## Cost
The state bucket: cents. CloudFormation itself is free (you pay for the resources it creates).

## Part A: Remote state for all your lessons

### 1. Bootstrap the state bucket (once, with local state)
`modules/02-aws/bootstrap/main.tf`:
```hcl
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "tfstate" {
  bucket = "tfstate-${data.aws_caller_identity.current.account_id}-use1"
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "tfstate" {
  bucket                  = aws_s3_bucket.tfstate.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "state_bucket" {
  value = aws_s3_bucket.tfstate.bucket
}
```

### 2. Add a backend to any lesson
`backend.tf` in a lesson folder (values must be literals; no variables):
```hcl
terraform {
  backend "s3" {
    bucket       = "tfstate-<account-id>-use1"
    key          = "module-02/lesson-02-vpc/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
```
```bash
terraform init -migrate-state      # copies existing local state into S3 (answer "yes")
aws s3 ls s3://tfstate-<account-id>-use1/module-02/ --recursive
```
**The bootstrap's own state stays local** (it manages the bucket the other states live in). Commit nothing secret; keep that folder's `terraform.tfstate` out of Git (your `.gitignore` already does).

### 3. Prove locking works
Run `terraform apply` in one terminal and leave it at the "yes?" prompt. In a second terminal, in the same folder, run `terraform plan`. You get **"Error acquiring the state lock."** Answer "no" in the first terminal and the lock is released.

## Part B: CloudFormation basics

`bucket.yaml`
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: Lesson 11 - versioned private bucket

Parameters:
  BucketPrefix:
    Type: String
    Default: lesson11

Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${BucketPrefix}-${AWS::AccountId}"
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      Tags:
        - Key: ManagedBy
          Value: cloudformation

Outputs:
  BucketName:
    Value: !Ref Bucket
  BucketArn:
    Value: !GetAtt Bucket.Arn
```

| CFN syntax | Meaning | Terraform equivalent |
|---|---|---|
| `Parameters` | Inputs | `variable` |
| `Resources` | Things to create | `resource` |
| `Outputs` | Exported values | `output` |
| `!Ref X` | ID/name of resource X, or a parameter's value | `aws_s3_bucket.x.id` / `var.x` |
| `!GetAtt X.Arn` | An attribute | `aws_s3_bucket.x.arn` |
| `!Sub "${A}-${AWS::AccountId}"` | String interpolation | `"${var.a}-${data.aws_caller_identity.current.account_id}"` |
| `Conditions` / `Mappings` | If-logic / lookup tables | conditionals / maps |

```bash
aws cloudformation validate-template --template-body file://bucket.yaml
aws cloudformation deploy --template-file bucket.yaml --stack-name lesson11      # creates a change set and executes it
aws cloudformation describe-stacks --stack-name lesson11 --query "Stacks[0].[StackStatus,Outputs]"
aws cloudformation describe-stack-events --stack-name lesson11 --max-items 10   # what happened, step by step
aws cloudformation detect-stack-drift --stack-name lesson11                      # then describe-stack-resource-drifts
aws cloudformation delete-stack --stack-name lesson11
```
**Preview first (the "plan"):** `aws cloudformation deploy ... --no-execute-changeset`, then review the change set in the console.

Console: CloudFormation → the stack → **Events**, **Resources**, **Outputs**, **Change sets**, **Drifts** tabs.

## Clean up
Delete the CloudFormation stack. **Keep the state bucket** (it has `prevent_destroy`) and use it from now on.

## Gotchas
- Backend blocks can't use variables; use `-backend-config` for per-environment values.
- **Never `terraform destroy` the bootstrap** while other states live in that bucket.
- A failed CloudFormation update rolls back automatically; a stack stuck in `UPDATE_ROLLBACK_FAILED` needs `continue-update-rollback`.
- A resource should be managed by **one** tool. Don't manage the same bucket in Terraform and CloudFormation.

## Interview questions
1. **How do you set up Terraform state for a team on AWS?** S3 with versioning, KMS encryption, blocked public access, locking, one key per stack, IAM-restricted access, and a separate bootstrap.
2. **Terraform vs. CloudFormation?** Multi-cloud with self-managed state vs. AWS-only with managed state, automatic rollback, and day-one feature support.
3. **What's a change set?** CloudFormation's preview of changes before executing them.
4. **How do you detect manual changes?** `terraform plan -refresh-only` / scheduled plans; CloudFormation drift detection; AWS Config rules.

---

# Lesson 12: CI/CD on AWS

## Why it matters
DevOps is about **shipping safely and often**. A pipeline that builds, scans, and deploys on every merge, using **no stored AWS keys**, is the core of the job and a standard interview topic.

## Concepts in plain words

| Term | Meaning |
|---|---|
| **CI** (Continuous Integration) | Every change is built and tested automatically |
| **CD** (Continuous Delivery/Deployment) | Every passing change can be (or is) released automatically |
| **OIDC federation** | GitHub proves "I am workflow X in repo Y" with a short-lived token; AWS trusts it and hands out temporary role credentials. **No access keys in GitHub.** |
| **Artifact** | The built output: a container image in ECR |
| **Immutable tag** | Tag images with the **git commit SHA**, never reuse a tag |
| **Environment protection** | GitHub "environments" with required reviewers = manual approval for prod |

### AWS-native CI/CD (good to know)

| Service | Role | GitHub equivalent |
|---|---|---|
| **CodePipeline** | Orchestrates stages | Workflow |
| **CodeBuild** | Runs build steps in containers | Job runner |
| **CodeDeploy** | Deploys to EC2/ECS/Lambda with blue/green and canary | Deploy step |
| **CodeArtifact** | Package repository (pip, npm, Maven) | GitHub Packages |

Most teams today use **GitHub Actions or GitLab CI with OIDC into AWS**, plus **ArgoCD** for Kubernetes.

### The pipeline we'll build
```
git push to main
   └─► GitHub Actions
         1. assume AWS role via OIDC (no keys)
         2. docker build → tag :<git-sha>
         3. push to ECR (scan on push)
         4. render a new task definition with the new image
         5. deploy to the ECS service → wait until stable
                (circuit breaker rolls back on failure)
```
This deploys to the **Lesson 06** ECS service, so apply Lesson 06 first.

## Cost
GitHub Actions minutes are free for public repos (and include a monthly allowance for private ones). IAM/OIDC are free. The ECS service costs what Lesson 06 costs.

## Terraform: the GitHub OIDC role
```hcl
variable "github_repo" {
  description = "owner/repo allowed to deploy"
  type        = string
  default     = "sairam145/ai-infra-learning"
}

data "aws_caller_identity" "current" {}

resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}

data "aws_iam_policy_document" "github_trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:ref:refs/heads/main"]   # only the main branch
    }
  }
}

resource "aws_iam_role" "github_deploy" {
  name               = "github-deploy-ecs"
  assume_role_policy = data.aws_iam_policy_document.github_trust.json
}

data "aws_iam_policy_document" "deploy" {
  statement {
    sid       = "EcrAuth"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }
  statement {
    sid = "EcrPush"
    actions = [
      "ecr:BatchCheckLayerAvailability", "ecr:InitiateLayerUpload", "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload", "ecr:PutImage", "ecr:BatchGetImage",
    ]
    resources = ["arn:aws:ecr:${var.region}:${data.aws_caller_identity.current.account_id}:repository/lesson06-app"]
  }
  statement {
    sid = "EcsDeploy"
    actions = [
      "ecs:DescribeTaskDefinition", "ecs:RegisterTaskDefinition",
      "ecs:UpdateService", "ecs:DescribeServices",
    ]
    resources = ["*"]
  }
  statement {
    sid       = "PassTaskRoles"
    actions   = ["iam:PassRole"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/lesson06-execution",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/lesson06-task",
    ]
  }
}

resource "aws_iam_role_policy" "deploy" {
  name   = "deploy-ecs"
  role   = aws_iam_role.github_deploy.id
  policy = data.aws_iam_policy_document.deploy.json
}

output "role_arn" {
  value = aws_iam_role.github_deploy.arn
}
```
An account can have only **one** OIDC provider per URL. If one already exists, read it with `data "aws_iam_openid_connect_provider"` instead of creating it.

## The workflow: `.github/workflows/deploy-ecs.yml`
```yaml
name: deploy-ecs
on:
  push:
    branches: [main]
    paths: ["apps/lesson06/**"]

permissions:
  id-token: write     # OIDC
  contents: read

concurrency: deploy-ecs   # never two deploys at once

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: lesson06-app
  ECS_CLUSTER: lesson06
  ECS_SERVICE: web
  CONTAINER: web

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - id: ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push
        id: build
        run: |
          IMAGE=${{ steps.ecr.outputs.registry }}/$ECR_REPOSITORY:${{ github.sha }}
          docker build -t $IMAGE apps/lesson06
          docker push $IMAGE
          echo "image=$IMAGE" >> $GITHUB_OUTPUT

      - name: Download current task definition
        run: |
          aws ecs describe-task-definition --task-definition lesson06-web \
            --query taskDefinition > taskdef.json

      - id: render
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: taskdef.json
          container-name: ${{ env.CONTAINER }}
          image: ${{ steps.build.outputs.image }}

      - uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.render.outputs.task-definition }}
          cluster: ${{ env.ECS_CLUSTER }}
          service: ${{ env.ECS_SERVICE }}
          wait-for-service-stability: true
```
Store the role ARN as a repo secret: GitHub → Settings → Secrets and variables → Actions → `AWS_DEPLOY_ROLE_ARN`. It isn't really secret, but this keeps account IDs out of workflow files.

**Terraform and CI deploys together:** once CI owns the image version, stop Terraform from reverting it. In the Lesson 06 service add:
```hcl
lifecycle {
  ignore_changes = [task_definition]
}
```

## Verify
1. Put a tiny `Dockerfile` in `apps/lesson06/` (e.g., `FROM public.ecr.aws/nginx/nginx:stable` plus your own `index.html`), commit, push to `main`.
2. GitHub → **Actions** → watch each step go green.
3. `aws ecs describe-services --cluster lesson06 --services web --query "services[0].taskDefinition"` → a new revision.
4. `curl` the task IP → your page.
5. Break it on purpose (e.g., a container command that exits) → the circuit breaker rolls back to the previous revision.

## Clean up
Destroy Lesson 06. Keep the OIDC provider and role if you'll reuse them (free); otherwise destroy.

## Gotchas
- `Not authorized to perform sts:AssumeRoleWithWebIdentity` → the `sub` condition doesn't match (branch, repo name, or environment), or `permissions: id-token: write` is missing.
- Scope `sub` tightly: `repo:org/repo:*` lets **any branch** deploy.
- `iam:PassRole` is required to register a task definition that uses roles. A missing PassRole is a classic error.
- Use one role per environment, with stricter conditions for prod (`environment:prod`).

## Interview questions
1. **How does GitHub Actions authenticate to AWS without keys?** OIDC: GitHub issues a signed token, and AWS's IAM OIDC provider plus the role's trust policy (`aud`/`sub` conditions) exchange it for temporary credentials.
2. **Why tag images with the commit SHA?** Traceability and rollback: each image maps to exact code, and tags are never overwritten.
3. **What gates would you put before prod?** Tests, image scan with a severity threshold, Terraform plan review, manual approval via environment protection, canary/blue-green with automatic rollback.
4. **What's `iam:PassRole` and why does CI need it?** Permission to hand a role to a service (ECS, Lambda). Without it, CI can't register a task definition referencing task roles.
5. **Blue/green vs. rolling?** Rolling replaces gradually in place; blue/green stands up a full new version and switches traffic at once, with instant rollback.

---

# Lesson 13: Serverless & data

## Why it matters
Not everything needs servers. **Queues decouple services**, **Lambda runs code on events**, and **managed databases** remove database operations work. For AI platforms: async inference requests, batch jobs, and metadata storage use exactly these.

## Concepts in plain words

| Service | Analogy | What it does |
|---|---|---|
| **Lambda** | A taxi: pay only for the ride | Runs a function on an event; scales automatically; max 15 minutes; billed per millisecond |
| **SQS** | A ticket queue at a deli | Stores messages until a worker processes them; absorbs spikes |
| **DLQ** (dead-letter queue) | The "problem orders" tray | Messages that failed N times go here for inspection |
| **SNS** | A megaphone | One message → many subscribers (fan-out) |
| **EventBridge** | A switchboard | Routes events by rules and schedules (cron) |
| **API Gateway** | A front desk | HTTPS API in front of Lambda/services, with auth, throttling, keys |
| **Step Functions** | A flowchart that runs | Orchestrates multi-step workflows with retries |
| **DynamoDB** | A giant, fast key-value notebook | Serverless NoSQL; millisecond reads at any scale |
| **RDS / Aurora** | A managed relational database | PostgreSQL/MySQL with backups, patching, Multi-AZ |
| **ElastiCache** | A sticky-note cache | Redis/Valkey in memory: caching, sessions, rate limits |

### Why queues matter
```
Without a queue:   API ──► worker        (worker slow or down = API fails)
With a queue:      API ──► SQS ──► workers   (API returns fast; workers catch up; failures retry)
```
**Async inference pattern:** the API puts the job on SQS → GPU workers pull jobs → results go to S3/DynamoDB → the client polls or gets notified. Scale workers on **queue depth** (KEDA on Kubernetes).

### SQS key settings

| Setting | Meaning |
|---|---|
| **Visibility timeout** | While a worker processes a message it's hidden; if not deleted in time, it reappears. **Set it ≥ 6× the Lambda timeout** |
| **maxReceiveCount** | After N failed attempts → DLQ |
| **Standard vs. FIFO** | Standard: huge throughput, at-least-once, best-effort order. FIFO: exactly-once processing, strict order, lower throughput |
| **Long polling** | Wait up to 20s for messages (fewer empty, billed requests) |

### Choosing a database

| Need | Pick |
|---|---|
| Relational data, joins, transactions | **RDS PostgreSQL** / Aurora |
| Key-value at any scale, serverless | **DynamoDB** |
| Cache, rate limiting, sessions | **ElastiCache** (Redis/Valkey) |
| Vector search for RAG | **OpenSearch**, **Aurora/RDS PostgreSQL + pgvector**, S3 Vectors |
| Analytics over files in S3 | **Athena** |

## Cost
All of this lesson is in the free tier: Lambda 1M requests/month, SQS 1M requests/month, DynamoDB on-demand with small usage. **RDS is not created here** (smallest instances still bill hourly).

## Console
Lambda → the function → **Monitor** (invocations, errors, duration) → **View CloudWatch logs**. SQS → the queue → **Send and receive messages**. DynamoDB → **Explore items**.

## CLI
```bash
aws sqs send-message --queue-url <url> --message-body '{"text":"hello"}'
aws sqs get-queue-attributes --queue-url <url> --attribute-names ApproximateNumberOfMessages
aws lambda invoke --function-name lesson13-worker --payload '{"Records":[]}' \
  --cli-binary-format raw-in-base64-out out.json && cat out.json
aws logs tail /aws/lambda/lesson13-worker --follow
aws dynamodb scan --table-name lesson13-jobs --max-items 5
aws dynamodb get-item --table-name lesson13-jobs --key '{"id":{"S":"<message-id>"}}'
```

## Terraform
SQS (+ DLQ) → Lambda → DynamoDB. Add the `archive` provider: `archive = { source = "hashicorp/archive", version = "~> 2.6" }`.

**`main.tf`**
```hcl
# ---------- queue + dead-letter queue ----------
resource "aws_sqs_queue" "dlq" {
  name                      = "lesson13-jobs-dlq"
  message_retention_seconds = 1209600            # 14 days to inspect failures
}

resource "aws_sqs_queue" "jobs" {
  name                       = "lesson13-jobs"
  visibility_timeout_seconds = 60                # >= 6 × Lambda timeout (10s)
  receive_wait_time_seconds  = 20                # long polling
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3
  })
}

# ---------- table ----------
resource "aws_dynamodb_table" "jobs" {
  name         = "lesson13-jobs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

# ---------- Lambda code (zipped from inline source) ----------
data "archive_file" "worker" {
  type        = "zip"
  output_path = "${path.module}/worker.zip"
  source {
    filename = "app.py"
    content  = <<-PY
      import json, os
      import boto3

      table = boto3.resource("dynamodb").Table(os.environ["TABLE"])

      def handler(event, context):
          for record in event["Records"]:
              body = json.loads(record["body"])
              if body.get("fail"):
                  raise ValueError("simulated failure")   # tests retries → DLQ
              table.put_item(Item={"id": record["messageId"], "text": body.get("text", "")})
          return {"processed": len(event["Records"])}
    PY
  }
}

# ---------- Lambda role ----------
data "aws_iam_policy_document" "lambda_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "worker" {
  name               = "lesson13-worker"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json
}

resource "aws_iam_role_policy_attachment" "logs" {
  role       = aws_iam_role.worker.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "worker" {
  statement {
    actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
    resources = [aws_sqs_queue.jobs.arn]
  }
  statement {
    actions   = ["dynamodb:PutItem"]
    resources = [aws_dynamodb_table.jobs.arn]
  }
}

resource "aws_iam_role_policy" "worker" {
  name   = "worker-access"
  role   = aws_iam_role.worker.id
  policy = data.aws_iam_policy_document.worker.json
}

# ---------- function + trigger ----------
resource "aws_cloudwatch_log_group" "worker" {
  name              = "/aws/lambda/lesson13-worker"
  retention_in_days = 7
}

resource "aws_lambda_function" "worker" {
  function_name    = "lesson13-worker"
  role             = aws_iam_role.worker.arn
  runtime          = "python3.12"
  handler          = "app.handler"
  filename         = data.archive_file.worker.output_path
  source_code_hash = data.archive_file.worker.output_base64sha256   # redeploy when code changes
  timeout          = 10
  memory_size      = 256

  environment {
    variables = {
      TABLE = aws_dynamodb_table.jobs.name
    }
  }

  depends_on = [aws_cloudwatch_log_group.worker]
}

resource "aws_lambda_event_source_mapping" "jobs" {
  event_source_arn = aws_sqs_queue.jobs.arn
  function_name    = aws_lambda_function.worker.arn
  batch_size       = 10
}

output "queue_url" {
  value = aws_sqs_queue.jobs.url
}
```

### Other building blocks (reference)
**HTTP API in front of a Lambda** (quick create):
```hcl
resource "aws_apigatewayv2_api" "api" {
  name          = "lesson13-api"
  protocol_type = "HTTP"
  target        = aws_lambda_function.worker.arn     # in practice: a separate "api" function
}

resource "aws_lambda_permission" "api" {
  statement_id  = "AllowApiGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.worker.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}
```
**RDS PostgreSQL done right** (not applied in this lesson; it bills hourly):
```hcl
resource "aws_db_instance" "main" {
  identifier                  = "app-db"
  engine                      = "postgres"
  engine_version              = "16"
  instance_class              = "db.t4g.micro"
  allocated_storage           = 20
  storage_encrypted           = true
  db_name                     = "app"
  username                    = "app_admin"
  manage_master_user_password = true            # password lives in Secrets Manager, never in state
  multi_az                    = true            # standby in a second AZ, automatic failover
  backup_retention_period     = 7
  deletion_protection         = true
  skip_final_snapshot         = false
  final_snapshot_identifier   = "app-db-final"
  db_subnet_group_name        = "private-data-subnets"
  vpc_security_group_ids      = ["sg-from-app-only"]
}
```

## Verify
```bash
Q=$(terraform output -raw queue_url)
aws sqs send-message --queue-url $Q --message-body '{"text":"first job"}'
sleep 10
aws dynamodb scan --table-name lesson13-jobs --query "Items[].text.S"        # ["first job"]

aws sqs send-message --queue-url $Q --message-body '{"fail":true}'           # fails 3 times → DLQ
sleep 240
aws sqs get-queue-attributes --queue-url $(aws sqs get-queue-url --queue-name lesson13-jobs-dlq --query QueueUrl --output text) \
  --attribute-names ApproximateNumberOfMessages                              # 1 ✅
aws logs tail /aws/lambda/lesson13-worker --since 10m | grep -i "simulated failure"
```

## Clean up
`terraform destroy`

## Gotchas
- Visibility timeout shorter than processing time → **duplicate processing**. Make consumers **idempotent** (safe to run twice).
- One failing message fails the **whole batch** unless you use partial batch responses (`ReportBatchItemFailures`).
- Lambda cold starts add latency; Lambda **isn't for GPU inference** (no GPUs, 15-minute limit). Use it for glue: triggers, routing, post-processing.
- DynamoDB design starts from **access patterns**: choose keys for how you'll query.
- RDS: `deletion_protection` and `skip_final_snapshot = false` in prod, always.

## Interview questions
1. **Why put a queue between an API and workers?** Decoupling, absorbing spikes, retries, independent scaling, and protection from downstream outages.
2. **What's a DLQ, and how do you use it?** A queue for messages that repeatedly fail; alarm on its depth, inspect, fix, redrive.
3. **SQS Standard vs. FIFO?** At-least-once delivery with huge throughput vs. ordered, exactly-once processing with lower throughput.
4. **RDS Multi-AZ vs. read replicas?** Multi-AZ is a synchronous standby for **availability** (automatic failover). Read replicas are asynchronous copies for **read scaling** (can be cross-region).
5. **How would you design async LLM inference?** API → SQS (+ DLQ) → GPU workers on EKS scaled by KEDA on queue depth → results in S3/DynamoDB → client polls or gets a webhook/SNS notification.

---

# Lesson 14: Reliability & disaster recovery

## Why it matters
Things fail: instances, AZs, occasionally whole regions, and humans with `delete`. Reliability is designing so failures don't become outages, and DR is getting back when they do. Senior interviews always go here.

## Concepts in plain words

| Term | Meaning |
|---|---|
| **High availability (HA)** | Survive component or AZ failures **without downtime** (multi-AZ, load balancers, auto scaling) |
| **Disaster recovery (DR)** | Recover from big failures: region outage, data deletion, ransomware |
| **RTO** (Recovery Time Objective) | How long you can be down: "back within 1 hour" |
| **RPO** (Recovery Point Objective) | How much data you can lose: "at most 15 minutes" |
| **Backup** | A point-in-time copy you can restore |
| **Replication** | Continuous copying to another place |

### The four DR strategies (cheapest → fastest)

| Strategy | What runs in the DR region | RTO | RPO | Cost |
|---|---|---|---|---|
| **Backup & restore** | Nothing; only backups | Hours | Hours | $ |
| **Pilot light** | Data replicated, core services off or minimal | 10s of minutes | Minutes | $$ |
| **Warm standby** | A scaled-down full copy running | Minutes | Seconds–minutes | $$$ |
| **Multi-site active/active** | Full capacity in both, serving traffic | ~0 | ~0 | $$$$ |

### Building blocks on AWS

| Layer | HA (within a region) | DR (across regions) |
|---|---|---|
| Compute | ASG / EKS nodes across ≥ 2 AZs | AMIs/images copied; IaC to rebuild |
| Load balancing | ALB across AZs | Route 53 failover / latency routing |
| Database | RDS **Multi-AZ** | Cross-region read replica / Aurora Global Database |
| Objects | S3 (multi-AZ by design) | **S3 Cross-Region Replication (CRR)** |
| Disks | EBS snapshots | Snapshot copies to another region |
| Everything | — | **AWS Backup** (central, cross-region copies, vault lock) |
| Infrastructure | — | **Terraform**: same code, different region |

### "Untested backups are just hopes"
Run **restore drills**. Measure the real RTO/RPO. Document it in a runbook.

### The Well-Architected Framework (six pillars)
Operational Excellence, Security, **Reliability**, Performance Efficiency, **Cost Optimization**, Sustainability. AWS's checklist for reviewing designs, often quoted in interviews.

## Cost
AWS Backup: storage only (cents for this lesson). CRR: storage in both regions plus replication transfer (cents). Cross-region RDS replicas and warm standby are where real DR costs appear.

## Console
AWS Backup → **Backup plans**, **Protected resources**, **Jobs**. S3 → bucket → **Management → Replication rules**.

## CLI
```bash
aws backup list-backup-plans
aws backup list-backup-jobs --by-state COMPLETED --max-results 5
aws backup start-backup-job --backup-vault-name lesson14 --resource-arn <arn> --iam-role-arn <backup-role-arn>
aws backup list-recovery-points-by-backup-vault --backup-vault-name lesson14
aws s3api get-bucket-replication --bucket <source-bucket>
aws s3api head-object --bucket <source> --key test.txt --query ReplicationStatus   # COMPLETED / PENDING / FAILED
aws ec2 copy-snapshot --source-region us-east-1 --source-snapshot-id snap-xxx --region us-west-2
```

## Terraform
**Part 1: AWS Backup plan for anything tagged `Backup = daily`**
```hcl
resource "aws_backup_vault" "main" {
  name          = "lesson14"
  force_destroy = true          # learning only
}

resource "aws_backup_plan" "daily" {
  name = "lesson14-daily"
  rule {
    rule_name         = "daily-7d"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 5 * * ? *)"      # 05:00 UTC daily
    lifecycle {
      delete_after = 7
    }
  }
}

data "aws_iam_policy_document" "backup_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["backup.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "backup" {
  name               = "lesson14-backup"
  assume_role_policy = data.aws_iam_policy_document.backup_trust.json
}

resource "aws_iam_role_policy_attachment" "backup" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

resource "aws_backup_selection" "tagged" {
  name         = "tagged-daily"
  plan_id      = aws_backup_plan.daily.id
  iam_role_arn = aws_iam_role.backup.arn
  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "daily"
  }
}
```

**Part 2: S3 Cross-Region Replication (us-east-1 → us-west-2)**
```hcl
provider "aws" {
  alias  = "dr"
  region = "us-west-2"
}

data "aws_caller_identity" "current" {}

locals {
  acct = data.aws_caller_identity.current.account_id
}

resource "aws_s3_bucket" "source" {
  bucket        = "lesson14-source-${local.acct}"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "source" {
  bucket = aws_s3_bucket.source.id
  versioning_configuration {
    status = "Enabled"              # replication requires versioning on BOTH buckets
  }
}

resource "aws_s3_bucket" "replica" {
  provider      = aws.dr
  bucket        = "lesson14-replica-${local.acct}"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "replica" {
  provider = aws.dr
  bucket   = aws_s3_bucket.replica.id
  versioning_configuration {
    status = "Enabled"
  }
}

data "aws_iam_policy_document" "s3_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "replication" {
  name               = "lesson14-replication"
  assume_role_policy = data.aws_iam_policy_document.s3_trust.json
}

data "aws_iam_policy_document" "replication" {
  statement {
    actions   = ["s3:GetReplicationConfiguration", "s3:ListBucket"]
    resources = [aws_s3_bucket.source.arn]
  }
  statement {
    actions   = ["s3:GetObjectVersionForReplication", "s3:GetObjectVersionAcl", "s3:GetObjectVersionTagging"]
    resources = ["${aws_s3_bucket.source.arn}/*"]
  }
  statement {
    actions   = ["s3:ReplicateObject", "s3:ReplicateDelete", "s3:ReplicateTags"]
    resources = ["${aws_s3_bucket.replica.arn}/*"]
  }
}

resource "aws_iam_role_policy" "replication" {
  name   = "replication"
  role   = aws_iam_role.replication.id
  policy = data.aws_iam_policy_document.replication.json
}

resource "aws_s3_bucket_replication_configuration" "source" {
  bucket     = aws_s3_bucket.source.id
  role       = aws_iam_role.replication.arn
  depends_on = [aws_s3_bucket_versioning.source, aws_s3_bucket_versioning.replica]

  rule {
    id     = "all-to-dr"
    status = "Enabled"
    filter {}
    delete_marker_replication {
      status = "Enabled"
    }
    destination {
      bucket        = aws_s3_bucket.replica.arn
      storage_class = "STANDARD_IA"        # cheaper copy in the DR region
    }
  }
}
```

## Verify
```bash
A=$(aws sts get-caller-identity --query Account --output text)
echo "dr test" > dr.txt && aws s3 cp dr.txt s3://lesson14-source-$A/dr.txt
sleep 30
aws s3api head-object --bucket lesson14-source-$A --key dr.txt --query ReplicationStatus   # "COMPLETED"
aws s3 ls s3://lesson14-replica-$A/ --region us-west-2                                    # dr.txt is there ✅
```
**Backup drill:** tag any EBS volume or DynamoDB table `Backup=daily`, run an on-demand job (`aws backup start-backup-job ...`), then **restore** it from the recovery point in the console and time it. That's your measured RTO.

## Clean up
`terraform destroy`

## Gotchas
- Replication only copies **new** objects after it's enabled (use S3 Batch Replication for existing ones).
- Replication is **one-way** unless you configure both directions.
- Deletes: delete markers replicate only if enabled; permanent version deletes never replicate (protection against malicious deletes).
- Backups in the **same account** don't protect against a compromised account. Copy to a separate account with **Vault Lock**.
- Multi-AZ isn't DR: it doesn't protect against a region failure or "I deleted the table."

## Interview questions
1. **RTO vs. RPO?** RTO = maximum downtime; RPO = maximum data loss, measured in time.
2. **Explain the four DR strategies.** Backup/restore → pilot light → warm standby → active/active: rising cost, falling RTO/RPO.
3. **RDS Multi-AZ: is it a DR solution?** It's HA within one region. For DR, add cross-region replicas/snapshots or Aurora Global Database.
4. **How do you protect backups from ransomware or a compromised admin?** Cross-account copies, AWS Backup Vault Lock (WORM), S3 Object Lock, MFA-protected deletion, least privilege.
5. **How do you know DR works?** Scheduled restore drills and game days that measure actual RTO/RPO, with runbooks.

---

# Lesson 15: Cost & FinOps

## Why it matters
Cloud bills grow quietly. **GPU workloads make cost the #1 concern**: one forgotten `p5` node costs more per month than a car. FinOps is making cost visible, owned, and optimized, and it's increasingly part of DevOps and platform roles.

## Concepts in plain words

| Tool / practice | What it does |
|---|---|
| **Budgets** | Alerts at % of a spend limit, actual or forecast (Lesson 01) |
| **Cost Explorer** | Graphs and filters of spend by service, account, tag, region |
| **Cost allocation tags** | Turn tags (`Project`, `Team`, `Environment`) into cost report dimensions; must be **activated** in Billing |
| **Cost Anomaly Detection** | ML that alerts on unusual spend spikes |
| **CUR / Data Exports** | Line-item billing data to S3 for Athena/QuickSight analysis |
| **Compute Optimizer** | Rightsizing recommendations for EC2, ASG, EBS, Lambda |
| **Trusted Advisor** | Checks for idle resources and savings |
| **Savings Plans / RIs** | Commit to usage for big discounts |
| **Spot** | Spare capacity at up to ~90% off, interruptible |

### The FinOps loop
```
Inform  → see who spends what (tags, dashboards, showback/chargeback)
Optimize → rightsize, spot, Savings Plans, scale to zero, delete waste
Operate  → budgets, anomaly alerts, policies (e.g., required tags), reviews
```

### Biggest savings levers (in typical order)
1. **Turn off what isn't used:** idle dev environments, forgotten GPUs, old snapshots, unattached EBS volumes, unused Elastic IPs, idle load balancers and **NAT gateways**
2. **Rightsize:** most instances are over-provisioned
3. **Scale to zero:** dev clusters at night; GPU node pools with Karpenter
4. **Spot** for interruptible work (batch, CI, some inference with fallback)
5. **Savings Plans** for the steady baseline
6. **Storage lifecycle:** S3 tiers, expiring versions, `gp2` → `gp3`
7. **Data transfer:** VPC endpoints instead of NAT for S3/ECR; keep traffic in-AZ where sensible

### GPU cost math (interview favourite)
```
Cost per 1M tokens = hourly instance price ÷ (tokens per second × 3600) × 1,000,000
```
Example: `g5.xlarge` at ~$1.006/hour serving **1,000 tokens/s** total:
`1.006 ÷ (1000 × 3600) × 1,000,000 ≈ $0.28 per million tokens`.
Double the throughput (batching, quantization) and you halve the cost per token. That's why vLLM tuning is a cost skill, not just a performance skill.

## Cost
Budgets (first two actions free), Anomaly Detection, Cost Explorer UI: free. The Cost Explorer **API** is ≈ $0.01 per request.

## Console
Billing → **Cost Explorer** (group by Service, then by Tag), **Budgets**, **Cost Anomaly Detection**, **Cost allocation tags** (activate `Project`, `Lesson`, `ManagedBy`). Compute Optimizer → recommendations.

## CLI
```bash
# Spend this month by service ($0.01 per call)
aws ce get-cost-and-usage --time-period Start=$(date +%Y-%m-01),End=$(date -d tomorrow +%F) \
  --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE \
  --query "ResultsByTime[0].Groups[].[Keys[0],Metrics.UnblendedCost.Amount]" --output table

# Spend by Project tag (after activating it)
aws ce get-cost-and-usage --time-period Start=$(date +%Y-%m-01),End=$(date -d tomorrow +%F) \
  --granularity MONTHLY --metrics UnblendedCost --group-by Type=TAG,Key=Project

# Find waste
aws ec2 describe-volumes --filters Name=status,Values=available \
  --query "Volumes[].[VolumeId,Size,CreateTime]" --output table                 # unattached EBS
aws ec2 describe-addresses --query "Addresses[?AssociationId==null].PublicIp"   # unused Elastic IPs
aws ec2 describe-nat-gateways --query "NatGateways[?State=='available'].[NatGatewayId,VpcId]"
aws ec2 describe-instances --filters Name=instance-state-name,Values=running \
  --query "Reservations[].Instances[].[InstanceId,InstanceType,Tags[?Key=='Name']|[0].Value]" --output table
```

## Terraform
```hcl
variable "alert_email" {
  type = string
}

# Budget per project tag
resource "aws_budgets_budget" "project" {
  name         = "ai-infra-learning"
  budget_type  = "COST"
  limit_amount = "30"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name   = "TagKeyValue"
    values = ["user:Project$ai-infra-learning"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }
}

# Anomaly detection across services
resource "aws_ce_anomaly_monitor" "services" {
  name              = "service-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_ce_anomaly_subscription" "email" {
  name             = "anomaly-alerts"
  frequency        = "DAILY"
  monitor_arn_list = [aws_ce_anomaly_monitor.services.arn]

  subscriber {
    type    = "EMAIL"
    address = var.alert_email
  }

  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
      match_options = ["GREATER_THAN_OR_EQUAL"]
      values        = ["5"]                       # alert on anomalies ≥ $5
    }
  }
}

# Activate tags for cost reports (the tag must already appear in billing data)
resource "aws_ce_cost_allocation_tag" "project" {
  tag_key = "Project"
  status  = "Active"
}
```
If the cost allocation tag errors with "tag not found," wait a day after first tagging resources, then apply again.

## Verify
Billing → Budgets shows `ai-infra-learning`. Cost Anomaly Detection → Monitors shows `service-monitor`. A day later, Cost Explorer → **Group by: Tag → Project** splits your spend.

## Clean up
Keep all of it: it's free and protects you for the rest of the course.

## Gotchas
- Tags only appear in cost reports **after activation**, and only for spend **after** activation.
- Tag everything from day one (`default_tags` in Terraform makes this automatic).
- Biggest hidden costs: **NAT gateway data processing**, cross-AZ/region data transfer, idle load balancers, public IPv4 addresses, CloudWatch Logs without retention, old snapshots.
- Savings Plans are a commitment: buy for the **stable baseline** only.

## Interview questions
1. **Your AWS bill doubled this month. How do you investigate?** Cost Explorer by service → by account/region → by tag; anomaly detection alerts; CloudTrail for what was created; then fix and prevent with budgets, tags, and policies.
2. **How do you reduce EC2 costs?** Turn off idle resources, rightsize, spot for interruptible work, Savings Plans for the baseline, Graviton where possible, autoscaling to zero for dev.
3. **How would you cut GPU inference costs?** Higher throughput per GPU (batching, quantization, vLLM tuning), scale to zero when idle, right GPU type per model, spot with fallback, Savings Plans for the baseline, cost per million tokens as the KPI.
4. **What are cost allocation tags?** Tags activated in Billing so spend can be grouped by them, enabling showback/chargeback per team or project.
5. **Savings Plans vs. Reserved Instances?** Savings Plans commit to $/hour spend and apply across instance families/regions (Compute SP); RIs commit to specific instance attributes.

---

# Lesson 16: AWS for ML

## Why it matters
This is where the module meets your AI/GPU DevOps goal. You need to know **which AWS option fits which ML workload**, and when to build on EKS versus buying a managed service.

## Concepts in plain words

### GPU and accelerator instances

| Family | Accelerator | GPU memory | Good for | On-demand (us-east-1, approx.) |
|---|---|---|---|---|
| `g4dn` | NVIDIA T4 | 16 GB | Small models, learning, cheap inference | `g4dn.xlarge` ≈ $0.53/h |
| `g5` | NVIDIA A10G | 24 GB | 7–13B models (quantized), mid inference | `g5.xlarge` ≈ $1.01/h |
| `g6` | NVIDIA L4 | 24 GB | Efficient inference | `g6.xlarge` ≈ $0.80/h |
| `g6e` | NVIDIA L40S | 48 GB | Larger models, more KV cache | `g6e.xlarge` ≈ $1.86/h |
| `p4d` / `p4de` | 8× A100 (40/80 GB) | 320/640 GB | Training, large-model serving | Tens of $/h |
| `p5` / `p5e` | 8× H100 / H200 | 640 GB+ | Frontier training and serving | Tens of $/h |
| `inf2` | AWS Inferentia2 | — | Low-cost inference (Neuron SDK) | Cheaper per token for supported models |
| `trn1` / `trn2` | AWS Trainium | — | Low-cost training (Neuron SDK) | — |

Prices change; check the EC2 pricing page. **Every GPU family needs its own quota** (G and VT for `g*`; P for `p*`), and capacity can be scarce.

### Getting GPU capacity

| Option | Guarantees capacity? | Use |
|---|---|---|
| On-Demand | No (can hit `InsufficientInstanceCapacity`) | Default |
| Spot | No, and can be reclaimed | Interruptible jobs |
| **On-Demand Capacity Reservations** | Yes, for as long as you pay | Production inference |
| **EC2 Capacity Blocks for ML** | Yes, for a booked window (days–weeks) | Planned training runs, launches |

### Ways to serve a model on AWS

| Option | You manage | Best when |
|---|---|---|
| **Bedrock** | Nothing; pay per token | You want hosted foundation models (Claude, Llama, Mistral…) via API |
| **SageMaker real-time endpoints** | Model + config | Managed hosting of your own model with autoscaling |
| **SageMaker serverless / async / batch** | Model | Spiky low traffic / long jobs / offline scoring |
| **EKS + vLLM on GPU nodes** | Everything | Full control, best cost at scale, portability: **the platform you're building** |
| **ECS on GPU EC2** | Most things | Simpler than Kubernetes, AWS-only |
| **EC2 + Docker** | Everything, manually | Prototypes |

### Build vs. buy

| Question | Leans to Bedrock / SageMaker | Leans to EKS + vLLM |
|---|---|---|
| Team has Kubernetes/GPU skills? | No | Yes |
| Traffic | Low or spiky | High and steady |
| Model | A hosted foundation model fits | Custom / fine-tuned / open weights |
| Cost at scale | Per-token pricing adds up | Cheaper per token when GPUs stay busy |
| Data residency / control | Fine with managed | Need full control |
| Time to market | Days | Weeks |

Many companies use **both**: Bedrock for general features, self-hosted models for high-volume or specialized ones.

### The supporting AWS stack for an LLM platform
```
Route 53 + ACM + CloudFront/WAF  →  ALB/NLB (API gateway layer: keys, rate limits)
   →  EKS (private subnets)
        ├─ GPU node pools (g5/g6e, Karpenter, taints, NVIDIA AMI)
        ├─ vLLM deployments (readiness probes, autoscaling on queue/latency)
        └─ Pod Identity → S3 (model weights) / Secrets Manager (HF token)
   S3 (weights, versioned) via gateway endpoint · ECR (images, scanned)
   CloudWatch / Managed Prometheus + Grafana (DCGM GPU metrics, vLLM metrics)
   Budgets + anomaly detection + tags (cost per team/model)
   Terraform for all of it, deployed by GitHub Actions via OIDC
```
Every lesson in this module maps to a box in that diagram.

## Cost
Bedrock: per input/output token. SageMaker endpoints: per instance-hour while running (they don't scale to zero by default; delete when done). GPU EC2: per hour. **The quota request itself is free.**

## Console
- **Service Quotas** → EC2 → "Running On-Demand G and VT instances" / "P instances"
- **EC2 → Capacity Reservations** → Capacity Blocks for ML (see availability and pricing)
- **Bedrock → Model catalog** (enable access to models before calling them) → Playgrounds
- **SageMaker AI → Inference → Endpoints**

## CLI
```bash
# GPU quotas
aws service-quotas get-service-quota --service-code ec2 --quota-code L-DB2E81BA --query Quota.Value   # G and VT vCPUs
aws service-quotas list-requested-service-quota-change-history --service-code ec2 \
  --query "RequestedQuotas[].[QuotaName,DesiredValue,Status]" --output table

# Where is a GPU type offered?
aws ec2 describe-instance-type-offerings --location-type availability-zone \
  --filters Name=instance-type,Values=g5.xlarge --query "InstanceTypeOfferings[].Location"

# GPU specs
aws ec2 describe-instance-types --instance-types g4dn.xlarge g5.xlarge g6.xlarge g6e.xlarge \
  --query "InstanceTypes[].[InstanceType,GpuInfo.Gpus[0].Name,GpuInfo.Gpus[0].MemoryInfo.SizeInMiB,VCpuInfo.DefaultVCpus]" --output table

# Bedrock: list models, then call one (after enabling access in the console)
aws bedrock list-foundation-models --query "modelSummaries[].modelId" --output text | tr '\t' '\n' | head -20
aws bedrock-runtime converse --model-id <model-id> \
  --messages '[{"role":"user","content":[{"text":"Explain KV cache in one sentence."}]}]' \
  --query "output.message.content[0].text" --output text

# SageMaker endpoints (and delete ones you forgot)
aws sagemaker list-endpoints --query "Endpoints[].[EndpointName,EndpointStatus]" --output table
```

## Terraform
No new resources in this lesson. The GPU node group is the commented `gpu` block in **Lesson 07**; uncomment it once your quota is approved. That GPU-enabled EKS cluster is **Phase 1–2 of the main project**.

## Verify
- Your G-instance quota shows ≥ 8 vCPUs
- `describe-instance-type-offerings` shows which AZs offer your GPU type, so you can pick subnets that actually have capacity

## Gotchas
- GPU quotas are **per region and per family**; approval can take hours to days.
- `InsufficientInstanceCapacity`: try another AZ or instance type; use several types in Karpenter or node groups.
- Bedrock models need **access enabled** per model and region first.
- SageMaker endpoints keep billing until deleted.
- Deep Learning AMIs and the EKS NVIDIA AMI include drivers; generic AMIs don't.

## Interview questions
1. **Which GPU would you pick for serving an 8B model, and why?** Typically `g5`/`g6` (24 GB): fits an 8B model at 4-bit/FP8 with room for KV cache; check throughput per dollar, and move to `g6e` (48 GB) for longer contexts or more concurrency.
2. **Bedrock vs. self-hosting on EKS?** Bedrock: zero ops, per-token pricing, hosted models. EKS + vLLM: control, custom models, lowest cost at steady high volume, but needs platform skills.
3. **How do you guarantee GPU capacity for a launch?** Capacity Reservations or Capacity Blocks, multiple AZs and instance types, quota requests well in advance.
4. **How do you keep GPU costs under control?** Scale to zero with Karpenter, maximize throughput per GPU, spot for interruptible work, Savings Plans for the baseline, tags and budgets per team/model, cost per million tokens as the KPI.

---

## Where to go next
- Practise the [Terraform practice ladder](TERRAFORM-ZERO-TO-ADVANCED.md#41-practice-ladder) alongside these lessons.
- Review the [interview notes](../../notes/module-02-aws-terraform-notes.md) before interviews.
- Then: **the main project**, EKS + GPU nodes + vLLM, built from Lessons 02, 07, 08, 09, 12, and 15.

*Part of my [AI Infrastructure learning log](../../README.md).*
