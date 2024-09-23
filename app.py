import tkinter as tk
from tkinter import Menu, Frame, Canvas, Scrollbar, Checkbutton, IntVar

# Parametros globales
numNodosDefault = 100       
probAristasDefault = 0.2

probAristas = probAristasDefault
numeroNodos = numNodosDefault

def on_enter(e):
    e.widget.config(bg='lightgrey')

def on_leave(e):
    e.widget.config(bg='SystemButtonFace')

def create_menu_item(menu, label):
    item = tk.Label(menu, text=label, padx=60, pady=5)
    item.bind("<Enter>", on_enter)
    item.bind("<Leave>", on_leave)
    item.pack(side=tk.LEFT)
    return item

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def show_submenu(event, submenu):
    submenu.post(event.x_root, event.y_root)
    
def update_sections():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    for i, var in enumerate(section_vars):
        if var.get():
            section = Frame(scrollable_frame, bg='white')
            section.pack(fill=tk.X, pady=5)
            label = tk.Label(section, text=f"Sección {i+1}", bg='white', anchor='nw', justify='left', padx=10, pady=10, width=15, height=13, wraplength=780)
            label.pack(fill=tk.BOTH, expand=True)
            separator = tk.Frame(scrollable_frame, height=4, bd=1, relief=tk.SUNKEN, bg='red', width=800)
            separator.pack(fill=tk.X, padx=5, pady=5)


def select_all():
    for var in section_vars:
        var.set(1)
    update_sections()

def deselect_all():
    for var in section_vars:
        var.set(0)
    update_sections()

def guardar_valor(valor, opcion):
    if(opcion == 1):
        global numeroNodos
        numeroNodos = int(float(valor))
        if(numeroNodos < 0): numeroNodos = 0
        if(numeroNodos > 1000): numeroNodos = 1000
        print(f"Valor guardado, nodos: {numeroNodos}")
    if(opcion == 2):
        global probAristas
        probAristas = float(valor)/100
        if(probAristas < 0): probAristas = 0
        if(probAristas > 1): probAristas = 1
        print(f"Valor guardado, probabilidad de aristas: {probAristas}")
    
def ventana_def_numero(encabezado, lim_inf, lim_sup, opcion, inc):
    miniventana = tk.Toplevel(root)
    miniventana.title("Seleccionar valor")
    miniventana.geometry("300x150")
    
    label = tk.Label(miniventana, text=encabezado)
    label.pack(pady=10)
    
    spinbox = tk.Spinbox(miniventana, from_=lim_inf, to=lim_sup, increment=inc)
    spinbox.pack(pady=10)
    
    def guardar():
        valor = spinbox.get()
        guardar_valor(valor, opcion)
        miniventana.destroy()
    
    boton_aceptar = tk.Button(miniventana, text="Aceptar", command=guardar)
    boton_aceptar.pack(pady=10)
    
def mostrar_grafo():
    print("Ahora se mostraría el grafo")
    
       
# Crear la ventana principal
root = tk.Tk()
root.geometry("820x540")
root.minsize(820, 540)
root.configure(bg='white')
root.resizable(False, False)

# Crear la barra de menú
menu_bar = tk.Frame(root, bg='white')
menu_bar.pack(side=tk.TOP, fill=tk.X)

# Crear los apartados del menú
apartado1 = create_menu_item(menu_bar, "Personalizar grafo")
apartado2 = create_menu_item(menu_bar, "Apartado 2")
apartado3 = create_menu_item(menu_bar, "Parámetros")

boton_label = tk.Label(menu_bar, text="Mostrar grafo", padx=10, pady=5)
boton_label.pack(side=tk.LEFT)

# Añadir eventos para el "botón"
boton_label.bind("<Enter>", on_enter)
boton_label.bind("<Leave>", on_leave)
boton_label.bind("<Button-1>", lambda e: mostrar_grafo())

# Crear los menús desplegables
submenu1 = Menu(root, tearoff=0)
submenu1.add_command(label="Número de nodos", command=lambda: ventana_def_numero("Seleccione el número de nodos:", 0, 1000, 1, 1))
submenu1.add_command(label="Probabilidad de conexión", command=lambda: ventana_def_numero("Seleccione la probabilidad de arista entre dos nodos (%):", 0.0, 100.0, 2, 0.5))
submenu1.add_command(label="Crear grafo aleatorio")

submenu2 = Menu(root, tearoff=0)
submenu2.add_command(label="Opción 2.1")
submenu2.add_command(label="Opción 2.2")

submenu3 = Menu(root, tearoff=0)
section_vars = [IntVar() for _ in range(6)]
for i, var in enumerate(section_vars):
    submenu3.add_checkbutton(label=f"Sección {i+1}", variable=var, command=update_sections)
submenu3.add_separator()
submenu3.add_command(label="Seleccionar todas", command=select_all)
submenu3.add_command(label="Deseleccionar todas", command=deselect_all)

# Asociar los menús desplegables a los apartados
apartado1.bind("<Button-1>", lambda e: show_submenu(e, submenu1))
apartado2.bind("<Button-1>", lambda e: show_submenu(e, submenu2))
apartado3.bind("<Button-1>", lambda e: show_submenu(e, submenu3))

# Crear el área scrolleable
scroll_frame = Frame(root, bg='white')
scroll_frame.pack(fill=tk.BOTH, expand=True)

canvas = Canvas(scroll_frame, bg='white')
scrollbar = Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg='white')

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Ejecutar la aplicación
root.mainloop()
