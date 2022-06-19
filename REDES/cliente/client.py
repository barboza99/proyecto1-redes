from datetime import date, datetime
from distutils.log import info
from ftplib import FTP, all_errors
from io import BufferedRandom, BufferedReader
import io
import json
import time
import tkinter as tk
from tkinter import Label, Widget, ttk, messagebox
from tkinter import filedialog as fd
from traceback import print_tb
from pyparsing import col
from conexionFTP import iniciarSesion
import Ventanas
from config import serv_ftp
from config import band
from config import nombreArchivo
from config import root
import numpy as np
import threading
from time import sleep
from VentanaVideo import GUI
import socket

HOST = '192.168.0.5'
PUERTO = 9688

def upload(e:Widget):
    e.widget.master.grid_remove()
    vetanaSubirArchivo = Ventanas.ventanaSeleccion(seleccionarVideo,subirArchivo, atras)

def streaming(e):
    e.widget.master.grid_remove()
    ventanaStreaming = Ventanas.VentanaStreaming(atras)
    frame_archs = None
    frameVideo = ttk.Frame(ventanaStreaming, name="frame_video")
    frameVideo.grid(row=0, column=1)
    labelVideo = ttk.Label(frameVideo, text="Directo", font=18, foreground="blue",justify="center", border=4)
    labelVideo.grid(row=0, column=0)

    for widget in ventanaStreaming.winfo_children():
        if  widget.winfo_name() == "frame_encabezado":
            for w in widget.winfo_children():
                if w.winfo_name() == "frame_archivos":
                    frame_archs = w
                    break
            break

    archivos = serv_ftp.nlst("videos")
    fila = 0
    hayArchivos = False
    archivos_json = []
    for archivo in archivos:
        if archivo.endswith(".json"):
            archivos_json.append(archivo)
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

    if hayArchivos:
        nombres = "Archivos_JSON,"
        for arch_json in archivos_json:
            nombres += arch_json + ","
        print(nombres)
        enviarSolicitud(nombres=nombres)

    if not hayArchivos:
        lbl = ttk.Label(frame_archs, text="No hay videos para mostrar")
        lbl.grid(row=1, column=0)

   

    ventanaStreaming.grid(row=0, column=0)

def enviarSolicitud(nombres):
    global HOST
    global PUERTO
    try:
        socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_video.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        socket_video.sendto(bytes(nombres,"UTF-8"), ('192.168.0.5', 9688))
        msj, _ = socket_video.recvfrom(65536)
        if msj.decode("UTF-8").startswith("Archivos_JSON"):
            
            ls = msj.decode("UTF-8").split(";")
            ls.pop(0)
            ls.pop(-1)
            print("Lista de jsons ----> ", ls)
            ls_jsons = []
            for js in ls:
                ls_jsons.append(json.loads(js))
                print("JSON: ", js)

            print("\nLista de jsons_loads ----> ", ls_jsons)
    except Exception as e:
        print("Expecion: ", e)

stream = None
def manejador(e,frm):
    global stream
    Nameparent = e.widget.winfo_parent()
    parent = Widget._nametowidget(e.widget.master,Nameparent)
    nombreVideo = ""
    for widget in parent.winfo_children():
        if widget.winfo_name() == "label":
                nombreVideo = widget.cget("text")
                break

    print("Nombre del video es: [",nombreVideo,"]")
    if not stream:
        stream = GUI(frm, nombreVideo)
    else:
        stream.enviarMensajeTerminacion("o_reproducir")
        stream.setNombreVideo(nombreVideo)


    #Aqui se debe setear la IP y el HOST

def atras(e):
    global stream
    if stream:
        stream.Terminado(True)
        stream.enviarMensajeTerminacion("terminar")
        print("Stream terminado")
    else:
        print("ERROR, no se ha seteado stream!!!")
    time.sleep(0.4)
    e.widget.master.destroy()
    ventaPrincipal = Ventanas.VentanaPrincipal(upload , streaming)
    ventaPrincipal.grid_configure(in_= root)

