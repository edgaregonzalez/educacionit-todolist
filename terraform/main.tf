terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0" # O la versión más reciente que estés utilizando
        }
    }
}

# Configuración del proveedor de AWS (asegúrate de tenerlo configurado)
provider "aws" {
    region = "us-east-1" # Reemplaza con tu región deseada
    # Aquí puedes añadir configuración de credenciales si es necesario
}

# Data source para obtener una VPC específica por su etiqueta "Name"
data "aws_vpc" "selected_vpc" {
    filter {
        name   = "tag:Name"
        values = ["default"] # Reemplaza con el valor de la etiqueta 'Name' de tu VPC
    }
    # Puedes añadir más filtros si es necesario:
    # filter {
    #   name   = "cidr-block"
    #   values = ["10.0.0.0/16"]
    # }
}

# Data source para obtener una Subnet ID
data "aws_subnets" "selected_subnets" {
    filter {
        name   = "vpc-id"
        values = [data.aws_vpc.selected_vpc.id] # <-- REEMPLAZA ESTO con el ID de tu VPC
    }
}

# Cluster Role
data "aws_iam_role" "selected_iam_cluster_role" {
    name = "AWSServiceRoleForAmazonEKS"
}

# NodeGroup Role
data "aws_iam_role" "selected_iam_nodegroup_role" {
    name = "AWSServiceRoleForAmazonEKSNodegroup"
}

# Output para mostrar el ID de la VPC seleccionada
output "selected_vpc_id" {
    description = "El ID de la VPC seleccionada."
    value       = data.aws_vpc.selected_vpc.id
}

# Output para mostrar el ID de la VPC seleccionada
output "selected_subnets_id" {
    description = "El ID de las subnets seleccionada."
    value       = data.aws_subnets.selected_subnets.ids
}
# Cluster Role
output "selected_iam_cluster_role" {
    description = "El ARN del role es"
    value       = data.aws_iam_role.selected_iam_cluster_role.arn
}

# Cluster Role
output "selected_iam_nodegroup_role" {
    description = "El ARN del role es"
    value       = data.aws_iam_role.selected_iam_nodegroup_role.arn
}

# Creacion del control plane

# ------------------------------------------------------------------------------
# Clúster EKS (Control Plane)
# ------------------------------------------------------------------------------
resource "aws_eks_cluster" "eks_cluster" {
    name     = "eks-terraform"
    version  = "1.32"
    role_arn = data.aws_iam_role.selected_iam_cluster_role.arn

    vpc_config {
        subnet_ids              = data.aws_subnets.selected_subnets.ids
        endpoint_private_access = true # Recomendado para seguridad
        endpoint_public_access  = true # Puedes restringirlo o deshabilitarlo si tienes acceso por VPN/DirectConnect
        # public_access_cidrs   = ["YOUR_HOME_IP/32"] # Si endpoint_public_access es true, restringe el acceso
    }

    # Habilitar logging del control plane (opcional pero recomendado)
    enabled_cluster_log_types = ["api", "audit", "authenticator"]

    tags = {
        Name        = "eks-terraform"
        Environment = "dev" # Ejemplo de etiqueta adicional
    }
}