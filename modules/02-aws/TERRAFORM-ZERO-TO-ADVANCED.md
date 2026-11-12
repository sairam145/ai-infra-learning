# Terraform: Zero to Advanced

> **What this is:** my complete Terraform reference, every concept from the first `resource` block to production CI/CD, explained in plain words with working examples. All examples use **AWS** and **Terraform ≥ 1.6** with the **AWS provider 6.x**.
>
> **How to use it:** read Parts 1–3 in order once. After that, jump to whatever you need. Every section stands on its own.

---

## Contents

**Part 1: Foundations**
1. [What Terraform is (and isn't)](#1-what-terraform-is-and-isnt)
2. [How Terraform works: the mental model](#2-how-terraform-works-the-mental-model)
3. [Install and set up](#3-install-and-set-up)
4. [Your first project, line by line](#4-your-first-project-line-by-line)
5. [The core workflow: init, fmt, validate, plan, apply, destroy](#5-the-core-workflow)
6. [Project files and folders](#6-project-files-and-folders)

**Part 2: The language (HCL)**
7. [Syntax: blocks, arguments, comments](#7-syntax-blocks-arguments-comments)
8. [Types and values](#8-types-and-values)
9. [References: connecting things together](#9-references-connecting-things-together)
10. [Variables (inputs)](#10-variables-inputs)
11. [Locals (named values)](#11-locals-named-values)
12. [Outputs](#12-outputs)
13. [Data sources (reading what exists)](#13-data-sources-reading-what-exists)
14. [Expressions: conditionals, for, splat, templates](#14-expressions-conditionals-for-splat-templates)
15. [Built-in functions you'll actually use](#15-built-in-functions-youll-actually-use)

**Part 3: Resources in depth**
16. [Resource behaviour and dependencies](#16-resource-behaviour-and-dependencies)
17. [count and for_each: making many](#17-count-and-for_each-making-many)
18. [dynamic blocks](#18-dynamic-blocks)
19. [lifecycle: controlling change](#19-lifecycle-controlling-change)
20. [Preconditions, postconditions, and check blocks](#20-preconditions-postconditions-and-check-blocks)
21. [Providers in depth: versions, aliases, multi-region, multi-account](#21-providers-in-depth)

**Part 4: State**
22. [What state is and why it matters](#22-what-state-is-and-why-it-matters)
23. [Remote state on S3 with locking](#23-remote-state-on-s3-with-locking)
24. [State commands](#24-state-commands)
25. [Drift, refresh, and import](#25-drift-refresh-and-import)
26. [Refactoring safely: moved, removed, -replace](#26-refactoring-safely-moved-removed--replace)
27. [Workspaces](#27-workspaces)
28. [Secrets and sensitive data](#28-secrets-and-sensitive-data)

**Part 5: Modules and project structure**
29. [Modules: write once, reuse everywhere](#29-modules-write-once-reuse-everywhere)
30. [Using public modules (terraform-aws-modules)](#30-using-public-modules)
31. [Structuring real projects: environments and layers](#31-structuring-real-projects)
32. [Sharing data between stacks](#32-sharing-data-between-stacks)

**Part 6: Quality, testing, and automation**
33. [Formatting, linting, and security scanning](#33-formatting-linting-and-security-scanning)
34. [terraform test](#34-terraform-test)
35. [CI/CD: Terraform in GitHub Actions with OIDC](#35-cicd-terraform-in-github-actions-with-oidc)
36. [Team platforms: Terraform Cloud, Atlantis, OpenTofu](#36-team-platforms)

**Part 7: Reference**
37. [Command cheat sheet](#37-command-cheat-sheet)
38. [Troubleshooting catalogue](#38-troubleshooting-catalogue)
39. [Best practices checklist](#39-best-practices-checklist)
40. [Interview questions and answers](#40-interview-questions-and-answers)
41. [Practice ladder: exercises from easy to hard](#41-practice-ladder)

---

# Part 1: Foundations

## 1. What Terraform is (and isn't)

**Terraform is a tool that creates and manages cloud infrastructure from text files.** You write *what you want* (a VPC, a server, an IAM role), and Terraform figures out *how* to make AWS match.

**The analogy: an architect's blueprint.**
- The `.tf` files are the **blueprint**.
- AWS is the **building site**.
- Terraform is the **builder**: it compares the blueprint with what's on the site and builds, changes, or demolishes only what's different.

### Why companies use it

| Without Terraform (clicking in the console) | With Terraform |
|---|---|
| Nobody remembers exactly what was clicked | Everything is written down in code |
| Hard to repeat for staging and prod | Same code, different inputs |
| No review before changes | Changes go through pull requests |
| "Who changed this?" is a mystery | Git history shows who, what, and why |
| Rebuilding after a disaster takes days | `terraform apply` rebuilds it |
| Deleting everything is error-prone | `terraform destroy` removes exactly what it made |

### Key terms

| Term | Plain meaning |
|---|---|
| **IaC** (Infrastructure as Code) | Managing infrastructure with code instead of clicking |
| **Declarative** | You describe the *end result*, not the steps. "I want 3 servers," not "create server, then another, then another" |
| **Provider** | A plugin that knows how to talk to one platform (AWS, Kubernetes, GitHub, Cloudflare…) |
| **Resource** | One thing Terraform creates and manages (a bucket, a role, a VPC) |
| **State** | Terraform's memory: a file mapping your code to the real things it created |
| **Plan** | A preview of what will change |
| **Apply** | Actually making the changes |
| **Module** | A reusable folder of Terraform code |
| **HCL** | HashiCorp Configuration Language, the language `.tf` files are written in |

### Terraform vs. the alternatives

| Tool | What it is | When it's used |
|---|---|---|
| **Terraform** | Multi-cloud IaC, huge ecosystem | The industry default; most DevOps job posts ask for it |
| **OpenTofu** | Open-source fork of Terraform (Linux Foundation) | Same language and commands; chosen for licensing reasons |
| **CloudFormation** | AWS's own IaC (YAML/JSON) | AWS-only shops; some AWS features appear here first |
| **AWS CDK** | Write CloudFormation in Python/TypeScript | Teams that prefer real programming languages |
| **Pulumi** | IaC in Python/TypeScript/Go, multi-cloud | Developer-heavy teams |
| **Ansible** | Configuration management (what's *inside* servers) | Installing packages and configuring OSes. **Complements Terraform; doesn't replace it.** |

**Terraform creates the house; Ansible furnishes the rooms.** For containers and Kubernetes, the "furnishing" is usually done by Docker images and Helm instead.

---

## 2. How Terraform works: the mental model

Every `plan` and `apply` compares **three things**:

```
   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
   │  YOUR CODE   │     │    STATE     │     │  REAL AWS    │
   │  (.tf files) │     │ (Terraform's │     │ (what really │
   │  = desired   │     │    memory)   │     │   exists)    │
   └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
          │                    │    refresh: read    │
          │                    │◄────────────────────┘
          │      compare       │
          └────────►───────────┘
                    │
                    ▼
          PLAN: + create   ~ update   - destroy   -/+ replace
                    │
                    ▼ (apply)
           API calls to AWS → state updated
```

1. **Read the code:** what you *want*.
2. **Refresh:** ask AWS what *actually exists* for everything in state.
3. **Compare and plan:** the difference becomes a list of actions.
4. **Apply:** call the AWS APIs in the right order, then save the results to state.

### The dependency graph
Terraform works out the **order** automatically. If a subnet refers to a VPC, the VPC is created first. Independent things are created **in parallel** (10 at a time by default). You almost never write the order yourself.

### Idempotency
Running `apply` twice in a row makes **no changes** the second time, because reality already matches the code. This is the property that makes Terraform safe to re-run.

---

## 3. Install and set up

### Install (Ubuntu / WSL2)
```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
terraform -version
```

**Multiple versions?** Use **tfenv** (`tfenv install 1.9.8 && tfenv use 1.9.8`) when different projects need different Terraform versions.

### Credentials
Terraform's AWS provider uses the **same credentials as the AWS CLI**, in this order:
1. Arguments in the `provider` block (avoid; never hard-code keys)
2. Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_PROFILE`, `AWS_REGION`
3. `~/.aws/credentials` and `~/.aws/config` (the `default` profile, or `AWS_PROFILE`)
4. IAM roles: EC2 instance profile, ECS task role, EKS IRSA/Pod Identity, GitHub OIDC

Check who Terraform will act as: `aws sts get-caller-identity`. If the CLI works, Terraform works.

### VS Code
- Extension: **HashiCorp Terraform** (install it *in WSL* when using WSL)
- You get: syntax colors, autocomplete for resources and arguments, hover docs, format on save
- Format on save: Settings → search "format on save" → tick it

---

## 4. Your first project, line by line

A folder with four files, the standard layout:

```
my-first-tf/
├── versions.tf     # which Terraform + providers, and provider settings
├── variables.tf    # inputs
├── main.tf         # the resources
└── outputs.tf      # what to print after apply
```

**versions.tf**
```hcl
terraform {
  required_version = ">= 1.6"          # Terraform CLI version this code needs

  required_providers {
    aws = {
      source  = "hashicorp/aws"        # registry address of the AWS plugin
      version = "~> 6.0"               # any 6.x, never 7.0 (no surprise breaking changes)
    }
  }
}

provider "aws" {
  region = var.region                  # comes from variables.tf

  default_tags {                       # added to every taggable resource automatically
    tags = {
      ManagedBy = "terraform"
      Project   = "first-tf"
    }
  }
}
```

**variables.tf**
```hcl
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_prefix" {
  description = "Prefix for the S3 bucket name"
  type        = string
  default     = "first-tf"
}
```

**main.tf**
```hcl
# A random suffix, because S3 bucket names must be globally unique
resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "demo" {
  bucket = "${var.bucket_prefix}-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_versioning" "demo" {
  bucket = aws_s3_bucket.demo.id
  versioning_configuration {
    status = "Enabled"
  }
}
```
`random_id` comes from the **random** provider. Add it to `required_providers`:
```hcl
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
```

**outputs.tf**
```hcl
output "bucket_name" {
  value = aws_s3_bucket.demo.bucket
}
```

**Run it:**
```bash
terraform init
terraform plan
terraform apply          # type "yes"
terraform output bucket_name
terraform destroy        # clean up
```

---

## 5. The core workflow

| Step | Command | What it does | Changes AWS? |
|---|---|---|---|
| 1 | `terraform init` | Downloads providers and modules, sets up the backend. Run first, and again after adding providers/modules or changing the backend. | No |
| 2 | `terraform fmt` | Fixes spacing and alignment in `.tf` files | No |
| 3 | `terraform validate` | Checks syntax and internal consistency (types, references) | No |
| 4 | `terraform plan` | Shows exactly what would change | No |
| 5 | `terraform apply` | Makes the changes (asks for "yes") | **Yes** |
| 6 | `terraform destroy` | Deletes everything this configuration manages | **Yes** |

### Reading a plan

```
  # aws_s3_bucket.demo will be created
  + resource "aws_s3_bucket" "demo" {
      + bucket = "first-tf-1a2b3c4d"
      + arn    = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

| Symbol | Meaning | Worry level |
|---|---|---|
| `+` | create | Normal |
| `~` | update in place | Read what changes |
| `-` | destroy | **Stop and check** |
| `-/+` | destroy, then create a replacement | **Stop and check**: data loss, downtime |
| `+/-` | create the replacement first, then destroy (`create_before_destroy`) | Safer replace |
| `<=` | read (data source) | Normal |
| `(known after apply)` | Value assigned by AWS when created | Normal |
| `# forces replacement` | This change can't be done in place | **Why is it replacing?** |

**The golden rule: read every plan before applying.** Most Terraform disasters are a `-/+` on a database that nobody read.

### Saved plans (how teams do it)
```bash
terraform plan -out=tfplan      # save exactly this plan
terraform show tfplan           # review it again later
terraform apply tfplan          # apply exactly what was reviewed (no prompt)
```
CI pipelines post the saved plan on the pull request, and after approval apply **that same file**. Add `tfplan` to `.gitignore`; it can contain sensitive values.

### Useful flags

| Flag | Use |
|---|---|
| `terraform apply -auto-approve` | Skip the "yes" (only in automation) |
| `terraform plan -var="region=us-west-2"` | Set a variable |
| `terraform plan -var-file=prod.tfvars` | Load variables from a file |
| `terraform plan -target=aws_s3_bucket.demo` | Only that resource (**emergency use only**) |
| `terraform plan -destroy` | Preview a destroy |
| `terraform plan -refresh=false` | Skip reading AWS (faster; less accurate) |
| `terraform apply -parallelism=5` | Fewer simultaneous API calls (helps with rate limits) |
| `terraform init -upgrade` | Get the newest provider versions allowed by your constraints |

---

## 6. Project files and folders

### What Terraform creates

| File/folder | What it is | Commit to Git? |
|---|---|---|
| `*.tf` | Your code | ✅ Yes |
| `.terraform.lock.hcl` | Exact provider versions + checksums | ✅ **Yes**: everyone gets the same versions |
| `.terraform/` | Downloaded providers and modules (cache) | ❌ No |
| `terraform.tfstate` | **State**: Terraform's memory | ❌ **Never**: can contain secrets; use remote state |
| `terraform.tfstate.backup` | Previous state | ❌ Never |
| `*.tfvars` | Variable values | ✅ If no secrets; ❌ if it has any |
| `tfplan` | Saved plan | ❌ No |
| `crash.log` | Crash details | ❌ No |

### Standard `.gitignore`
```
.terraform/
*.tfstate
*.tfstate.*
*.tfplan
tfplan
crash.log
crash.*.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json
.terraformrc
terraform.rc
# secret variable files
secrets.auto.tfvars
*.secret.tfvars
```

### File naming conventions

| File | Contains |
|---|---|
| `versions.tf` (or `terraform.tf`) | `terraform {}` block, `required_providers` |
| `providers.tf` | `provider` blocks |
| `main.tf` | Main resources (split by topic when it grows: `network.tf`, `iam.tf`, `s3.tf`) |
| `variables.tf` | All `variable` blocks |
| `outputs.tf` | All `output` blocks |
| `locals.tf` | `locals` blocks |
| `data.tf` | `data` sources |
| `backend.tf` | Backend (remote state) configuration |
| `terraform.tfvars` | Default variable values (loaded automatically) |

**Terraform doesn't care about file names.** It reads every `.tf` file in the folder as one configuration. File names are only for humans.

---
# Part 2: The language (HCL)

## 7. Syntax: blocks, arguments, comments

Everything is a **block**:
```hcl
<BLOCK TYPE> "<LABEL>" "<LABEL>" {
  <ARGUMENT> = <VALUE>          # an argument: name = value

  <NESTED BLOCK> {              # a block inside a block (no "=")
    <ARGUMENT> = <VALUE>
  }
}
```

**Example, annotated:**
```hcl
resource "aws_s3_bucket" "logs" {   # block type: resource | label 1: resource TYPE | label 2: your NAME for it
  bucket = "my-logs-bucket"         # argument
  tags = {                          # argument whose value is a map (note the "=")
    Team = "platform"
  }
}
```

**Argument vs. nested block: the `=` sign matters.**
```hcl
tags = { Team = "platform" }        # argument: a map value → uses "="

versioning_configuration {          # nested block → NO "="
  status = "Enabled"
}
```
Which one to use is defined by the provider's documentation for each resource. If you get it wrong, `terraform validate` tells you.

### All the top-level block types

| Block | Labels | Purpose |
|---|---|---|
| `terraform` | none | Required versions, providers, backend |
| `provider` | provider name | Configure a provider |
| `resource` | type, name | Create and manage something |
| `data` | type, name | Read something that already exists |
| `variable` | name | An input |
| `output` | name | An exported value |
| `locals` | none | Named values computed inside the config |
| `module` | name | Use another folder of Terraform code |
| `import` | none | Bring an existing resource under management (1.5+) |
| `moved` | none | Tell Terraform a resource was renamed (1.1+) |
| `removed` | none | Stop managing a resource without destroying it (1.7+) |
| `check` | name | A health assertion that warns, never blocks (1.5+) |

### Comments
```hcl
# single-line comment (preferred style)
// also a single-line comment
/* multi-line
   comment */
```

### Naming rules
- Your names (labels): letters, digits, underscores, hyphens. **Convention: `snake_case`**, e.g. `aws_iam_role.lab_readonly`.
- Don't repeat the type in the name: `aws_s3_bucket.logs`, not `aws_s3_bucket.logs_bucket`.
- Use `this` or `main` when there's only one of something: `aws_vpc.main`.

---

## 8. Types and values

### Primitive types

| Type | Example | Notes |
|---|---|---|
| `string` | `"us-east-1"` | Always double quotes |
| `number` | `8`, `0.5` | Whole or decimal |
| `bool` | `true`, `false` | No quotes |
| `null` | `null` | "Not set": the argument acts as if omitted |

### Collection types

| Type | Example | Notes |
|---|---|---|
| `list(string)` | `["a", "b", "a"]` | Ordered, duplicates allowed, index from 0 |
| `set(string)` | `toset(["a", "b"])` | Unordered, no duplicates (good for `for_each`) |
| `map(string)` | `{ env = "dev", team = "ml" }` | Key → value, all values the same type |

### Structural types

| Type | Example | Notes |
|---|---|---|
| `object({...})` | `{ name = "web", port = 80 }` | Named fields, each with its own type |
| `tuple([...])` | `["web", 80, true]` | Fixed positions, each with its own type |

**Object type with optional fields (1.3+):**
```hcl
variable "node_group" {
  type = object({
    instance_type = string
    min_size      = number
    max_size      = number
    disk_gb       = optional(number, 50)       # optional, default 50
    labels        = optional(map(string), {})  # optional, default empty map
  })
}
```

### Strings: escapes, heredocs, templates
```hcl
"line one\nline two"               # \n newline, \" quote, \\ backslash
"Hello, ${var.name}!"              # interpolation
"%{ if var.prod }PROD%{ else }dev%{ endif }"   # template directive

user_data = <<-EOT                 # heredoc; "-" strips leading indentation
  #!/bin/bash
  echo "Region: ${var.region}" > /tmp/info
EOT
```
To write a literal `${`, escape it as `$${`. This comes up in shell scripts.

### Type conversion
Terraform converts automatically when it safely can (`"5"` ↔ `5`, `"true"` ↔ `true`). Explicitly: `tostring()`, `tonumber()`, `tobool()`, `tolist()`, `toset()`, `tomap()`.

---

## 9. References: connecting things together

| You want | Syntax | Example |
|---|---|---|
| A variable | `var.<name>` | `var.region` |
| A local | `local.<name>` | `local.common_tags` |
| A resource attribute | `<TYPE>.<NAME>.<ATTR>` | `aws_vpc.main.id` |
| A data source attribute | `data.<TYPE>.<NAME>.<ATTR>` | `data.aws_caller_identity.current.account_id` |
| A module output | `module.<NAME>.<OUTPUT>` | `module.vpc.private_subnets` |
| One of many (`count`) | `<TYPE>.<NAME>[<index>]` | `aws_subnet.private[0].id` |
| One of many (`for_each`) | `<TYPE>.<NAME>["<key>"]` | `aws_subnet.private["us-east-1a"].id` |
| All of many (splat) | `<TYPE>.<NAME>[*].<ATTR>` | `aws_subnet.private[*].id` |
| Inside `count` | `count.index` | `"web-${count.index}"` |
| Inside `for_each` | `each.key`, `each.value` | `each.value.cidr` |
| The current resource (in conditions/provisioners) | `self.<ATTR>` | `self.private_ip` |
| Paths | `path.module`, `path.root`, `path.cwd` | `file("${path.module}/policy.json")` |
| Current workspace | `terraform.workspace` | `"app-${terraform.workspace}"` |

**References create dependencies.** When `aws_subnet` uses `aws_vpc.main.id`, Terraform knows to create the VPC first. That's why you rarely need `depends_on`.

**Attributes vs. arguments:**
- **Arguments** are what *you* set (`cidr_block = "10.0.0.0/16"`).
- **Attributes** are what AWS *gives back* (`id`, `arn`). Every argument is also readable as an attribute.
- The resource's documentation page lists both: "Argument Reference" and "Attribute Reference".

---

## 10. Variables (inputs)

```hcl
variable "environment" {
  description = "Deployment environment"     # always write one
  type        = string
  default     = "dev"                         # no default = required input

  validation {                                # reject bad values early
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}

variable "db_password" {
  type      = string
  sensitive = true      # hidden in plan/apply output (still stored in state!)
  nullable  = false     # null is not accepted
}
```

### Ways to set a variable

| Method | Example |
|---|---|
| Default in the block | `default = "dev"` |
| Environment variable | `export TF_VAR_environment=prod` |
| `terraform.tfvars` (auto-loaded) | `environment = "prod"` |
| `*.auto.tfvars` (auto-loaded) | `prod.auto.tfvars` |
| `-var-file` | `terraform plan -var-file=envs/prod.tfvars` |
| `-var` | `terraform plan -var="environment=prod"` |
| Interactive prompt | If required and not set anywhere |

### Precedence (later wins)
1. `default` in the variable block
2. `TF_VAR_*` environment variables
3. `terraform.tfvars`
4. `terraform.tfvars.json`
5. `*.auto.tfvars` / `*.auto.tfvars.json` (alphabetical order)
6. `-var` and `-var-file` on the command line (in the order given)

**Example `envs/prod.tfvars`:**
```hcl
environment    = "prod"
instance_type  = "g5.xlarge"
min_nodes      = 2
allowed_cidrs  = ["10.0.0.0/8"]
tags           = { CostCenter = "ml-platform" }
```

### More validation examples
```hcl
variable "cidr" {
  type = string
  validation {
    condition     = can(cidrhost(var.cidr, 0))           # can() = "does this work without error?"
    error_message = "cidr must be a valid CIDR block, e.g. 10.0.0.0/16."
  }
}

variable "instance_type" {
  type = string
  validation {
    condition     = can(regex("^(g4dn|g5|g6|p4d|p5)\\.", var.instance_type))
    error_message = "Only GPU instance families are allowed."
  }
}
```

---

## 11. Locals (named values)

**Locals are named values computed inside the configuration.** Use them to avoid repeating yourself and to give complex expressions a readable name.

```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"       # "ml-platform-dev"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = "sairam"
  }

  is_prod = var.environment == "prod"
  azs     = slice(data.aws_availability_zones.available.names, 0, 3)
}

resource "aws_s3_bucket" "models" {
  bucket = "${local.name_prefix}-models"
  tags   = merge(local.common_tags, { Purpose = "model-weights" })
}
```

| | Variable | Local |
|---|---|---|
| Set from outside? | Yes (tfvars, CLI, env) | No |
| Can use other values/functions? | Only in `validation` | Yes, anything |
| Use for | Inputs that change per environment | Derived values, naming, tags |

---

## 12. Outputs

```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "db_password" {
  value     = random_password.db.result
  sensitive = true          # shown as (sensitive value) in the terminal
}
```

| Command | Shows |
|---|---|
| `terraform output` | All outputs |
| `terraform output vpc_id` | One output |
| `terraform output -raw vpc_id` | Without quotes (for scripts) |
| `terraform output -json` | Everything as JSON (sensitive values revealed!) |

**Outputs are how things connect:**
- **Module → parent:** `module.vpc.vpc_id`
- **Stack → stack:** `terraform_remote_state` reads another stack's outputs ([section 32](#32-sharing-data-between-stacks))
- **Terraform → scripts/CI:** `$(terraform output -raw cluster_name)`

---

## 13. Data sources (reading what exists)

A **data source reads** information without creating anything. It's shown as `<=` in a plan.

```hcl
# Who am I? (account ID, my ARN)
data "aws_caller_identity" "current" {}

# Which region am I in?
data "aws_region" "current" {}

# Which AZs are available here?
data "aws_availability_zones" "available" {
  state = "available"
}

# The newest Amazon Linux 2023 AMI, without hard-coding an ID
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# The latest EKS-optimized GPU AMI ID, from AWS's public parameter store
data "aws_ssm_parameter" "eks_gpu_ami" {
  name = "/aws/service/eks/optimized-ami/1.33/amazon-linux-2023/x86_64/nvidia/recommended/image_id"
}

# Something created outside this code (e.g., a VPC made by another team)
data "aws_vpc" "shared" {
  tags = { Name = "shared-vpc" }
}

# Build IAM policy JSON safely
data "aws_iam_policy_document" "read_models" {
  statement {
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = [aws_s3_bucket.models.arn, "${aws_s3_bucket.models.arn}/*"]
  }
}
```

**Use a data source when:**
- The thing already exists and isn't managed by this code
- You need dynamic lookups (latest AMI, account ID, AZ list)
- You're building policy JSON (`aws_iam_policy_document` is better than hand-written JSON: validated and composable)

**Avoid hard-coding:** AMI IDs, account IDs, and AZ names all differ between accounts and regions. Look them up.

---

## 14. Expressions: conditionals, for, splat, templates

### Conditional (ternary)
```hcl
instance_type = var.environment == "prod" ? "g5.2xlarge" : "g4dn.xlarge"
min_size      = local.is_prod ? 3 : 1
```
Pattern: `condition ? value_if_true : value_if_false`. Both sides must be the same type.

### Create something only sometimes
```hcl
resource "aws_cloudwatch_log_group" "debug" {
  count = var.enable_debug ? 1 : 0          # 0 = don't create
  name  = "/app/debug"
}
# refer to it safely:
# one(aws_cloudwatch_log_group.debug[*].name)  → the name, or null if not created
```

### `for` expressions (transforming collections)
```hcl
locals {
  names       = ["api", "worker", "gpu"]

  upper_names = [for n in local.names : upper(n)]                 # ["API","WORKER","GPU"]
  name_map    = { for n in local.names : n => "${n}-svc" }        # {api="api-svc", ...}
  only_gpu    = [for n in local.names : n if startswith(n, "gpu")]  # filter: ["gpu"]

  # map → list
  subnet_ids  = [for k, s in aws_subnet.private : s.id]

  # group by: "..." collects duplicates into lists
  by_az = { for s in var.subnets : s.az => s.cidr... }
}
```
- `[ for ... ]` produces a **list**; `{ for ... }` produces a **map**.
- `if` filters items.

### Splat
```hcl
aws_instance.web[*].id            # list of IDs (count resources)
values(aws_subnet.private)[*].id  # for_each resources: convert map → list first
```

### Operators

| Kind | Operators |
|---|---|
| Arithmetic | `+ - * / %` |
| Comparison | `== != < <= > >=` |
| Logic | `&& \|\| !` |

---

## 15. Built-in functions you'll actually use

Try any of them interactively with **`terraform console`**:
```bash
$ terraform console
> cidrsubnet("10.0.0.0/16", 8, 1)
"10.0.1.0/24"
> upper("gpu")
"GPU"
```

### Strings
| Function | Example → result |
|---|---|
| `format` | `format("%s-%03d", "node", 7)` → `"node-007"` |
| `join` / `split` | `join(",", ["a","b"])` → `"a,b"` |
| `lower` / `upper` / `title` | `upper("dev")` → `"DEV"` |
| `replace` | `replace("a-b-c", "-", "_")` → `"a_b_c"` |
| `trimspace` / `trimprefix` / `trimsuffix` | `trimsuffix("file.tf", ".tf")` → `"file"` |
| `substr` | `substr("abcdef", 0, 3)` → `"abc"` |
| `regex` / `regexall` | extract text with a pattern |
| `startswith` / `endswith` | `startswith("g5.xlarge","g5")` → `true` |

### Collections
| Function | Example → result |
|---|---|
| `length` | `length(["a","b"])` → `2` |
| `concat` | `concat(["a"], ["b"])` → `["a","b"]` |
| `merge` | `merge({a=1}, {b=2})` → `{a=1,b=2}` (later wins on conflicts) |
| `lookup` | `lookup(var.sizes, "prod", "small")` → value, or default |
| `contains` | `contains(["dev","prod"], "dev")` → `true` |
| `keys` / `values` | keys or values of a map |
| `element` | `element(["a","b"], 3)` → wraps around → `"b"` |
| `slice` | `slice(["a","b","c"], 0, 2)` → `["a","b"]` |
| `flatten` | `flatten([["a"],["b","c"]])` → `["a","b","c"]` |
| `distinct` | removes duplicates |
| `toset` / `tolist` / `tomap` | convert |
| `zipmap` | `zipmap(["a","b"], [1,2])` → `{a=1,b=2}` |
| `one` | the single element, or `null` if empty (errors if more) |
| `try` | `try(var.config.port, 8080)` → first that works |
| `can` | `can(tonumber("x"))` → `false` |
| `coalesce` | first non-null, non-empty value |

### Networking
| Function | Example → result |
|---|---|
| `cidrsubnet(prefix, newbits, num)` | `cidrsubnet("10.0.0.0/16", 8, 2)` → `"10.0.2.0/24"` |
| `cidrhost(prefix, n)` | `cidrhost("10.0.1.0/24", 5)` → `"10.0.1.5"` |
| `cidrnetmask` | `cidrnetmask("10.0.0.0/16")` → `"255.255.0.0"` |
| `cidrsubnets` | carve several subnets at once |

**`cidrsubnet` explained:** start with `/16`, add 8 bits → `/24` subnets; the third number picks which one (0, 1, 2…). A `/16` gives 256 possible `/24`s.

### Files and encoding
| Function | Use |
|---|---|
| `file("${path.module}/policy.json")` | Read a file as a string |
| `templatefile("${path.module}/user_data.sh.tftpl", { region = var.region })` | Read a file and fill in `${...}` variables |
| `jsonencode({...})` / `jsondecode(str)` | HCL ↔ JSON |
| `yamlencode` / `yamldecode` | HCL ↔ YAML (Kubernetes manifests, Helm values) |
| `base64encode` / `base64decode` | e.g., EC2 user data |
| `filemd5` / `filesha256` | Detect file changes (e.g., Lambda zip) |
| `fileset(path.module, "configs/*.yaml")` | List matching files |

### Type and time
`tostring`, `tonumber`, `tobool`, `type` (in console), `timestamp()` (changes every run; avoid in resources), `formatdate`.

---
# Part 3: Resources in depth

## 16. Resource behaviour and dependencies

### What happens when you change an argument
Every argument falls into one of two groups, listed in the provider docs:

| Change type | What Terraform does | Plan symbol | Example |
|---|---|---|---|
| **Updatable in place** | Calls an "update" API | `~` | Changing tags, an S3 bucket policy, an ASG's max size |
| **Forces replacement** | Destroys and recreates | `-/+` | Changing an EC2 instance's AMI, a subnet's CIDR, an RDS engine |

The plan marks the cause: `# forces replacement`. **Always look for it.**

### Implicit dependencies (automatic)
```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "a" {
  vpc_id     = aws_vpc.main.id       # ← this reference makes the VPC go first
  cidr_block = "10.0.1.0/24"
}
```

### Explicit dependencies: `depends_on`
Use it only when there's a **hidden** dependency that no reference shows:
```hcl
resource "aws_instance" "app" {
  ami           = data.aws_ami.al2023.id
  instance_type = "t3.micro"

  # The app reads S3 at boot via its IAM role, but nothing in this block refers to the policy.
  depends_on = [aws_iam_role_policy_attachment.app_s3]
}
```
Overusing `depends_on` slows plans and makes values unknown until apply. Prefer references.

### See the graph
```bash
terraform graph | dot -Tsvg > graph.svg    # needs graphviz: sudo apt install graphviz
```

### Meta-arguments (work on every resource)

| Meta-argument | Purpose | Section |
|---|---|---|
| `depends_on` | Hidden dependency | above |
| `count` | N copies by number | [17](#17-count-and-for_each-making-many) |
| `for_each` | One copy per map/set item | [17](#17-count-and-for_each-making-many) |
| `provider` | Use a specific provider configuration (alias) | [21](#21-providers-in-depth) |
| `lifecycle` | Control create/destroy behaviour | [19](#19-lifecycle-controlling-change) |

---

## 17. count and for_each: making many

### `count`: N identical-ish copies
```hcl
resource "aws_iam_user" "devs" {
  count = 3
  name  = "dev-${count.index}"        # dev-0, dev-1, dev-2
}
# addresses: aws_iam_user.devs[0], [1], [2]
```

### `for_each`: one per item, keyed by name
```hcl
variable "teams" {
  type    = set(string)
  default = ["ml", "platform", "data"]
}

resource "aws_s3_bucket" "team" {
  for_each = var.teams
  bucket   = "acme-${each.key}-artifacts"     # for a set, each.key == each.value
}
# addresses: aws_s3_bucket.team["ml"], ["platform"], ["data"]
```

**With a map of objects (the most useful form):**
```hcl
variable "subnets" {
  type = map(object({
    cidr = string
    az   = string
  }))
  default = {
    private-a = { cidr = "10.0.1.0/24", az = "us-east-1a" }
    private-b = { cidr = "10.0.2.0/24", az = "us-east-1b" }
  }
}

resource "aws_subnet" "private" {
  for_each          = var.subnets
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az
  tags              = { Name = each.key }
}
```

### count vs. for_each: which one?

| | `count` | `for_each` |
|---|---|---|
| Address | `[0]`, `[1]`, `[2]` (position) | `["private-a"]` (name) |
| Remove the middle item | **Everything after it shifts and gets destroyed/recreated** ⚠️ | Only that item is destroyed ✅ |
| Input | A number | A map or a set of strings |
| Best for | On/off switch (`count = var.enabled ? 1 : 0`), truly identical copies | **Almost everything else** |

**The classic count bug:**
```
count over ["a", "b", "c"]  →  [0]=a  [1]=b  [2]=c
remove "a"                  →  [0]=b  [1]=c
Terraform sees: [0] changed a→b, [1] changed b→c, [2] deleted   ← recreates b and c!
```
With `for_each`, removing `"a"` deletes only `["a"]`.

### for_each rules
- Keys must be **known at plan time**. You can't use an attribute that only exists after apply (like an ID) as a key.
- A list must be converted: `for_each = toset(var.names)`.
- You can't use `count` and `for_each` on the same resource.

### for_each over a nested structure
```hcl
locals {
  # every (team, env) pair
  team_envs = {
    for pair in setproduct(["ml", "data"], ["dev", "prod"]) :
    "${pair[0]}-${pair[1]}" => { team = pair[0], env = pair[1] }
  }
}

resource "aws_s3_bucket" "team_env" {
  for_each = local.team_envs
  bucket   = "acme-${each.value.team}-${each.value.env}"
}
```

---

## 18. dynamic blocks

Generate **repeated nested blocks** from a collection, for example security group rules:

```hcl
variable "ingress_ports" {
  type    = list(number)
  default = [22, 80, 443]
}

resource "aws_security_group" "web" {
  name   = "web"
  vpc_id = aws_vpc.main.id

  dynamic "ingress" {                    # the nested block's name
    for_each = var.ingress_ports
    content {                            # what each generated block contains
      from_port   = ingress.value        # iterator is named after the block
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["10.0.0.0/16"]
    }
  }
}
```
- `ingress.value` is the item; `ingress.key` is the index (lists) or key (maps).
- Rename the iterator with `iterator = port`, then use `port.value`.
- Make an optional block: `for_each = var.enable_x ? [1] : []`.

**Don't overuse it.** Dynamic blocks make code harder to read. For security group rules, separate `aws_vpc_security_group_ingress_rule` resources with `for_each` are cleaner.

---

## 19. lifecycle: controlling change

```hcl
resource "aws_db_instance" "main" {
  # ...

  lifecycle {
    prevent_destroy       = true              # any plan that destroys this → ERROR
    create_before_destroy = true              # on replace: build the new one first
    ignore_changes        = [tags["LastScanned"], desired_count]  # don't fight outside changes
    replace_triggered_by  = [terraform_data.app_version]          # replace when that changes
  }
}
```

| Setting | What it does | Use for |
|---|---|---|
| `prevent_destroy = true` | Refuses any plan that would destroy it | Databases, state buckets, KMS keys, anything you can't lose |
| `create_before_destroy = true` | New copy first, then delete the old one | Zero-downtime replacement: launch templates, certificates, security groups in use |
| `ignore_changes = [attr]` | Ignore drift on those attributes | Values changed by autoscalers, other tools, or AWS itself (e.g., an ASG's `desired_capacity`) |
| `ignore_changes = all` | Ignore every change after creation | Rarely; resources handed over to another system |
| `replace_triggered_by = [ref]` | Force replacement when another resource/attribute changes | Re-create instances when a config version changes |

**`create_before_destroy` catch:** the two copies exist at the same time, so **unique names clash**. Use `name_prefix` instead of `name` where the resource supports it.

### `terraform_data` (1.4+)
A built-in placeholder resource that holds a value and triggers replacement. It replaced the old `null_resource`:
```hcl
resource "terraform_data" "app_version" {
  input = var.app_version          # change this → anything with replace_triggered_by gets replaced
}
```

### Provisioners: last resort
`local-exec` and `remote-exec` run scripts during create or destroy. **HashiCorp itself calls them a last resort**: they aren't in the plan, failures leave half-built resources, and they don't re-run on change. Prefer user data, cloud-init, baked AMIs (Packer), or configuration tools.
```hcl
provisioner "local-exec" {
  command = "echo ${self.private_ip} >> inventory.txt"
}
```

---

## 20. Preconditions, postconditions, and check blocks

### `precondition` / `postcondition`: block bad applies
```hcl
resource "aws_instance" "gpu" {
  ami           = data.aws_ami.gpu.id
  instance_type = var.instance_type

  lifecycle {
    precondition {                                       # checked BEFORE create/update
      condition     = data.aws_ami.gpu.architecture == "x86_64"
      error_message = "The GPU AMI must be x86_64."
    }
    postcondition {                                      # checked AFTER, using self
      condition     = self.public_ip == ""
      error_message = "GPU instances must not get a public IP."
    }
  }
}
```
Outputs can have preconditions too. If a condition fails, **the run stops with your error message.**

### `check` blocks (1.5+): warn, never block
```hcl
check "model_endpoint_healthy" {
  data "http" "health" {
    url = "https://${aws_lb.api.dns_name}/health"
  }
  assert {
    condition     = data.http.health.status_code == 200
    error_message = "Model API health check is failing."
  }
}
```
A failed check prints a **warning** on every plan and apply but doesn't stop anything. It's continuous validation, e.g., "is the certificate about to expire?" or "is the endpoint up?". (The `http` data source comes from the `hashicorp/http` provider.)

| | Variable `validation` | `precondition` / `postcondition` | `check` |
|---|---|---|---|
| Checks | Input values | Assumptions around one resource | Overall health |
| On failure | Error | Error | **Warning only** |

---

## 21. Providers in depth

### Version constraints

| Constraint | Allows |
|---|---|
| `= 6.2.0` | Exactly that version |
| `>= 6.0` | 6.0 or newer, including 7.x (risky) |
| `~> 6.0` | ≥ 6.0 and < 7.0 ✅ (recommended for root modules) |
| `~> 6.2.0` | ≥ 6.2.0 and < 6.3.0 (patches only) |
| `>= 6.0, < 7.0` | Same as `~> 6.0`, explicit |

### The lock file
`.terraform.lock.hcl` records the **exact** version chosen and its checksums. Commit it. Upgrade deliberately:
```bash
terraform init -upgrade                                  # move to the newest allowed versions
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64 -platform=windows_amd64
#   ↑ record checksums for teammates on other operating systems
```

### Aliases: multiple configurations of one provider
```hcl
provider "aws" {
  region = "us-east-1"                 # default (no alias)
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

resource "aws_s3_bucket" "replica" {
  provider = aws.west                  # this bucket goes to us-west-2
  bucket   = "acme-models-replica"
}
```
Typical uses: cross-region replication and DR, **ACM certificates for CloudFront (must be in us-east-1)**, and multiple accounts.

### Multi-account: assume a role
```hcl
provider "aws" {
  alias  = "prod"
  region = "us-east-1"
  assume_role {
    role_arn     = "arn:aws:iam::111122223333:role/terraform-deploy"
    session_name = "terraform"
  }
}
```
This is how one pipeline deploys to dev, staging, and prod accounts: same code, different role.

### Passing providers to modules
```hcl
module "dr_bucket" {
  source    = "./modules/bucket"
  providers = {
    aws = aws.west                      # inside the module, "aws" means aws.west
  }
}
```

### Useful AWS provider settings
```hcl
provider "aws" {
  region              = "us-east-1"
  allowed_account_ids = ["111122223333"]   # refuse to run against any other account
  default_tags {
    tags = { ManagedBy = "terraform", Repo = "ai-infra-learning" }
  }
}
```
`allowed_account_ids` is a cheap safety net against applying dev code to prod credentials.

### Provider-defined functions (1.8+)
Providers can ship their own functions:
```hcl
locals {
  parsed = provider::aws::arn_parse(aws_iam_role.app.arn)   # → { account_id, service, resource, ... }
}
```

### Other providers DevOps engineers use with AWS

| Provider | Manages |
|---|---|
| `hashicorp/kubernetes` | Kubernetes objects (namespaces, service accounts) |
| `hashicorp/helm` | Helm releases (install charts from Terraform) |
| `hashicorp/random` | Random names, passwords, IDs |
| `hashicorp/tls` | Keys and certificates |
| `hashicorp/http` | HTTP GET in data sources and checks |
| `hashicorp/archive` | Zip files (Lambda packages) |
| `integrations/github` | Repos, secrets, branch protection |
| `cloudflare/cloudflare`, `DataDog/datadog`, `PagerDuty/pagerduty` | DNS, monitoring, on-call |

---
# Part 4: State

## 22. What state is and why it matters

**State is Terraform's memory.** It's a JSON file that maps each block in your code to the real thing in AWS:
```
aws_iam_role.lab_readonly   →   arn:aws:iam::111122223333:role/lab-readonly
aws_s3_bucket.models        →   bucket "acme-models-7f3a"
```

**Why Terraform needs it:**
1. **Mapping:** to know which real resource each block controls. Without state, `apply` would create duplicates.
2. **Speed:** it doesn't have to search all of AWS to find its resources.
3. **Dependencies for deletion:** it remembers the order things must be deleted in, even after you remove the code.
4. **Remembering outputs and attributes** that other stacks read.

**Three things to know about state:**
- **It can contain secrets in plain text:** database passwords, private keys, tokens. **Never commit it to Git.**
- **It must never be edited by hand.** Use the `terraform state` commands.
- **Two people applying at once can corrupt it.** That's why teams use **remote state with locking**.

### Local vs. remote state

| | Local (`terraform.tfstate` on my laptop) | Remote (S3, Terraform Cloud…) |
|---|---|---|
| Teamwork | ❌ Only on one machine | ✅ Everyone shares one state |
| Locking | ❌ | ✅ Stops two applies at once |
| Backup and versioning | ❌ Lose the laptop, lose the state | ✅ S3 versioning |
| Encryption | ❌ | ✅ |
| Use for | Learning, throwaway experiments | **Everything real** |

---

## 23. Remote state on S3 with locking

### Step 1: Create the state bucket once (the "bootstrap")
The bucket must exist **before** the backend can use it. Create it with a tiny separate Terraform config (with local state) or by hand, and never manage it from the state stored inside it.

```hcl
# bootstrap/main.tf
resource "aws_s3_bucket" "tfstate" {
  bucket = "sairam-tfstate-<account-id>"      # globally unique; including the account ID helps
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  versioning_configuration {
    status = "Enabled"                         # recover old state versions
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "tfstate" {
  bucket                  = aws_s3_bucket.tfstate.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### Step 2: Point each project at it
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket       = "sairam-tfstate-<account-id>"
    key          = "module-02/lesson-02-vpc/terraform.tfstate"   # unique path per stack
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true      # native S3 locking (Terraform 1.10+)
  }
}
```
Then:
```bash
terraform init                     # "Successfully configured the backend s3!"
terraform init -migrate-state      # if you already had local state: copies it into S3
```

### Locking, explained
While someone runs `plan` or `apply`, Terraform holds a **lock**. A second run waits or fails with `Error acquiring the state lock`. This stops two people from corrupting the state at the same moment.
- **Modern (1.10+):** `use_lockfile = true` stores a `.tflock` file next to the state in S3.
- **Older setups:** a **DynamoDB table** with a `LockID` key (`dynamodb_table = "terraform-locks"`). This is now deprecated, but you'll see it in many companies.

If a crashed run leaves a stale lock, and **only after confirming nobody is running**:
```bash
terraform force-unlock <LOCK_ID>
```

### Backend rules
- **Backend blocks can't use variables.** Values must be literal, or passed at init time:
  ```bash
  terraform init -backend-config="key=prod/vpc.tfstate" -backend-config=backend-prod.hcl
  ```
  This "partial configuration" is how one codebase uses different state files per environment.
- Changing backend settings requires `terraform init -reconfigure` (start fresh) or `-migrate-state` (move the state).
- One state file per stack. Never share one key between two folders.

### Permissions needed for the S3 backend
`s3:ListBucket` on the bucket; `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject` on the state key **and** on the `.tflock` key; KMS permissions if encrypted with a customer-managed key.

---

## 24. State commands

| Command | What it does |
|---|---|
| `terraform state list` | Every resource address in state |
| `terraform state show aws_s3_bucket.models` | All recorded attributes of one resource |
| `terraform show` | Human-readable view of the whole state |
| `terraform show -json \| jq` | Machine-readable state |
| `terraform state mv A B` | Rename an address (prefer `moved` blocks, [section 26](#26-refactoring-safely-moved-removed--replace)) |
| `terraform state rm A` | Forget a resource; it **stays in AWS** (prefer `removed` blocks) |
| `terraform state pull > backup.tfstate` | Download the current state (take a backup before risky work) |
| `terraform state push backup.tfstate` | Upload a state file (**dangerous**; last resort) |
| `terraform state replace-provider A B` | Change a provider's source address |

**Before any state surgery: `terraform state pull > backup-$(date +%F).tfstate`.**

---

## 25. Drift, refresh, and import

### Drift: when reality no longer matches the code
Someone changes something in the console: adds a tag, opens a port, resizes an instance. That's **drift**.

| Command | What it does |
|---|---|
| `terraform plan` | Shows drift as changes needed to put things back the way the code says |
| `terraform plan -refresh-only` | Shows **only** what changed outside Terraform |
| `terraform apply -refresh-only` | Accepts those outside changes **into state** without touching AWS |

**What to do about drift:**
- The outside change was wrong → `terraform apply` puts things back.
- The outside change was right → **update the code to match**, then plan shows no changes.
- Something changes it constantly (an autoscaler) → `lifecycle { ignore_changes = [...] }`.

Teams detect drift by running a scheduled `terraform plan -detailed-exitcode` in CI. Exit codes: **0** = no changes, **1** = error, **2** = changes or drift present.

### Import: adopting resources created outside Terraform

**Modern way: `import` blocks (1.5+)**
```hcl
# import.tf
import {
  to = aws_s3_bucket.legacy
  id = "old-bucket-made-in-console"
}
```
```bash
terraform plan -generate-config-out=generated.tf   # Terraform WRITES the resource code for you
# review and tidy generated.tf, move it into main.tf
terraform plan     # should show: 1 to import, 0 to add, 0 to change
terraform apply
```
Delete the `import` block afterwards. It's done its job.

Import many with `for_each`:
```hcl
import {
  for_each = toset(["bucket-a", "bucket-b"])
  to       = aws_s3_bucket.legacy[each.key]
  id       = each.key
}
```

**Old way (still works):** `terraform import aws_s3_bucket.legacy old-bucket-made-in-console`. You must write the resource block yourself first, and nothing shows in a plan beforehand.

**The import ID differs by resource type.** Every resource's documentation ends with an "Import" section saying what to use (a bucket name, an instance ID, `role-name/policy-arn`, etc.).

---

## 26. Refactoring safely: moved, removed, -replace

### Renaming without destroying: `moved` (1.1+)
You rename `aws_s3_bucket.bucket` to `aws_s3_bucket.models`. Without help, Terraform plans to **destroy the old one and create a new one**. Instead:
```hcl
moved {
  from = aws_s3_bucket.bucket
  to   = aws_s3_bucket.models
}
```
The plan now shows `has moved to`, with no destroy. It works for moving resources into modules too:
```hcl
moved {
  from = aws_vpc.main
  to   = module.network.aws_vpc.this
}
```
And for switching `count` to `for_each`:
```hcl
moved {
  from = aws_subnet.private[0]
  to   = aws_subnet.private["us-east-1a"]
}
```
Keep `moved` blocks for a while (until every environment has applied them), then delete them.

### Stop managing without deleting: `removed` (1.7+)
```hcl
removed {
  from = aws_s3_bucket.legacy
  lifecycle {
    destroy = false          # forget it in state; leave it in AWS
  }
}
```
This is the reviewable, in-code version of `terraform state rm`.

### Force a rebuild: `-replace`
```bash
terraform apply -replace="aws_instance.gpu_worker"
```
This destroys and recreates one resource, e.g., a broken instance. It replaced the old `terraform taint`, which is deprecated.

---

## 27. Workspaces

**Workspaces = several state files for the same code in the same folder.**
```bash
terraform workspace list
terraform workspace new dev
terraform workspace new prod
terraform workspace select dev
terraform workspace show
```
```hcl
locals {
  instance_type = terraform.workspace == "prod" ? "g5.2xlarge" : "g4dn.xlarge"
}
```
With the S3 backend, non-default workspaces are stored under `env:/<workspace>/<key>`.

**Workspaces vs. separate folders per environment:**

| | CLI workspaces | Folder per environment (`envs/dev`, `envs/prod`) |
|---|---|---|
| Code | Exactly the same | Same modules, small per-env root files |
| Easy to see what's deployed where | ❌ Hidden in a command | ✅ Visible in the repo |
| Different backends/accounts per env | ❌ Hard | ✅ Easy |
| Mistake risk | Higher ("I thought I was on dev") | Lower |
| Industry use | Temporary/feature environments | **Most common for dev/staging/prod** |

**Common advice:** use folders (or separate state keys plus tfvars) for long-lived environments, and workspaces for short-lived copies.

---

## 28. Secrets and sensitive data

### Rules
1. **Never put secrets in `.tf` or committed `.tfvars` files.**
2. **Assume state contains secrets.** Encrypt the backend and restrict who can read it.
3. `sensitive = true` hides values in output **but not in state**.

### Patterns

**Let AWS generate and store the secret (best for databases):**
```hcl
resource "aws_db_instance" "main" {
  # ...
  manage_master_user_password = true    # RDS creates the password in Secrets Manager; it's never in state
}
```

**Read an existing secret at runtime, not in Terraform:**
Give the app's IAM role `secretsmanager:GetSecretValue`, and let the app fetch the secret itself. Terraform only creates the secret *container* and the permissions.

**Write-only arguments (Terraform 1.11+, supported by some resources):** values that are sent to AWS but **never saved in state**:
```hcl
resource "aws_secretsmanager_secret_version" "api_key" {
  secret_id                = aws_secretsmanager_secret.api_key.id
  secret_string_wo         = var.api_key        # write-only: not stored in state
  secret_string_wo_version = 1                  # bump this to send a new value
}
```

**Ephemeral values (1.10+):** `ephemeral "..."` resources and `ephemeral = true` variables exist only during a run and are never written to plan or state files. Use them for short-lived tokens and passwords passed into write-only arguments.

**Pass secrets via environment variables in CI:** `TF_VAR_api_key` comes from GitHub Secrets or AWS Secrets Manager, never from files.

---
# Part 5: Modules and project structure

## 29. Modules: write once, reuse everywhere

**A module is just a folder of `.tf` files.** The folder you run `terraform` in is the **root module**. Any folder it calls is a **child module**.

**The analogy:** a module is a **function**. Variables are its parameters, resources are the body, and outputs are its return values.

### Write a module
```
modules/
└── s3-bucket/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── versions.tf
    └── README.md
```

**modules/s3-bucket/variables.tf**
```hcl
variable "name" {
  description = "Bucket name"
  type        = string
}

variable "versioning" {
  description = "Enable versioning"
  type        = bool
  default     = true
}

variable "tags" {
  type    = map(string)
  default = {}
}
```

**modules/s3-bucket/main.tf**
```hcl
resource "aws_s3_bucket" "this" {
  bucket = var.name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = var.versioning ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket                  = aws_s3_bucket.this.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

**modules/s3-bucket/outputs.tf**
```hcl
output "id"  { value = aws_s3_bucket.this.id }
output "arn" { value = aws_s3_bucket.this.arn }
```

**modules/s3-bucket/versions.tf** (child modules declare providers, but **don't configure them**)
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.0"          # modules use a minimum; the root module pins with ~>
    }
  }
}
```

### Use it
```hcl
module "models_bucket" {
  source = "./modules/s3-bucket"
  name   = "acme-models-${var.environment}"
  tags   = local.common_tags
}

module "logs_bucket" {
  source     = "./modules/s3-bucket"
  name       = "acme-logs-${var.environment}"
  versioning = false
}

# use the outputs
resource "aws_iam_policy" "read_models" {
  name   = "read-models"
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject"]
      Resource = "${module.models_bucket.arn}/*"
    }]
  })
}
```
Run `terraform init` again after adding a module.

### Module sources

| Source | Example |
|---|---|
| Local folder | `source = "./modules/s3-bucket"` |
| Terraform Registry | `source = "terraform-aws-modules/vpc/aws"` plus `version = "~> 6.0"` |
| GitHub | `source = "github.com/acme/tf-modules//s3-bucket?ref=v1.4.0"` |
| Any Git (SSH) | `source = "git::ssh://git@github.com/acme/tf-modules.git//s3-bucket?ref=v1.4.0"` |
| S3 | `source = "s3::https://s3.amazonaws.com/acme-modules/s3-bucket.zip"` |

- `//` separates the repo from a subfolder.
- **Always pin a version** (`version =` for the registry, `?ref=` a tag for Git). Unpinned modules change under you.

### Meta-arguments on modules
`count`, `for_each`, `depends_on`, and `providers` all work on `module` blocks:
```hcl
module "team_bucket" {
  source   = "./modules/s3-bucket"
  for_each = toset(["ml", "data"])
  name     = "acme-${each.key}"
}
# outputs: module.team_bucket["ml"].arn
```

### What makes a good module

| Do | Don't |
|---|---|
| One clear job (network, cluster, bucket-with-policies) | A "god module" that builds everything |
| Sensible, secure defaults | Make callers set 40 variables |
| `description` and `type` on every variable | Untyped `any` everywhere |
| Output every ID/ARN a caller might need | Make callers use data sources to find what you made |
| Version and tag releases | Point everyone at `main` |
| A README with an example | Make people read the code to learn the inputs |
| Keep provider configuration in the root | Put `provider` blocks inside child modules |

**Don't wrap a single resource in a module** unless the module adds real value: defaults, policies, naming.

---

## 30. Using public modules

The **terraform-aws-modules** collection (on registry.terraform.io) is the de-facto standard for AWS. Most companies use these modules directly, or wrap them.

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"

  name = "ml-platform"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true          # one NAT for dev (cheaper); one per AZ for prod
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"
  # ...
}
```

**Before using any public module:**
- Read its **README inputs/outputs** and **examples/** folder.
- Check the **major version** you're pinning. Major versions rename inputs; `vpc` v5 → v6 and `eks` v20 → v21 both changed variable names. Read the upgrade guide when bumping.
- Run `terraform plan` and read what it creates: modules can create **far more** than you expect (NAT gateways, flow logs, KMS keys) and those cost money.

---

## 31. Structuring real projects

### Small project
```
infra/
├── versions.tf
├── backend.tf
├── variables.tf
├── main.tf
├── outputs.tf
└── terraform.tfvars
```

### Environments: one folder per environment, shared modules
```
infra/
├── modules/                    # reusable building blocks (versioned)
│   ├── network/
│   ├── eks-cluster/
│   └── s3-bucket/
└── envs/
    ├── dev/
    │   ├── backend.tf          # key = "dev/platform.tfstate"
    │   ├── main.tf             # calls ../../modules/...
    │   └── terraform.tfvars    # dev sizes: small, single NAT, spot
    ├── staging/
    └── prod/
        ├── backend.tf          # different account or bucket
        ├── main.tf
        └── terraform.tfvars    # prod sizes: multi-AZ, on-demand, deletion protection
```
**The rule: environments differ only by inputs (tfvars), never by copied code.**

### Layers: split by how often things change and how risky they are
```
infra/
├── 00-bootstrap/   state bucket, OIDC role for CI          (once)
├── 10-network/     VPC, subnets, NAT, endpoints             (rarely changes)
├── 20-cluster/     EKS, node groups, IAM                    (sometimes)
├── 30-platform/    add-ons: GPU operator, monitoring        (often)
└── 40-apps/        app-specific buckets, queues, DNS        (very often)
```
Each layer is its **own state**. This gives:
- **Smaller blast radius:** a mistake in `40-apps` can't destroy the VPC.
- **Faster plans:** fewer resources to refresh.
- **Clearer ownership:** the network team owns `10-network`.

Lower layers publish **outputs**; higher layers read them ([section 32](#32-sharing-data-between-stacks)).

### Naming and tagging conventions
```hcl
locals {
  name = "${var.project}-${var.environment}"         # acme-ml-prod
  tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    CostCenter  = var.cost_center
    ManagedBy   = "terraform"
    Repo        = "github.com/sairam145/ai-infra-learning"
  }
}
```
Tags drive **cost reports**, ownership, and automation (e.g., "stop every `Environment=dev` instance at night").

---

## 32. Sharing data between stacks

### Option 1: `terraform_remote_state` (read another stack's outputs)
```hcl
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "sairam-tfstate-<account-id>"
    key    = "10-network/terraform.tfstate"
    region = "us-east-1"
  }
}

module "eks" {
  # ...
  vpc_id     = data.terraform_remote_state.network.outputs.vpc_id
  subnet_ids = data.terraform_remote_state.network.outputs.private_subnet_ids
}
```
**Downside:** the reader needs access to the *whole* state file, including any secrets in it.

### Option 2: data sources by tag (loosely coupled)
```hcl
data "aws_vpc" "main" {
  tags = { Name = "ml-platform", Environment = var.environment }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
  tags = { Tier = "private" }
}
```

### Option 3: SSM Parameter Store (publish and subscribe)
```hcl
# network stack publishes
resource "aws_ssm_parameter" "vpc_id" {
  name  = "/platform/${var.environment}/vpc_id"
  type  = "String"
  value = module.vpc.vpc_id
}

# cluster stack reads
data "aws_ssm_parameter" "vpc_id" {
  name = "/platform/${var.environment}/vpc_id"
}
```

| Option | Coupling | Security | Common in |
|---|---|---|---|
| `terraform_remote_state` | Tight (needs the state's bucket and key) | Reader sees the whole state | Small teams |
| Data sources by tag | Loose | Only normal AWS read permissions | Many teams |
| SSM parameters | Loose, explicit contract | Fine-grained IAM per parameter | Larger orgs |

---
# Part 6: Quality, testing, and automation

## 33. Formatting, linting, and security scanning

| Tool | Catches | Command |
|---|---|---|
| `terraform fmt` | Formatting | `terraform fmt -recursive` (fix) · `terraform fmt -check -recursive` (CI: fail if unformatted) |
| `terraform validate` | Syntax, types, bad references | `terraform validate` (after `init`) |
| **TFLint** | Provider-specific mistakes: invalid instance types, deprecated syntax, unused variables | `tflint --init && tflint --recursive` |
| **Trivy** (`trivy config`) | Security misconfigurations: public buckets, open security groups, no encryption | `trivy config .` |
| **Checkov** | Same idea; large policy library | `checkov -d .` |
| **terraform-docs** | Writes the module README inputs/outputs table | `terraform-docs markdown table . > README.md` |
| **Infracost** | Cost estimate of a plan, posted on PRs | `infracost breakdown --path .` |

**`.tflint.hcl` with the AWS ruleset:**
```hcl
plugin "aws" {
  enabled = true
  version = "0.38.0"   # pin the latest release from the tflint-ruleset-aws GitHub page
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}
```

**Run everything on every commit with pre-commit** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.96.1
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_trivy
      - id: terraform_docs
```

**Silencing a finding on purpose:** add a comment explaining *why*, e.g. `#trivy:ignore:AVD-AWS-0089 -- access logging not needed for the log bucket itself`. Never silence findings blindly.

---

## 34. terraform test

Built-in tests (1.6+), written in `.tftest.hcl` files inside a `tests/` folder:

```hcl
# tests/s3_bucket.tftest.hcl
variables {
  name = "test-bucket-tf"
}

run "versioning_on_by_default" {
  command = plan                     # plan only: fast, creates nothing

  assert {
    condition     = aws_s3_bucket_versioning.this.versioning_configuration[0].status == "Enabled"
    error_message = "Versioning should be enabled by default."
  }
}

run "versioning_can_be_disabled" {
  command = plan
  variables {
    versioning = false
  }
  assert {
    condition     = aws_s3_bucket_versioning.this.versioning_configuration[0].status == "Suspended"
    error_message = "versioning=false should suspend versioning."
  }
}
```
```bash
terraform test
```

| `command =` | What happens | Cost |
|---|---|---|
| `plan` | Only plans and checks assertions | Free, seconds |
| `apply` (default) | **Really creates** resources, checks, then destroys them | Real AWS cost and time |

**Mock providers (1.7+):** test without any AWS credentials:
```hcl
mock_provider "aws" {}
```
Use them for logic-heavy modules (naming, conditionals, for_each maps).

**Terratest** (Go) is the older, more powerful option: deploy for real, then make HTTP calls, SSH, and so on. Many companies still use it for critical modules.

---

## 35. CI/CD: Terraform in GitHub Actions with OIDC

### The standard team flow
```
feature branch ──► Pull Request
                     │  fmt -check → validate → tflint → trivy → plan
                     │  plan output posted as a PR comment
                     ▼
                   Review + approve
                     │
                     ▼
                 merge to main ──► apply (dev/staging automatically)
                                       │
                                       ▼
                              manual approval gate ──► apply (prod)
```

### Step 1: Let GitHub log in to AWS without stored keys (OIDC)
GitHub gets a short-lived token, and AWS trusts it for **one specific repo and branch**. There are no access keys to leak.

```hcl
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
      values   = ["repo:sairam145/ai-infra-learning:*"]      # ONLY this repo
    }
  }
}

resource "aws_iam_role" "github_terraform" {
  name               = "github-terraform"
  assume_role_policy = data.aws_iam_policy_document.github_trust.json
}

resource "aws_iam_role_policy_attachment" "github_terraform" {
  role       = aws_iam_role.github_terraform.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"   # learning only; scope this down for real
}
```
For real use, narrow `sub` to a branch or environment, e.g. `repo:org/repo:ref:refs/heads/main` or `repo:org/repo:environment:prod`.

### Step 2: The workflow
```yaml
# .github/workflows/terraform.yml
name: terraform
on:
  pull_request:
    paths: ["infra/**"]
  push:
    branches: [main]
    paths: ["infra/**"]

permissions:
  id-token: write          # required for OIDC
  contents: read
  pull-requests: write     # to comment the plan

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: infra/envs/dev
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::<account-id>:role/github-terraform
          aws-region: us-east-1

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.9.8

      - run: terraform fmt -check -recursive
      - run: terraform init -input=false
      - run: terraform validate
      - run: terraform plan -input=false -out=tfplan

      - name: Apply (main branch only)
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: terraform apply -input=false tfplan
```
For production, put the apply job behind a **GitHub Environment** with required reviewers. That's the "manual approval gate."

### Pipeline safety rules
- `-input=false` everywhere: CI must never wait for a prompt.
- **Apply the saved plan** that was reviewed, not a fresh one.
- **One pipeline per state** at a time (`concurrency:` in GitHub Actions), on top of state locking.
- Plan on every PR; apply only from `main`.
- A separate, more restricted role for prod.

---

## 36. Team platforms

| Platform | What it adds | Notes |
|---|---|---|
| **HCP Terraform / Terraform Cloud** | Remote state, remote runs, policy checks (Sentinel/OPA), private module registry, team access | HashiCorp's SaaS; free tier for small teams |
| **Terraform Enterprise** | Self-hosted version of the above | Large enterprises |
| **Atlantis** | Open-source bot: comment `atlantis plan` / `atlantis apply` on a PR | Popular, self-hosted |
| **Spacelift, env0, Scalr** | Commercial Terraform automation platforms | Policy, drift detection, cost controls |
| **OpenTofu** | Open-source fork of Terraform; `tofu` instead of `terraform` | Same HCL; diverges slightly in newer features |

**Terraform Stacks** (HCP Terraform) is HashiCorp's newer way to deploy many related configurations across environments and regions together. It's worth knowing the name; most companies still use folders and pipelines.

---
# Part 7: Reference

## 37. Command cheat sheet

### Everyday
| Command | What it does |
|---|---|
| `terraform init` | Set up: providers, modules, backend |
| `terraform init -upgrade` | Upgrade providers/modules within constraints |
| `terraform init -reconfigure` | Re-set the backend, ignoring the old config |
| `terraform init -migrate-state` | Move state to a new backend |
| `terraform init -backend-config=file.hcl` | Supply backend settings at init |
| `terraform fmt -recursive` | Format every `.tf` file |
| `terraform fmt -check -recursive` | CI check: fail if unformatted |
| `terraform validate` | Check syntax and references |
| `terraform plan` | Preview changes |
| `terraform plan -out=tfplan` | Save the plan |
| `terraform plan -var-file=prod.tfvars` | Plan with a variable file |
| `terraform plan -refresh-only` | Show drift only |
| `terraform plan -detailed-exitcode` | Exit 0 = no change, 1 = error, 2 = changes |
| `terraform plan -generate-config-out=gen.tf` | Write code for `import` blocks |
| `terraform apply` | Apply (asks "yes") |
| `terraform apply tfplan` | Apply a saved plan |
| `terraform apply -auto-approve` | No prompt (automation only) |
| `terraform apply -replace=ADDR` | Force recreate one resource |
| `terraform apply -target=ADDR` | Only one resource (emergencies) |
| `terraform destroy` | Delete everything in this state |
| `terraform destroy -target=ADDR` | Delete one thing |

### Inspecting
| Command | What it does |
|---|---|
| `terraform output` / `output -raw NAME` / `output -json` | Show outputs |
| `terraform show` / `show tfplan` / `show -json` | Show state or a saved plan |
| `terraform state list` | List managed resources |
| `terraform state show ADDR` | One resource's attributes |
| `terraform console` | Interactive expression testing |
| `terraform providers` | Which providers each module uses |
| `terraform graph` | Dependency graph (DOT format) |
| `terraform version` | Terraform and provider versions |

### State surgery (back up first: `terraform state pull > backup.tfstate`)
| Command | What it does |
|---|---|
| `terraform state mv A B` | Rename an address (prefer `moved {}`) |
| `terraform state rm ADDR` | Forget without deleting (prefer `removed {}`) |
| `terraform import ADDR ID` | Old-style import (prefer `import {}`) |
| `terraform force-unlock LOCK_ID` | Remove a stale lock |
| `terraform state push FILE` | Overwrite remote state (last resort) |

### Workspaces
`terraform workspace list | new NAME | select NAME | show | delete NAME`

### Environment variables
| Variable | Use |
|---|---|
| `TF_VAR_name=value` | Set a variable |
| `TF_LOG=DEBUG` (or `TRACE`, `INFO`) | Verbose logs for debugging |
| `TF_LOG_PATH=tf.log` | Write logs to a file |
| `TF_IN_AUTOMATION=1` | Tidier output in CI |
| `TF_CLI_ARGS_plan="-parallelism=5"` | Default flags per command |
| `TF_PLUGIN_CACHE_DIR=~/.terraform.d/plugin-cache` | Share downloaded providers across projects (saves disk and time) |
| `AWS_PROFILE=lab` | Which AWS CLI profile the provider uses |

---

## 38. Troubleshooting catalogue

| Error / symptom | Cause | Fix |
|---|---|---|
| `Error: Inconsistent dependency lock file` | Providers changed since the lock file was written | `terraform init -upgrade`, commit the new lock file |
| `Backend configuration changed` / `Backend initialization required` | Backend settings changed | `terraform init -reconfigure` or `-migrate-state` |
| `Error acquiring the state lock` | Another run is active, or a crash left a lock | Wait; confirm nobody is running → `terraform force-unlock ID` |
| `No valid credential sources found` | AWS credentials missing or expired | `aws sts get-caller-identity`; check `AWS_PROFILE`; re-run `aws configure` or SSO login |
| `AccessDenied` / `UnauthorizedOperation` during apply | The identity lacks permission | Read which action was denied; add exactly that permission |
| `EntityAlreadyExists` / `BucketAlreadyExists` / `already exists` | It exists outside this state (made by hand, or by another stack) | `import` it, or rename yours |
| `BucketAlreadyOwnedByYou` | Your bucket exists but isn't in this state | Import it |
| `Error: Invalid for_each argument ... known only after apply` | `for_each` keys depend on values not yet created | Use keys known at plan time (names from variables), not IDs |
| `Error: Unsupported argument` / `Unsupported block type` | Typo, wrong provider version, or argument vs. block confusion (`=`) | Check the docs for **your** provider version |
| `Error: Reference to undeclared resource` | Typo in an address, or it's in another module | Fix the address; use module outputs |
| `Cycle: A, B` | Two resources depend on each other | Break the loop: separate rule resources (e.g., SG rules), or restructure |
| Plan shows changes on every run (perpetual diff) | AWS normalizes a value differently (JSON order, case), or something else changes it | Use `jsonencode`/policy documents; `ignore_changes` for outside writers |
| Plan shows `-/+` unexpectedly | Changed an argument that forces replacement | Look for `# forces replacement`; reconsider, or use `create_before_destroy` |
| Plan wants to destroy everything | Wrong backend key/workspace, or empty state | **Stop.** Check `terraform workspace show` and the backend `key` |
| `Provider produced inconsistent result after apply` | Provider bug, or eventual consistency | Re-run `apply`; upgrade the provider |
| `timeout while waiting for state to become ...` | AWS is slow (EKS, RDS, CloudFront can take 10–30 min) | Wait; increase `timeouts {}` in the resource |
| `RequestLimitExceeded` / throttling | Too many API calls | `-parallelism=5`; retry |
| `DependencyViolation` on destroy | Something outside Terraform still uses it (e.g., an ENI left by a load balancer or Kubernetes) | Delete the leftover dependency, then destroy again |
| `Error: Value for undeclared variable` | A tfvars key with no matching `variable` block | Add the variable or remove the key |

**Debugging approach:**
1. Read the **whole** error: the resource address and the AWS error code are in it.
2. `terraform validate` → syntax.
3. `aws sts get-caller-identity` → am I who I think I am, in the right account?
4. `TF_LOG=DEBUG terraform plan 2> debug.log` → see the actual API calls.
5. Check the provider docs **for your version**.

---

## 39. Best practices checklist

**Code**
- [ ] Pin Terraform (`required_version`) and providers (`~>`); commit `.terraform.lock.hcl`
- [ ] Every variable has `description` and `type`; validate important ones
- [ ] No hard-coded account IDs, AMI IDs, AZs, or regions; use data sources and variables
- [ ] `for_each` over `count` for collections
- [ ] Consistent naming (`snake_case`), consistent tags via `default_tags`
- [ ] `aws_iam_policy_document` instead of hand-written JSON
- [ ] Small, focused modules with versioned releases

**State**
- [ ] Remote state (S3) with versioning, encryption, locking, public access blocked
- [ ] One state per environment per layer; small blast radius
- [ ] Never commit state; never edit it by hand
- [ ] `prevent_destroy` on critical resources

**Security**
- [ ] No secrets in code or tfvars; use Secrets Manager / `manage_master_user_password` / write-only arguments
- [ ] CI uses **OIDC roles**, not access keys
- [ ] Least-privilege deploy roles; separate prod role with approval
- [ ] Security scanning (Trivy/Checkov) in CI
- [ ] `allowed_account_ids` on the provider

**Process**
- [ ] Every change through a PR with the plan visible
- [ ] Apply the reviewed saved plan
- [ ] Scheduled drift detection
- [ ] Fix drift in code, not in the console
- [ ] `terraform fmt`, `validate`, `tflint` on every commit (pre-commit)

---

## 40. Interview questions and answers

**Basics**

**Q: What is Terraform state, and why is it needed?**
A: A file mapping code to real resources. Terraform uses it to know what it manages, plan changes without searching all of AWS, track dependencies for deletion, and store outputs. It can contain secrets, so it's stored remotely, encrypted, and locked.

**Q: What happens during `terraform plan`?**
A: Terraform reads the code, refreshes the state against real infrastructure, compares desired vs. actual, and outputs the actions (create/update/replace/destroy) without changing anything.

**Q: `count` vs. `for_each`?**
A: `count` indexes by position, so removing a middle item shifts and recreates the rest. `for_each` keys by name, so removing one item only affects that item. Use `count` for on/off toggles and `for_each` for collections.

**Q: Variable vs. local vs. output?**
A: Variables are inputs set from outside; locals are computed values used inside; outputs expose values to callers, other stacks, or scripts.

**Q: What does `terraform init` do?**
A: Downloads the providers and modules, configures the backend, and writes or verifies the lock file.

**Q: What's a data source?**
A: A read-only lookup of something that already exists: an AMI, an account ID, a VPC made by another team.

**State and teams**

**Q: How do you store state for a team?**
A: An S3 backend with versioning, encryption, blocked public access, and locking (native S3 `use_lockfile`, or DynamoDB in older setups). One key per environment and layer, with access restricted via IAM.

**Q: Two engineers run `apply` at the same time. What happens?**
A: The first acquires the lock; the second fails with "Error acquiring the state lock." Without locking, the state could be corrupted.

**Q: Someone changed a resource in the console. How do you handle it?**
A: `terraform plan -refresh-only` to see the drift. If the change was wrong, `apply` reverts it. If it was right, update the code to match. If something legitimately keeps changing it, use `ignore_changes`. Then prevent it from happening again: limit console write access and run scheduled drift detection.

**Q: How do you bring an existing resource under Terraform?**
A: An `import` block with `terraform plan -generate-config-out`, review the generated code, apply, then remove the import block.

**Q: How do you rename a resource without recreating it?**
A: A `moved` block from the old address to the new one.

**Q: How do you stop managing a resource without deleting it?**
A: A `removed` block with `lifecycle { destroy = false }`, or `terraform state rm`.

**Q: What's in your `.gitignore` for Terraform?**
A: `.terraform/`, `*.tfstate*`, plan files, crash logs, and secret tfvars. The lock file is committed.

**Design**

**Q: How do you structure Terraform for dev, staging, and prod?**
A: Shared versioned modules, plus a root configuration per environment, each with its own state (often its own account) and tfvars. Environments differ only by inputs. Large systems are also split into layers (network, cluster, platform, apps) to limit blast radius.

**Q: Workspaces or separate folders?**
A: Folders (or separate state keys) for long-lived environments: clearer, separate backends and accounts possible, fewer mistakes. Workspaces suit short-lived copies of the same stack.

**Q: How do stacks share values?**
A: `terraform_remote_state`, data sources by tag, or SSM parameters as a published contract. Remote state is simplest but exposes the whole state.

**Q: How do you handle secrets?**
A: Never in code or committed tfvars. Use AWS-managed secrets (e.g., RDS `manage_master_user_password`), Secrets Manager with apps reading at runtime, write-only arguments/ephemeral values, and `TF_VAR_` from CI secrets. Treat state as sensitive.

**Q: How do you avoid downtime when Terraform replaces something?**
A: `create_before_destroy` (with `name_prefix` to avoid name clashes), check the plan for `# forces replacement`, and use blue/green patterns for databases and clusters.

**Q: How does your CI/CD run Terraform?**
A: On PR: fmt, validate, tflint, security scan, plan, with the plan posted for review. On merge: apply the saved plan to lower environments, and to prod after manual approval. AWS access via GitHub OIDC roles, no stored keys, concurrency limited per state.

**Troubleshooting**

**Q: The plan wants to destroy and recreate your production database. What do you do?**
A: Stop. Find the `# forces replacement` attribute. Usually a changed immutable argument, a renamed address (fix with `moved`), or wrong state/workspace. Fix the cause; never apply it. `prevent_destroy` should have blocked it anyway.

**Q: "Error acquiring the state lock" and nobody is running anything?**
A: A crashed run left a stale lock. Confirm nobody is running, then `terraform force-unlock <ID>`.

**Q: `for_each` errors with "known only after apply." Why?**
A: The keys depend on values created during apply. Keys must be known at plan time, so key by names from variables, not by generated IDs.

**Q: Destroy fails with DependencyViolation on a subnet or security group.**
A: Something outside Terraform still uses it, typically network interfaces left by a load balancer or Kubernetes. Delete those first, e.g., the Kubernetes LoadBalancer services, then destroy again.

---

## 41. Practice ladder

Do these in order. Each builds on the last. **Destroy after each one.**

| # | Exercise | Concepts practiced |
|---|---|---|
| 1 | IAM read-only role + test with a CLI profile *(done in Lesson 01)* | providers, data sources, resources, outputs |
| 2 | S3 bucket with versioning, encryption, public access block | resource separation, references |
| 3 | Same bucket, name from variables with validation; tags from locals | variables, validation, locals, merge |
| 4 | Three team buckets with `for_each`; remove the middle one and watch the plan | for_each vs. count |
| 5 | Turn the bucket into a module; call it twice | modules, inputs, outputs |
| 6 | Create the state bucket; move an existing project to the S3 backend | backends, `-migrate-state`, locking |
| 7 | Create a bucket in the console, then `import` it with generated config | import blocks |
| 8 | Rename a resource; use `moved` so nothing is recreated | moved blocks |
| 9 | VPC with public/private subnets across 2 AZs using `cidrsubnet` + `for_each` | functions, for expressions |
| 10 | Same VPC with `terraform-aws-modules/vpc`; compare | public modules, versions |
| 11 | `dev` and `prod` folders using one module with different tfvars | environment structure |
| 12 | `terraform test` with plan-only assertions for your bucket module | testing |
| 13 | GitHub Actions: plan on PR, apply on main, via OIDC | CI/CD, OIDC |
| 14 | Network stack + cluster stack reading its outputs | layering, remote state / SSM |
| 15 | Break things: force a lock, cause drift, trigger a cycle, then fix each | troubleshooting |

---

*Part of my [AI Infrastructure learning log](../../README.md). Companion: [AWS + Terraform lesson guide](AWS-TERRAFORM-GUIDE.md).*
