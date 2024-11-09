output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_default_vpc.default_vpc.id
}

output "subnet_ids" {
  description = "The IDs of the subnets"
  value       = [aws_default_subnet.default_subnet_a.id, aws_default_subnet.default_subnet_b.id, aws_default_subnet.default_subnet_c.id]
}

output "service_security_group_id" {
  description = "The ID of the security group"
  value       = aws_security_group.service_security_group.id
}

output "load_balancer_security_group_id" {
  description = "The ID of the security group"
  value       = aws_security_group.load_balancer_security_group.id
}

output "load_balancer" {
  description = "The ARN of the ALB"
  value       = aws_alb.application_load_balancer.arn
}

output "target_group_arn" {
  description = "The ARN of the target group"
  value       = aws_lb_target_group.mutant_app_target_group.arn
}