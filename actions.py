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
    #transfer_button = button_widget



def pick_usb_drive():
    """Allows the user to select a folder as the USB destination."""
    from tkinter import filedialog
    folder_selected = filedialog.askdirectory(title="Select USB Drive")
    if folder_selected:
        usb_entry.configure(state='normal')
        usb_entry.delete(0, tk.END)
        usb_entry.insert(0, folder_selected)
        usb_entry.configure(state='readonly')
        status_label.configure(text_color="#2980b9", text="📁 USB drive selected.")



def transfer_to_usb():
    """Executes the BAT script and displays the output in the console."""
    destination = usb_entry.get()

    # 🔒 Desactivar botón
    #transfer_button.config(state='disabled')
    status_label.configure(text_color="#2980b9", text="⏳ Copying file...")

    if not os.path.isdir(destination):
        status_label.configure(text_color="#c0392b", text="❌ Invalid path. Please select a valid folder.")
        console.configure(state=tk.NORMAL)
        console.insert(tk.END, "Invalid path. Please select a valid folder.\n")
        console.configure(state=tk.DISABLED)
        #transfer_button.config(state='normal')  # 🔓 Reactivar
        return

    console.configure(state=tk.NORMAL)
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
            status_label.configure(text_color="#c0392b", text="❌ Error during copy.")
        elif result.returncode == 0:
            status_label.configure(text_color="#27ae60", text="✔ File copied successfully.")
        else:
            status_label.configure(text_color="#c0392b", text="⚠️ Finished with error code.")

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPTION]: {e}\n")
        status_label.configure(text_color="#c0392b", text="❌ Exception occurred while executing the script.")

    console.insert(tk.END, "\n--- END ---\n")
    console.see(tk.END)
    console.configure(state=tk.DISABLED)

    # 🔓 Reactivar botón al final
    #transfer_button.config(state='normal')



def backup_files():
    """Executes the backup scripts 200 and 900 sequentially and displays the output in the console."""
    status_label.configure(text_Color="#2980b9", text="⏳ Performing backup...")

    console.configure(state=tk.NORMAL)
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
            status_label.configure(text_color="#c0392b", text="❌ Error during backup 900.")
        elif res900.returncode == 0:
            status_label.configure(text_color="#27ae60", text="✔ Both backups completed successfully.")
        else:
            status_label.configure(text_color="#c0392b", text="⚠️ Backup 900 finished with error code.")

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPTION]: {e}\n")
        status_label.configure(text_color="#c0392b", text="❌ Exception occurred while executing the backup.")

    console.insert(tk.END, "\n--- END BACKUP ---\n")
    console.see(tk.END)
    console.configure(state=tk.DISABLED)



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
        console.configure(state=tk.NORMAL)
        console.insert(tk.END, f"[ERROR opening documentation]: {e}\n")
        console.configure(state=tk.DISABLED)



def register_widgets(entry_widget, console_widget, status_widget, button_widget):
    global usb_entry, console, status_label, transfer_button, progressbar
    usb_entry = entry_widget
    console = console_widget
    status_label = status_widget
    #transfer_button = button_widget
    


def generate_label(folder):
    """
    Reads the filenames in a folder,
    ignores 'crate.xml',
    takes the first 7 characters of the first valid file,
    and writes that value to 'label.txt' with 4 spaces at the end.
    Also prints the label in the app console.
    """
    try:
        if not os.path.exists(folder):
            console.configure(state=tk.NORMAL)
            console.insert(tk.END, f"Folder does not exist: {folder}\n")
            console.configure(state=tk.DISABLED)
            return

        files = os.listdir(folder)

        label = None
        for file in files:
            if os.path.isfile(os.path.join(folder, file)):
                if file.lower() == "crate.xml":
                    continue  # ignore crate.xml
                label = file[:7]
                break

        if label:
            with open(os.path.join(folder, "label.txt"), "w", encoding="utf-8") as f:
                f.write(str(label) + "    ")
            console.configure(state=tk.NORMAL)
            console.insert(tk.END, f"Label found: {label}\nFile 'label.txt' generated successfully.\n")
            console.configure(state=tk.DISABLED)
        else:
            console.configure(state=tk.NORMAL)
            console.insert(tk.END, "No valid file found.\n")
            console.configure(state=tk.DISABLED)

    except Exception as e:
        console.configure(state=tk.NORMAL)
        console.insert(tk.END, f"Error generating label: {e}\n")
        console.configure(state=tk.DISABLED)




