import tkinter as tk
import subprocess
import os
from tkinter import ttk, Menu, filedialog

#Funcion para copiar archivos
import subprocess

def transfer_to_usb():
    destino = usb_entry.get()

    if not os.path.isdir(destino):
        console.config(state=tk.NORMAL)
        console.insert(tk.END, "Ruta inválida. Por favor selecciona una carpeta válida.\n")
        console.config(state=tk.DISABLED)
        return

    # Habilitar console y limpiar si deseas
    console.config(state=tk.NORMAL)
    console.insert(tk.END, f"Ejecutando copia a: {destino}\n")

    # Ejecutar el archivo BAT y capturar salida
    try:
        result = subprocess.run(
            ["copiar_archivos.bat", destino],
            capture_output=True,
            text=True,
            shell=True
        )

        # Mostrar la salida del BAT en la consola GUI
        console.insert(tk.END, result.stdout)
        if result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + result.stderr)

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPCIÓN]: {e}\n")

    console.insert(tk.END, "\n--- FIN ---\n")
    console.see(tk.END)  # Auto scroll
    console.config(state=tk.DISABLED)


# Crear ventana principal
root = tk.Tk()
root.title("USB Configuration Tool")
root.geometry("1000x600")
root.resizable(False, False)
root.configure(bg="#f4f4f4")  # Fondo suave

# ===== Estilo UI =====
style = ttk.Style()
style.theme_use('clam')

# Colores y estilo global
style.configure("Rounded.TButton",
                background="#2980b9",
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                padding=10,
                borderwidth=0,
                relief="flat")

style.map("Rounded.TButton",
          background=[("active", "#3498db")],
          foreground=[("disabled", "gray")])


# Colores y estilo global
style.configure("TFrame", background="#f4f4f4")
style.configure("TLabel", background="#f4f4f4", foreground="#2c3e50", font=("Segoe UI", 10))
style.configure("TButton", background="#2980b9", foreground="white", font=("Segoe UI", 10, "bold"))
style.map("TButton",
          background=[("active", "#3498db")],
          foreground=[("disabled", "gray")])

# ===== Función para elegir USB =====
def pick_usb_drive():
    folder_selected = filedialog.askdirectory(title="Select USB Drive")
    if folder_selected:
        usb_entry.config(state='normal')
        usb_entry.delete(0, tk.END)
        usb_entry.insert(0, folder_selected)
        usb_entry.config(state='readonly')

# ===== Menú =====
menubar = Menu(root)
for label in ["File", "Device", "Tools", "Help"]:
    menubar.add_cascade(label=label, menu=Menu(menubar, tearoff=0))
root.config(menu=menubar)

# ===== Frame principal =====
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# ===== IZQUIERDA =====
left_frame = ttk.Frame(main_frame, width=480)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

ttk.Label(left_frame, text="Actions", font=("Segoe UI", 11, "bold")).pack(anchor='w', pady=(0, 10))

# Botones principales
ttk.Button(left_frame, text="Transfer files to USB", command= transfer_to_usb, style="Rounded.TButton").pack(anchor='w', fill=tk.X, pady=5)
ttk.Button(left_frame, text="Backup files", style="Rounded.TButton").pack(anchor='w', fill=tk.X, pady=5)
ttk.Button(left_frame, text="Transfer files to all configurations", style="Rounded.TButton").pack(anchor='w', fill=tk.X, pady=5)
ttk.Button(left_frame, text="Pick USB Drive", command=pick_usb_drive, style="Rounded.TButton").pack(anchor='w', fill=tk.X, pady=(0,5))


usb_entry = ttk.Entry(left_frame, width=40, state='readonly', font=("Segoe UI", 9))
usb_entry.pack(anchor='w', fill=tk.X, pady=(0, 5))

# ===== DERECHA =====
right_frame = ttk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

ttk.Label(right_frame, text="Console Output", font=("Segoe UI", 11, "bold")).pack(anchor='w', pady=(0, 10))

# Consola solo lectura
console = tk.Text(right_frame, bg="#2c3e50", fg="#00FF66", font=("Consolas", 10), wrap="word")
console.insert(tk.END, "Console output will appear here...\n")
console.config(state=tk.DISABLED)
console.pack(fill=tk.BOTH, expand=True)

# ===== Iniciar =====
root.mainloop()

