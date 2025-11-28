import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class AppMatriculas:
    def __init__(self,root):
        self.root = root  #Self sirve para poder modificar la ventana creada en cualquier función
        self.root.title("Gestor de matriculas")
        self.root.geometry("500x450")
        
        #Variable para almacenar los archivos seleccionados
        #usamos self para que la lista sobreviva durante toda la ejecución sin depender solo de la función
        
        self.archivos_seleccionados = []
        
        #Se llama a la función que dibuja los botones y textos
        self.crear_widgets()
        
    #Interfaz
    def crear_widgets(self):
        #--Entrada Manual--
        #Ayudará a ajustar el recuadro con el titulo
        frame_manual = ttk.LabelFrame(self.root, text= "Entrada Manual ", padding = 10)
        frame_manual.pack(fill = "x", padx = 15, pady= 18) #organiza los elementos en la ventana
        
        lbl_instruccion = ttk.Label(frame_manual, text= "Ingrese una matricula")
        lbl_instruccion.pack(side="left", padx= 5)
        
        self.entry_matricula = ttk.Entry(frame_manual, width=20 )
        self.entry_matricula.pack(side="left", padx=5)
        
        #--Carga de archivos--
        frame_archvios = ttk.LabelFrame(self.root, text="Archivos escogidos ", padding=10)
        frame_archvios.pack(fill="both", expand=True, padx=15, pady=5)
        
        #--Botón para cargar archivos--
        btn_cargar = ttk.Button(frame_archvios, text="Seleccionar archivos", command=self.cargar_archivos)
        btn_cargar.pack(fill="x", pady=5)
        
        #--Lista visual
        self.lista_archivos = tk.Listbox(frame_archvios, height=8, selectmode = tk.EXTENDED)
        self.lista_archivos.pack(fill="both", expand=True, pady=5)
        
        #--Botón Limpiar
        btn_limpiar = ttk.Button(frame_archvios, text="Limpiar Lista", command= self.limpiar_lista)
        btn_limpiar.pack(fill="x", pady=5)
        
        #Botón principal
        self.btn_procesar = ttk.Button(self.root, text="Procesar Datos", command=self.iniciar_procesamiento)
        self.btn_procesar.pack(fill="x",padx=15, pady=15, side="bottom")
        
    def cargar_archivos(self):
        #Abrir el explorador archivos
        rutas = filedialog.askopenfile(
            title="Seleccionar archivos",
            filetypes=[("Todos","*.*"), ("Excel/CSV/Txt", "*.xlsx *.csv *.txt")])
        
        if rutas:
            for ruta in rutas:
                if ruta not in self.archivos_seleccionados:
                    self.archivos_seleccionados.append(ruta)
                    
                    nombre_archivo = os.path.basename(ruta)
                    self.lista_archivos.insert(ttk.END, nombre_archivo)
                    
                    
    def limpiar_lista(self):
        self.archivos_seleccionados = []
        self.lista_archivos.delete(0, tk.END)
        
    def iniciar_procesamiento(self):
        matricula_texto = self.entry_matricula.get().strip()
        lista_rutas = self.archivos_seleccionados
        
        if not matricula_texto and not lista_rutas:
            messagebox.showwarning("Escribe una matricula o carga un archivo")
            
        self.btn_procesar.config(state="disabled",text="Enviando...")
        self.root.upadte()
        
        try:
            # Llamamos a la función que conecta con tu código externo
            self.enviar_al_backend(matricula_texto, lista_rutas)
            
            messagebox.showinfo("Listo", "Datos enviados correctamente.")
            
            # Limpieza opcional
            self.entry_matricula.delete(0, tk.END)
            self.limpiar_lista()
            
        except Exception as error:
            messagebox.showerror("Error", f"Algo falló: {error}")
        finally:
            # Pase lo que pase, reactivamos el botón al final
            self.btn_procesar.config(state="normal", text="PROCESAR DATOS")

    # 4. CONEXIÓN CON TU BACKEND
    def enviar_al_backend(self, matricula, archivos):
        """
        Esta función recibe los datos limpios de la interfaz.
        Aquí es donde pegas tu lógica o importas tu otro script.
        """
        print("--- CONECTANDO CON BACKEND ---")
        if matricula:
            print(f"Backend recibió matrícula manual: {matricula}")
            # Ejemplo: mi_backend.buscar_matricula(matricula)
        
        if archivos:
            print(f"Backend recibió {len(archivos)} archivos para leer.")
            # Ejemplo: mi_backend.procesar_excels(archivos)


if __name__ == "__main__":
    # Creamos la ventana raíz 
    ventana_principal = tk.Tk()
    
    # Opcional: Le ponemos un tema visual moderno
    estilo = ttk.Style()
    estilo.theme_use('clam') 
    
    # "Instanciamos" nuestra clase. Aquí nace 'self'.
    mi_app = AppMatriculas(ventana_principal)
    
    # El bucle infinito que mantiene la ventana abierta esperando clics
    ventana_principal.mainloop()            
        