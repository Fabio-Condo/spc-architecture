from diagrams import Diagram, Cluster
from diagrams.onprem.database import MySQL
from diagrams.onprem.compute import Server
from diagrams.custom import Custom
from diagrams.programming.framework import Angular, Spring

# Custom components
evolis_service_provider = "images/evolis_logo.png"
logs_url = "images/txt-image.png"

with Diagram("Infraestrutura da Aplicação Full-Stack", show=True):
    with Cluster("Server"):
        with Cluster("Docker Containers"):
            with Cluster("Frontend"):
                angular = Angular("Angular (UI)")
            with Cluster("Backend"):
                spring = Spring("Spring Boot (API)")
            with Cluster("Database"):
                mysql = MySQL("MySQL Database")
        
        # Logs dentro do Servidor com Docker
        with Cluster("Logs"):
            logs = Custom("Logs", logs_url)

        #service_provider = Custom("Evolis Service Provider", evolis_service_provider)
        with Cluster("Print Services"):
            service_provider = Custom("Evolis Service Provider", evolis_service_provider)

        # Frontend e Backend
        angular >> spring
        spring >> mysql
        spring >> logs
        spring >> service_provider

    with Cluster("Servidor Central"):
        ldap = Server("Servidor LDAP")

    # Conexões
    spring >> ldap
