from ftplib import FTP, all_errors
import time
import tkinter as tk
from tkinter import Label, Widget, ttk, messagebox
from tkinter import filedialog as fd
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
import prueba

HOST = ""
PUERTO = 0

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
    stream = prueba.GUI(frm, nombreVideo)

    #Aqui se debe setear la IP y el HOST

def atras(e):
    global stream
    if stream:
        stream.Terminado()
        print("Stream terminado")
    else:
        print("ERROR, no se ha seteado stream!!!")
    time.sleep(1)
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

            #ventaPrincipal = Ventanas.VentanaPrincipal( upload , streaming)
            #ventaPrincipal.grid_configure(in_= root)

            #Aqui debe ir la direccion IP

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
                            print(w.winfo_name())
                            btn_ok = w
            
            btn_ok.bind("<Button-1>", lambda e: aceptarIP(e, in_1, in_2))

        else:
            label_info = ttk.Label(ventana, text='Usuario y/o contrase??a incorrectos.', foreground='red')
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
    if messagebox.askokcancel("Salir", "Est?? seguro de salir?"):
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
    iniciar.daemon = True
    iniciar.start()

