import customtkinter as ctk
import tkinter as tk
from tkinter import Menu
from actions import transfer_to_usb, pick_usb_drive, register_widgets
from style import apply_styles
from actions import transfer_to_usb, pick_usb_drive, backup_files
from actions import open_documentation
from actions import update_navdb
from actions import restore_navdb
from actions import copy_temp

def create_main_ui(root):
    import tkinter as tk
    import customtkinter as ctk

    # Apariencia
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # ---- Ventana sin bordes (oculta la barra antigua) ----
    root.geometry("1000x600+200+120")
    root.overrideredirect(True)           # <-- quita la barra de Windows
    root.configure(bg="#121212")          # fondo detrás del marco

    # re-aplicar sin bordes al restaurar desde la barra de tareas
    root.bind("<Map>", lambda e: root.overrideredirect(True))

    # Marco contenedor con borde suave
    window = ctk.CTkFrame(root, corner_radius=12)
    window.pack(fill="both", expand=True, padx=6, pady=6)

    # ---------------- Barra de título personalizada ----------------
    title_bar = ctk.CTkFrame(window, height=36, corner_radius=10)
    title_bar.pack(fill="x", padx=6, pady=(6, 0))

    title_label = ctk.CTkLabel(
        title_bar, text="Navigation Database Update",
        font=ctk.CTkFont(size=13, weight="bold")
    )
    title_label.pack(side="left", padx=(10, 12))

    # Menús emergentes (reemplazan al menú nativo)
    file_menu = tk.Menu(root, tearoff=0)
    file_menu.add_command(label="Exit", command=root.destroy)

    help_menu = tk.Menu(root, tearoff=0)
    help_menu.add_command(
        label="Open the procedure how to update the navigation database",
        command=open_documentation
    )

    def popup_menu(widget, menu):
        menu.tk_popup(widget.winfo_rootx(), widget.winfo_rooty() + widget.winfo_height())

    file_btn = ctk.CTkButton(title_bar, text="File", width=56, height=26,
                             command=lambda: popup_menu(file_btn, file_menu))
    help_btn = ctk.CTkButton(title_bar, text="Help", width=56, height=26,
                             command=lambda: popup_menu(help_btn, help_menu))
    file_btn.pack(side="left", padx=(0, 6))
    help_btn.pack(side="left")
    file_btn.configure(fg_color="transparent", hover_color="#1900fb", text_color="white")
    help_btn.configure(fg_color="transparent", hover_color="#1900fb", text_color="white")


    # Botones de ventana (minimizar y cerrar)
    def minimize():
        # Quita temporalmente el borderless para que Windows cree el icono en la barra
        root.overrideredirect(False)
        root.update_idletasks()
        root.iconify()

    def on_map(event):
    # Cuando vuelve de la barra de tareas (estado normal), re-aplica el borderless
        if root.state() == "normal":
            root.overrideredirect(True)

    def on_unmap(event):
        # Cuando se minimiza (iconic), mantener sin borderless para que siga en la barra
        if root.state() == "iconic":
            root.overrideredirect(False)

    root.bind("<Map>", on_map)
    root.bind("<Unmap>", on_unmap)


    btn_min = ctk.CTkButton(title_bar, text="—", width=36, height=26, command=minimize)
    btn_close = ctk.CTkButton(title_bar, text="✕", width=36, height=26, command=root.destroy)
    btn_close.pack(side="right", padx=(6, 8))
    btn_min.pack(side="right")

    # Arrastrar la ventana
    def start_move(e):
        root._drag_x = e.x_root
        root._drag_y = e.y_root

    def do_move(e):
        dx = e.x_root - root._drag_x
        dy = e.y_root - root._drag_y
        root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")
        root._drag_x = e.x_root
        root._drag_y = e.y_root

    for w in (title_bar, title_label):
        w.bind("<Button-1>", start_move)
        w.bind("<B1-Motion>", do_move)

    # ---------------- Contenido de tu app ----------------
    content = ctk.CTkFrame(window, corner_radius=10)
    content.pack(fill="both", expand=True, padx=6, pady=(6, 6))

    # Main frame
    main_frame = ctk.CTkFrame(content)
    main_frame.pack(fill=ctk.BOTH, expand=True)

    # Left frame
    left_frame = ctk.CTkFrame(main_frame, width=480)
    left_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=20, pady=20)
    ctk.CTkLabel(left_frame, text="Actions",
                 font=ctk.CTkFont(size=14, weight="bold")).pack(anchor='w', pady=(0, 10))

    ctk.CTkButton(left_frame, text="Copy files from Temp", command=copy_temp)\
        .pack(anchor='w', fill=ctk.X, pady=(0, 5))
    ctk.CTkButton(left_frame, text="Restore files", command=restore_navdb)\
        .pack(anchor='w', fill=ctk.X, pady=5)
    ctk.CTkButton(left_frame, text="Update all configurations", command=update_navdb)\
        .pack(anchor='w', fill=ctk.X, pady=5)

    # Right frame
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)
    ctk.CTkLabel(right_frame, text="Console Output",
                 font=ctk.CTkFont(size=14, weight="bold")).pack(anchor='w', pady=(0, 10))

    console = ctk.CTkTextbox(
        right_frame, fg_color="#2c3e50", text_color="#00FF66",
        font=("Consolas", 13), wrap="word"
    )
    console.configure(state=tk.DISABLED)
    console.pack(fill=ctk.BOTH, expand=True)

    status_label = ctk.CTkLabel(right_frame, text="", font=ctk.CTkFont(size=12, slant="italic"))
    status_label.pack(anchor='w', pady=(0, 5))

    # Registrar widgets para actions.py
    register_widgets(None, console, status_label, None)


