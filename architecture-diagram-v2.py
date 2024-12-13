from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.database import MySQL
from diagrams.programming.framework import Angular, Spring

with Diagram("Arquitetura da Aplicação de Impressão de Cartões", show=True):

    # Usuário
    user = User("Agente de caixa")

    # Servidor Principal
    with Cluster("Computador do Agente de caixa"):

        browser = Custom("Browser", "images/chrome-browser.png")

        with Cluster("Frontend"):
            angular = Angular("Angular (UI)")

        with Cluster("Backend"):
            spring_boot = Spring("Spring Boot (API)")

        with Cluster("Database"):
            mysql = MySQL("MySQL")    

        with Cluster("Serviços de Impressão"):
            print_service = Custom("Evolis Service Provider", "images/evolis_logo.png")


    # Impressoras
    elypso = Custom("Elypso/Primacy", "images/elypso-64.png")
    privelio = Custom("Privelio XT", "images/privelio-64.png")

    # Fluxo de Conexões
    user >> browser >> angular >> spring_boot
    spring_boot >> mysql
    spring_boot >> print_service
    spring_boot >> Edge(label="Conexão Direta", color="red") >> privelio
    print_service >> Edge(label="Envio de comandos", color="blue") >> elypso
    elypso >> Edge(label="Status e Respostas", color="green") >> print_service
    privelio >> Edge(label="Status e Respostas", color="green") >> spring_boot
    print_service >> Edge(label="Respostas", style="dotted", color="orange") >> spring_boot
