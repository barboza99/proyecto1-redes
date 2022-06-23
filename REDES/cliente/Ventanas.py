import tkinter as tk
from tkinter import ttk

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
    frame_seleccion = ttk.Frame(padding=10, name="frame-seleccion", width=40)
    frame_seleccion.grid(row=0, column=0)

    frame_secundario = ttk.Frame(frame_seleccion, padding=10)
    frame_secundario.grid(row=0, column=0)

    label_seleccion = ttk.Label(frame_secundario, width=23,name="label_seleccion" ,text='Seleccione un archivo', background='lightgreen')
    label_seleccion.grid(row=0, column=0, sticky=tk.E)

    boton_seleccion = ttk.Button(frame_secundario, text="Seleccionar" ,cursor='spider')
    boton_seleccion.grid(row=0, column=1, padx=10)
    boton_seleccion.bind('<Button-1>', seleccionarVideo)

    label_genero = ttk.Label(frame_secundario, text="Género", width=23, background='lightgreen')
    label_genero.grid(row=1, column=0, pady=4)

    comboBox_genero = ttk.Combobox(frame_secundario, name="cmbx_genero")
    comboBox_genero['values'] = ('Drama', 'Accion', 'Comedia', 'Musica', 'Terror', 'Romance')
    comboBox_genero['state'] = 'readonly'
    comboBox_genero.current(0)
    comboBox_genero.grid(row=1, column=1, padx=10,  pady=4)
    
    label_duracion = ttk.Label(frame_secundario, width=23, background='lightgreen', text="Duracion aprox: ")
    label_duracion.grid(row=2, column=0, pady=4)

    input_duracion = ttk.Entry(frame_secundario, width=23, name="input_duracion")
    input_duracion.grid(row=2, column=1, pady=4)

    frame_botonSubir = ttk.Frame(frame_seleccion)
    frame_botonSubir.grid(row=1, column=0)

    boton_subir = ttk.Button(frame_botonSubir, text="Subir", cursor='circle')
    boton_subir.bind("<Button-1>", lambda e: subirArchivo(comboBox_genero, input_duracion) )
    boton_subir.grid(row=0, column=0, pady=10)

    boton_atras = ttk.Button(frame_seleccion,text="Atrás", name="btn_atras_subirArchivo")
    boton_atras.grid(row=2, column=0, sticky="W")
    boton_atras.bind("<Button-1>", atras)


def VentanaStreaming(atras, filtrarVideos):

    frame_streaming = ttk.Frame(padding=10, name="frame_streaming", cursor="star")

    frame_filtro = ttk.Frame(frame_streaming, name="frame_filtro", padding=2, width=15)
    frame_filtro.grid(row=0, column=0)

    lbl_filtrar = ttk.Label(frame_filtro, text="Filtrar por: ", padding=4,  background="lightblue", width=12)
    lbl_filtrar.grid(row=0, column=0, pady=1)

    comboBox = ttk.Combobox(frame_filtro, background="lightyellow")
    comboBox['values'] = ('Nombre', 'Genero', 'Duracion', 'Fecha')
    comboBox['state'] = 'readonly'
    comboBox.current(0)
    comboBox.grid(row=0, column=1, padx=4)

    lbl_valor_filtrar = ttk.Label(frame_filtro, text="Valor: ", padding=4, background="lightblue", width=12)
    lbl_valor_filtrar.grid(row=1, column=0, pady=1)

    in_busqueda = ttk.Entry(frame_filtro, width=23)
    in_busqueda.grid(row=1, column=1)

    btn_filtrar = ttk.Button(frame_filtro, text="Filtrar")
    btn_filtrar.grid(row=2, column=1)
    btn_filtrar.bind('<Button-1>', lambda e: filtrarVideos(comboBox, in_busqueda))
    
    frame_encabezado = ttk.Frame(frame_streaming,padding=10, name="frame_encabezado", cursor="spider")
    frame_encabezado.grid(row=0, column=1)

    lbl_TotalVideos = ttk.Label(frame_encabezado, text="Videos disponibles en el servidor", foreground="white", background="blue", font=20)
    lbl_TotalVideos.grid(row=0, column=0)

    frame_archivos = ttk.Frame(frame_encabezado, name="frame_archivos")
    frame_archivos.grid(row=1, column=0)
    
    boton_atras = ttk.Button(frame_filtro,text="Atrás", name="btn_atras_streaming")
    boton_atras.grid(row=3, column=0, sticky="W")
    boton_atras.bind("<Button-1>", atras)

    return frame_streaming

def VentanaIngresoIPyPort():
    
    frame_ventana = ttk.Frame()

    frame_labels = ttk.Frame(frame_ventana, name="frm1")
    frame_labels.grid(row=0, column=0)

    label_IP = ttk.Label(frame_labels, text="IP Servidor", background="red", foreground="white")
    label_IP.grid(row=0, column=0, padx=3)

    label_PORT = ttk.Label(frame_labels, text="PORT Servidor", background="red", foreground="white")
    label_PORT.grid(row=0, column=1, padx=3)

    input_IP = ttk.Entry(frame_labels, name="entry_ip")
    input_IP.grid(row=1, column=0, padx=3)

    input_PORT = ttk.Entry(frame_labels, name="entry_port")
    input_PORT.grid(row=1, column=1, padx=3)

    frameBTN = ttk.Frame(frame_ventana, name="frm2")
    frameBTN.grid(row=1, column=0)
    btn_OK = ttk.Button(frameBTN, text="Aceptar", name="btn_ok")
    btn_OK.grid(row=0, column=0)
    
    return frame_ventana