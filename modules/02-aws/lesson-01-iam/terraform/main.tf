# READ: who am I? (gives the account ID without typing it)
data "aws_caller_identity" "current" {}

# READ/BUILD: the trust policy = WHO is allowed to wear this role
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

# CREATE: the role itself
resource "aws_iam_role" "lab_readonly" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

# CREATE: attach permissions = WHAT the role is allowed to do
resource "aws_iam_role_policy_attachment" "readonly" {
  role       = aws_iam_role.lab_readonly.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}