import os
import tkinter as tk
import subprocess
import platform

# Referencias globales compartidas
usb_entry = None
console = None
status_label = None
transfer_button = None

def register_widgets(entry_widget, console_widget, status_widget, button_widget):
    """Registra referencias a widgets externos para manipulación global."""
    global usb_entry, console, status_label, transfer_button
    usb_entry = entry_widget
    console = console_widget
    status_label = status_widget
    transfer_button = button_widget

def pick_usb_drive():
    """Permite al usuario seleccionar una carpeta como destino USB."""
    from tkinter import filedialog
    folder_selected = filedialog.askdirectory(title="Select USB Drive")
    if folder_selected:
        usb_entry.config(state='normal')
        usb_entry.delete(0, tk.END)
        usb_entry.insert(0, folder_selected)
        usb_entry.config(state='readonly')
        status_label.config(foreground="#2980b9", text="📁 Unidad USB seleccionada.")

def transfer_to_usb():
    """Ejecuta el script BAT y muestra la salida en la consola."""
    destino = usb_entry.get()

    # 🔒 Desactivar botón
    transfer_button.config(state='disabled')
    status_label.config(foreground="#2980b9", text="⏳ Copiando archivo...")

    if not os.path.isdir(destino):
        status_label.config(foreground="#c0392b", text="❌ Ruta inválida. Selecciona una carpeta válida.")
        console.config(state=tk.NORMAL)
        console.insert(tk.END, "Ruta inválida. Por favor selecciona una carpeta válida.\n")
        console.config(state=tk.DISABLED)
        transfer_button.config(state='normal')  # 🔓 Reactivar
        return

    console.config(state=tk.NORMAL)
    console.insert(tk.END, f"Ejecutando copia a: {destino}\n")

    try:
        result = subprocess.run(
            ["copiar_archivos.bat", destino],
            capture_output=True,
            text=True,
            shell=True
        )

        console.insert(tk.END, result.stdout)
        if result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + result.stderr)
            status_label.config(foreground="#c0392b", text="❌ Error durante la copia.")
        elif result.returncode == 0:
            status_label.config(foreground="#27ae60", text="✔ Archivo copiado exitosamente.")
        else:
            status_label.config(foreground="#c0392b", text="⚠️ Finalizó con código de error.")

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPCIÓN]: {e}\n")
        status_label.config(foreground="#c0392b", text="❌ Excepción en la ejecución del script.")

    console.insert(tk.END, "\n--- FIN ---\n")
    console.see(tk.END)
    console.config(state=tk.DISABLED)

    # 🔓 Reactivar botón al final
    transfer_button.config(state='normal')

import subprocess
import tkinter as tk

def backup_files():
    """Ejecuta los scripts de backup 200 y 900 secuencialmente y muestra la salida en la consola."""
    status_label.config(foreground="#2980b9", text="⏳ Realizando copia de seguridad...")

    console.config(state=tk.NORMAL)
    console.insert(tk.END, "Iniciando backup 200...\n")

    try:
        # 1. Ejecuta el primer script
        res200 = subprocess.run(
            ["backup_archivos_200.bat"],
            capture_output=True,
            text=True,
            shell=True
        )
        console.insert(tk.END, res200.stdout)
        if res200.stderr:
            console.insert(tk.END, "\n[ERROR 200]:\n" + res200.stderr)
            raise RuntimeError("Error en backup_archivos_200.bat")

        console.insert(tk.END, "\nBackup 200 completado correctamente.\n")
        console.insert(tk.END, "Iniciando backup 900...\n")

        # 2. Ejecuta el segundo script solo si el primero fue exitoso
        res900 = subprocess.run(
            ["backup_archivos_900.bat"],
            capture_output=True,
            text=True,
            shell=True
        )
        console.insert(tk.END, res900.stdout)
        if res900.stderr:
            console.insert(tk.END, "\n[ERROR 900]:\n" + res900.stderr)
            status_label.config(foreground="#c0392b", text="❌ Error durante backup 900.")
        elif res900.returncode == 0:
            status_label.config(foreground="#27ae60", text="✔ Ambos backups realizados exitosamente.")
        else:
            status_label.config(foreground="#c0392b", text="⚠️ Backup 900 finalizó con código de error.")

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPCIÓN]: {e}\n")
        status_label.config(foreground="#c0392b", text="❌ Excepción en la ejecución del backup.")

    console.insert(tk.END, "\n--- FIN BACKUP ---\n")
    console.see(tk.END)
    console.config(state=tk.DISABLED)


def open_documentation():
    """Abre el archivo de documentación .docx con el programa predeterminado del sistema."""
    doc_path = os.path.abspath("Documentation\Programa para Navigation database CRJ.pdf")

    try:
        if platform.system() == "Windows":
            os.startfile(doc_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", doc_path])
        else:  # Linux
            subprocess.run(["xdg-open", doc_path])
    except Exception as e:
        console.config(state=tk.NORMAL)
        console.insert(tk.END, f"[ERROR al abrir la documentación]: {e}\n")
        console.config(state=tk.DISABLED)