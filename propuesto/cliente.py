import tkinter as tk
from tkinter import ttk, messagebox
import socket
import json

TABLAS = {
    "Departamento": ["IDDpto", "Nombre", "Telefono", "Fax"],
    "Proyecto": ["IDProy", "Nombre", "Fec_Inicio", "Fec_Termino", "IDDpto"],
    "Ingeniero": ["IDIng", "Nombre", "Especialidad", "Cargo"]
}

def enviar_peticion(peticion):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("localhost", 5000))
        cliente.sendall(json.dumps(peticion).encode())
        respuesta = cliente.recv(4096).decode()
        cliente.close()
        return json.loads(respuesta)
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

class ClienteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Base de Datos")

        self.tabla_seleccionada = tk.StringVar()
        self.registros = []
        self.indice = 0
        self.campos = []

        frame_top = tk.Frame(root)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Selecciona tabla:").pack(side=tk.LEFT)
        self.combo_tabla = ttk.Combobox(frame_top, values=list(TABLAS.keys()), textvariable=self.tabla_seleccionada)
        self.combo_tabla.pack(side=tk.LEFT)
        self.combo_tabla.bind("<<ComboboxSelected>>", self.cargar_tabla)

        self.frame_campos = tk.Frame(root)
        self.frame_campos.pack(pady=10)

        self.frame_botones = tk.Frame(root)
        self.frame_botones.pack(pady=5)

        tk.Button(self.frame_botones, text="Anterior", command=self.anterior).grid(row=0, column=0)
        tk.Button(self.frame_botones, text="Siguiente", command=self.siguiente).grid(row=0, column=1)
        tk.Button(self.frame_botones, text="Insertar", command=self.insertar).grid(row=0, column=2)
        tk.Button(self.frame_botones, text="Actualizar", command=self.actualizar).grid(row=0, column=3)
        tk.Button(self.frame_botones, text="Eliminar", command=self.eliminar).grid(row=0, column=4)

        self.frame_consultas = tk.Frame(root)
        self.frame_consultas.pack(pady=10)

        tk.Label(self.frame_consultas, text="ID Departamento:").grid(row=0, column=0)
        self.id_dpto_entry = tk.Entry(self.frame_consultas)
        self.id_dpto_entry.grid(row=0, column=1)
        tk.Button(self.frame_consultas, text="Ver Proyectos", command=self.consultar_proyectos).grid(row=0, column=2)

        tk.Label(self.frame_consultas, text="ID Proyecto:").grid(row=1, column=0)
        self.id_proy_entry = tk.Entry(self.frame_consultas)
        self.id_proy_entry.grid(row=1, column=1)
        tk.Button(self.frame_consultas, text="Ver Ingenieros", command=self.consultar_ingenieros).grid(row=1, column=2)
        tk.Label(self.frame_consultas, text="Asignar Ing. a Proyecto").grid(row=2, column=0, columnspan=3)

        tk.Label(self.frame_consultas, text="ID Proyecto:").grid(row=3, column=0)
        self.id_proy_asignar_entry = tk.Entry(self.frame_consultas)
        self.id_proy_asignar_entry.grid(row=3, column=1)

        tk.Label(self.frame_consultas, text="ID Ingeniero:").grid(row=4, column=0)
        self.id_ing_asignar_entry = tk.Entry(self.frame_consultas)
        self.id_ing_asignar_entry.grid(row=4, column=1)

        tk.Button(self.frame_consultas, text="Asignar", command=self.asignar_ingeniero).grid(row=4, column=2)
        self.estado = tk.Label(root, text="", fg="blue")
        self.estado.pack(pady=5)

    def cargar_tabla(self, event=None):
        tabla = self.tabla_seleccionada.get()
        self.campos = TABLAS[tabla]

        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.entry_vars = {}

        for idx, campo in enumerate(self.campos):
            tk.Label(self.frame_campos, text=campo).grid(row=idx, column=0, sticky="e")
            var = tk.StringVar()
            entry = tk.Entry(self.frame_campos, textvariable=var)
            entry.grid(row=idx, column=1)
            self.entry_vars[campo] = var

        peticion = {"comando": "consultar_todo", "tabla": tabla}
        respuesta = enviar_peticion(peticion)

        if respuesta["status"] == "ok":
            self.registros = respuesta["registros"]
            self.indice = 0
            self.mostrar_registro()
        else:
            messagebox.showerror("Error", respuesta["mensaje"])

    def mostrar_registro(self):
        if not self.registros:
            self.estado.config(text="No hay registros")
            for campo in self.campos:
                self.entry_vars[campo].set("")
            return
        reg = self.registros[self.indice]
        for i, campo in enumerate(self.campos):
            self.entry_vars[campo].set(str(reg[i]))
        self.estado.config(text=f"Registro {self.indice + 1} de {len(self.registros)}")

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_registro()

    def siguiente(self):
        if self.indice < len(self.registros) - 1:
            self.indice += 1
            self.mostrar_registro()

    def get_datos_actuales(self):
        return {campo: self.entry_vars[campo].get() for campo in self.campos}

    def insertar(self):
        datos = self.get_datos_actuales()
        peticion = {"comando": "insertar", "tabla": self.tabla_seleccionada.get(), "valores": datos}
        respuesta = enviar_peticion(peticion)
        messagebox.showinfo("Insertar", respuesta.get("mensaje", ""))
        self.cargar_tabla()

    def actualizar(self):
        datos = self.get_datos_actuales()
        peticion = {"comando": "actualizar", "tabla": self.tabla_seleccionada.get(), "valores": datos}
        respuesta = enviar_peticion(peticion)
        messagebox.showinfo("Actualizar", respuesta.get("mensaje", ""))
        self.cargar_tabla()

    def eliminar(self):
        datos = self.get_datos_actuales()
        clave = list(datos.values())[0]  # Asume que la primera columna es la clave primaria
        peticion = {"comando": "eliminar", "tabla": self.tabla_seleccionada.get(), "clave": clave}
        respuesta = enviar_peticion(peticion)
        messagebox.showinfo("Eliminar", respuesta.get("mensaje", ""))
        self.cargar_tabla()

    def consultar_proyectos(self):
        id_dpto = self.id_dpto_entry.get()
        if not id_dpto:
            messagebox.showwarning("Consulta", "Ingresa ID del Departamento")
            return
        peticion = {"comando": "proyectos_por_departamento", "IDDpto": id_dpto}
        respuesta = enviar_peticion(peticion)
        if respuesta["status"] == "ok":
            proyectos = respuesta["registros"]
            texto = "\n".join([f"{p[0]} - {p[1]} ({p[2]} a {p[3]})" for p in proyectos])
            messagebox.showinfo("Proyectos", texto if texto else "Sin proyectos.")
        else:
            messagebox.showerror("Error", respuesta["mensaje"])

    def consultar_ingenieros(self):
        id_proy = self.id_proy_entry.get()
        if not id_proy:
            messagebox.showwarning("Consulta", "Ingresa ID del Proyecto")
            return
        peticion = {"comando": "ingenieros_por_proyecto", "IDProy": id_proy}
        respuesta = enviar_peticion(peticion)
        if respuesta["status"] == "ok":
            ingenieros = respuesta["registros"]
            texto = "\n".join([f"{i[0]} - {i[1]} | {i[2]} - {i[3]}" for i in ingenieros])
            messagebox.showinfo("Ingenieros", texto if texto else "Sin ingenieros.")
        else:
            messagebox.showerror("Error", respuesta["mensaje"])
            
    def asignar_ingeniero(self):
        id_proy = self.id_proy_asignar_entry.get()
        id_ing = self.id_ing_asignar_entry.get()

        if not id_proy or not id_ing:
            messagebox.showwarning("Asignación", "Debe ingresar ambos IDs")
            return

        peticion = {
            "comando": "asignar_ingeniero",
            "IDProy": id_proy,
            "IDIng": id_ing
        }
        respuesta = enviar_peticion(peticion)

        if respuesta["status"] == "ok":
            messagebox.showinfo("Asignación", respuesta["mensaje"])
        else:
            messagebox.showerror("Error", respuesta["mensaje"])

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteGUI(root)
    root.mainloop()
