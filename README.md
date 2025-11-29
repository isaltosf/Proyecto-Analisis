# Gestor de Codificación de Cadenas

Aplicación de escritorio en Python (Tkinter) para **codificar y decodificar** cadenas numéricas.  
Permite trabajar tanto con **matrículas ESPOL** como con **cadenas genéricas**, soportando ingreso manual y procesamiento mediante archivos `.txt`.

---

## 🧩 Funcionalidades

- **Codificación**
  - Modo **Matrícula ESPOL**:
    - Valida el formato de la matrícula (`20XXXXXXXX`) y evita 4 dígitos repetidos consecutivos.
    - Aplica un algoritmo de codificación “clásico” que genera:
      - Una cadena codificada.
      - Una clave asociada para poder decodificarla.
  - Modo **Cadena genérica**:
    - Codifica mediante **XOR** usando una **clave alfabética en minúsculas**.
    - La misma función permite codificar y decodificar (XOR reversible).

- **Decodificación**
  - Manual:
    - Matrícula: espera el formato `cadena_codificada|k1,k2,k3,...`.
    - Cadena XOR: recibe la cadena codificada y la clave usada.
  - Desde archivo:
    - Selección de un archivo `.txt` con líneas codificadas.
    - Genera un nuevo archivo con las cadenas **decodificadas**.
    - Informa cuántas líneas fueron válidas y cuántas se marcaron como inválidas.

- **Manejo de archivos**
  - Carga masiva de archivos `.txt` para **codificación**.
  - Validación de extensión: solo se aceptan archivos `.txt`.
  - Guardado automático de archivos de salida con sufijo (por ejemplo `_out`).
  
- **Interfaz gráfica (Tkinter)**
  - Menú principal con:
    - Ingreso Manual (codificar).
    - Carga de Archivos (codificar).
    - Decodificación Manual.
    - Decodificación desde Archivo.
  - Campos que aparecen/desaparecen según el modo (matrícula/cadena, codificar/decodificar).
  - Copia automática de la cadena codificada al portapapeles en el modo manual.

---

## 📁 Estructura del proyecto

Archivos principales (los nombres pueden variar según tu repositorio):

- `main.py` → Ventana principal (`AppMatriculas`) y lógica de la interfaz.
- `codificacion.py` → Algoritmos de codificación (clásico).
- `decodificacion.py` → Algoritmos de decodificación (clásico).
- `algoritmos.py` → Función `procesarXOR` y otros auxiliares.
- `contextoCodificar.py` → Implementación del patrón Strategy para codificar.
- `contextoDecodificar.py` → Implementación del patrón Strategy para decodificar.
- `utils.py` → Utilidades (por ejemplo, `es_matricula_valida`, etc.).
- `archivos.py` → Funciones para leer y escribir archivos (`leer_lineas_archivo`, `guardar_archivo_salida`, etc.).

> Ajusta los nombres en esta sección según cómo tengas organizados tus módulos.

---

## 🔧 Requisitos

- **Python 3.8+** (recomendado)
- Módulos de la biblioteca estándar:
  - `tkinter`
  - `os`
  - `re`
  - `abc`
- No se requieren librerías externas adicionales.

---

## ▶️ Cómo ejecutar el programa

1. **Clonar el repositorio**
2. **Ejecutar la aplicación**
   ```bash
    python frames.py
