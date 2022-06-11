from multiprocessing.managers import BaseManager
import tkinter as tk
from tkinter import ttk
from config import serv_ftp

def VentanaInicioSesion(obtenerCredenciales):
    frame_login = ttk.Frame(padding=30, width= 400)
    frame_widgets = ttk.Frame(frame_login, padding=5)
    frame_widgets.grid(row=0, column=0)

    label_user = ttk.Label(frame_widgets, text="Username: ", background='yellow')
    label_user.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    input_user = ttk.Entry(frame_widgets, width=30)
    input_user.grid(row=0, column=1, sticky=tk.E ,padx=5, pady=5)

    label_password = ttk.Label(frame_widgets, text="Password: ", background='yellow')
    label_password.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

    input_password = ttk.Entry(frame_widgets, show='*', width=30)
    input_password.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

    frame_boton = ttk.Frame(frame_login, padding=2)
    frame_boton.grid(row=1, column=0)
    frame_boton.config(cursor="spider")
    frame_boton.grid_rowconfigure(0, weight=1)
    frame_boton.grid_columnconfigure(0, weight=1)
    
    boton_login = ttk.Button(frame_boton, text="Login", width=20)
    boton_login.grid(row=2, column=0)
    boton_login.bind('<Button-1>', lambda e:obtenerCredenciales(input_user, input_password))
    
    return frame_login

def VentanaPrincipal(upload, streaming):
    contenedor = ttk.Frame(padding=40)
    
    boton_upload = ttk.Button(master=contenedor, text="Subir archivo")
    boton_streaming = ttk.Button(master= contenedor, text="Streaming")
    boton_upload.grid(row=0, column=0, padx=40)
    boton_streaming.grid(row=0, column=1, padx=40)
    
    boton_upload.bind("<Button-1>", upload )
    boton_streaming.bind("<Button-1>",  streaming)

    return contenedor

def ventanaSeleccion(seleccionarVideo, subirArchivo, atras):
    #global label_seleccion
    frame_seleccion = ttk.Frame(padding=10, name="frame-seleccion")
    frame_seleccion.grid(row=0, column=0)

    frame_secundario = ttk.Frame(frame_seleccion, padding=10)
    frame_secundario.grid(row=0, column=0)

    lbl = ttk.Label(frame_secundario)
    lbl.grid(row=1, column=0)

    label_seleccion = ttk.Label(frame_secundario, name="label_seleccion" ,text='Seleccione un archivo', background='lightgreen')
    label_seleccion.grid(row=0, column=0, sticky=tk.E)

    

    boton_seleccion = ttk.Button(frame_secundario, text="Seleccionar" ,cursor='spider')
    boton_seleccion.grid(row=0, column=1, padx=10)
    boton_seleccion.bind('<Button-1>', seleccionarVideo)
    boton_subir = ttk.Button(frame_secundario, text="Subir", cursor='circle')
    boton_subir.bind("<Button-1>", subirArchivo )
    boton_subir.grid(row=3, column=0)

    boton_atras = ttk.Button(frame_seleccion,text="Atrás")
    boton_atras.grid(row=1, column=0, sticky="W")
    boton_atras.bind("<Button-1>", atras)


def VentanaStreaming(atras):

    frame_streaming = ttk.Frame(padding=10, name="frame_streaming", cursor="star")

    frame_encabezado = ttk.Frame(frame_streaming,padding=10, name="frame_encabezado", cursor="spider")
    frame_encabezado.grid(row=0, column=0)

    lbl_TotalVideos = ttk.Label(frame_encabezado, text="Videos disponibles en el servidor", foreground="white", background="blue", font=20)
    lbl_TotalVideos.grid(row=0, column=0)

    frame_archivos = ttk.Frame(frame_encabezado, name="frame_archivos")
    frame_archivos.grid(row=1, column=0)
    
    boton_atras = ttk.Button(frame_streaming,text="Atrás")
    boton_atras.grid(row=1, column=0, sticky="W")
    boton_atras.bind("<Button-1>", atras)

    return frame_streaming