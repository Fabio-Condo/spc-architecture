from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, ECR
from diagrams.aws.database import RDS
from diagrams.aws.network import VPC, InternetGateway, RouteTable, PublicSubnet, PrivateSubnet, ELB
from diagrams.aws.security import IAM
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.aws.management import Cloudwatch

# Criando o diagrama
with Diagram("AWS Infrastructure for Ku Dondza", show=False, direction="LR"):
    # VPC
    with Cluster("VPC"):
        vpc = VPC("ku-dondza-vpc")

        # Internet Gateway
        igw = InternetGateway("ku-dondza-igw")
        vpc >> igw

        # Route Table
        route_table = RouteTable("ku-dondza-public-route-table")
        igw >> route_table

        # Subnets
        with Cluster("Public Subnets"):
            public_subnet_1 = PublicSubnet("public-subnet-1\n(us-east-1a)")
            public_subnet_2 = PublicSubnet("public-subnet-2\n(us-east-1b)")
            public_subnet_1 >> route_table
            public_subnet_2 >> route_table

        with Cluster("Private Subnets"):
            private_subnet_1 = PrivateSubnet("private-subnet-1\n(us-east-1a)")
            private_subnet_2 = PrivateSubnet("private-subnet-2\n(us-east-1b)")

    # RDS
    with Cluster("RDS"):
        rds = RDS("ku-dondza-db")
        rds_sg = IAM("ku-dondza-db-sg")
        rds >> rds_sg
        rds - Edge(color="brown") >> private_subnet_1
        rds - Edge(color="brown") >> private_subnet_2

    # ECS
    with Cluster("ECS"):
        ecs_cluster = ECS("ku-dondza-cluster")
        ecs_service = ECS("ku-dondza-service")
        ecs_task = ECS("ku-dondza-task")
        ecr = ECR("ku-dondza-repo")

        ecs_cluster >> ecs_service >> ecs_task
        ecs_task >> ecr

    # Load Balancer
    alb = ELB("ku-dondza-lb")
    alb >> public_subnet_1
    alb >> public_subnet_2
    alb >> ecs_service

    # CloudWatch Logs
    cloudwatch = Cloudwatch("ku-dondza-app-logs")
    ecs_task >> cloudwatch

    # IAM Role
    iam_role = IAM("ku-dondza-ecs-task-execution-role")
    ecs_task >> iam_role

    # Security Groups
    web_sg = IAM("ku-dondza-web-sg")
    ecs_service >> web_sg
    alb >> web_sg

    # Outputs
    outputs = SimpleStorageServiceS3("Outputs")
    outputs >> Edge(label="ALB DNS Name") >> alb
    outputs >> Edge(label="RDS Endpoint") >> rds
    outputs >> Edge(label="ECR Repository URL") >> ecr
    outputs >> Edge(label="ECS Cluster Name") >> ecs_cluster