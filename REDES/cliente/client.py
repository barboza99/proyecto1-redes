from datetime import date, datetime
from ftplib import FTP, all_errors
import io
import json
import time
import tkinter as tk
from tkinter import Widget, ttk, messagebox
from tkinter import filedialog as fd
from conexionFTP import iniciarSesion
import Ventanas
from config import serv_ftp
from config import band
from config import nombreArchivo
from config import root
import numpy as np
import threading
from VentanaVideo import GUI
import socket

HOST = '192.168.0.2'
PUERTO = 9688
salidoAntes = False
volviAEntrar = False

def upload(e:Widget):
    e.widget.master.grid_remove()
    vetanaSubirArchivo = Ventanas.ventanaSeleccion(seleccionarVideo,subirArchivo, atras)

def streaming(e):

    e.widget.master.grid_remove()
    listaInfoVideos = []
    frame_archs = None
    

    def filtrarVideos(comboBox, input):
        #global frame_archs
        if input.get() == "" or input.get() == None:
            for w in frame_archs.winfo_children():
                w.destroy()

            frame_archs_sec = ttk.Frame(frame_archs)
            frame_archs_sec.grid(row=0, column=0)
            fila = 0
           
            for js in listaInfoVideos:
                if input.get().upper() in js['Nombre'].upper():
                    contenedor = ttk.Frame(frame_archs_sec, name= str(fila))
                    contenedor.grid(row=fila, column=0)
                
                    boton = ttk.Button(contenedor, text="Reproducir")
                    boton.bind('<Button-1>',lambda e: manejador(e,frameVideo))
                    lbl = ttk.Label(contenedor, text=js['Nombre'], background="lightgreen",name="label")
                    lbl.grid(row=0, column=0, pady=2)
                    boton.grid(row=0, column=1, pady=2, padx=2)
                    fila += 1;
            return
    
        if comboBox.get() == "Nombre" and len(input.get()) > 0:
            for w in frame_archs.winfo_children():
                w.destroy()

            frame_archs_sec = ttk.Frame(frame_archs)
            frame_archs_sec.grid(row=0, column=0)
            fila = 0
            bandera = False
            for js in listaInfoVideos:
                if input.get().upper() in js['Nombre'].upper():
                    bandera = True
                    contenedor = ttk.Frame(frame_archs_sec, name= str(fila))
                    contenedor.grid(row=fila, column=0)
                
                    boton = ttk.Button(contenedor, text="Reproducir")
                    boton.bind('<Button-1>',lambda e: manejador(e,frameVideo))
                    lbl = ttk.Label(contenedor, text=js['Nombre'], background="lightgreen",name="label")
                    lbl.grid(row=0, column=0, pady=2)
                    boton.grid(row=0, column=1, pady=2, padx=2)
                    fila += 1;

            if not bandera:
                lbl = ttk.Label(frame_archs_sec, text="No hay coincidencias")
                lbl.grid(row=1, column=0)


        elif comboBox.get() == "Genero" and len(input.get()) > 0:
            for w in frame_archs.winfo_children():
                w.destroy()

            frame_archs_sec = ttk.Frame(frame_archs)
            frame_archs_sec.grid(row=0, column=0)
            fila = 0
            bandera = False
            for js in listaInfoVideos:
                if input.get() == js['Genero']:
                    bandera = True
                    contenedor = ttk.Frame(frame_archs_sec, name= str(fila))
                    contenedor.grid(row=fila, column=0)

                    boton = ttk.Button(contenedor, text="Reproducir")
                    boton.bind('<Button-1>',lambda e: manejador(e,frameVideo))
                    lbl = ttk.Label(contenedor, text=js['Nombre'], background="lightgreen",name="label")
                    lbl.grid(row=0, column=0, pady=2)
                    boton.grid(row=0, column=1, pady=2, padx=2)
                    fila += 1;
            if not bandera:
                lbl = ttk.Label(frame_archs_sec, text="No hay coincidencias")
                lbl.grid(row=1, column=0)

        elif comboBox.get() == "Duracion" and len(input.get()) > 0:
            for w in frame_archs.winfo_children():
                w.destroy()

            frame_archs_sec = ttk.Frame(frame_archs)
            frame_archs_sec.grid(row=0, column=0)
            fila = 0
            bandera = False
            for js in listaInfoVideos:
                if input.get() == js['Duracion']:
                    bandera = True
                    contenedor = ttk.Frame(frame_archs_sec, name= str(fila))
                    contenedor.grid(row=fila, column=0)
                
                    boton = ttk.Button(contenedor, text="Reproducir")
                    boton.bind('<Button-1>',lambda e: manejador(e,frameVideo))
                    lbl = ttk.Label(contenedor, text=js['Nombre'], background="lightgreen",name="label")
                    lbl.grid(row=0, column=0, pady=2)
                    boton.grid(row=0, column=1, pady=2, padx=2)
                    fila += 1

            if not bandera:
                lbl = ttk.Label(frame_archs_sec, text="No hay coincidencias")
                lbl.grid(row=1, column=0)

        elif comboBox.get() == "Fecha" and len(input.get()) > 0:
            if len(input.get().split("/")) > 2 and len(input.get().split("/")) < 4:
                for w in frame_archs.winfo_children():
                    w.destroy()

                frame_archs_sec = ttk.Frame(frame_archs)
                frame_archs_sec.grid(row=0, column=0)
                fila = 0
                bandera = False
                for js in listaInfoVideos:
                    if input.get() == js['Fecha_publicacion']:
                        bandera = True
                        contenedor = ttk.Frame(frame_archs_sec, name= str(fila))
                        contenedor.grid(row=fila, column=0)
                    
                        boton = ttk.Button(contenedor, text="Reproducir")
                        boton.bind('<Button-1>',lambda e: manejador(e,frameVideo))
                        lbl = ttk.Label(contenedor, text=js['Nombre'], background="lightgreen",name="label")
                        lbl.grid(row=0, column=0, pady=2)
                        boton.grid(row=0, column=1, pady=2, padx=2)
                        fila += 1

                if not bandera:
                    lbl = ttk.Label(frame_archs_sec, text="No hay coincidencias")
                    lbl.grid(row=1, column=0)
            else:
                messagebox.showinfo("Formato de fecha", "EL formato de fecha debe ser dd/mm/yy")
    
    ventanaStreaming = Ventanas.VentanaStreaming(atras, filtrarVideos)
    
    frameVideo = ttk.Frame(ventanaStreaming, name="frame_video")
    frameVideo.grid(row=0, column=2)
    labelVideo = ttk.Label(frameVideo, text="Directo", foreground="blue", justify="center", border=4)
    labelVideo.grid(row=0, column=0)

    for widget in ventanaStreaming.winfo_children():
        if  widget.winfo_name() == "frame_encabezado":
            for w in widget.winfo_children():
                if w.winfo_name() == "frame_archivos":
                    frame_archs = w
                    break
            break
    try:
        archivos = serv_ftp.nlst("videos")
        fila = 0
        hayArchivos = False
        archivos_json = []

        for archivo in archivos:
            if archivo.endswith(".json"):
                hayArchivos = True
                archivos_json.append(archivo)

        if hayArchivos:
            nombres = "Archivos_JSON,"
            for arch_json in archivos_json:
                nombres += arch_json + ","

            listaInfoVideos = enviarSolicitud(nombres=nombres)
            frame_archs_sec = ttk.Frame(frame_archs)
            frame_archs_sec.grid(row=0, column=0)
            for js in listaInfoVideos:
                contenedor = ttk.Frame(frame_archs_sec, name= str(fila))
                contenedor.grid(row=fila, column=0)
                
                boton = ttk.Button(contenedor, text="Reproducir")
                boton.bind('<Button-1>',lambda e: manejador(e,frameVideo))
                lbl = ttk.Label(contenedor, text=js['Nombre'], background="lightgreen",name="label")
                lbl.grid(row=0, column=0, pady=2)
                boton.grid(row=0, column=1, pady=2, padx=2)
                fila += 1;

        else:
            lbl = ttk.Label(frame_archs_sec, text="No hay videos para mostrar")
            lbl.grid(row=1, column=0)
    except Exception as e:
        if str(e).split(" ")[0] == "550":
            lbl = ttk.Label(frame_archs, text="No hay videos para mostrar")
            lbl.grid(row=1, column=0)

    ventanaStreaming.grid(row=0, column=0)

