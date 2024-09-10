from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.database import MySQL
from diagrams.programming.framework import Angular, Spring
from diagrams.custom import Custom
from diagrams.onprem.compute import Server

# Custom components
evolis_elypso_printer_url = "images/elypso-64.png"
evolis_privelio_printer_url = "images/privelio-64.png"
evolis_service_provider = "images/evolis_logo.png"
browser = "images/chrome-browser.png"

with Diagram("SCI Fullstack Card Printing Application Architecture", show=True):
    user = User("User")
    browser = Custom("Browser", browser)

    with Cluster("Server"):
        with Cluster("Frontend"):
            angular = Angular("Angular (UI)")

        with Cluster("Backend"):
            spring = Spring("Spring Boot (API)")

        with Cluster("Database"):
            mysql = MySQL("MySQL Database")

        with Cluster("Print Services"):
            service_provider = Custom("Evolis Service Provider", evolis_service_provider)

    # Impressoras fora do servidor
    evolis_elypso_printer = Custom("Evolis Elypso/Primacy", evolis_elypso_printer_url)
    evolis_privelio_printer = Custom("Evolis Privelio XT", evolis_privelio_printer_url)

    # Servidor central contendo o Active Directory
    with Cluster("Central Server"):
        ad_server = Server("Active Directory")

    # Conexões principais
    user >> browser >> angular >> spring
    spring >> mysql
    spring >> service_provider >> evolis_elypso_printer
    spring >> evolis_privelio_printer
    spring >> ad_server  # Conexão ao Active Directory no servidor central

    # Resposta
    spring >> angular >> browser >> user
    evolis_elypso_printer >> service_provider
    service_provider >> spring
    mysql >> spring
    evolis_privelio_printer >> spring
    ad_server >> spring
