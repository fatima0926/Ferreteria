import tkinter as tk
from tkinter import PhotoImage
from clase_principal import CatalogoFerreteria

class VentanaInicio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catálogo de Ferretería V1.01")
        self.geometry("1365x750")

        # Logo de la empresa
        self.logo = PhotoImage(file=r"C:\Users\MINEDUCYT\Documents\UES\Ciclo II - 2024\Programación I\Computo IV\Catalogo_ferreteria ejemplo\Proyecto_Progra\logo_empresa.png")  
        tk.Label(self, image=self.logo).pack(pady=20)

        # Mensaje de bienvenida
        tk.Label(self, text="Bienvenido al Catálogo de Ferretería La Nueva", font=("Helvetica", 18)).pack(pady=20)

        # Botón para acceder al catálogo
        tk.Button(self, text="Ingresar al Programa", font=("Arial", 14), command=self.ver_catalogo, bg="#4CAF50", fg="white").pack(pady=20)

    def ver_catalogo(self):
        # Cerrar la ventana de inicio y mostrar la ventana del catálogo
        self.destroy()
        ventana_inicio = tk.Tk()
        global app
        app= CatalogoFerreteria(ventana_inicio)
        ventana_inicio.mainloop()