def aceptarIP(e, in1, in2):
    global HOST
    global PUERTO
    if len(in1.get()) < 4 or len(in2.get()) < 4:
        print("Error")
    else:
        HOST = in1.get()
        PUERTO = int(in2.get())
        e.widget.master.master.grid_remove()
        ventaPrincipal = Ventanas.VentanaPrincipal( upload , streaming)
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
            ventana_ingresoIP = Ventanas.VentanaIngresoIPyPort()
            ventana_ingresoIP.grid_configure(in_= root)
            in_1 = None
            in_2 = None
            btn_ok = None
            for widget in ventana_ingresoIP.winfo_children():
                if widget.winfo_name() == "frm1":
                    for w in widget.winfo_children():
                        if w.winfo_name() == "entry_ip":
                            in_1 = w
                        elif w.winfo_name() == "entry_port":
                            in_2 = w
                elif widget.winfo_name() == "frm2":
                    for w in widget.winfo_children():
                        if w.winfo_name() == "btn_ok":
                            btn_ok = w
            
            btn_ok.bind("<Button-1>", lambda e: aceptarIP(e, in_1, in_2))

        else:
            label_info = ttk.Label(ventana, text='Usuario y/o contraseña incorrectos.', foreground='red')
            label_info.grid(row=3, column=0)
        
ventana = Ventanas.VentanaInicioSesion(obtenerCredenciales)
ventana.grid_configure(in_= root)

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
        parent = Widget._nametowidget(e.widget.master,Nameparent)
        label_seleccion = None
        
        for widget in parent.winfo_children():
            if widget.winfo_name() == "label_seleccion":
                label_seleccion = widget
                break

        band = True
        name = nombreArchivo.split("/")[-1]
        label_seleccion.config(text=name)

def subirArchivo(cmbx, inputDuracion):
    #print(msg)
    print("Valor del combobox: ", cmbx.get())
    print("Valor del input: ", inputDuracion.get())
    global band
    global serv_ftp
    if band is not False and len(inputDuracion.get()) > 0:
        if not inputDuracion.get().isnumeric():
            messagebox.showinfo("Duracion", "El campo debe ser un número!!")
            return
        fl = open(nombreArchivo, "rb")
        name = nombreArchivo.split("/")[-1]
        try:
            path = serv_ftp.mkd("videos")
            print("-->", path)
        except Exception as e:
            print("Except: ", e)

        serv_ftp.cwd("videos")
        #serv_ftp.storbinary(f"STOR {name}", fl)
        if  serv_ftp.storbinary(f"STOR {name}", fl).split(" ")[0] == "226":
            
            fecha = datetime.now()
            print(fecha.date())
            info_video = {"Nombre": name,
                            "Duracion": int(inputDuracion.get()),
                            "Genero": cmbx.get(), "Fecha_publicacion": fecha.date().strftime("%d/%m/%Y")}
           
            json_convert = json.dumps(info_video)
            file = io.BytesIO()
            file.write(bytes(json_convert, encoding="UTF-8"))
            file.seek(0)
            nameJSON = name.split(".")[0] + ".json"
            serv_ftp.storbinary(f"STOR {nameJSON}", file)
            file.close()
            messagebox.showinfo("Éxito","Video subido con éxito!!!")
        else:
            messagebox.showerror("Error","Ocurrió un error al subir el archivo!!!")

        serv_ftp.cwd("../")
        fl.flush()
        fl.close()
        #ftpselector.quit()
    else:
        messagebox.showinfo("Seleccionar", "Seleccione un archivo y llene todos los campos")

def salir():
    if messagebox.askokcancel("Salir", "Está seguro de salir?"):
        print("Saliendo... ")
        try:
            if serv_ftp is not None:
                serv_ftp.quit()
                if stream:
                    stream.enviarMensajeTerminacion("terminar")
        except all_errors as error:
            print(error)
        root.destroy()

root.protocol("WM_DELETE_WINDOW", salir )

if __name__ == "__main__":
    iniciar = threading.Thread(root.mainloop())
    iniciar.daemon = True
    iniciar.start()