# def create_main_ui(root):
#     ctk.set_appearance_mode("dark")  # "dark", "light", or "system"
#     ctk.set_default_color_theme("blue")

#     root.title("Navigation Database Update")
#     root.geometry("1000x600")
#     root.resizable(False, False)
#     root.configure(bg="gray86")  # color de fondo base

#     # Menú superior (usando tkinter.Menu, customtkinter no tiene menú propio)
#     menubar = Menu(root)
#     help_menu = Menu(menubar, tearoff=0)
#     help_menu.add_command(
#         label="Open the procedure how to update the navigation database",
#         command=open_documentation
#     )

#     file_menu = Menu(menubar, tearoff=0)
#     file_menu.add_command(label="Exit", command=root.quit)
#     menubar.add_cascade(label="File", menu=file_menu)
#     menubar.add_cascade(label="Help", menu=help_menu)
#     root.config(menu=menubar)

#     # Main frame
#     main_frame = ctk.CTkFrame(root)
#     main_frame.pack(fill=ctk.BOTH, expand=True)

#     # Left frame
#     left_frame = ctk.CTkFrame(main_frame, width=480)
#     left_frame.pack(side=ctk.LEFT, fill=ctk.Y, padx=20, pady=20)
#     ctk.CTkLabel(
#         left_frame, text="Actions", font=ctk.CTkFont(size=14, weight="bold")
#     ).pack(anchor='w', pady=(0, 10))

#     ctk.CTkButton(
#         left_frame, text="Copy files from Temp", command=copy_temp
#     ).pack(anchor='w', fill=ctk.X, pady=(0, 5))
#     ctk.CTkButton(
#         left_frame, text="Restore files", command=restore_navdb
#     ).pack(anchor='w', fill=ctk.X, pady=5)
#     ctk.CTkButton(
#         left_frame, text="Update all configurations", command=update_navdb
#     ).pack(anchor='w', fill=ctk.X, pady=5)

#     # Right frame
#     right_frame = ctk.CTkFrame(main_frame)
#     right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)
#     ctk.CTkLabel(
#         right_frame, text="Console Output", font=ctk.CTkFont(size=14, weight="bold")
#     ).pack(anchor='w', pady=(0, 10))

#     console = ctk.CTkTextbox(
#         right_frame,
#         fg_color="#2c3e50",
#         text_color="#00FF66",
#         font=("Consolas", 13),
#         wrap="word"
#     )
#     console.configure(state=tk.DISABLED)
#     console.pack(fill=ctk.BOTH, expand=True)

#     # Status label
#     status_label = ctk.CTkLabel(
#         right_frame, text="", font=ctk.CTkFont(size=12, slant="italic")
#     )
#     status_label.pack(anchor='w', pady=(0, 5))

#     # Register widgets for actions.py
#     register_widgets(None, console, status_label, None)

