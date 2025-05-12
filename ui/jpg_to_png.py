import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from utils import config

def open_jpg_to_png_window(root):
    win = tk.Toplevel(root)
    win.title("Convertir JPG a PNG")
    win.geometry("800x600")
    win.configure(bg=config.UI_BACKGROUND_COLOR)

    # Entradas de ruta y nombre
    frame = tk.Frame(win, bg=config.UI_BACKGROUND_COLOR)
    frame.pack(padx=20, pady=20)

    tk.Label(frame, text="Archivo JPG de origen:", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).grid(row=0, column=0, sticky='w')
    path_entry = tk.Entry(frame, width=60)
    path_entry.grid(row=1, column=0)
    tk.Button(frame, text="📂", command=lambda: select_jpg(path_entry), bg=config.BUTTON_BG_COLOR, fg=config.BUTTON_FG_COLOR).grid(row=1, column=1)

    tk.Label(frame, text="Carpeta de destino:", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).grid(row=2, column=0, sticky='w', pady=(20, 0))
    output_entry = tk.Entry(frame, width=60)
    output_entry.grid(row=3, column=0)
    tk.Button(frame, text="📂", command=lambda: select_folder(output_entry), bg=config.BUTTON_BG_COLOR, fg=config.BUTTON_FG_COLOR).grid(row=3, column=1)

    tk.Label(frame, text="Nombre de salida (sin .png):", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).grid(row=4, column=0, sticky='w', pady=(20, 0))
    name_entry = tk.Entry(frame, width=40)
    name_entry.grid(row=5, column=0, sticky='w')

    # Botón para convertir
    def convertir():
        path = path_entry.get().strip()
        folder = output_entry.get().strip()
        name = name_entry.get().strip() or "exported"
        if not path or not folder:
            messagebox.showerror("Faltan datos", "Debe especificarse imagen de origen y carpeta de destino")
            return
        try:
            img = Image.open(path).convert("RGBA")
            out_path = f"{folder}/{name}.png"
            img.save(out_path, "PNG")
            messagebox.showinfo("Éxito", f"Imagen convertida:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Convertir", command=convertir, width=20, bg=config.BUTTON_BG_COLOR, fg=config.BUTTON_FG_COLOR).grid(row=6, column=0, pady=30)


def select_jpg(entry):
    path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def select_folder(entry):
    path = filedialog.askdirectory()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)