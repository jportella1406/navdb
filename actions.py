import os
import tkinter as tk
import subprocess
import platform

# Referencias globales compartidas
usb_entry = None
console = None
status_label = None
transfer_button = None
progressbar = None

def register_widgets(entry_widget, console_widget, status_widget, button_widget):
    """Registers references to external widgets for global manipulation."""
    global usb_entry, console, status_label, transfer_button
    usb_entry = entry_widget
    console = console_widget
    status_label = status_widget
    transfer_button = button_widget

def pick_usb_drive():
    """Allows the user to select a folder as the USB destination."""
    from tkinter import filedialog
    folder_selected = filedialog.askdirectory(title="Select USB Drive")
    if folder_selected:
        usb_entry.config(state='normal')
        usb_entry.delete(0, tk.END)
        usb_entry.insert(0, folder_selected)
        usb_entry.config(state='readonly')
        status_label.config(foreground="#2980b9", text="📁 USB drive selected.")

def transfer_to_usb():
    """Executes the BAT script and displays the output in the console."""
    destination = usb_entry.get()

    # 🔒 Desactivar botón
    transfer_button.config(state='disabled')
    status_label.config(foreground="#2980b9", text="⏳ Copying file...")

    if not os.path.isdir(destination):
        status_label.config(foreground="#c0392b", text="❌ Invalid path. Please select a valid folder.")
        console.config(state=tk.NORMAL)
        console.insert(tk.END, "Invalid path. Please select a valid folder.\n")
        console.config(state=tk.DISABLED)
        transfer_button.config(state='normal')  # 🔓 Reactivar
        return

    console.config(state=tk.NORMAL)
    console.insert(tk.END, f"Executing copy to: {destination}\n")

    try:
        result = subprocess.run(
            ["copiar_archivos.bat", destination],
            capture_output=True,
            text=True,
            shell=True
        )

        console.insert(tk.END, result.stdout)
        if result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + result.stderr)
            status_label.config(foreground="#c0392b", text="❌ Error during copy.")
        elif result.returncode == 0:
            status_label.config(foreground="#27ae60", text="✔ File copied successfully.")
        else:
            status_label.config(foreground="#c0392b", text="⚠️ Finished with error code.")

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPTION]: {e}\n")
        status_label.config(foreground="#c0392b", text="❌ Exception occurred while executing the script.")

    console.insert(tk.END, "\n--- END ---\n")
    console.see(tk.END)
    console.config(state=tk.DISABLED)

    # 🔓 Reactivar botón al final
    transfer_button.config(state='normal')

import subprocess
import tkinter as tk

def backup_files():
    """Executes the backup scripts 200 and 900 sequentially and displays the output in the console."""
    status_label.config(foreground="#2980b9", text="⏳ Performing backup...")

    console.config(state=tk.NORMAL)
    console.insert(tk.END, "Starting backup 200...\n")

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
            raise RuntimeError("Error in backup_archivos_200.bat")

        console.insert(tk.END, "\nBackup 200 completed successfully.\n")
        console.insert(tk.END, "Starting backup 900...\n")

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
            status_label.config(foreground="#c0392b", text="❌ Error during backup 900.")
        elif res900.returncode == 0:
            status_label.config(foreground="#27ae60", text="✔ Both backups completed successfully.")
        else:
            status_label.config(foreground="#c0392b", text="⚠️ Backup 900 finished with error code.")

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPTION]: {e}\n")
        status_label.config(foreground="#c0392b", text="❌ Exception occurred while executing the backup.")

    console.insert(tk.END, "\n--- END BACKUP ---\n")
    console.see(tk.END)
    console.config(state=tk.DISABLED)


def open_documentation():
    """Opens the documentation .docx file with the system's default program."""
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
        console.insert(tk.END, f"[ERROR opening documentation]: {e}\n")
        console.config(state=tk.DISABLED)


def register_widgets(entry_widget, console_widget, status_widget, button_widget):
    global usb_entry, console, status_label, transfer_button, progressbar
    usb_entry = entry_widget
    console = console_widget
    status_label = status_widget
    transfer_button = button_widget
    

def update_navdb():
    """Executes the BAT script to update the navdb in all configurations and displays the output in the console."""
    status_label.config(foreground="#2980b9", text="⏳ Updating Navigation Database...")
    status_label.update()

    transfer_button.config(state='disabled')
    console.config(state=tk.NORMAL)
    console.insert(tk.END, "Navigation Database Update in progress...\n")
    status_label.update()

    try:
        result = subprocess.run(
            ["update_ndb.bat"],
            capture_output=True,
            text=True,
            shell=True
        )

        console.insert(tk.END, result.stdout)
        if result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + result.stderr)
            status_label.config(foreground="#c0392b", text="❌ Error during update.")
        elif result.returncode == 0:
            status_label.config(foreground="#27ae60", text="✔ Navigation Database updated successfully.")
        else:
            status_label.config(foreground="#c0392b", text="⚠️ Finished with error code.")

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPTION]: {e}\n")
        status_label.config(foreground="#c0392b", text="❌ Exception occurred while executing the script.")

    console.insert(tk.END, "\n--- END UPDATE ---\n")
    console.see(tk.END)
    console.config(state=tk.DISABLED)
    transfer_button.config(state='normal')