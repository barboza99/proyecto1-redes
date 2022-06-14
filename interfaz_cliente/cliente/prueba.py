from tkinter import *
from tkinter import ttk
from tkinter.tix import Tree
import cv2
import socket
import numpy as np
import time
import os
import base64
from time import sleep
import threading
import queue
from PIL import Image
from PIL import ImageTk
from PIL import ImageTk, Image
class GUI:

    pausa = False
    terminado = False
    BUFF_SIZE = 65536
    cola_audio = queue.Queue(1000)
    cola_video = queue.Queue(1000)
    host_ip = '192.168.0.4'
    port = 9688
    client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket_video.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

    #client_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #client_socket_audio.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

    def __init__(self, frame, nombreVideo):
        self.frame = frame
        self.nomVideo = nombreVideo

        self.video = Label(self.frame)
        self.video.grid(row=1, column=0)

        self.frameFooter = ttk.Frame(frame)
        self.frameFooter.grid(row=2, column=0)
        self.frameFooter.grid_columnconfigure(0, weight=1)
        self.frameFooter.grid_rowconfigure(0, weight=1)

        self.lblIndicador = Label(self.frameFooter,justify="center",height=1, width=42, text="Dale play", background="#B7BED9")
        self.lblIndicador.grid(row=0, column=0)

        self.frameBotones = ttk.Frame(self.frameFooter)
        self.frameBotones.grid(row=1, column=0)
        
       

        self.btn = Button(self.frameBotones,
                          text="PLAY",
                          font="12",
                          command=lambda: self.play())
        self.btn.grid(row=0,column=0, sticky="", padx=2)

        # self.btnPausa = Button(self.frameBotones,
        #                   text="Pausar",
        #                   font="12",
        #                   command=lambda: self.Pausa())
        # self.btnPausa.grid(row=0,column=1, sticky="", padx=2)


    def Pausa(self):
        self.pausa = not self.pausa
    
    def Terminado(self):
        self.terminado = True
        self.cola_video = queue.Queue(1000)
        #self.client_socket_video.shutdown(1)
        #self.client_socket_video.close()

    def play(self):
        self.lblIndicador.configure(text="Cargando...")
        rcv = threading.Thread(target=self.receive)
        #aud = threading.Thread(target=self.audio)
        rcv.daemon = True
        #aud.daemon = True
        rcv.start()
        #aud.start()

    def receive(self):
        self.client_socket_video.sendto(bytes(self.nomVideo,"UTF-8"), (self.host_ip, self.port))
        
        def getVideoData():
            ultimoTiempo = time.time()
            while not self.terminado:
                
                # if (time.time() - ultimoTiempo) > 3:
                #     #print("AQUI...")
                #     self.client_socket_video.sendto(bytes("OK","UTF-8"), (self.host_ip, self.port))
                #     ultimoTiempo = time.time()
                
                packet, _ = self.client_socket_video.recvfrom(self.BUFF_SIZE)
                
                data = base64.b64decode(packet, ' /')
                npdata = np.fromstring(data, dtype=np.uint8)

                frame = cv2.imdecode(npdata, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                self.cola_video.put(frame)
                #print('Tamaño cola de video...',self.cola_video.qsize())
        hiloGetVideo = threading.Thread(target=getVideoData)
        hiloGetVideo.daemon = True
        hiloGetVideo.start()
        time.sleep(4)
        self.lblIndicador.configure(text="Reproduciendo")
        print('Now Playing video...')
       
        while not self.terminado and not self.cola_video.empty():
            if not self.pausa:
                frame = self.cola_video.get()
                
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                self.video.config(image=img)
                self.video.image = img
                time.sleep(0.0288888888)
        
        if not self.terminado:
            self.lblIndicador.configure(text="Transmisión finalizada...")
            img = ImageTk.PhotoImage(Image.open("interfaz_cliente/cliente/kakashi.png"))
            self.video.config(image=img)
            self.video.image = img
        #self.client_socket.close()
        print('Video closed')
        #os._exit(1)


    # def audio(self):
    #     # client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #     # client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,self.BUFF_SIZE)
    #     self.client_socket_audio.sendto(bytes(self.nomVideo, "UTF-8"),(self.host_ip, self.port-1))

    #     p = pyaudio.PyAudio()
    #     CHUNK = 10*1024
    #     stream = p.open(format=p.get_format_from_width(2),
    #                     channels=2,
    #                     rate=44100,
    #                     output=True,
    #                     frames_per_buffer=CHUNK)
                        
    #     # create socket
    #     #socket_address = (self.host_ip, self.port-1)
        
    #     def getAudioData():
    #         while not self.terminado:
    #             frame,_= self.client_socket_audio.recvfrom(self.BUFF_SIZE)
    #             self.cola_audio.put(frame)
    #             print('Queue size...',self.cola_audio.qsize())
        
    #     hiloGetAudio = threading.Thread(target=getAudioData, args=())
    #     hiloGetAudio.daemon = True
    #     hiloGetAudio.start()

    #     time.sleep(9.60)
    #     self.lblIndicador.configure(text="Reproduciendo")
    #     print('Now Playing Audio...')

    #     while not self.terminado:
    #         if not self.pausa:
    #             frame = self.cola_audio.get()
    #             stream.write(frame)

    #     #client_socket.close()
    #     print('Audio closed')
    #     #os._exit(1)

#g = GUI()
