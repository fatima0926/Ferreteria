# FALTA LA PARTE DE LAS IMPORTACIONES Y LA CLASE


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



