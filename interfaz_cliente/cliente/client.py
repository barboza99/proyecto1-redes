from ftplib import FTP, all_errors
import tkinter as tk
from tkinter import Label, Widget, ttk, messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from pyparsing import col
from conexionFTP import iniciarSesion
import Ventanas
from config import serv_ftp
from config import band
from config import nombreArchivo
from config import root

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
    
    labelVideo = ttk.Label(master=ventanaStreaming, text="Aquí va el video")
    #img = ImageTk.PhotoImage(Image.open("interfaz_cliente/cliente/kakashi.jpg"))
    #labelVideo.config(image=img)
    labelVideo.grid(row=0, column=1)
   

    for widget in ventanaStreaming.winfo_children():
        if  widget.winfo_name() == "frame_encabezado":
            for w in widget.winfo_children():
                if w.winfo_name() == "frame_archivos":
                    frame_archs = w
                    break
            break

    #serv_ftp.dir()
    #print(serv_ftp.getresp())
    archivos = serv_ftp.nlst()
    fila = 0
    hayArchivos = False
    for archivo in archivos:
        if archivo.endswith(".mp4"):
            hayArchivos = True
            contenedor = ttk.Frame(frame_archs, name= str(fila))
            contenedor.grid(row=fila, column=0)
            boton = ttk.Button(contenedor, name=str(fila), text="Reproducir")
            boton.bind('<Button-1>', manejador)
            lbl = ttk.Label(contenedor, text=archivo, background="lightgreen")
            lbl.grid(row=0, column=0, pady=2)
            boton.grid(row=0, column=1, pady=2, padx=2)
            fila += 1;

    if not hayArchivos:
        lbl = ttk.Label(frame_archs, text="No hay videos para mostrar")
        lbl.grid(row=1, column=0)

    
    ventanaStreaming.grid(row=0, column=0)

def manejador(e):
    print(e.widget.winfo_name())

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
    root.mainloop()

