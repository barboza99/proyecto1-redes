from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import TLS_FTPHandler
import socket
from threading import Thread

HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)

def iniciarServidorFTP():
    authorizer = DummyAuthorizer()
    authorizer.add_user('angel', '1234', '.', perm='elradfmwMT')

    handler = TLS_FTPHandler
    handler.certfile = 'servidores/crt.pem'
    handler.authorizer = authorizer
    
    handler.banner = "CONECTADO!!!."
    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = (HOST_IP, 5000)
    print("HOST IP: ", HOST_IP)
    server = FTPServer(address, handler)
    
    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5
    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    servFTP = Thread(target=iniciarServidorFTP)
    servFTP.start()