def enviarSolicitud(nombres):
    global HOST
    global PUERTO
    ls_jsons = []
    try:
        socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_video.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        socket_video.sendto(bytes(nombres,"UTF-8"), (HOST, PUERTO))
        msj, _ = socket_video.recvfrom(65536)
        if msj.decode("UTF-8").startswith("Archivos_JSON"):
            
            ls = msj.decode("UTF-8").split(";")
            ls.pop(0)
            ls.pop(-1)
            
            for js in ls:
                ls_jsons.append(json.loads(js))

            return ls_jsons
    except Exception as e:
        print("Exepcion: ", e)
        return ls_jsons
       

stream = None
def manejador(e,frm):
    global stream
    global salidoAntes
    global HOST
    global PUERTO

    Nameparent = e.widget.winfo_parent()
    parent = Widget._nametowidget(e.widget.master,Nameparent)
    nombreVideo = ""
    for widget in parent.winfo_children():
        if widget.winfo_name() == "label":
                nombreVideo = widget.cget("text")
                break

    if not stream:
        stream = GUI(frm, nombreVideo)
        stream.setIP(HOST)
        stream.setPORT(PUERTO)
    else:
        if not stream.getTerminado():
            stream.enviarMensajeTerminacion("o_reproducir")
            stream.setNombreVideo(nombreVideo)
        else:
            if not salidoAntes:
                stream.setTerminado(False)
                stream.enviarMensajeTerminacion("o_reproducir")
                stream.setNombreVideo(nombreVideo)
            else:
                stream = GUI(frm, nombreVideo)
                stream.setIP(HOST)
                stream.setPORT(PUERTO)
                time.sleep(0.1)
                salidoAntes = False

