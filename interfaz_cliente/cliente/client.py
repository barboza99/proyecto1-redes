from asyncio.windows_events import NULL
from ftplib import FTP, all_errors
import tkinter as tk
from tkinter import Label, Widget, ttk, messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from cv2 import textureFlattening
from pyparsing import col
from conexionFTP import iniciarSesion
import Ventanas
from config import serv_ftp
from config import band
from config import nombreArchivo
from config import root
import cv2
import base64
import socket
import numpy as np
import queue
import threading
from time import sleep
import time
import pyaudio
import prueba

import os

message = b'Hola soy Angel'
BUFF_SIZE = 65536
q2 = queue.Queue(maxsize=2000)
q = queue.Queue(maxsize=2000)

def upload(e:Widget):
    e.widget.master.grid_remove()
    vetanaSubirArchivo = Ventanas.ventanaSeleccion(seleccionarVideo,subirArchivo, atras)
    #vetanaSubirArchivo.grid(row=0, column=0)
    #print(msg)
global img 

def streaming(e):
    global img
    e.widget.master.grid_remove()
    ventanaStreaming = Ventanas.VentanaStreaming(atras)
    frame_archs = None
    frameVideo = ttk.Frame(ventanaStreaming)
    frameVideo.grid(row=0, column=1)
    labelVideo = ttk.Label(frameVideo, text="Directo", font=18, foreground="blue",justify="center", border=4)
    #img = ImageTk.PhotoImage(Image.open("interfaz_cliente/cliente/kakashi.png"))
    #labelVideo.config(image=img)
    labelVideo.grid(row=0, column=0)
   

    for widget in ventanaStreaming.winfo_children():
        if  widget.winfo_name() == "frame_encabezado":
            for w in widget.winfo_children():
                if w.winfo_name() == "frame_archivos":
                    frame_archs = w
                    break
            break

    archivos = serv_ftp.nlst()
    fila = 0
    hayArchivos = False
    for archivo in archivos:
        if archivo.endswith(".mp4"):
            hayArchivos = True
            contenedor = ttk.Frame(frame_archs, name= str(fila))
            contenedor.grid(row=fila, column=0)
            
            boton = ttk.Button(contenedor, text="Reproducir")
            boton.bind('<Button-1>',lambda e: manejador(e,frameVideo))
            lbl = ttk.Label(contenedor, text=archivo, background="lightgreen",name="label")
            lbl.grid(row=0, column=0, pady=2)
            boton.grid(row=0, column=1, pady=2, padx=2)
            fila += 1;

    if not hayArchivos:
        lbl = ttk.Label(frame_archs, text="No hay videos para mostrar")
        lbl.grid(row=1, column=0)

    ventanaStreaming.grid(row=0, column=0)


def manejador(e,frm):
    print(e.widget.winfo_parent())
    Nameparent = e.widget.winfo_parent()
    parent = Widget._nametowidget(e.widget.master,Nameparent)
    nombreVideo = ""
    for widget in parent.winfo_children():
        if widget.winfo_name() == "label":
                nombreVideo = widget.cget("text")
                break

    print("Nombre del video es: [",nombreVideo,"]")
    stream = prueba.GUI(frm, nombreVideo)
    

def conexionStreaming(lblvideo):
    print("XDXD")
    host_ip = '192.168.0.4'
    port = 9688
   

    rcv = threading.Thread(target=receive(host_ip, port, lblvideo))
    rcv.start()
    #aud = threading.Thread(target=audio(host_ip, port))
    #aud.start()



def receive(host_ip, port, video):
    global message
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    client_socket.sendto(message,(host_ip,port))

    def getVideoData():
        while True:
            packet, _ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet, ' /')
            npdata = np.frombuffer(data, dtype=np.uint8)

            frame = cv2.imdecode(npdata, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



            q2.put(frame)

    t2 = threading.Thread(target=getVideoData, args=())
    t2.start()
    time.sleep(5)
    print('Now Playing...')
    while not q2.empty():
        frame = q2.get()
        
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        video.config(image=img)
        video.image = img
        sleep(0.023)
        print(q2.qsize())

    client_socket.close()
    print('Video closed')
    os._exit(1)

def audio(host_ip, port):
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
    client_socket.sendto(message,(host_ip,port-1))
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

def atras(e):
    e.widget.master.grid_remove()
    ventaPrincipal = Ventanas.VentanaPrincipal(upload , streaming)
    ventaPrincipal.grid_configure(in_= root)

def obtenerCredenciales(in_user, in_pass):
    user = in_user.get()
    passw = in_pass.get()
    global serv_ftp
    if len(user) < 1 or len(passw) < 1:
        label_info = ttk.Label(ventana, text='Debe ingresar los datos', foreground='red')
        label_info.grid(row=3, column=0)
    else:
        serv_ftp = iniciarSesion(user, passw)

        if serv_ftp is not None:
            ventana.grid_remove()
            ventaPrincipal = Ventanas.VentanaPrincipal( upload , streaming)
            ventaPrincipal.grid_configure(in_= root)
            #ventanaSeleccion(serv_ftp)
            #value.quit()
        else:
            label_info = ttk.Label(ventana, text='Usuario y/o contraseña incorrectos.', foreground='red')
            label_info.grid(row=3, column=0)
        
ventana = Ventanas.VentanaInicioSesion(obtenerCredenciales)
ventana.grid_configure(in_= root)
#serv_ftp = None

def seleccionarVideo(e):
    global nombreArchivo
    global band
    
    filetypes = (
        ('Video Files', '*.mp4'),
        ('Others', '.mkv'),
        ('All Files', '.*'),
        ('Img', '*.jpg')
    )
   
    nombreArchivo = fd.askopenfilename(filetypes=filetypes, title="Elegir un video")
    if len(nombreArchivo) > 0:

        Nameparent = e.widget.winfo_parent()
        #parent = Widget.nametowidget(e.widget.master, Nameparent)
        parent = Widget._nametowidget(e.widget.master,Nameparent)
        label_seleccion = None
        #listaWidgets = parent.winfo_children()
        
        for widget in parent.winfo_children():
            if widget.winfo_name() == "label_seleccion":
                label_seleccion = widget
                break

        band = True
        name = nombreArchivo.split("/")[-1]
        label_seleccion.config(text=name)

def subirArchivo(e):
    #print(msg)
    global band
    global serv_ftp
    if band is not False:
        #print(nombreArchivo.split("/"))
        fl = open(nombreArchivo, "rb")
        name = nombreArchivo.split("/")[-1]
        serv_ftp.storbinary(f"STOR {name}", fl)
        fl.flush()
        fl.close()
        #ftpselector.quit()
    else:
        messagebox.showinfo("Seleccionar", "Seleccione un archivo")

def salir():
    if messagebox.askokcancel("Salir", "Está seguro de salir?"):
        print("Saliendo... ")
        try:
            if serv_ftp is not None:
                serv_ftp.quit()
        except all_errors as error:
            print(error)
        root.destroy()

root.protocol("WM_DELETE_WINDOW", salir )

if __name__ == "__main__":
    iniciar = threading.Thread(root.mainloop())
    iniciar.start()

