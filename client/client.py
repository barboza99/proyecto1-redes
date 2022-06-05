import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from  tkvideo  import  tkvideo 

root = tk.Tk()
root.title("VENTANA DE PRUEBA")
root.minsize(width=600, height=380)
frame_seleccion = ttk.Frame(root, padding=10)
frame_seleccion.grid()
lbl = ttk.Label(frame_seleccion)
lbl.grid(row=1, column=0)
lbl_video = ttk.Label(frame_seleccion)
lbl_video.grid(row=2, column=0)

label_seleccion = ttk.Label(frame_seleccion, text='Seleccione un archivo')
label_seleccion.grid(row=0, column=0, sticky=tk.E)

def seleccionarVideo(e):
    filetypes = (
        ('Video Files', '*.mp4'),
        ('Others', '.mkv'),
        ('All Files', '.*')
    )
    video = fd.askopenfile( mode='r',filetypes=filetypes, title="Elegir un video")

    if video is not None:
        name = video.name.split('/')[-1];
        label_seleccion.config(text=name)

boton_seleccion = ttk.Button(frame_seleccion, text="Seleccionar" ,cursor='spider')
boton_seleccion.grid(row=0, column=1, padx=10)
boton_seleccion.bind('<Button-1>', seleccionarVideo)
boton_subir = ttk.Button(frame_seleccion, text="Subir", cursor='circle')
boton_subir.grid(row=3, column=0)

root.mainloop()

