import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class AppMatriculas:
    def __init__(self,root):
        self.root = root  #Self sirve para poder modificar la ventana creada en cualquier función
        self.root.title("Gestor de matriculas")
        self.root.geometry("400x350")
        self.root.resizable(False,False)
        self.root.configure(bg="#f0f4f8")
        
        self.configurar_estilos()
        #intercambio de pantallas
        self.contenedor= tk.Frame(self.root, bg="#f0f4f8")
        self.contenedor.pack(fill= "both", expand=True, padx=15, pady=15)
        #Variable para almacenar los archivos seleccionados
        #usamos self para que la lista sobreviva durante toda la ejecución sin depender solo de la función
        
        self.frame_inicio = None
        self.frame_manual = None
        self.frame_archivos = None
        self.pagina_actual = None
        self.archivos_seleccionados = []
        
        #Se llama a la función que dibuja los botones y textos
        self.frame_inicio = self.crear_pagina_inicio()
        self.frame_manual = self.crear_pagina_manual()
        self.frame_archivos = self.crear_pagina_archivos()
        
        
        self.ir_a_inicio()       
    
    
    def ir_a_inicio(self):
        self.mostrar_pagina(self.frame_inicio)

    def ir_a_manual(self):
        self.mostrar_pagina(self.frame_manual)

    def ir_a_archivos(self):
        self.mostrar_pagina(self.frame_archivos)

    def mostrar_pagina(self, frame_destino):
        """ Oculta la página actual y muestra la nueva """
        if self.pagina_actual is not None:
            self.pagina_actual.pack_forget() # Ocultar anterior
        
        frame_destino.pack(fill="both", expand=True) # Mostrar nueva
        self.pagina_actual = frame_destino
    
    #Interfaz
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        bg_color = "#f0f4f8"
        azul = "#3498db"
        verde = "#27ae60"
        naranja = "#e67e22"
        gris_oscuro = "#2c3e50"
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"), foreground=gris_oscuro)
        
        # Botones del Menú
        style.configure("Manual.BigBtn.TButton", font=("Segoe UI", 10, "bold"), background=azul, foreground="white")
        style.configure("File.BigBtn.TButton", font=("Segoe UI", 10, "bold"), background=verde, foreground="white")
        
        # Botón Volver (Gris)
        style.configure("Back.TButton", font=("Segoe UI", 8), background="#7f8c8d", foreground="white", borderwidth=0)
        
        # Botón Acción
        style.configure("Action.TButton", font=("Segoe UI", 9, "bold"), background=naranja, foreground="white")
        
        # Efectos Hover (ratón encima)
        style.map("Manual.BigBtn.TButton", background=[('active', '#2980b9')])
        style.map("File.BigBtn.TButton", background=[('active', '#219653')])
        style.map("Back.TButton", background=[('active', '#95a5a6')])


    def crear_pagina_inicio(self):
        frame = ttk.Frame(self.contenedor)
        
        ttk.Label(frame, text="Sistema de Matrículas", style="Header.TLabel").pack(pady=(15,5))
        ttk.Label(frame, text="Seleccione una opción:").pack(pady=(0, 15))

        btn_manual = ttk.Button(frame, text="✍️ Ingreso Manual", style="Manual.BigBtn.TButton",
                                command=self.ir_a_manual)
        btn_manual.pack(pady=5, padx=40)

        btn_files = ttk.Button(frame, text="📁 Carga de Archivos", style="File.BigBtn.TButton",
                               command=self.ir_a_archivos)
        btn_files.pack(pady=5, padx=40)
        
        return frame

    def crear_pagina_manual(self):
        frame = ttk.Frame(self.contenedor)
        
        btn_volver = ttk.Button(frame, text="⬅ Volver", style="Back.TButton",
                                command=self.ir_a_inicio)
        btn_volver.pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="Ingreso Manual", style="Header.TLabel").pack(pady=5)
        
        self.entry_manual = ttk.Entry(frame, font=("Consolas", 12), justify='center')
        self.entry_manual.pack(pady=10, ipady=3)

        ttk.Button(frame, text="PROCESAR", style="Action.TButton",
                   command=self.procesar_manual).pack(pady=16, fill="x", padx=80)

        return frame

    def crear_pagina_archivos(self):
        frame = ttk.Frame(self.contenedor)
        
        btn_volver = ttk.Button(frame, text="⬅ Volver", style="Back.TButton",
                                command=self.ir_a_inicio)
        btn_volver.pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="Carga Masiva", style="Header.TLabel").pack(pady=(0,10))

        self.lista_archivos = tk.Listbox(frame, width= 45, height=6, bd=0, highlightthickness=1)
        self.lista_archivos.pack(pady=(0,10))

        # Botones laterales de la lista
        frame_btns = tk.Frame(frame, bg="#f0f4f8")
        frame_btns.pack(pady=(0,15))
        
        btn_add = ttk.Button(frame_btns, text="Agregar archivos", command=self.cargar_archivos_dialog)
        btn_add.pack(side="left", padx=5) # padx separa los botones entre sí
        
        # Botón Eliminar (Texto completo)
        btn_del = ttk.Button(frame_btns, text="Limpiar lista", command=self.limpiar_lista)
        btn_del.pack(side="left", padx=5)

        # 3. Botón Procesar (Al final)
        ttk.Button(frame, text="PROCESAR ARCHIVOS", style="Action.TButton",
                   command=self.procesar_archivos).pack(fill="x", padx=60)

        return frame


    def cargar_archivos_dialog(self):
        rutas = filedialog.askopenfilenames(title="Seleccionar archivos")
        for ruta in rutas:
            if ruta not in self.archivos_seleccionados:
                self.archivos_seleccionados.append(ruta)
                self.lista_archivos.insert(tk.END, os.path.basename(ruta))

    def limpiar_lista(self):
        self.archivos_seleccionados = []
        self.lista_archivos.delete(0, tk.END)

    def procesar_manual(self):
        dato = self.entry_manual.get()
        if dato:
            self.enviar_backend("manual", dato)
            messagebox.showinfo("OK", f"Enviado: {dato}")

    def procesar_archivos(self):
        if self.archivos_seleccionados:
            self.enviar_backend("archivos", self.archivos_seleccionados)
            messagebox.showinfo("OK", "Archivos enviados")

    def enviar_backend(self, tipo, datos):
        print(f"Enviando al backend -> Tipo: {tipo} | Datos: {datos}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMatriculas(root)
    root.mainloop()