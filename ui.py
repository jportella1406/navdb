import tkinter as tk
from tkinter import ttk, Menu
from actions import transfer_to_usb, pick_usb_drive, register_widgets
from style import apply_styles
from actions import transfer_to_usb, pick_usb_drive, backup_files
from actions import open_documentation
from actions import update_navdb

def create_main_ui(root):
    root.title("Navigation Database Update")
    root.geometry("1000x600")
    root.resizable(False, False)
    root.configure(bg="#f4f4f4")

    apply_styles(ttk)  # Aplicar estilos visuales

    # Menú superior
    menubar = Menu(root)
    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="Open the procedure how to update the navigation database", command=open_documentation)

    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
   
   #Esto fue comentado para poder usar las otras pestañas en el futuro
   # for label in ["Device", "Tools"]:
   #     menubar.add_cascade(label=label, menu=Menu(menubar, tearoff=0))

    menubar.add_cascade(label="Help", menu=help_menu)
    root.config(menu=menubar)

    # Frame principal
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame izquierdo
    left_frame = ttk.Frame(main_frame, width=480)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
    ttk.Label(left_frame, text="Actions", font=("Segoe UI", 11, "bold")).pack(anchor='w', pady=(0, 10))

    # Botones y entrada
    ttk.Button(left_frame, text="Backup files", command=backup_files, style="Rounded.TButton").pack(anchor='w', fill=tk.X, pady=5)
    ttk.Button(left_frame, text="Pick USB Drive", command=pick_usb_drive, style="Rounded.TButton").pack(anchor='w', fill=tk.X, pady=(0, 5))
    usb_entry = ttk.Entry(left_frame, width=40, state='readonly', font=("Segoe UI", 9))
    usb_entry.pack(anchor='w', fill=tk.X, pady=(0, 5))
    transfer_btn = ttk.Button(left_frame, text="Transfer files to USB", command=transfer_to_usb, style="Rounded.TButton")
    transfer_btn.pack(anchor='w', fill=tk.X, pady=5) 
    ttk.Button(left_frame, text="Update all configurations", command=update_navdb, style="Rounded.TButton").pack(anchor='w', fill=tk.X, pady=5)

    # Frame derecho
    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    ttk.Label(right_frame, text="Console Output", font=("Segoe UI", 11, "bold")).pack(anchor='w', pady=(0, 10))
    console = tk.Text(right_frame, bg="#2c3e50", fg="#00FF66", font=("Consolas", 10), wrap="word")
    console.config(state=tk.DISABLED)
    console.pack(fill=tk.BOTH, expand=True)

    # Etiqueta de estado
    status_label = ttk.Label(right_frame, text="", font=("Segoe UI", 10, "italic"))
    status_label.pack(anchor='w', pady=(0, 5))

    status_frame = ttk.Frame(right_frame)
    status_frame.pack(anchor='w', pady=(0, 5))

    status_label = ttk.Label(status_frame, text="", font=("Segoe UI", 10, "italic"))
    status_label.pack(side=tk.LEFT)

    # Registrar widgets globales para uso en actions.py
    register_widgets(usb_entry, console, status_label, transfer_btn)