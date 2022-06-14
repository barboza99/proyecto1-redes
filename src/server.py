import random
import cv2, imutils, socket
import numpy as np
import time
import base64
import threading, wave, pyaudio,pickle,struct
import queue
import os

q = queue.Queue(maxsize=1000)

from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    #executor.submit(audio_stream)
    #executor.submit(video_stream_gen)
    #executor.submit(video_stream)

    #filename =  "TeEscondes.mp4"
    filename = ""

    BUFF_SIZE = 65536
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip = '192.168.0.4' #socket.gethostbyname(host_name)
    print(host_ip)
    port = 9688
    socket_address = (host_ip,port)
    server_socket.bind(socket_address)
    print('Listening at:',socket_address)
    
    vid = None
    FPS = None

    BREAK=False
    AUDIOCREADO = False
    MENSAJERECIBIDO = False

    def validar():
        global vid
        global FPS
        global filename
        global AUDIOCREADO

        vid = cv2.VideoCapture(filename)
        FPS = vid.get(cv2.CAP_PROP_FPS)
        print("File name: ", filename)
        command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(filename,'temp.wav')
        os.system(command)
        AUDIOCREADO = True
        totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        durationInSeconds = float(totalNoFrames) / float(FPS)
        d=vid.get(cv2.CAP_PROP_POS_MSEC)
        print("Duracion en segundos: ", durationInSeconds,d)
        print('FPS:',FPS)

    def video_stream_gen():
        global vid
        WIDTH=400
        while True:
            if MENSAJERECIBIDO:
                contador = 1
                while(vid.isOpened()):
                    print("estoy en video gen: ", contador)
                    contador += 1
                    try:
                        _,frame = vid.read()
                        frame = imutils.resize(frame,width=WIDTH)
                        q.put(frame)
                    except:
                        print("ERROR")
                        os._exit(1)
                print('Player closed')
                BREAK=True
                vid.release()

    #validar()

    def video_stream():
        global filename
        global AUDIOCREADO
        global MENSAJERECIBIDO

        cont = 0
        while True:
            print(cont)
            cont+=1
            msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
            filename = msg.decode('utf-8')
            if filename != "":
                print("Entro al if y el msj es: ", filename)
                validar()
                time.sleep(2)
                MENSAJERECIBIDO = True
                AUDIOCREADO = True
                #time.sleep(1)
               
                print("Esto es despues del metodo validar")
                
            print("Conexion establecida con: ",client_addr)
            print("Mensaje recibido: ", msg.decode('utf-8'))
            if AUDIOCREADO:
                time.sleep(7)
                while(True):
                    frame = q.get()
                    encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
                    message = base64.b64encode(buffer)
                    server_socket.sendto(message,client_addr)
                    time.sleep(0.018)


    def audio_stream():
        global AUDIOCREADO
        BUFF_SIZE = 65536
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        server_socket.bind((host_ip, (port-1)))
        CHUNK = 10*1024
        while True:
            if AUDIOCREADO:
               
                wf = wave.open("temp.wav")
                p = pyaudio.PyAudio()
                print('server listening at',(host_ip, (port)),wf.getframerate())
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                input=True,
                                frames_per_buffer=CHUNK)

                data = None
                sample_rate = wf.getframerate()
                while True:
                    msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
                    print('Conexion establecida con:',client_addr,msg.decode('utf-8'))
                    
                    while True:
                        data = wf.readframes(CHUNK)
                        server_socket.sendto(data,client_addr)
                        time.sleep(0.8*CHUNK/sample_rate)

                        print(0.8*CHUNK/sample_rate)

    executor.submit(video_stream)
    executor.submit(video_stream_gen)
    executor.submit(audio_stream)
