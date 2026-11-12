variable "region" {
  description = "AWS region to work in"
  type        = string
  default     = "us-east-1"
}

variable "role_name" {
  description = "Name of the read-only IAM role"
  type        = string
  default     = "lab-readonly"
}