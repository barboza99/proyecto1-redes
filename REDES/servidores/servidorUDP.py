import threading
import cv2, imutils, socket
import time
import base64
import queue
import os
from concurrent.futures import ThreadPoolExecutor

colaVideo1 = queue.Queue(maxsize=1000)
colaVideo2 = queue.Queue(maxsize=1000)
colaVideo3 = queue.Queue(maxsize=1000)

def iniciarServidorUDP():
    with ThreadPoolExecutor(max_workers=2) as executor:
        nombreVideo = ""
        video = None
        FPS = None
        MENSAJERECIBIDO = False
        BUFF_SIZE = 65536
        direcciones_clientes = []

        server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        HOST_NAME = socket.gethostname()
        HOST_IP = socket.gethostbyname(HOST_NAME)
        #host_ip = '192.168.0.5' #socket.gethostbyname(host_name)
        port = 5001
        socket_address = (HOST_IP,port)
        server_socket.bind(socket_address)
        print('Escuchando en :[',socket_address,"]")

        def video_stream():
            cont = 0
            band = False
            while True:
                (mensaje, client_addr) = server_socket.recvfrom(BUFF_SIZE)
                if mensaje.decode("UTF-8").startswith("Archivos_JSON"):
                    arr = mensaje.decode("UTF-8").split(",")
                    arr.pop(0)
                    arr.pop(-1)

                    files_abiertos = "Archivos_JSON;"
                    path = os.getcwd()
                    for element in arr:
                        try:
                            f = open(path+"/videos/"+element, "r")
                            strin = f.read()
                            files_abiertos += strin + ";"
                        except Exception as e:
                            print("Err-> ", e)
                    server_socket.sendto(files_abiertos.encode("UTF-8"), client_addr)
                    continue
                
                if not (client_addr in direcciones_clientes):
                    direcciones_clientes.append(client_addr)
                    cont+=1
                try:
                    if cont == 1 and mensaje.decode("UTF-8") != "o_reproducir" and mensaje.decode("UTF-8") != "terminar":
                        first = Transmision(client_addr, server_socket)
                        first.setNombreVideo(mensaje.decode("UTF-8"))
                        first.daemon = True
                        first.comenzar()
                        first.toString()
                    elif cont == 2 and mensaje.decode("UTF-8") != "o_reproducir" and mensaje.decode("UTF-8") != "terminar":
                        first2 = Transmision(client_addr, server_socket)
                        first2.setNombreVideo(mensaje.decode("UTF-8"))
                        first2.daemon = True
                        first2.comenzar()
                        first.toString()
                    elif cont == 3 and mensaje.decode("UTF-8") != "o_reproducir" and mensaje.decode("UTF-8") != "terminar":
                        first3 = Transmision(client_addr, server_socket)
                        first3.setNombreVideo(mensaje.decode("UTF-8"))
                        first3.daemon = True
                        first3.comenzar()
                        first.toString()
                except Exception as e:
                    if not band:
                        print("Exception -> ", e)
                    band = True

        class Transmision:
            cola = queue.Queue(1500)
            video = None
            FPS = 0
            totalNoFrames = 0
            durationInSeconds = 0
            finalizar = False
            nomVideo = ""
            def __init__(self, address, socket):
                self.addr = address
                self.socket = socket

            def setNombreVideo(self, nomVid):
                self.nomVideo = nomVid
                try:
                    self.video = None
                    self.video = cv2.VideoCapture("videos/"+self.nomVideo)
                    self.FPS = video.get(cv2.CAP_PROP_FPS)
                    self.totalNoFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.durationInSeconds = float(self.totalNoFrames) / float(FPS)
                except Exception as e:
                    print(e)

            def toString(self):
                print("*-----------------------------*")
                print("Cliente: ", self.addr)
                print("Video a reproducir: [", self.nomVideo,"]")
                print("Duracion en minutos: ", (self.durationInSeconds/60))
                print('FPS:',self.FPS)
                print("*-----------------------------*")

            def terminar(self):
                self.finalizar = True;
                with self.cola.mutex:
                    self.cola.queue.clear()

            def comenzar(self):
                hilo_transmision = threading.Thread(target=self.iniciarTransmision, name="hilo_transmision")
                hilo_generarVideo = threading.Thread(target=self.generarVideo, name="hilo_generarVideo")
                hilo_verificarFinalizar = threading.Thread(target=self.verificarFinalizar, name="hilo_verificarFinalizar")
                hilo_generarVideo.daemon = True
                hilo_transmision.daemon = True
                hilo_verificarFinalizar.daemon = True
                hilo_generarVideo.start()
                time.sleep(3)
                hilo_transmision.start()
                hilo_verificarFinalizar.start()

            def verificarFinalizar(self):
                while True:
                    (mensaje, address) = self.socket.recvfrom(55535)
                    if address == self.addr:
                        if mensaje.decode("UTF-8") == "terminar":
                            self.terminar()
                            break
                        elif mensaje.decode("UTF-8") == "o_reproducir":
                            with self.cola.mutex:
                                self.cola.queue.clear()
                            if self.video:
                                self.video.release()
                        else:
                            self.setNombreVideo( mensaje.decode("UTF-8"))

            def iniciarTransmision(self):
                while not self.finalizar or not self.cola.empty():
                    if self.cola.empty():
                        break
                    frame = self.cola.get()
                    encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
                    message = base64.b64encode(buffer)
                    self.socket.sendto(message, self.addr)
                    time.sleep(0.018)
                if not self.finalizar:
                    self.socket.sendto("500".encode("UTF-8"), self.addr)
                    self.finalizar = True

            def generarVideo(self):
                WIDTH=400
                #while True:
                while self.video.isOpened() and not self.finalizar:
                    try:
                        _,frame = self.video.read()
                        frame = imutils.resize(frame,width=WIDTH)
                        self.cola.put(frame)
                    except Exception as e:
                        print(e)
                self.video.release()

        executor.submit(video_stream)
if __name__ == '__main__':
    iniciarServidorUDP()