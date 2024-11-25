import sqlite3
import tkinter as tk 
from tkinter import messagebox
import random
import string
from clase_pricipal import *

# Ruta a la base de datos
ruta_bd = r"C:\Users\MINEDUCYT\Documents\UES\Ciclo II - 2024\Programación I\Computo IV\Catalogo_ferreteria ejemplo\Proyecto_Progra\catalogo_ferretero.db"

# Función para buscar productos por categoría
def buscar_por_categoria(categoria):
    conectar = sqlite3.connect(ruta_bd)
    cursor = conectar.cursor()
    cursor.execute('SELECT * FROM productos WHERE categoria = ?', (categoria,))
    productos = cursor.fetchall()
    conectar.close()
    return productos

# Función para buscar productos por nombre
def buscar_por_nombre(nombre):
    conectar = sqlite3.connect(ruta_bd)
    cursor = conectar.cursor()
    cursor.execute('SELECT * FROM productos WHERE nombre LIKE ?', ('%' + nombre + '%',))
    productos = cursor.fetchall()
    conectar.close()
    return productos

# Función para generar un código aleatorio
def generar_codigo_aleatorio():
    longitud_codigo = 7
    # Generar un código aleatorio que consiste en letras y dígitos
    codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=longitud_codigo))
    return codigo

# Función para agregar un producto
def agregar_producto(categoria):
    # Crear una nueva ventana para agregar un producto
    agregar_ventana = tk.Toplevel()
    agregar_ventana.title(f"Agregar producto a {categoria}")
    agregar_ventana.geometry("400x300")

    # Generar un código aleatorio y mostrarlo en la entrada
    codigo_aleatorio = generar_codigo_aleatorio()

    # Campos para ingresar los detalles del nuevo producto
    tk.Label(agregar_ventana, text="Código:").pack(pady=5)
    codigo_entrada = tk.Entry(agregar_ventana, width=30)
    codigo_entrada.insert(0, codigo_aleatorio)  # Insertar el código aleatorio
    codigo_entrada.config(state='readonly')  
    codigo_entrada.pack(pady=5)

    tk.Label(agregar_ventana, text="Nombre:").pack(pady=5)
    nombre_entrada = tk.Entry(agregar_ventana, width=30)
    nombre_entrada.pack(pady=5)

    tk.Label(agregar_ventana, text="Descripción:").pack(pady=5)
    descripcion_entrada = tk.Entry(agregar_ventana, width=30)
    descripcion_entrada.pack(pady=5)

    tk.Label(agregar_ventana, text="Precio:").pack(pady=5)
    precio_entry = tk.Entry(agregar_ventana, width=30)
    precio_entry.pack(pady=5)
    

    # Función para guardar el producto
    def guardar_producto():
        codigo = codigo_entrada.get()
        nombre = nombre_entrada.get()
        descripcion = descripcion_entrada.get()
        try:
            precio = float(precio_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return
        
        conn = sqlite3.connect(ruta_bd)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO productos (codigo, nombre, descripcion, precio, categoria)
                          VALUES (?, ?, ?, ?, ?)''', (codigo, nombre, descripcion, precio, categoria))
        conn.commit()
        conn.close()

        
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        agregar_ventana.destroy()

        # Actualizar la categoría inmediatamente después de agregar el producto
        app.mostrar_categoria(categoria)

    # Botón para guardar el nuevo producto
    tk.Button(agregar_ventana, text="Agregar Producto", command=guardar_producto).pack(pady=20)

# Función para modificar un producto
def modificar_producto(codigo):
    # Obtener los datos del producto seleccionado
    conn = sqlite3.connect(ruta_bd)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE codigo = ?', (codigo,))
    producto = cursor.fetchone()
    conn.close()

    if not producto:
        messagebox.showerror("Error", "Producto no encontrado.")
        return

    # Crear ventana de modificación
    modificar_ventana = tk.Toplevel()
    modificar_ventana.title(f"Modificar producto {producto[1]}")
    modificar_ventana.geometry("400x300")

    # Campos para modificar los detalles del producto
    tk.Label(modificar_ventana, text="Código:").pack(pady=5)
    codigo_entrada = tk.Entry(modificar_ventana, width=30)
    codigo_entrada.insert(0, producto[0])
    codigo_entrada.config(state="disabled")  # No permitir cambiar el código
    codigo_entrada.pack(pady=5)

    tk.Label(modificar_ventana, text="Nombre:").pack(pady=5)
    nombre_entrada = tk.Entry(modificar_ventana, width=30)
    nombre_entrada.insert(0, producto[1])
    nombre_entrada.pack(pady=5)

    tk.Label(modificar_ventana, text="Descripción:").pack(pady=5)
    descripcion_entrada = tk.Entry(modificar_ventana, width=30)
    descripcion_entrada.insert(0, producto[2])
    descripcion_entrada.pack(pady=5)

    tk.Label(modificar_ventana, text="Precio:").pack(pady=5)
    precio_entrada = tk.Entry(modificar_ventana, width=30)
    precio_entrada.insert(0, str(producto[3]))
    precio_entrada.pack(pady=5)

    # Función para guardar los cambios
    def guardar_modificacion():
        nombre = nombre_entrada.get()
        descripcion = descripcion_entrada.get()
        try:
            precio = float(precio_entrada.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return
        
        conn = sqlite3.connect(ruta_bd)
        cursor = conn.cursor()
        cursor.execute('''UPDATE productos SET nombre = ?, descripcion = ?, precio = ?
                          WHERE codigo = ?''', (nombre, descripcion, precio, codigo))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Producto modificado correctamente.")
        modificar_ventana.destroy()

    # Botón para guardar la modificación
    tk.Button(modificar_ventana, text="Guardar Cambios", command=guardar_modificacion).pack(pady=20)

# Función para eliminar un producto
def eliminar_producto(codigo):
    confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?")
    if confirmacion:
        conn = sqlite3.connect(ruta_bd)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE codigo = ?', (codigo,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
