variable "availability_zones" {
  description = "us-east-2 AZs"
  type        = list(string)
  default     = ["us-east-2a", "us-east-2b", "us-east-2c"]
}