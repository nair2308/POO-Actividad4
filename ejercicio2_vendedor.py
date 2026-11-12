import tkinter as tk
from tkinter import ttk


class Vendedor:
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = None

    def verificar_edad(self, edad):
        if edad < 0 or edad > 120:
            raise ValueError("La edad no puede ser negativa ni mayor a 120.")
        if edad < 18:
            raise ValueError("El vendedor debe ser mayor de 18 años.")
        self.edad = edad

    def imprimir(self):
        return (f"Nombre del vendedor = {self.nombre}\n"
                f"Apellidos del vendedor = {self.apellidos}\n"
                f"Edad del vendedor = {self.edad}")


class VentanaVendedor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 6.5 - Vendedor")
        self.geometry("460x400")
        self.minsize(420, 380)
        self._crear_widgets()

    def _crear_widgets(self):
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Registro de vendedor",
                  font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2,
                                                   sticky="w", pady=(0, 10))

        self.var_nombre = tk.StringVar()
        self.var_apellidos = tk.StringVar()
        self.var_edad = tk.StringVar()

        for fila, (texto, variable) in enumerate(
                (("Nombre:", self.var_nombre),
                 ("Apellidos:", self.var_apellidos),
                 ("Edad:", self.var_edad)), start=1):
            ttk.Label(marco, text=texto).grid(row=fila, column=0, sticky="w", pady=4)
            ttk.Entry(marco, textvariable=variable, width=32).grid(
                row=fila, column=1, sticky="ew", pady=4, padx=(8, 0))

        botones = ttk.Frame(marco)
        botones.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)
        ttk.Button(botones, text="Crear vendedor",
                   command=self.crear_vendedor).pack(side="left")
        ttk.Button(botones, text="Limpiar",
                   command=self.limpiar).pack(side="left", padx=6)

        self.estado = tk.Label(marco, text="", wraplength=400, justify="left",
                               anchor="w")
        self.estado.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.salida = tk.Text(marco, height=5, state="disabled",
                              font=("Courier New", 11))
        self.salida.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(8, 0))

        marco.columnconfigure(1, weight=1)
        marco.rowconfigure(6, weight=1)

    def _leer_edad(self):
        try:
            return int(self.var_edad.get().strip())
        except ValueError:
            raise ValueError("La edad debe ser un número entero.") from None

    def _mostrar_salida(self, texto):
        self.salida.config(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.insert("1.0", texto)
        self.salida.config(state="disabled")

    def crear_vendedor(self):
        nombre = self.var_nombre.get().strip()
        apellidos = self.var_apellidos.get().strip()
        try:
            if not nombre or not apellidos:
                raise ValueError("El nombre y los apellidos son obligatorios.")
            vendedor = Vendedor(nombre, apellidos)
            vendedor.verificar_edad(self._leer_edad())
        except ValueError as error:
            self.estado.config(text=f"Error: {error}", fg="red")
            self._mostrar_salida("")
        else:
            self.estado.config(text="Vendedor creado correctamente.", fg="green")
            self._mostrar_salida(vendedor.imprimir())

    def limpiar(self):
        for variable in (self.var_nombre, self.var_apellidos, self.var_edad):
            variable.set("")
        self.estado.config(text="")
        self._mostrar_salida("")


def main():
    VentanaVendedor().mainloop()


if __name__ == "__main__":
    main()
