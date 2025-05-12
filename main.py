import tkinter as tk
from tkinter import PhotoImage
from ui.jpg_to_png import open_jpg_to_png_window
from ui.palette_extractor import open_palette_extractor_window
from PIL import ImageTk
from utils import config
import os
import sys


app = tk.Tk()
app.title("EasyPixel Toolbox")
app.geometry("350x360")
app.configure(bg=config.UI_BACKGROUND_COLOR)
app.resizable(False, False)

def resource_path(relative_path):
    """Devuelve la ruta absoluta al recurso empaquetado (compatible PyInstaller)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

icon_img = ImageTk.PhotoImage(file=resource_path("assets/icon32x32.png"))
app.iconphoto(False, icon_img)

header_frame = tk.Frame(app, bg=config.UI_BACKGROUND_COLOR)
header_frame.pack(pady=10)

logo_img = ImageTk.PhotoImage(file=resource_path("assets/icon128x128.png"))
logo_label = tk.Label(header_frame, image=logo_img, bg=config.UI_BACKGROUND_COLOR)
logo_label.image = logo_img
logo_label.pack()

tk.Label(
    header_frame,
    text="EasyPixel Toolbox",
    font=("Helvetica", 18, "bold"),
    fg=config.UI_FOREGROUND_COLOR,
    bg=config.UI_BACKGROUND_COLOR
).pack(pady=4)

tk.Button(
    app,
    text="📷 Convertir JPG a PNG",
    width=30,
    command=lambda: open_jpg_to_png_window(app),
    bg=config.BUTTON_BG_COLOR,
    fg=config.BUTTON_FG_COLOR,
    activebackground=config.BUTTON_ACTIVE_BG
).pack(pady=10)

tk.Button(
    app,
    text="🎨 Extraer Paleta y Generar Imagen",
    width=30,
    command=lambda: open_palette_extractor_window(app),
    bg=config.BUTTON_BG_COLOR,
    fg=config.BUTTON_FG_COLOR,
    activebackground=config.BUTTON_ACTIVE_BG
).pack(pady=10)

app.mainloop()