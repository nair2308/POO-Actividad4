import io
import tkinter as tk
from tkinter import filedialog, ttk


class LeerArchivo:
    def __init__(self, nombre_archivo="prueba.txt"):
        self.nombre_archivo = nombre_archivo

    def leer(self, convertir_mayusculas=False):
        for codificacion in ("utf-8-sig", "latin-1"):
            try:
                return self._leer_con(codificacion, convertir_mayusculas)
            except UnicodeDecodeError:
                continue
        return []

    def _leer_con(self, codificacion, convertir_mayusculas):
        archivo = open(self.nombre_archivo, "rb")
        try:
            conversor = io.TextIOWrapper(archivo, encoding=codificacion)
            lineas = []
            linea = conversor.readline()
            while linea != "":
                linea = linea.rstrip("\r\n")
                lineas.append(linea.upper() if convertir_mayusculas else linea)
                linea = conversor.readline()
            return lineas
        finally:
            archivo.close()


class VentanaLeerArchivo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 6.8 - Lectura de archivos")
        self.geometry("620x480")
        self.minsize(560, 420)
        self._crear_widgets()

    def _crear_widgets(self):
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Lectura de un archivo de texto",
                  font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 10))

        fila = ttk.Frame(marco)
        fila.pack(fill="x")
        ttk.Label(fila, text="Archivo:").pack(side="left")
        self.var_ruta = tk.StringVar(value="prueba.txt")
        ttk.Entry(fila, textvariable=self.var_ruta).pack(
            side="left", fill="x", expand=True, padx=8)
        ttk.Button(fila, text="Examinar…", command=self.examinar).pack(side="left")

        opciones = ttk.Frame(marco)
        opciones.pack(fill="x", pady=8)
        self.var_mayusculas = tk.BooleanVar(value=False)
        ttk.Button(opciones, text="Leer archivo",
                   command=self.leer_archivo).pack(side="left")
        ttk.Button(opciones, text="Crear prueba.txt de ejemplo",
                   command=self.crear_ejemplo).pack(side="left", padx=6)
        ttk.Checkbutton(opciones, text="Mostrar en MAYÚSCULAS",
                        variable=self.var_mayusculas).pack(side="left", padx=6)

        contenedor = ttk.Frame(marco)
        contenedor.pack(fill="both", expand=True)
        self.salida = tk.Text(contenedor, state="disabled", wrap="word",
                              font=("Courier New", 11))
        barra = ttk.Scrollbar(contenedor, command=self.salida.yview)
        self.salida.config(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.salida.pack(side="left", fill="both", expand=True)

        self.estado = tk.Label(marco, text="", anchor="w", justify="left",
                               wraplength=570)
        self.estado.pack(fill="x", pady=(8, 0))

    def _mostrar(self, texto):
        self.salida.config(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.insert("1.0", texto)
        self.salida.config(state="disabled")

    def examinar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccione un archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if ruta:
            self.var_ruta.set(ruta)
            self.leer_archivo()

    def leer_archivo(self):
        ruta = self.var_ruta.get().strip()
        try:
            lineas = LeerArchivo(ruta).leer(self.var_mayusculas.get())
        except OSError:
            self._mostrar("")
            self.estado.config(text="No se pudo leer el archivo.", fg="red")
            return
        self._mostrar("\n".join(lineas))
        self.estado.config(text=f"Archivo leído correctamente: {len(lineas)} línea(s).",
                           fg="green")

    def crear_ejemplo(self):
        try:
            with open("prueba.txt", "w", encoding="utf-8") as archivo:
                for numero in range(1, 6):
                    archivo.write(f"Línea {numero}\n")
        except OSError:
            self.estado.config(text="No se pudo crear el archivo de ejemplo.", fg="red")
            return
        self.var_ruta.set("prueba.txt")
        self.estado.config(text="Se creó prueba.txt en la carpeta del programa.",
                           fg="green")


def main():
    VentanaLeerArchivo().mainloop()


if __name__ == "__main__":
    main()
