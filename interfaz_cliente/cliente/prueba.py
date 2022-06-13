from tkinter import *
import cv2
import socket
import numpy as np
import time
import os
import base64
from time import sleep
import threading
import pyaudio
import queue
from PIL import Image
from PIL import ImageTk

BUFF_SIZE = 65536
BREAK = False

host_name = socket.gethostname()
host_ip = '192.168.0.4'
print(host_ip)
port = 9688
message = b'Hello'

q2 = queue.Queue(maxsize=2000)
q = queue.Queue(maxsize=2000)

class GUI:
    # constructor method
    def __init__(self, frame, nombreVideo):
        self.frame = frame
        self.nomVideo = nombreVideo
        # self.Window = Tk()
        # self.Window.configure(cursor='heart')
        # self.Window.minsize(width=600, height=380)
        self.btn = Button(self.frame,
                          text="PLAY",
                          font="Helvetica 14 bold",
                          command=lambda: self.play())

        self.btn.grid(row=1,column=0)

        self.video = Label(self.frame)
        self.video.grid(row=2, column=0)

    def play(self):

        rcv = threading.Thread(target=self.receive)
        aud = threading.Thread(target=self.audio)
        rcv.daemon = True
        rcv.start()
        aud.daemon = True
        aud.start()

    def receive(self):
        
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        client_socket.sendto(bytes(self.nomVideo,"UTF-8"),(host_ip,port))

        def getVideoData():
            while True:
                packet, _ = client_socket.recvfrom(BUFF_SIZE)
                data = base64.b64decode(packet, ' /')
                npdata = np.fromstring(data, dtype=np.uint8)

                frame = cv2.imdecode(npdata, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                q2.put(frame)

        t2 = threading.Thread(target=getVideoData, args=())
        t2.start()
        time.sleep(5)
        print('Now Playing video...')
        while True:
            frame = q2.get()
            
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            self.video.config(image=img)
            self.video.image = img
            sleep(0.023)

        client_socket.close()
        print('Video closed')
        os._exit(1)


    def audio(self):
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        p = pyaudio.PyAudio()
        CHUNK = 10*1024
        stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=CHUNK)
                        
        # create socket
        message = b'Hello'
        client_socket.sendto(bytes(self.nomVideo,"UTF-8"),(host_ip,port-1))
        socket_address = (host_ip,port-1)
        
        def getAudioData():
            while True:
                frame,_= client_socket.recvfrom(BUFF_SIZE)
                q.put(frame)
                print('Queue size...',q.qsize())
        t1 = threading.Thread(target=getAudioData, args=())
        t1.start()
        time.sleep(5)
        print('Now Playing...')
        while True:
            frame = q.get()
            stream.write(frame)

        client_socket.close()
        print('Audio closed')
        os._exit(1)

#g = GUI()
