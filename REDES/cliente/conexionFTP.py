from fileinput import filename
import socket
from ftplib import FTP, all_errors

HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
USERNAME = "angel"
PASSWORD = "1234"

def iniciarSesion(HOST, user, password):
    
    ftp_server = FTP()
    ftp_server.connect(HOST, 5000)
    try:
        codigo = ftp_server.login(user, password).split(" ")[0]
        ftp_server.encoding = "UTF-8"
        return ftp_server
    except all_errors as error:
        ftp_server.quit()
        

#iniciarSesion(USERNAME, PASSWORD)