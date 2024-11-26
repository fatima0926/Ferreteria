import tkinter as tk
import sqlite3 
from tkinter import ttk, messagebox
from base_datos import buscar_por_categoria, buscar_por_nombre, agregar_producto, ruta_bd

class CatalogoFerreteria():
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Catálogo de Ferretería")
        self.ventana.geometry("1365x750")
        self.ventana.config(bg="#f4f4f9")
        global app
        app = self

        # Título
        self.titulo = tk.Label(ventana, text="Catálogo de Ferretería La Nueva", font=("Helvetica", 20), bg="#4CAF50", fg="white", pady=10)
        self.titulo.pack(fill=tk.X)

        # Marco principal del programa 
        self.main_frame = tk.Frame(ventana, bg="#f4f4f9")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Cuadro principal  para categorías
        self.categorias = tk.Frame(self.main_frame, bg="#e0e0e0", width=250)
        self.categorias.pack(side=tk.LEFT, fill=tk.Y)

        # Scroll para categorías (parte del frame)
        self.canvas = tk.Canvas(self.categorias, bg="#e0e0e0")
        self.scrollbar = ttk.Scrollbar(self.categorias, orient="vertical", command=self.canvas.yview)
        self.cuadro_categorias = tk.Frame(self.canvas, bg="#e0e0e0")

        self.cuadro_categorias.bind(
            "<Configure>", #EVENTOS
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.cuadro_categorias, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Listado de categorías
        tk.Label(self.cuadro_categorias, text="Categorías", font=("Arial", 14), bg="#e0e0e0").pack(pady=10, padx=30)
        self.categorias = [
            'Automotriz', 'Fontanería', 'Jardín y exteriores', 'Lámparas e iluminación', 'Limpieza',
            'Muebles y organización', 'Pinturas', 'Pisos y cerámica', 'Seguridad hogar y oficina',
            'Herramientas y protecciones', 'Ferretería', 'Baños', 'Cerrajería', 'Cocina', 'Climatización',
            'Decoración', 'Construcción', 'Electrodomésticos', 'Electricidad', 'Navidad'
        ]

        self.boton_categoria = {}
        for categoria in self.categorias:
            btn = tk.Button(self.cuadro_categorias, text=categoria, width=45, command=lambda c=categoria: self.mostrar_categoria(c))
            btn.pack(pady=5, padx=30)
            btn.bind('<Enter>', lambda e, c=categoria: self.sombrear_categoria(e, c))#Eventos para los sombreados 
            btn.bind('<Leave>', lambda e, c=categoria: self.desombrear_categoria(e, c))
            self.boton_categoria[categoria] = btn

        # Área de búsqueda       
        self.cuadro_busqueda = tk.Frame(self.main_frame, bg="#f4f4f9")
        self.cuadro_busqueda.pack(fill=tk.X, pady=10)

        tk.Label(self.cuadro_busqueda, text="Buscar producto:", font=("Arial", 14), bg="#f4f4f9").pack(side=tk.LEFT, padx=10)
        self.entrada_produc = tk.Entry(self.cuadro_busqueda, font=("Arial", 12), width=40)
        self.entrada_produc.pack(side=tk.LEFT)

        self.entrada_produc.bind("<Return>", self.buscar_producto_evento)#EVENTO PARA BUSCAR UN PORDUCTO BPE
        tk.Button(self.cuadro_busqueda, text="Buscar", command=self.buscar_producto).pack(side=tk.LEFT, padx=10)

        # Botón de iniciar sesión
        self.inicio_session = tk.Button(self.cuadro_busqueda, text="Iniciar sesión", font=("Arial", 12), command=self.iniciar_sesion)
        self.inicio_session.pack(side=tk.LEFT, padx=10)

        # Área de productos
        self.frame_productos = tk.Frame(self.main_frame, bg="#f4f4f9")
        self.frame_productos.pack(fill=tk.BOTH, expand=True)

        # Cuadro principal para mostrar productos 
        self.canvas2 = tk.Canvas(self.frame_productos, bg="#f4f4f9")
        self.scrollbar2 = ttk.Scrollbar(self.frame_productos, orient="vertical", command=self.canvas2.yview)
        self.cuadro_mostrar_prod = tk.Frame(self.canvas2, bg="#f4f4f9")

        self.cuadro_mostrar_prod.bind(
            "<Configure>", #EVENTO
            lambda e: self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))
        )

        self.canvas2.create_window((0, 0), window=self.cuadro_mostrar_prod, anchor="nw")
        self.canvas2.configure(yscrollcommand=self.scrollbar2.set)

        self.canvas2.pack(side="left", fill="both", expand=True)
        self.scrollbar2.pack(side="right", fill="y")

        # Variable de categoría seleccionada
        self.categoria_seleccionada = None

        # Muestra que el usuario no esta logeado 
        self.logged_in = False

    def sombrear_categoria(self, event, categoria):#Eventos para sombreados 
        self.boton_categoria[categoria].config(bg="#a5d6a7")

    def desombrear_categoria(self, event, categoria):#eventos sombreados 
        if categoria != self.categoria_seleccionada:
            self.boton_categoria[categoria].config(bg="#e0e0e0")
    
    def mostrar_categoria(self, categoria):
        self.categoria_seleccionada = categoria
        # Reinicia el sombreado de todas las categorías
        for btn in self.boton_categoria.values():
            btn.config(bg="#e0e0e0") #color de los label 
        
        # Sombrear la categoría seleccionada
        self.boton_categoria[categoria].config(bg="#a5d6a7")

        productos = buscar_por_categoria(categoria)
        self.mostrar_productos(productos, f"Productos en la categoría: {categoria}")

    def buscar_producto(self):
        busqueda = self.entrada_produc.get().strip()
        if not busqueda:
            messagebox.showwarning("Advertencia", "Ingrese un nombre de producto para buscar.")
            return
        
        productos = buscar_por_nombre(busqueda)
        
        if productos:
            self.mostrar_productos(productos, f"Resultados de búsqueda para: {busqueda}")
        else:
            # Si no se encuentran productos, mostrar mensaje de error
            messagebox.showerror("Producto no encontrado", "No se encontraron productos con ese nombre.")

    def buscar_producto_evento(self, event):#BPE 
        """Método para buscar un producto al presionar Enter."""
        self.buscar_producto()#BPE


    def mostrar_productos(self, productos, encabezado):
        # Limpiar los productos anteriores
        for widget in self.cuadro_mostrar_prod.winfo_children():
            widget.destroy()

        # Mostrar el encabezado
        tk.Label(self.cuadro_mostrar_prod, text=encabezado, font=("Arial", 14, "bold"), bg="#f4f4f9").pack(pady=10)

        if self.logged_in:
            # Si está logueado, mostrar botón de agregar producto
            tk.Button(self.cuadro_mostrar_prod, 
                     text="Agregar Producto",
                     command=lambda: agregar_producto(self.categoria_seleccionada)).pack(pady=10)

        # Crear frame para la tabla
        tabla_frame = tk.Frame(self.cuadro_mostrar_prod, bg="#f4f4f9")
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Encabezados de columna
        if self.logged_in:
            encabezados = ['Nombre', 'Precio']  # Si está logueado solo Nombre y Precio
        else:
            encabezados = ['Nombre', 'Descripción', 'Precio']  # Si no está logueado, mostrar también Descripción

        # Crear encabezados
        for i, header in enumerate(encabezados):
            tk.Label(tabla_frame, text=header, font=("Arial", 12, "bold"), 
                    bg="#e0e0e0", width=20).grid(row=0, column=i, padx=2, pady=5)

        # Mostrar productos
        for i, producto in enumerate(productos, start=1):
            # Mostrar nombre                                    #Alineacion 
            tk.Label(tabla_frame, text=producto[1], width=45, anchor='w').grid(row=i, column=0, padx=2, pady=2)
            # Mostrar descripción solo si no está logueado
            if not self.logged_in:
                tk.Label(tabla_frame, text=producto[2], wraplength=250, justify=tk.LEFT, anchor='w',height=2).grid(row=i, column=1, padx=2, pady=2, sticky="w")

                # Precio se coloca en la siguiente columna (columna 2)
                tk.Label(tabla_frame, text=f"${producto[3]:.2f}", width=10).grid(row=i, column=2, padx=2, pady=2)
            else:
                # Si está logueado, el precio va en la columna 1 (al lado de nombre)
                tk.Label(tabla_frame, text=f"${producto[3]:.2f}", width=20).grid(row=i, column=1, padx=2, pady=2)


            if self.logged_in:
                # Botones de modificar y eliminar
                btn_frame = tk.Frame(tabla_frame, bg="#f4f4f9")
                btn_frame.grid(row=i, column=4, padx=5, pady=2)

                tk.Button(btn_frame, text="Modificar", 
                         command=lambda p=producto: self.abrir_ventana_modificar(p)).pack(side=tk.LEFT, padx=2)
                tk.Button(btn_frame, text="Eliminar", 
                         command=lambda p=producto[0]: self.confirmar_eliminar(p)).pack(side=tk.LEFT, padx=2)
        
    def abrir_ventana_modificar(self, producto):
        ventana_modificar = tk.Toplevel(self.ventana)
        ventana_modificar.title("Modificar Producto")
        ventana_modificar.geometry("400x300")
        ventana_modificar.transient(self.ventana)
        ventana_modificar.grab_set()

        # Campos para modificar
        tk.Label(ventana_modificar, text="Código:").pack(pady=5)
        codigo_entry = tk.Entry(ventana_modificar)
        codigo_entry.insert(0, producto[0])
        codigo_entry.config(state='readonly')
        codigo_entry.pack(pady=5)

        tk.Label(ventana_modificar, text="Nombre:").pack(pady=5)
        nombre_entry = tk.Entry(ventana_modificar)
        nombre_entry.insert(0, producto[1])
        nombre_entry.pack(pady=5)

        tk.Label(ventana_modificar, text="Descripción:").pack(pady=5)
        descripcion_entry = tk.Entry(ventana_modificar)
        descripcion_entry.insert(0, producto[2])
        descripcion_entry.pack(pady=5)

        tk.Label(ventana_modificar, text="Precio:").pack(pady=5)
        precio_entry = tk.Entry(ventana_modificar)
        precio_entry.insert(0, str(producto[3]))
        precio_entry.pack(pady=5)


        def guardar_cambios():
                    try:
                        precio = float(precio_entry.get())
                        conn = sqlite3.connect(ruta_db)
                        cursor = conn.cursor()
                        cursor.execute('''UPDATE productos 
                                        SET nombre = ?, descripcion = ?, precio = ?
                                        WHERE codigo = ?''', 
                                    (nombre_entry.get(), descripcion_entry.get(), precio, producto[0]))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Éxito", "Producto modificado correctamente")
                        ventana_modificar.destroy()
                        self.mostrar_categoria(self.categoria_seleccionada)
                        # Actualizar la categoría después de agregar el producto
                        self.mostrar_categoria(self.categoria_seleccionada)
                    except ValueError:
                        messagebox.showerror("Error", "El precio debe ser un número válido")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error al modificar el producto: {str(e)}")


                tk.Button(ventana_modificar, text="Guardar cambios", command=guardar_cambios).pack(pady=20)

    def confirmar_eliminar(self, codigo):
        if messagebox.askyesno("Confirmar eliminación", 
                            "¿Está seguro de que desea eliminar este producto?"):
            conn = sqlite3.connect(ruta_db)
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM productos WHERE codigo = ?', (codigo,))
                conn.commit()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                # Actualizar la categoría después de eliminar el producto
                self.mostrar_categoria(self.categoria_seleccionada)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al eliminar el producto: {str(e)}")
            finally:
                conn.close()
            # Actualizar la categoría después de eliminar el producto
            self.mostrar_categoria(self.categoria_seleccionada)

    def iniciar_sesion(self):
        self.ventana_login = tk.Toplevel(self.root)
        self.ventana_login.title("Iniciar sesión")
        self.ventana_login.geometry("300x250")  # Aumenté un poco la altura
        self.ventana_login.transient(self.root)
        self.ventana_login.grab_set()

        # Centrar la ventana
        self.ventana_login.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50))

        # Frame principal
        main_frame = tk.Frame(self.ventana_login, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Usuario
        tk.Label(main_frame, text="Usuario:", font=("Arial", 12)).pack(pady=5)
        self.usuario_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.usuario_entry.pack(fill=tk.X, pady=5)

        # Contraseña
        tk.Label(main_frame, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
        self.contraseña_entry = tk.Entry(main_frame, show="*", font=("Arial", 12))
        self.contraseña_entry.pack(fill=tk.X, pady=5)

        # Frame para botones
        botones_frame = tk.Frame(main_frame)
        botones_frame.pack(pady=20)

        # Botón de login
        tk.Button(botones_frame, text="Iniciar sesión", 
                command=self.validar_login,
                font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # Botón de cancelar
        tk.Button(botones_frame, text="Cancelar", 
                command=self.ventana_login.destroy,
                font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # Vincular la tecla Enter
        self.usuario_entry.bind('<Return>', lambda e: self.contraseña_entry.focus())
        self.contraseña_entry.bind('<Return>', lambda e: self.validar_login())

    def validar_login(self):
        usuario = self.usuario_entry.get().strip()
        contraseña = self.contraseña_entry.get().strip()

        if usuario and contraseña:
            # Consulta a la base de datos para verificar las credenciales
            conn = sqlite3.connect(ruta_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
            usuario_valido = cursor.fetchone()
            conn.close()

            if usuario_valido:
                self.logged_in = True
                self.ventana_login.destroy()
                self.login_button.config(text="Cerrar sesión", command=self.cerrar_sesion)
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                if self.categoria_seleccionada:
                    self.mostrar_categoria(self.categoria_seleccionada)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                self.contraseña_entry.delete(0, tk.END)
                self.contraseña_entry.focus()

    def cerrar_sesion(self):
        self.logged_in = False
        self.login_button.config(text="Iniciar sesión", command=self.iniciar_sesion)
        self.mostrar_categoria(self.categoria_seleccionada)
        messagebox.showinfo("Cerrado sesión", "Sesión cerrada exitosamente.")
                
        for categoria in self.categorias:
            btn = tk.Button(self.scrollable_frame, text=categoria, width=45, command=lambda c=categoria: self.mostrar_categoria(c))

class VentanaInicio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catálogo de Ferretería V1.01")
        self.geometry("10000x10000")

        # Logo de la empresa
        self.logo = PhotoImage(file=r"C:\Users\MINEDUCYT\Desktop\Proyecto_Progra\Proyecto_Progra\logo_empresa.png")  
        tk.Label(self, image=self.logo).pack(pady=20)

        # Mensaje de bienvenida
        tk.Label(self, text="Bienvenido al Catálogo de Ferretería La Nueva", font=("Helvetica", 18), pady=20).pack()

        # Botón para acceder al catálogo
        tk.Button(self, text="Ingresar al Programa", font=("Arial", 14), command=self.ver_catalogo, bg="#4CAF50", fg="white").pack(pady=20)

    def ver_catalogo(self):
        # Cerrar la ventana de inicio y mostrar la ventana del catálogo
        self.destroy()
        root = tk.Tk()
        global app
        app = CatalogoFerreteriaApp(root)
        root.mainloop()

#Inicia la ventana principal
app = VentanaInicio() 
app.mainloop()



