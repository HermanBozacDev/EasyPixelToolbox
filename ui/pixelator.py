
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils import config, image_utils

def open_pixelator_window(parent, image_path, palette):
    if not image_path or not palette:
        messagebox.showerror("Faltan datos", "Cargá una imagen y seleccioná colores para continuar")
        return

    win = tk.Toplevel(parent)
    win.title("Pixelar Imagen")
    win.geometry("800x600")
    win.configure(bg=config.UI_BACKGROUND_COLOR)
    win.lift()
    win.focus_force()

    top_frame = tk.Frame(win, bg=config.UI_BACKGROUND_COLOR)
    top_frame.pack(pady=10, padx=10, fill='both', expand=True)

    form_frame = tk.Frame(top_frame, bg=config.UI_BACKGROUND_COLOR)
    form_frame.pack(side='left', padx=10, fill='y')

    tk.Label(form_frame, text="Ancho", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).pack()
    w_entry = tk.Entry(form_frame, width=6); w_entry.insert(0, str(config.DEFAULT_WIDTH)); w_entry.pack()
    tk.Label(form_frame, text="Alto", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).pack()
    h_entry = tk.Entry(form_frame, width=6); h_entry.insert(0, str(config.DEFAULT_HEIGHT)); h_entry.pack()
    tk.Label(form_frame, text="Bloque", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).pack()
    b_entry = tk.Entry(form_frame, width=6); b_entry.insert(0, str(config.DEFAULT_BLOCK_SIZE)); b_entry.pack()
    tk.Label(form_frame, text="Nombre PNG", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).pack()
    n_entry = tk.Entry(form_frame, width=15); n_entry.insert(0, "mi_sprite"); n_entry.pack()

    preview_frame = tk.Frame(top_frame, bg=config.UI_BACKGROUND_COLOR)
    preview_frame.pack(side='right', padx=10, fill='both', expand=True)
    preview = tk.Label(preview_frame)
    preview.pack(expand=True)

    def procesar():
        try:
            w, h, b = int(w_entry.get()), int(h_entry.get()), int(b_entry.get())
        except: return
        img = Image.open(image_path).convert("RGB").resize((w,h), Image.NEAREST)
        result = image_utils.approximate_image_to_palette(img, palette, b)
        tkimg = ImageTk.PhotoImage(result.resize((config.CANVAS_PREVIEW_SIZE, config.CANVAS_PREVIEW_SIZE), Image.NEAREST))
        preview.config(image=tkimg); preview.image = tkimg; preview.result = result

    def exportar():
        if not hasattr(preview, 'result'):
            return
        filename = n_entry.get().strip() or "exported"
        result = preview.result
        rgba = result.convert("RGBA")
        datas = rgba.getdata()
        new_data = [(0, 0, 0, 0) if px[:3] == (0,0,0) else (*px[:3], 255) for px in datas]
        rgba.putdata(new_data)
        rgba.save(f"{filename}.png")
        messagebox.showinfo("Guardado", f"Imagen guardada como {filename}.png")

    btns = tk.Frame(win, bg=config.UI_BACKGROUND_COLOR)
    btns.pack(pady=10)
    tk.Button(btns, text="Previsualizar", command=procesar, bg=config.BUTTON_BG_COLOR, fg=config.BUTTON_FG_COLOR).pack(side='left', padx=10)
    tk.Button(btns, text="Exportar como PNG", command=exportar, bg=config.BUTTON_BG_COLOR, fg=config.BUTTON_FG_COLOR).pack(side='left', padx=10)
