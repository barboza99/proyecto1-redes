from tkinter import *
from tkinter import ttk
import cv2
import socket
import numpy as np
import time
import base64
import threading
import queue
from PIL import Image
from PIL import ImageTk
from PIL import ImageTk, Image


class GUI:
    pausa = False
    terminado = False
    otraReproduccion = False
    BUFF_SIZE = 65536
    cola_video = queue.Queue(1000)
    host_ip = '192.168.0.2'
    port = 9688
    client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket_video.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

    def __init__(self, frame, nombreVideo):
        self.frame = frame
        self.nomVideo = nombreVideo

        self.video = Label(self.frame)
        self.video.grid(row=1, column=0)

        self.frameFooter = ttk.Frame(frame)
        self.frameFooter.grid(row=2, column=0)
        self.frameFooter.grid_columnconfigure(0, weight=1)
        self.frameFooter.grid_rowconfigure(0, weight=1)

        self.lblIndicador = Label(self.frameFooter,name="lbl_indicador",justify="center",height=1, width=42, text="Dale play", background="#B7BED9")
        self.lblIndicador.grid(row=0, column=0)

        self.frameBotones = ttk.Frame(self.frameFooter)
        self.frameBotones.grid(row=1, column=0)
        
       

        self.btn = Button(self.frameBotones,
                          text="PLAY",
                          font="12",
                          command=lambda: self.play())
        self.btn.grid(row=0,column=0, sticky="", padx=2)

    def setIP(self, ip):
        self.host_ip = ip

    def setPORT(self, port):
        self.port = port

    def Pausa(self):
        self.pausa = not self.pausa
    
    def setTerminado(self, term:bool):
        self.terminado = term
    
    def getTerminado(self):
        return self.terminado

    def play(self):
        self.setTerminado(False)
        self.lblIndicador.configure(text="Cargando...")
        rcv = threading.Thread(target=self.receive)
        rcv.daemon = True
        rcv.start()
    
    def setNombreVideo(self, nomVid):
        self.nomVideo = nomVid

    def enviarMensajeTerminacion(self, mensaje):

        if not self.terminado and mensaje != "o_reproducir":
            self.lblIndicador.configure(text="Terminado...")
            self.setTerminado(True)
        elif mensaje == "o_reproducir":
            self.lblIndicador.configure(text="Dale play...")

        self.client_socket_video.sendto(mensaje.encode("UTF-8"), (self.host_ip, self.port))
        
        with self.cola_video.mutex:
                self.cola_video.queue.clear()

    def receive(self):

        self.client_socket_video.sendto(bytes(self.nomVideo,"UTF-8"), (self.host_ip, self.port))
        
        def getVideoData():
            while not self.terminado:
                
                packet, _ = self.client_socket_video.recvfrom(self.BUFF_SIZE)
                if packet.decode("UTF-8") == "500":
                    self.lblIndicador.configure(text="Finalizado")
                    self.setTerminado(True)
                    break

                data = base64.b64decode(packet, ' /')
                npdata = np.fromstring(data, dtype=np.uint8)

                frame = cv2.imdecode(npdata, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                self.cola_video.put(frame)
        hiloGetVideo = threading.Thread(target=getVideoData)
        hiloGetVideo.daemon = True
        hiloGetVideo.start()
        time.sleep(5)
        self.lblIndicador.configure(text="Reproduciendo")
       
        while not self.terminado:
            if not self.pausa:
                frame = self.cola_video.get()
                
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                self.video.config(image=img)
                self.video.image = img
                time.sleep(0.0288888888)
        
        if not self.terminado:
            self.lblIndicador.configure(text="Transmisión finalizada...")

