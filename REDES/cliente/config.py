from tkinter import ttk
import tkinter as tk


root = tk.Tk()
root.title("VENTANA DE PRUEBA")
root.minsize(width=600, height=380)
root.config(background='lightblue')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.configure(cursor='heart')

serv_ftp = None
nombreArchivo = ""
band = False

