from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.database import MySQL
from diagrams.programming.framework import Angular, Spring
from diagrams.custom import Custom
from diagrams.onprem.compute import Server

# Custom components
evolis_kiosk_printer_url = "images/kiosk.jpg"
evolis_privelio_printer_url = "images/privelio-64.png"
evolis_service_provider = "images/evolis_logo.png"
browser_img = "images/chrome-browser.png"
logs_url = "images/txt-image.png"

with Diagram("SCI Fullstack Card Printing Application Architecture", show=True, direction="LR"):
    user = User("Client")

    # Cluster para o Kiosk Card Printer
    with Cluster("Kiosk Card Printer"):
        with Cluster("Kiosk PC"):
            browser = Custom("Browser", browser_img)

            with Cluster("Frontend"):
                angular = Angular("Angular (UI)")

            with Cluster("Backend"):
                spring = Spring("Spring Boot (API)")

            with Cluster("Database"):
                mysql = MySQL("MySQL Database")
            
            #with Cluster("Logs"):
                #logs = Custom("Logs", logs_url)

            with Cluster("Print Services"):
                service_provider = Custom("Evolis Service Provider", evolis_service_provider)

        evolis_kiosk_printer = Custom("Evolis Kiosk", evolis_kiosk_printer_url)

    # Cluster para o Bank Central Server
    with Cluster("Bank Central Server"):
        otp_service = Server("OTP Service")

    # Conexões
    user >> browser >> angular >> spring  # Comunicação do usuário até o Spring
    spring >> mysql  # Conexão Spring com o MySQL
    #spring >> logs  # Conexão Spring com os logs
    spring >> service_provider >> evolis_kiosk_printer  # Comunicação do Spring com o serviço de impressão
    spring >> otp_service  # Comunicação do Spring com o serviço OTP
    user >> otp_service  # Comunicação direta do usuário com o serviço OTP
