import tkinter as tk
from tkinter import ttk


class PruebaExcepciones:
    def ejecutar(self):
        salida = []

        try:
            salida.append("Ingresando al primer try")
            cociente = 10000 / 0
            salida.append("Después de la división")
        except ZeroDivisionError:
            salida.append("División por cero")
        finally:
            salida.append("Ingresando al primer finally")

        try:
            salida.append("Ingresando al segundo try")
            objeto = None
            objeto.upper()
            salida.append("Imprimiendo objeto")
        except ZeroDivisionError:
            salida.append("División por cero")
        except Exception:
            salida.append("Ocurrió una excepción")
        finally:
            salida.append("Ingresando al segundo finally")

        return salida


class VentanaPruebaExcepciones(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 6.4 - Prueba de excepciones")
        self.geometry("540x430")
        self.minsize(480, 380)
        self.prueba = PruebaExcepciones()
        self._crear_widgets()

    def _crear_widgets(self):
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill="both", expand=True)

        ttk.Label(
            marco,
            text="Prueba de excepciones (try / except / finally)",
            font=("Arial", 13, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            marco,
            text="Pulse «Ejecutar» para correr los dos bloques try y ver "
                 "qué se imprime en pantalla.",
            wraplength=490,
        ).pack(anchor="w", pady=(4, 10))

        botones = ttk.Frame(marco)
        botones.pack(fill="x")
        ttk.Button(botones, text="Ejecutar", command=self.ejecutar).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=6)

        self.salida = tk.Text(marco, height=14, state="disabled",
                              font=("Courier New", 11), wrap="word")
        self.salida.pack(fill="both", expand=True, pady=(10, 0))

    def _mostrar(self, texto):
        self.salida.config(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.insert("1.0", texto)
        self.salida.config(state="disabled")

    def ejecutar(self):
        mensajes = self.prueba.ejecutar()
        self._mostrar("\n".join(mensajes))

    def limpiar(self):
        self._mostrar("")


def main():
    VentanaPruebaExcepciones().mainloop()


if __name__ == "__main__":
    main()
