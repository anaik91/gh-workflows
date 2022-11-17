variable "project_id" {
  description = "The ID of the project in which to provision resources."
  type        = string
}

module "service_account" {
  source     = "terraform-google-modules/service-accounts/google"
  version    = "~> 4.1.1"
  project_id = var.project_id
  prefix     = "gh-workload"
  names      = ["simple"]
  project_roles = ["${var.project_id}=>roles/workflows.invoker",
  "${var.project_id}=>roles/owner"]
}

module "gh_oidc" {
  source      = "terraform-google-modules/github-actions-runners/google//modules/gh-oidc"
  project_id  = var.project_id
  pool_id     = "example-pool"
  provider_id = "example-gh-provider"
  sa_mapping = {
    "gh-workload-simple@${var.project_id}.iam.gserviceaccount.com" = {
      sa_name   = "projects/${var.project_id}/serviceAccounts/gh-workload-simple@${var.project_id}.iam.gserviceaccount.com"
      attribute = "attribute.repository/anaik91/gh-workflows"
    }
  }
  depends_on = [
    module.service_account
  ]
}