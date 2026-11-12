import math
import tkinter as tk
from tkinter import ttk


class CalculosNumericos:
    @staticmethod
    def logaritmo_neperiano(valor):
        if valor <= 0:
            raise ArithmeticError("El valor debe ser un número positivo")
        return math.log(valor)

    @staticmethod
    def raiz_cuadrada(valor):
        if valor < 0:
            raise ArithmeticError("El valor debe ser un número positivo")
        return math.sqrt(valor)


class VentanaCalculos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 6.6 - Cálculos numéricos")
        self.geometry("500x330")
        self.minsize(460, 300)
        self._crear_widgets()

    def _crear_widgets(self):
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Logaritmo neperiano y raíz cuadrada",
                  font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 10))

        fila = ttk.Frame(marco)
        fila.pack(fill="x")
        ttk.Label(fila, text="Valor numérico =").pack(side="left")
        self.var_valor = tk.StringVar()
        entrada = ttk.Entry(fila, textvariable=self.var_valor, width=20)
        entrada.pack(side="left", padx=8)
        entrada.bind("<Return>", lambda evento: self.calcular())
        ttk.Button(fila, text="Calcular", command=self.calcular).pack(side="left")
        ttk.Button(fila, text="Limpiar", command=self.limpiar).pack(side="left", padx=6)

        self.lbl_log = tk.Label(marco, text="", anchor="w", justify="left",
                                wraplength=450)
        self.lbl_log.pack(fill="x", pady=(18, 4))
        self.lbl_raiz = tk.Label(marco, text="", anchor="w", justify="left",
                                 wraplength=450)
        self.lbl_raiz.pack(fill="x", pady=4)

    def _leer_valor(self):
        texto = self.var_valor.get().strip().replace(",", ".")
        valor = float(texto)
        if not math.isfinite(valor):
            raise ValueError("Valor no finito")
        return valor

    def _calcular(self, funcion, nombre, etiqueta):
        try:
            valor = self._leer_valor()
            resultado = funcion(valor)
            etiqueta.config(text=f"{nombre} = {resultado:.6g}", fg="green")
        except ArithmeticError:
            etiqueta.config(
                text=f"El valor debe ser un número positivo para calcular {nombre.lower()}",
                fg="red")
        except ValueError:
            etiqueta.config(
                text=f"El valor debe ser numérico para calcular {nombre.lower()}",
                fg="red")

    def calcular(self):
        self._calcular(CalculosNumericos.logaritmo_neperiano,
                       "Logaritmo neperiano", self.lbl_log)
        self._calcular(CalculosNumericos.raiz_cuadrada,
                       "Raíz cuadrada", self.lbl_raiz)

    def limpiar(self):
        self.var_valor.set("")
        self.lbl_log.config(text="")
        self.lbl_raiz.config(text="")


def main():
    VentanaCalculos().mainloop()


if __name__ == "__main__":
    main()
