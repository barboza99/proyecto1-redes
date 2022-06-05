from tkinter import *
import cv2
import imutils
import socket
import numpy as np
import time
import os
import base64
import threading
import wave
import pyaudio
import pickle
import struct
from PIL import Image
from PIL import ImageTk
BUFF_SIZE = 65536

BREAK = False
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '192.168.8.104'
print(host_ip)
port = 9688
message = b'Hello'

client_socket.sendto(message, (host_ip, port))

class GUI:
    # constructor method
    def __init__(self):
        self.Window = Tk()

        self.Window.geometry('640x500')

        self.btn = Button(self.Window,
                          text="PLAY",
                          font="Helvetica 14 bold",
                          command=lambda: self.play())

        self.btn.pack()

        self.video = Label(self.Window)
        self.video.pack()

        self.Window.mainloop()

    def play(self):
        
        rcv = threading.Thread(target=self.receive)
        aud = threading.Thread(target=self.audio)
        rcv.start()
        aud.start()


    def receive(self):
        while True:
            try:
                packet, _ = client_socket.recvfrom(BUFF_SIZE)
                data = base64.b64decode(packet, ' /')
                npdata = np.fromstring(data, dtype=np.uint8)

                frame = cv2.imdecode(npdata, 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                self.video.config(image=img)
                self.video.image = img

            except:
                print("An error occured!")
                socket.close()
                break

    def audio(self):
        p = pyaudio.PyAudio()
        CHUNK = 1024
        stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=CHUNK)

        # create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_address = (host_ip, port-1)
        print('server listening at', socket_address)
        client_socket.connect(socket_address)
        print("CLIENT CONNECTED TO", socket_address)
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            try:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024)  # 4K
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                stream.write(frame)

            except:

                break

        client_socket.close()
        print('Audio closed', BREAK)
        os._exit(1)


g = GUI()