#Aqui se debe setear la IP y el HOST

def atras(e):
    global stream
    global salidoAntes
    if stream:
        stream.setTerminado(True)
        stream.enviarMensajeTerminacion("terminar")
        salidoAntes = True
    else:
        print()

    time.sleep(0.10)
    if e.widget.winfo_name() == "btn_atras_subirArchivo":
        e.widget.master.destroy()
    else:
        e.widget.master.master.grid_remove()

    ventaPrincipal = Ventanas.VentanaPrincipal(upload , streaming)
    ventaPrincipal.grid_configure(in_= root)

def aceptarIP(e, in1, in2):
    global ventana
    global HOST
    global PUERTO
    if len(in1.get().split(".")) < 4 or len(in1.get().split(".")) > 4 or in2.get() == "" or in2.get() == None:
        messagebox.showinfo("Formato incorrecto", "El formato de la IP es incorrecto o el puerto está vacío")
    else:
        HOST = in1.get()
        PUERTO = int(in2.get())
        e.widget.master.master.grid_remove()
        ventana = Ventanas.VentanaInicioSesion(obtenerCredenciales)
        ventana.grid_configure(in_= root)

#ventana = Ventanas.VentanaInicioSesion(obtenerCredenciales)
ventana = Ventanas.VentanaIngresoIPyPort()
ventana.grid_configure(in_= root)
in_1 = None
in_2 = None
btn_ok = None
for widget in ventana.winfo_children():
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
ventana.grid_configure(in_= root)

def obtenerCredenciales(in_user, in_pass):
    global HOST
    global ventana
    user = in_user.get()
    passw = in_pass.get()
    global serv_ftp

    if len(user) < 1 or len(passw) < 1:
        label_info = ttk.Label(ventana, text='Debe ingresar los datos', foreground='red')
        label_info.grid(row=3, column=0)
    else:
        serv_ftp = iniciarSesion(HOST, user, passw)

        if serv_ftp is not None:
            ventana.grid_remove()
            ventaPrincipal = Ventanas.VentanaPrincipal( upload , streaming)
            ventaPrincipal.grid_configure(in_= root)

        else:
            label_info = ttk.Label(ventana, text='Usuario y/o contraseña incorrectos.', foreground='red')
            label_info.grid(row=3, column=0)


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
        except Exception as e:
            print("Except: ", e)

        serv_ftp.cwd("videos")
        #serv_ftp.storbinary(f"STOR {name}", fl)
        if  serv_ftp.storbinary(f"STOR {name}", fl).split(" ")[0] == "226":
            
            fecha = datetime.now()
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