variable "mutant_repo_url" {
  description = "The URL of the Docker image for the Mutant app"
  type        = string
}

variable "mutant_repo_arn" {
  description = "The ARN of the Docker image for the Mutant app"
  type        = string
}

variable "alb_tg_arn" {
  description = "The ARN of the target group for the load balancer"
  type        = string
}

variable "subnet_ids" {
  description = "The IDs of the subnets"
  type        = list(string)
}

variable "service_security_group_id" {
  description = "The ID of the security group for the service"
  type        = string
}