def copy_temp():
    """Executes the BAT script to copy files from Temp to the FMS repository and displays the output in the console."""
    status_label.configure(text_color="#2980b9", text="⏳ Restoring Navigation Database...")
    status_label.update()

    target_folder = r"C:\Users\josep\Desktop\CAE"
    #target_folder = r"C:\Users\ios1\Desktop\NavDB\Temp"
    generate_label(target_folder)

    #transfer_button.config(state='disabled')
    console.configure(state=tk.NORMAL)
    console.insert(tk.END, "Copying Temp folder to FMS repository to update the navigation database from the CDU...\n")
    status_label.update()

    try:
        copytemp_result = subprocess.run(
            ["copy_temp.bat"],
            capture_output=True,
            text=True,
            shell=True
        )
        console.insert(tk.END, copytemp_result.stdout)
        if copytemp_result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + copytemp_result.stderr)
        if copytemp_result.returncode != 0:
            status_label.configure(text_Color="#c0392b", text="❌ Error during copy to temp. Aborting operation.")
            console.insert(tk.END, "\nAborting copy from temp due to error.\n")
            console.configure(state=tk.DISABLED)
            #transfer_button.config(state='normal')
            return

        status_label.configure(text_color="#27ae60", text="✔ Files copied from Temp to FMS successfully.")
        console.insert(tk.END, "Files copied from Temp successfully.\n")
        console.update()

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPTION]: {e}\n")
        status_label.configure(text_color="#c0392b", text="❌ Exception occurred while copying files from Temp.")

    console.insert(tk.END, "\n--- END COPY FROM TEMP ---\n")
    console.see(tk.END)
    console.configure(state='normal')



def restore_navdb():
    """Executes the BAT script to restore the navdb in all configurations and displays the output in the console."""
    status_label.configure(text_color="#2980b9", text="⏳ Restoring Navigation Database...")
    status_label.update()

    #transfer_button.config(state='disabled')
    console.configure(state=tk.NORMAL)
    console.insert(tk.END, "Navigation Database Restore in progress...\n")
    status_label.update()

    try:
        restore_result = subprocess.run(
            ["ndb_restore.bat"],
            capture_output=True,
            text=True,
            shell=True
        )
        console.insert(tk.END, restore_result.stdout)
        if restore_result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + restore_result.stderr)
        if restore_result.returncode != 0:
            status_label.configure(text_color="#c0392b", text="❌ Error during restore. Aborting operation.")
            console.insert(tk.END, "\nAborting restore due to error.\n")
            console.configure(state=tk.DISABLED)
            #transfer_button.config(state='normal')
            return

        status_label.configure(text_color="#27ae60", text="✔ Navigation Database restored successfully.")
        console.insert(tk.END, "Navigation Database Restore completed successfully.\n")
        console.update()

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPTION]: {e}\n")
        status_label.configure(text_color="#c0392b", text="❌ Exception occurred while restoring the database.")

    console.insert(tk.END, "\n--- END RESTORE ---\n")
    console.see(tk.END)
    console.configure(state='normal')



def update_navdb():
    """Executes the BAT script to update the navdb in all configurations and displays the output in the console."""
    status_label.configure(text_color="#2980b9", text="⏳ Updating Navigation Database...")
    status_label.update()

    #transfer_button.config(state='disabled')
    console.configure(state=tk.NORMAL)
    console.insert(tk.END, "Navigation Database Update in progress...\n")
    status_label.update()

    try:
        backup_result = subprocess.run(
            ["ndb_backup.bat"],
            capture_output=True,
            text=True,
            shell=True
        )
        console.insert(tk.END, backup_result.stdout)
        if backup_result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + backup_result.stderr)
        if backup_result.returncode != 0:
            status_label.configure(text_color="#c0392b", text="❌ Error during backup. Aborting update.")
            console.insert(tk.END, "\nAborting update due to backup error.\n")
            console.configure(state=tk.DISABLED)
            #transfer_button.config(state='normal')
            return

        status_label.configure(text_color="#2980b9", text="⏳ Backing Up Navigation Database...")
        status_label.update()
        console.insert(tk.END, "Navigation Database Backup in progress...\n")
        console.update()

        delete_result = subprocess.run(
            ["ndb_delete.bat"],
            capture_output=True,
            text=True,
            shell=True
        )
        console.insert(tk.END, delete_result.stdout)
        if delete_result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + delete_result.stderr)
        if delete_result.returncode != 0:
            status_label.configure(text_color="#c0392b", text="❌ Error during deletion. Aborting update.")
            console.insert(tk.END, "\nAborting update due to deletion error.\n")
            console.configure(state=tk.DISABLED)
            #transfer_button.config(state='normal')
            return

        status_label.configure(text_color="#2980b9", text="⏳ Updating Navigation Database...")
        status_label.update()
        console.insert(tk.END, "Navigation Database Update in progress...\n")
        console.update()
        
        result = subprocess.run(
            ["ndb_update.bat"],
            capture_output=True,
            text=True,
            shell=True
        )

        console.insert(tk.END, result.stdout)
        if result.stderr:
            console.insert(tk.END, "\n[ERROR]:\n" + result.stderr)
            status_label.configure(text_color="#c0392b", text="❌ Error during update.")
        elif result.returncode == 0:
            status_label.configure(text_color="#27ae60", text="✔ Navigation Database updated successfully.")
        else:
            status_label.configure(text_color="#c0392b", text="⚠️ Finished with error code.")

    except Exception as e:
        console.insert(tk.END, f"\n[EXCEPTION]: {e}\n")
        status_label.configure(text_color="#c0392b", text="❌ Exception occurred while executing the script.")

    console.insert(tk.END, "\n--- END UPDATE ---\n")
    console.see(tk.END)
    console.configure(state=tk.DISABLED)
    #transfer_button.config(state='normal')