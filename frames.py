import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from codificacion import *
from decodificacion import *
from contextoCodificar import *
from contextoDecodificar import *
from utils import *
from archivos import *
import os

class AppMatriculas:
    def __init__(self,root):
        self.root = root  #Self sirve para poder modificar la ventana creada en cualquier función
        self.root.title("Gestor de codificación")
        self.root.geometry("400x400")
        self.root.resizable(False,False)
        self.root.configure(bg="#f0f4f8")
        
        self.configurar_estilos()
        #intercambio de pantallas
        self.contenedor = tk.Frame(self.root, bg="#f0f4f8")
        self.contenedor.pack(fill= "both", expand=True, padx=15, pady=15)
        #Variable para almacenar los archivos seleccionados
        #usamos self para que la lista sobreviva durante toda la ejecución sin depender solo de la función

        self.tipo_entrada = tk.StringVar()
        self.tipo_entrada.set("matricula")  # valor por defecto
        
        self.frame_inicio = None
        self.frame_manual = None
        self.frame_archivos = None
        self.pagina_actual = None
        self.archivo_decodificar = None
        self.archivos_seleccionados = [] #lista de los archivos
        self.matricula_guardada = ""
        
        #Se llama a la función que dibuja los botones y textos
        self.frame_inicio = self.crear_pagina_inicio()
        self.frame_manual = self.crear_pagina_manual()
        self.frame_archivos = self.crear_pagina_archivos()
        self.frame_manual_decodificar = self.crear_pagina_manual_decodificar()
        self.frame_archivo_decodificar = self.crear_pagina_archivo_decodificar()
        
        self.ir_a_inicio()       
    
    
    def ir_a_inicio(self):
        self.mostrar_pagina(self.frame_inicio)

    def ir_a_manual(self):
        self.mostrar_pagina(self.frame_manual)

    def ir_a_archivos(self):
        self.mostrar_pagina(self.frame_archivos)
    
    def ir_a_manual_decodificar(self):
        self.mostrar_pagina(self.frame_manual_decodificar)
    
    def ir_a_archivo_decodificar(self):
        self.mostrar_pagina(self.frame_archivo_decodificar)



    def mostrar_pagina(self, frame_destino):
        """ Oculta la página actual y muestra la nueva """
        if self.pagina_actual is not None:
            self.pagina_actual.pack_forget() # Ocultar anterior
        
        frame_destino.pack(fill="both", expand=True) # Mostrar nueva
        self.pagina_actual = frame_destino

        if frame_destino == self.frame_manual:
            self.actualizar_campos_manual()
        elif frame_destino == self.frame_archivos:
            self.actualizar_campos_archivos()
        elif frame_destino == self.frame_manual_decodificar:
            self.actualizar_campos_manual_decodificar()
        elif frame_destino == self.frame_archivo_decodificar:  
            self.actualizar_campos_archivo_decodificar()
    
    
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
        
        ttk.Label(frame, text="Sistema de Codificación de Cadenas", style="Header.TLabel").pack(pady=(15,5))
        ttk.Label(frame, text="¿Qué desea procesar?").pack(pady=(0, 15))

        # RadioButtons para elegir el tipo de dato
        rb_matricula = ttk.Radiobutton(
            frame,
            text="Matrículas",
            value="matricula",
            variable=self.tipo_entrada,
            command=self.on_tipo_entrada_cambiado 
        )
        rb_matricula.pack(anchor="w", padx=20, pady=(2, 0))

        rb_cadena = ttk.Radiobutton(
            frame,
            text="Cadenas numéricas",
            value="cadena",
            variable=self.tipo_entrada,
            command=self.on_tipo_entrada_cambiado
        )
        rb_cadena.pack(anchor="w", padx=20, pady=(0, 10))

        btn_manual = ttk.Button(frame, text="✍️ Ingreso Manual", style="Manual.BigBtn.TButton",
                                command=self.ir_a_manual)
        btn_manual.pack(pady=10, padx=40)

        btn_files = ttk.Button(frame, text="📁 Carga de Archivos", style="File.BigBtn.TButton",
                               command=self.ir_a_archivos)
        btn_files.pack(pady=5, padx=40)

        btn_manual_dec = ttk.Button(
            frame, text="🔓 Decodificar Manual", style="Manual.BigBtn.TButton",
            command=self.ir_a_manual_decodificar
        )
        btn_manual_dec.pack(pady=10, padx=40)

        btn_archivo_dec = ttk.Button(
            frame, text="📄 Decodificar desde archivo", style="File.BigBtn.TButton",
            command=self.ir_a_archivo_decodificar
        )
        btn_archivo_dec.pack(pady=5, padx=40)


        
        return frame

    def on_tipo_entrada_cambiado(self):
        # Si estamos en la página manual, actualizamos los campos visibles
        if self.pagina_actual == self.frame_manual:
            self.actualizar_campos_manual()
        elif self.pagina_actual == self.frame_archivos:
            self.actualizar_campos_archivos()
        elif self.pagina_actual == self.frame_manual_decodificar:
            self.actualizar_campos_manual_decodificar()
        elif self.pagina_actual == self.frame_archivo_decodificar:  # 👈 NUEVO
            self.actualizar_campos_archivo_decodificar()


    def crear_pagina_manual(self):
        frame = ttk.Frame(self.contenedor)
        
        btn_volver = ttk.Button(frame, text="⬅ Volver", style="Back.TButton",
                                command=self.ir_a_inicio)
        btn_volver.pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="Ingreso Manual", style="Header.TLabel").pack(pady=5)
        ttk.Label(frame, text="Cadena numérica (solo dígitos)").pack(pady=(10, 0))
        self.entry_manual = ttk.Entry(frame, font=("Consolas", 12), justify='center')
        self.entry_manual.pack(pady=10, ipady=3)

        #ttk.Label(frame, text="Clave", style="Header.TLabel").pack(pady=5)
        self.label_clave = ttk.Label(frame, text="Clave de codificación (solo letras minúsculas)")
        self.entry_clave = ttk.Entry(frame, font=("Consolas", 12), justify='center')

        ttk.Button(frame, text="PROCESAR", style="Action.TButton",
                   command=self.procesar_manual).pack(pady=16, fill="x", padx=80)

        return frame
    
    def actualizar_campos_manual(self):
        tipo = self.tipo_entrada.get()

        if tipo == "cadena":
            # Siempre intentamos mostrarlos
            self.label_clave.pack(pady=(10, 0))
            self.entry_clave.pack(pady=10, ipady=3)
        else:
            # Siempre intentamos ocultarlos
            self.label_clave.pack_forget()
            self.entry_clave.pack_forget()


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

        self.label_clave_arch = ttk.Label(frame, text="Clave de codificación (solo letras minúsculas)")
        self.entry_clave_arch = ttk.Entry(frame, font=("Consolas", 12), justify='center')

        # 3. Botón Procesar (Al final)
        ttk.Button(frame, text="PROCESAR ARCHIVOS", style="Action.TButton",
                   command=self.procesar_archivos).pack(fill="x", padx=60)

        return frame
    

    
    def actualizar_campos_archivos(self):
        tipo = self.tipo_entrada.get()

        if tipo == "cadena":
            self.label_clave_arch.pack(pady=(5, 0))
            self.entry_clave_arch.pack(pady=10, ipady=3)
        else:
            self.label_clave_arch.pack_forget()
            self.entry_clave_arch.pack_forget()

    def crear_pagina_manual_decodificar(self):
        frame = ttk.Frame(self.contenedor)

        btn_volver = ttk.Button(frame, text="⬅ Volver", style="Back.TButton",
                                command=self.ir_a_inicio)
        btn_volver.pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="Decodificación Manual", style="Header.TLabel").pack(pady=5)
        ttk.Label(frame, text="Cadena codificada en el formato correspondiente").pack(pady=(10, 0))

        self.entry_manual_dec = ttk.Entry(frame, font=("Consolas", 12), justify='center')
        self.entry_manual_dec.pack(pady=10, ipady=3)

        self.label_clave_dec = ttk.Label(frame, text="Clave de decodificación (solo letras minúsculas)")
        self.entry_clave_dec = ttk.Entry(frame, font=("Consolas", 12), justify='center')

        ttk.Button(frame, text="DECODIFICAR", style="Action.TButton",
                command=self.procesar_manual_decodificar).pack(pady=16, fill="x", padx=80)

        return frame
    
    def actualizar_campos_manual_decodificar(self):
        tipo = self.tipo_entrada.get()

        if tipo == "cadena":
            self.label_clave_dec.pack(pady=(10, 0))
            self.entry_clave_dec.pack(pady=10, ipady=3)
        else:
            self.label_clave_dec.pack_forget()
            self.entry_clave_dec.pack_forget()
    
    def crear_pagina_archivo_decodificar(self):
        frame = ttk.Frame(self.contenedor)

        btn_volver = ttk.Button(
            frame, text="⬅ Volver", style="Back.TButton",
            command=self.ir_a_inicio
        )
        btn_volver.pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="Decodificación desde archivo", style="Header.TLabel").pack(pady=5)

        # Mostrar ruta del archivo seleccionado
        ttk.Label(frame, text="Archivo .txt a decodificar:").pack(pady=(5, 0))
        self.label_archivo_dec = ttk.Label(frame, text="Ningún archivo seleccionado")
        self.label_archivo_dec.pack(pady=(0, 10))

        btn_sel_arch = ttk.Button(
            frame, text="Seleccionar archivo",
            command=self.cargar_archivo_decodificar_dialog
        )
        btn_sel_arch.pack(pady=(0, 10))

        # Clave para XOR cuando tipo == "cadena"
        self.label_clave_arch_dec = ttk.Label(frame, text="Clave de decodificación (solo letras minúsculas)")
        self.entry_clave_arch_dec = ttk.Entry(frame, font=("Consolas", 12), justify='center')

        ttk.Button(
            frame, text="DECODIFICAR ARCHIVO", style="Action.TButton",
            command=self.procesar_archivo_decodificar
        ).pack(pady=16, fill="x", padx=60)

        return frame
    
    def actualizar_campos_archivo_decodificar(self):
        tipo = self.tipo_entrada.get()

        if tipo == "cadena":
            self.label_clave_arch_dec.pack(pady=(5, 0))
            self.entry_clave_arch_dec.pack(pady=10, ipady=3)
        else:
            self.label_clave_arch_dec.pack_forget()
            self.entry_clave_arch_dec.pack_forget()
    
    def cargar_archivo_decodificar_dialog(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo a decodificar")

        if not ruta:
            return  # usuario canceló

        extension = os.path.splitext(ruta)[1].lower()
        if extension != ".txt":
            messagebox.showwarning(
                "Archivo inválido",
                f"El archivo '{os.path.basename(ruta)}' no es un archivo .txt\n"
                "Por favor seleccione solamente archivos de texto."
            )
            return

        self.archivo_decodificar = ruta
        self.label_archivo_dec.config(text=os.path.basename(ruta))


    def cargar_archivos_dialog(self):
        rutas = filedialog.askopenfilenames(title="Seleccionar archivos")
        for ruta in rutas:
            extension = os.path.splitext(ruta)[1].lower()
            if extension != ".txt":
                messagebox.showwarning(
                    "Archivo inválido",
                    f"El archivo '{os.path.basename(ruta)}' no es un archivo .txt\n"
                    "Por favor seleccione solamente archivos de texto."
                )
                continue  # NO agregarlo

            if ruta not in self.archivos_seleccionados:
                self.archivos_seleccionados.append(ruta)
                self.lista_archivos.insert(tk.END, os.path.basename(ruta))

    def limpiar_lista(self):
        self.archivos_seleccionados = []
        self.lista_archivos.delete(0, tk.END)

    def procesar_manual(self):
        dato = self.entry_manual.get().strip()
        tipo = self.tipo_entrada.get()

        if not dato:
            messagebox.showwarning("Atención", "El campo de cadena está vacío.")
            return

        if not dato.isdigit():
            messagebox.showwarning("Atención", "La cadena debe contener solo dígitos.")
            return
        
        self.matricula_guardada = dato

        if tipo == "matricula":
            
            if not es_matricula_valida(self.matricula_guardada):
                messagebox.showwarning("Atención", "La matrícula ingresada no tiene el formato correcto (formato ESPOL).")
                return

            estrategia = CodificarClasico()
        else:  # tipo == "cadena"
            clave = self.entry_clave.get().strip()

            if not clave:
                messagebox.showwarning("Atención", "Debe ingresar una clave para codificar con XOR.")
                return
            
            if not clave.islower() or not clave.isalpha():
                messagebox.showwarning("Atención", "La clave para la codificación solo debe contener letras minúsculas")
                return
            
            estrategia = CodificarXOR(clave)

        contexto = ContextoCodificar(estrategia)
        self.cadenaCodificada = contexto.ejecutar(dato)

        self.root.clipboard_clear()
        self.root.clipboard_append(self.cadenaCodificada)
        self.root.update()

        messagebox.showinfo(
            "OK",
            f"Tipo seleccionado: {tipo}\nCadena codificada: {self.cadenaCodificada}\nLa cadena fue copiada en su portapapeles, puede pegarla en cualquier lado."
        )
        
    def procesar_archivos(self):
        tipo = self.tipo_entrada.get()
        if len(self.archivos_seleccionados) == 0:
            messagebox.showwarning("Atención", "No ha seleccionado archivos para la carga masiva.")
            return


        # Si es XOR, necesitamos clave
        if tipo == "cadena":
            clave = self.entry_clave_arch.get().strip()

            if not clave:
                messagebox.showwarning("Atención", "Debe ingresar una clave para codificar con XOR.")
                return

            if not clave.islower() or not clave.isalpha():
                messagebox.showwarning("Atención", "La clave debe contener solo letras minúsculas.")
                return

            estrategia = CodificarXOR(clave)

        else:  # tipo == matricula
            estrategia = CodificarClasico()

        contexto = ContextoCodificar(estrategia)

        # Resumen
        total_archivos = 0
        total_lineas = 0
        total_invalidas = 0
        archivos_generados = []

        for archivo in self.archivos_seleccionados:

            total_archivos += 1

            lineas = leer_lineas_archivo(archivo)
            nuevas, invalidas = procesar_lineas(lineas, tipo, contexto)

            total_lineas += len(lineas)
            total_invalidas += len(invalidas)

            nuevo_path = guardar_archivo_salida(archivo, nuevas)
            archivos_generados.append(nuevo_path)

        # Mostrar resultados
        messagebox.showinfo(
            "Proceso completado",
            f"Archivos procesados: {total_archivos}\n"
            f"Líneas totales: {total_lineas}\n"
            f"Líneas inválidas: {total_invalidas}\n\n"
            f"Archivos generados:\n" + "\n".join(archivos_generados)
        )
    
    def procesar_manual_decodificar(self):
        dato = self.entry_manual_dec.get().strip()
        tipo = self.tipo_entrada.get()

        if not dato:
            messagebox.showwarning("Atención", "El campo de cadena codificada está vacío.")
            return

        # MATRÍCULA -> decodificación clásica
        if tipo == "matricula":
            # Esperamos formato: <cadena>|<k1,k2,k3,...>
            if "|" not in dato:
                messagebox.showwarning(
                    "Atención",
                    "La cadena codificada no tiene el formato esperado: parte_codificada|k1,k2,k3,..."
                )
                return

            partes = dato.split("|")
            if len(partes) != 2:
                messagebox.showwarning(
                    "Atención",
                    "La cadena codificada no tiene el formato correcto (debe contener una sola barra |)."
                )
                return

            cadena_codificada = partes[0]
            key_str = partes[1]

            key_list = key_str.split(",")  # lista de strings, igual que en tu ejemplo

            estrategia = DecodificarClasico()
            contexto = ContextoDecodificar(estrategia)

            try:
                resultado = contexto.ejecutar(cadena_codificada, key_list)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al decodificar: {e}")
                return

            messagebox.showinfo("Decodificación completada", f"Cadena original:\n{resultado}")

        # CADENA NUMÉRICA -> XOR
        else:  # tipo == "cadena"
            clave = self.entry_clave_dec.get().strip()

            if not clave:
                messagebox.showwarning("Atención", "Debe ingresar una clave para decodificar con XOR.")
                return

            if not clave.islower() or not clave.isalpha():
                messagebox.showwarning(
                    "Atención",
                    "La clave para la decodificación XOR solo debe contener letras minúsculas."
                )
                return

            estrategia = DecodificarXOR()
            contexto = ContextoDecodificar(estrategia)

            try:
                resultado = contexto.ejecutar(dato, clave)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al decodificar: {e}")
                return

            messagebox.showinfo("Decodificación completada", f"Cadena original:\n{resultado}")

    def procesar_archivo_decodificar(self):
        tipo = self.tipo_entrada.get()

        if not self.archivo_decodificar:
            messagebox.showwarning("Atención", "No ha seleccionado un archivo para decodificar.")
            return

        # Preparar estrategia según el tipo
        if tipo == "cadena":
            clave = self.entry_clave_arch_dec.get().strip()

            if not clave:
                messagebox.showwarning("Atención", "Debe ingresar una clave para decodificar con XOR.")
                return

            if not clave.islower() or not clave.isalpha():
                messagebox.showwarning(
                    "Atención",
                    "La clave para la decodificación XOR solo debe contener letras minúsculas."
                )
                return

            estrategia = DecodificarXOR()
            contexto = ContextoDecodificar(estrategia)

        else:  # tipo == "matricula"
            estrategia = DecodificarClasico()
            contexto = ContextoDecodificar(estrategia)

        # Leer líneas del archivo
        lineas = leer_lineas_archivo(self.archivo_decodificar)

        nuevas = []
        invalidas = []

        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue  # saltar vacías

            try:
                if tipo == "matricula":
                    # esperamos: cadena|k1,k2,k3,...
                    if "|" not in linea:
                        invalidas.append(linea)
                        continue

                    partes = linea.split("|")
                    if len(partes) != 2:
                        invalidas.append(linea)
                        continue

                    cadena_codificada = partes[0]
                    key_str = partes[1]
                    key_list = key_str.split(",")

                    original = contexto.ejecutar(cadena_codificada, key_list)
                else:
                    # XOR: cada línea es una cadena codificada con la misma clave
                    original = contexto.ejecutar(linea, clave)

                nuevas.append(original)
            except Exception:
                invalidas.append(linea)

        if not nuevas:
            messagebox.showwarning(
                "Sin resultados",
                "No se pudo decodificar ninguna línea válida del archivo. Por favor verifique el formato de su archivo de acuerdo al modo de codificación seleccionado."
            )
            return

        # Guardar archivo de salida (reutilizamos tu helper)
        nuevo_path = guardar_archivo_salida(self.archivo_decodificar, nuevas)

        messagebox.showinfo(
            "Decodificación completada",
            f"Archivo de entrada: {os.path.basename(self.archivo_decodificar)}\n"
            f"Líneas leídas: {len(lineas)}\n"
            f"Líneas decodificadas: {len(nuevas)}\n"
            f"Líneas inválidas: {len(invalidas)}\n\n"
            f"Archivo generado:\n{nuevo_path}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMatriculas(root)
    root.mainloop()