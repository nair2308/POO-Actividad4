import tkinter as tk
from tkinter import ttk


class EquipoLlenoError(Exception):
    pass


class Programador:
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos


class EquipoMaratonProgramacion:
    MINIMO = 2
    MAXIMO = 3

    def __init__(self, nombre_equipo, universidad, lenguaje_programacion):
        if not (nombre_equipo and universidad and lenguaje_programacion):
            raise ValueError("Nombre del equipo, universidad y lenguaje "
                             "son obligatorios.")
        self.nombre_equipo = nombre_equipo
        self.universidad = universidad
        self.lenguaje_programacion = lenguaje_programacion
        self.programadores = []

    @property
    def tamano_equipo(self):
        return len(self.programadores)

    def esta_lleno(self):
        return self.tamano_equipo == self.MAXIMO

    def tiene_minimo(self):
        return self.tamano_equipo >= self.MINIMO

    def anadir(self, programador):
        if self.esta_lleno():
            raise EquipoLlenoError("El equipo está completo. "
                                   "No se pudo agregar programador.")
        self.programadores.append(programador)

    @staticmethod
    def validar_campo(campo):
        if not campo.strip():
            raise ValueError("El campo es obligatorio.")
        for caracter in campo:
            if caracter.isdigit():
                raise ValueError("El nombre no puede tener dígitos.")
        if len(campo) >= 20:
            raise ValueError("La longitud debe ser inferior a 20 caracteres.")


class VentanaEquipo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejercicio 6.7 - Equipo de maratón de programación")
        self.geometry("560x560")
        self.minsize(520, 520)
        self.equipo = None
        self._crear_widgets()

    def _crear_widgets(self):
        marco = ttk.Frame(self, padding=15)
        marco.pack(fill="both", expand=True)

        grupo_equipo = ttk.LabelFrame(marco, text="Datos del equipo", padding=10)
        grupo_equipo.pack(fill="x")
        self.var_equipo = tk.StringVar()
        self.var_universidad = tk.StringVar()
        self.var_lenguaje = tk.StringVar()
        for fila, (texto, variable) in enumerate(
                (("Nombre del equipo:", self.var_equipo),
                 ("Universidad:", self.var_universidad),
                 ("Lenguaje de programación:", self.var_lenguaje))):
            ttk.Label(grupo_equipo, text=texto).grid(row=fila, column=0,
                                                     sticky="w", pady=3)
            ttk.Entry(grupo_equipo, textvariable=variable, width=30).grid(
                row=fila, column=1, sticky="ew", padx=(8, 0), pady=3)
        grupo_equipo.columnconfigure(1, weight=1)
        self.btn_crear = ttk.Button(grupo_equipo, text="Crear equipo",
                                    command=self.crear_equipo)
        self.btn_crear.grid(row=3, column=0, sticky="w", pady=(8, 0))

        grupo_prog = ttk.LabelFrame(marco, text="Integrantes del equipo", padding=10)
        grupo_prog.pack(fill="x", pady=(12, 0))
        self.var_nombre = tk.StringVar()
        self.var_apellidos = tk.StringVar()
        ttk.Label(grupo_prog, text="Nombre:").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(grupo_prog, textvariable=self.var_nombre, width=30).grid(
            row=0, column=1, sticky="ew", padx=(8, 0), pady=3)
        ttk.Label(grupo_prog, text="Apellidos:").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(grupo_prog, textvariable=self.var_apellidos, width=30).grid(
            row=1, column=1, sticky="ew", padx=(8, 0), pady=3)
        grupo_prog.columnconfigure(1, weight=1)
        self.btn_anadir = ttk.Button(grupo_prog, text="Añadir programador",
                                     command=self.anadir_programador,
                                     state="disabled")
        self.btn_anadir.grid(row=2, column=0, sticky="w", pady=(8, 0))

        self.tabla = ttk.Treeview(marco, columns=("nombre", "apellidos"),
                                  show="headings", height=4)
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("apellidos", text="Apellidos")
        self.tabla.pack(fill="x", pady=(12, 0))

        self.lbl_tamano = ttk.Label(marco, text="Cree un equipo para comenzar.")
        self.lbl_tamano.pack(anchor="w", pady=(8, 0))
        self.estado = tk.Label(marco, text="", wraplength=500, justify="left",
                               anchor="w")
        self.estado.pack(fill="x", pady=(4, 0))

        ttk.Button(marco, text="Reiniciar", command=self.reiniciar).pack(
            anchor="w", pady=(8, 0))

    def _actualizar_tamano(self):
        if self.equipo is None:
            self.lbl_tamano.config(text="Cree un equipo para comenzar.")
            return
        texto = (f"Equipo «{self.equipo.nombre_equipo}» - integrantes: "
                 f"{self.equipo.tamano_equipo}/{self.equipo.MAXIMO}")
        if self.equipo.esta_lleno():
            texto += " (equipo completo)"
        elif self.equipo.tiene_minimo():
            texto += " (mínimo alcanzado)"
        else:
            texto += f" (mínimo {self.equipo.MINIMO})"
        self.lbl_tamano.config(text=texto)

    def crear_equipo(self):
        try:
            self.equipo = EquipoMaratonProgramacion(
                self.var_equipo.get().strip(),
                self.var_universidad.get().strip(),
                self.var_lenguaje.get().strip())
        except ValueError as error:
            self.estado.config(text=f"Error: {error}", fg="red")
            return
        self.btn_anadir.config(state="normal")
        self.btn_crear.config(state="disabled")
        self.estado.config(text="Equipo creado. Añada sus integrantes.", fg="green")
        self._actualizar_tamano()

    def anadir_programador(self):
        nombre = self.var_nombre.get().strip()
        apellidos = self.var_apellidos.get().strip()
        try:
            EquipoMaratonProgramacion.validar_campo(nombre)
            EquipoMaratonProgramacion.validar_campo(apellidos)
            self.equipo.anadir(Programador(nombre, apellidos))
        except (ValueError, EquipoLlenoError) as error:
            self.estado.config(text=f"Error: {error}", fg="red")
            return
        self.tabla.insert("", "end", values=(nombre, apellidos))
        self.var_nombre.set("")
        self.var_apellidos.set("")
        self.estado.config(text="Programador añadido correctamente.", fg="green")
        self._actualizar_tamano()

    def reiniciar(self):
        self.equipo = None
        for variable in (self.var_equipo, self.var_universidad, self.var_lenguaje,
                         self.var_nombre, self.var_apellidos):
            variable.set("")
        self.tabla.delete(*self.tabla.get_children())
        self.btn_crear.config(state="normal")
        self.btn_anadir.config(state="disabled")
        self.estado.config(text="")
        self._actualizar_tamano()


def main():
    VentanaEquipo().mainloop()


if __name__ == "__main__":
    main()
