from fileinput import filename
import socket
from ftplib import FTP, all_errors

HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
USERNAME = "angel"
PASSWORD = "1234"

def iniciarSesion(user, password):
    
    ftp_server = FTP()
    ftp_server.connect('192.168.0.5', 5000)
    try:
        codigo = ftp_server.login(user, password).split(" ")[0]
        ftp_server.encoding = "UTF-8"

        #print(ftp_server.getwelcome())
        #ftp_server.encoding = "UTF-8"

        #filename = "cliente/Te Escondes.mp4"
        #nombreNuevo = "videoNuevo.mp4"
        #fl = open(filename, "rb")
        #ftp_server.storbinary(f"STOR {nombreNuevo}", fl)
        #     # with open("holamundo.txt", "rb") as file:
        #     #     ftp_server.storbinary(f"STOR {filename}", file)
        #ftp_server.dir()


        return ftp_server
    except all_errors as error:
        ftp_server.quit()
        

#iniciarSesion(USERNAME, PASSWORD)