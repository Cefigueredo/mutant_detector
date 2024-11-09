terraform {
  backend "s3" {
    bucket  = "terraform-state-files-carlos-figueredo"
    key     = "mutant/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}