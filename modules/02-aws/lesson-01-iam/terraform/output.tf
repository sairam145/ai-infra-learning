output "role_arn" {
  description = "ARN of the read-only role"
  value       = aws_iam_role.lab_readonly.arn
}