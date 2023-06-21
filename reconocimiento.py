import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import cv2
import mysql.connector
import datetime
import numpy as np
import sqlite3

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
 
# Capturar video de la cámara
video_capture = cv2.VideoCapture(0)
# Configurar el tamaño de la ventana
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
 


def registro_camara():
    while True:
    # Leer el video fotograma a fotograma
        ret, frame = video_capture.read()

    # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en la imagen en escala de grises
        faces = face_cascade.detectMultiScale(gray, 1.6, 10)

    # Dibujar rectángulos alrededor de las caras detectadas y mostrar las coordenadas x, y y las dimensiones
        for (x, y, w, h) in faces:
        # Dibujar un rectángulo alrededor de la cara detectada
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Mostrar las coordenadas x, y y las dimensiones de la cara detectada
            cv2.putText(frame, f"x: {x}px, y: {y}px, w: {w}px, h: {h}px", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostrar el video en una ventana
            cv2.imshow('Video', frame)

    # Salir del programa si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberar la cámara y cerrar la ventana
    video_capture.release()
    cv2.destroyAllWindows() 

    pass

def registros():
    #Formulario
    # Conectar a la base de datos
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="reconocimiento_facial"
    )

    # Crear una tabla si no existe
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
    codigo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    X VARCHAR(255),
    Y VARCHAR(255),
    W VARCHAR(255),
    h VARCHAR(255)
    )
    """)

    class Application(Frame):
        def __init__(self, master=None):
            super().__init__(master)
            self.master = master
            self.master.title("Registro de datos")
            self.pack()
            self.create_widgets()
        def create_widgets(self):
            self.nombre_label = Label(self, text="Nombre:")
            self.nombre_label.grid(row=0, column=0)
            self.nombre_entry = Entry(self)
            self.nombre_entry.grid(row=0, column=1)
            
            self.x_label = Label(self, text="X:")
            self.x_label.grid(row=1, column=0)
            self.x_entry = Entry(self)
            self.x_entry.grid(row=1, column=1)

            self.y_label = Label(self, text="Y:")
            self.y_label.grid(row=2, column=0)
            self.y_entry = Entry(self)
            self.y_entry.grid(row=2, column=1)

            self.w_label = Label(self, text="W:")
            self.w_label.grid(row=3, column=0)
            self.w_entry = Entry(self)
            self.w_entry.grid(row=3, column=1)

            self.h_label = Label(self, text="Z:")
            self.h_label.grid(row=4, column=0)
            self.h_entry = Entry(self)
            self.h_entry.grid(row=4, column=1)

            self.submit_button = Button(self, text="Enviar", command=self.submit)
            self.submit_button.grid(row=5, column=1)

        def submit(self):
            nombre = self.nombre_entry.get()
            x = self.x_entry.get()
            y = self.y_entry.get()
            w = self.w_entry.get()
            H = self.h_entry.get()

            cursor = db.cursor()
            cursor.execute("""
            INSERT INTO personas (nombre, X, Y, W, H)
            VALUES (%s, %s, %s, %s, %s)
            """, (nombre, x, y, w, H))
            db.commit()

            self.nombre_entry.delete(0, END)
            self.x_entry.delete(0, END)
            self.y_entry.delete(0, END)
            self.w_entry.delete(0, END)
            self.h_entry.delete(0, END)

    root = Tk()
    app = Application(master=root)
    app.mainloop()
    
    pass

def reconocimiento():
    # Código para la funcionalidad del botón de reconocimiento
    pass


def informes():
        # Conectar con la base de datos
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="reconocimiento_facial"
    )

    # Crear una nueva ventana de Tkinter
    informes_window = tk.Toplevel()
    informes_window.title("Informes")

    # Crear un combobox para seleccionar el nombre de la persona
    nombres = []
    cursor = db.cursor()
    cursor.execute("SELECT nombre FROM personas")
    for nombre in cursor:
        nombres.append(nombre[0])
    cursor.close()

    nombre_var = tk.StringVar()
    nombre_combobox = ttk.Combobox(informes_window, textvariable=nombre_var, values=nombres)
    nombre_combobox.grid(column=0, row=0, padx=10, pady=10)

    # Crear una tabla para mostrar los registros
    registros_table = ttk.Treeview(informes_window)
    registros_table["columns"] = ("codigo", "nombre", "fecha", "hora", "anotacion")
    registros_table.column("#0", width=0, stretch=tk.NO)
    registros_table.column("codigo", anchor=tk.CENTER, width=100)
    registros_table.column("nombre", anchor=tk.CENTER, width=100)
    registros_table.column("fecha", anchor=tk.CENTER, width=100)
    registros_table.column("hora", anchor=tk.CENTER, width=100)
    registros_table.column("anotacion", anchor=tk.CENTER, width=200)
    registros_table.heading("codigo", text="Código")
    registros_table.heading("nombre", text="Nombre")
    registros_table.heading("fecha", text="Fecha")
    registros_table.heading("hora", text="Hora")
    registros_table.heading("anotacion", text="Anotación")
    registros_table.grid(column=0, row=1, padx=10, pady=10)

    # Función para cargar los registros en la tabla
    def cargar_registros():
        cursor = db.cursor()
        cursor.execute("""
            SELECT registros.codigo, personas.nombre, registros.fecha, registros.hora, registros.anotacion
            FROM registros
            INNER JOIN personas ON registros.codigo = personas.codigo
            WHERE personas.nombre = %s
        """, (nombre_var.get(),))
        registros = cursor.fetchall()
        registros_table.delete(*registros_table.get_children())
        for registro in registros:
            registros_table.insert("", tk.END, values=registro)
        cursor.close()

    # Cargar registros al iniciar la ventana
    cargar_registros()

    # Crear un botón para cargar los registros en la tabla
    cargar_registros_button = tk.Button(informes_window, text="Cargar registros", command=cargar_registros)
    cargar_registros_button.grid(column=0, row=2, padx=10, pady=10)

    # Ejecutar el bucle principal de Tkinter para la ventana de informes
    informes_window.mainloop()
    pass









# Crear ventana principal
root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")
root.geometry("500x300")
root.configure(background='#F5F5F5')

# Crear botones
registro_camara_btn = tk.Button(root, text="Registro de Persona Camara", font=("Helvetica", 18), bg='#4CAF50', fg='#FFFFFF', bd=0, pady=20)
registro_camara_btn.config(command=registro_camara)
registros_btn = tk.Button(root, text="Registro de Persona", font=("Helvetica", 18), bg='#4CAF50', fg='#FFFFFF', bd=0, pady=20)
registros_btn.config(command=registros)
reconocimiento_btn = tk.Button(root, text="Reconocimiento de Persona", font=("Helvetica", 18), bg='#2196F3', fg='#FFFFFF', bd=0, pady=20)
reconocimiento_btn.config(command=reconocimiento)
informes_btn = tk.Button(root, text="Mostrar registros", font=("Helvetica", 18), bg='#9C27B0', fg='#FFFFFF', bd=0, pady=20)
informes_btn.config(command=informes)


# Agregar botones a la ventana
registro_camara_btn.pack(fill='both', padx=40)
registros_btn.pack(fill='both', padx=40)
reconocimiento_btn.pack(fill='both', padx=40)
informes_btn.pack(fill='both', padx=40, pady=(0, 20))

# Mostrar ventana
root.mainloop()