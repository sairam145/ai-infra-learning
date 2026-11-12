# Module 2: AWS + Terraform 🚧

> AWS for DevOps and AI infrastructure, built three ways in every lesson: **console** (see it), **CLI** (script it), **Terraform** (how companies do it).

## The three documents

| Document | Use it for |
|---|---|
| 📘 [**AWS + Terraform lesson guide**](AWS-TERRAFORM-GUIDE.md) | Working through the 16 lessons: concepts, console, CLI, complete Terraform, verify, clean up, interview questions |
| 📗 [**Terraform: zero to advanced**](TERRAFORM-ZERO-TO-ADVANCED.md) | Any Terraform question: syntax, state, modules, testing, CI/CD, troubleshooting, interview Q&A |
| 📝 [**Interview notes**](../../notes/module-02-aws-terraform-notes.md) | Revising for DevOps interviews |

## Lessons

| # | Lesson | Status | My code |
|---|---|---|---|
| 01 | Account, billing & IAM | ✅ Done | [`lesson-01-iam/terraform`](lesson-01-iam/terraform) |
| 02 | VPC networking | ⏳ Next | |
| 03 | EC2 | ⬜ | |
| 04 | Load balancing & auto scaling | ⬜ | |
| 05 | Storage: S3, EBS, EFS | ⬜ | |
| 06 | Containers: ECR & ECS Fargate | ⬜ | |
| 07 | EKS | ⬜ | |
| 08 | Observability: CloudWatch & CloudTrail | ⬜ | |
| 09 | Security & secrets | ⬜ | |
| 10 | DNS, TLS & CDN | ⬜ | |
| 11 | Infrastructure as Code (remote state, CloudFormation) | ⬜ | |
| 12 | CI/CD on AWS (GitHub Actions + OIDC) | ⬜ | |
| 13 | Serverless & data | ⬜ | |
| 14 | Reliability & DR | ⬜ | |
| 15 | Cost & FinOps | ⬜ | |
| 16 | AWS for ML | ⬜ | |

## Lesson 01 results
- Root account protected with budgets: $50 monthly + zero-spend alert
- IAM user `sairam-cli` with console access, used instead of root
- `lab-readonly` role **written in Terraform** (4 files + lock file): plan showed `2 to add`
- Least-privilege test: wearing the role (CLI profile or console **Switch role**) can list S3, but creating a bucket → **AccessDenied**
- ⏳ GPU quota (G and VT, 8 vCPUs, us-east-1): request it and check status with the commands in Lesson 16

## Rules for this module
- Read each lesson's **Cost** section before applying
- `terraform destroy` at the end of every session unless the lesson says keep
- Never commit `terraform.tfstate`, `.terraform/`, or plan files; **do** commit `.terraform.lock.hcl`

---

*Part of my [AI Infrastructure learning log](../../README.md).*
