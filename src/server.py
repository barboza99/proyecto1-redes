#import random
import threading
import cv2, imutils, socket
from cv2 import add
from cv2 import medianBlur
import time
import base64
#import threading, wave, pyaudio,pickle,struct
import queue
import os
from concurrent.futures import ThreadPoolExecutor

colaVideo = queue.Queue(maxsize=1000)



with ThreadPoolExecutor(max_workers=2) as executor:
    #executor.submit(audio_stream)
    #executor.submit(video_stream_gen)
    #executor.submit(video_stream)

    #nombreVideo =  "TeEscondes.mp4"
    nombreVideo = ""
    video = None
    FPS = None
    #BREAK=False
    #AUDIOCREADO = False
    MENSAJERECIBIDO = False
    BUFF_SIZE = 65536
    direcciones_clientes = []

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    #server_socket.settimeout(5.5)
    HOST_NAME = socket.gethostname()
    HOST_IP = socket.gethostbyname(HOST_NAME)
    host_ip = '192.168.0.5' #socket.gethostbyname(host_name)
    #print(host_ip)
    port = 9688
    socket_address = (host_ip,port)
    server_socket.bind(socket_address)
    print('Escuchando en :[',socket_address,"]")

    def validar():
        global video
        global FPS
        global nombreVideo
        global AUDIOCREADO

        video = cv2.VideoCapture(nombreVideo)
        FPS = video.get(cv2.CAP_PROP_FPS)
        print("Video a reproducir: [", nombreVideo,"]")
        #command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(nombreVideo,'temp.wav')
        #os.system(command)
        #AUDIOCREADO = True
        totalNoFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        durationInSeconds = float(totalNoFrames) / float(FPS)
        #d = video.get(cv2.CAP_PROP_POS_MSEC)
        print("Duracion en minutos: ", (durationInSeconds/60))
        print('FPS:',FPS)

    def video_stream_gen():
        global video
        global MENSAJERECIBIDO
        WIDTH=400
        contador = 1

        while True:
            if MENSAJERECIBIDO:
                while video.isOpened():
                    #print("estoy en video_stream_gen: ", contador)
                    contador += 1
                    try:
                        _,frame = video.read()
                        frame = imutils.resize(frame,width=WIDTH)
                        colaVideo.put(frame)
                        #print("Cola size... ", colaVideo.qsize())
                    except:
                        print("Cola llena o error de leer el video")
                        print("Cola size... ", colaVideo.qsize())
                        video.release()
                        #print("Cola size... ", colaVideo.qsize())
                        #os._exit(1)
                #print('Player closed')
                #BREAK=True
                video.release()

    #validar()

    def video_stream():
        #global nombreVideo
        #global AUDIOCREADO
        #global MENSAJERECIBIDO
        # print("Escucho...")
        
        # print("El mensaje es: ",mensaje.decode('utf-8'))
        # print("Salgo de escuchar...")
        cont = 0
        while True:
            print("Contador: ",cont)
            cont+=1
            (mensaje, client_addr) = server_socket.recvfrom(BUFF_SIZE)
            if mensaje.decode("UTF-8") != "OK":
                first = threading.Thread(target=initTransmision, args=(mensaje, client_addr))
                first.daemon = True
                first.start()
                print("Esto es despues de recibir el mensaje")


    def initTransmision(mensaje, address):
        global MENSAJERECIBIDO
        global nombreVideo
        nombreVideo = mensaje.decode('utf-8')
        if nombreVideo != "":
            print("Entro al IF")
            validar()
            time.sleep(1)
            MENSAJERECIBIDO = True
            #AUDIOCREADO = True
            time.sleep(1)
            
        print("Conexion establecida con: ", address)
        print("Mensaje recibido: ", mensaje.decode('utf-8'))
        
        #if AUDIOCREADO:
        #time.sleep(7)
        while True:
            if not colaVideo.empty():
                frame = colaVideo.get()
                encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
                message = base64.b64encode(buffer)
                server_socket.sendto(message, address)
                time.sleep(0.018)
                
                #print("Cola size: ", colaVideo.qsize())
            #else:
                #print("El video ha finalizado...")
        print("El video ha finalizado")

    """
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
    """
    executor.submit(video_stream)
    executor.submit(video_stream_gen)
    #executor.submit(audio_stream)
