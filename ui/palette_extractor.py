import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from utils import config, color_utils, image_utils
from ui.pixelator import open_pixelator_window

def open_palette_extractor_window(root):
    win = tk.Toplevel(root)
    win.title("Exportador de Paletas")
    win.geometry("800x600")
    win.configure(bg=config.UI_BACKGROUND_COLOR)
    win.lift()
    win.focus_force()

    check_vars = []
    zoom_level = 1.0
    canvas_offset = [175, 175]
    drag_start = [0, 0]
    image_original = None
    current_image_path = ""
    image_on_canvas = None

    def show_palette_selection(palette):
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        check_vars.clear()
        for color in palette:
            r, g, b = color
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            var = tk.BooleanVar(value=True)
            check_vars.append((var, (r, g, b)))
            frame = tk.Frame(scroll_frame, bg=config.UI_BACKGROUND_COLOR)
            frame.pack(fill='x')
            tk.Checkbutton(frame, variable=var, bg=config.UI_BACKGROUND_COLOR).pack(side='left')
            tk.Label(frame, bg=color_hex, width=4, height=1).pack(side='left', padx=4)
            tk.Label(frame, text=str((r, g, b)), fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).pack(side='left')

    def update_image_display():
        nonlocal image_on_canvas
        if image_original is None:
            return
        w, h = image_original.size
        scaled = image_original.resize((int(w * zoom_level), int(h * zoom_level)), Image.NEAREST)
        photo = ImageTk.PhotoImage(scaled)
        image_canvas.delete("all")
        image_on_canvas = image_canvas.create_image(canvas_offset[0], canvas_offset[1], anchor="center", image=photo)
        image_canvas.image = photo

    def select_image():
        nonlocal current_image_path, image_original
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if path:
            try:
                num_colors = int(entry_colors.get())
            except:
                num_colors = config.DEFAULT_NUM_COLORS
            current_image_path = path
            palette = color_utils.extract_palette(path, num_colors)
            show_palette_selection(palette)
            image_original = Image.open(path).convert("RGBA")
            update_image_display()

    def export_selected_palette():
        selected = [color for var, color in check_vars if var.get()]
        if not selected:
            return
        name = entry_name.get().strip() or config.DEFAULT_PALETTE_NAME
        folder = export_path_entry.get().strip() or os.getcwd()
        path = os.path.join(folder, f"{name}.gpl")
        color_utils.save_gpl_file(selected, path, name)
        messagebox.showinfo("Éxito", f"Paleta guardada en:\n{path}")

    def zoom_in():
        nonlocal zoom_level
        zoom_level *= 1.25
        update_image_display()

    def zoom_out():
        nonlocal zoom_level
        zoom_level /= 1.25
        update_image_display()

    def start_drag(e):
        drag_start[0], drag_start[1] = e.x, e.y

    def do_drag(e):
        dx, dy = e.x - drag_start[0], e.y - drag_start[1]
        canvas_offset[0] += dx
        canvas_offset[1] += dy
        drag_start[0], drag_start[1] = e.x, e.y
        update_image_display()

    # Layout
    header = tk.Frame(win, bg=config.UI_BACKGROUND_COLOR)
    header.pack(pady=4)

    tk.Label(header, text="Nombre del archivo GPL:", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).grid(row=0, column=0)
    entry_name = tk.Entry(header, width=30)
    entry_name.insert(0, config.DEFAULT_PALETTE_NAME)
    entry_name.grid(row=0, column=1)

    tk.Label(header, text="Cantidad de colores:", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).grid(row=1, column=0)
    entry_colors = tk.Entry(header, width=30)
    entry_colors.insert(0, str(config.DEFAULT_NUM_COLORS))
    entry_colors.grid(row=1, column=1)

    tk.Label(header, text="Ruta de exportación:", fg=config.UI_FOREGROUND_COLOR, bg=config.UI_BACKGROUND_COLOR).grid(row=2, column=0)
    export_path_entry = tk.Entry(header, width=30)
    export_path_entry.grid(row=2, column=1)

    tk.Button(header, text="Seleccionar imagen", command=select_image, bg=config.BUTTON_BG_COLOR, fg=config.BUTTON_FG_COLOR).grid(row=3, column=0, columnspan=2, pady=8)

    main_frame = tk.Frame(win, bg=config.UI_BACKGROUND_COLOR)
    main_frame.pack()
    left_frame = tk.Frame(main_frame, bg=config.UI_BACKGROUND_COLOR)
    left_frame.pack(side='left')
    right_frame = tk.Frame(main_frame, bg=config.UI_BACKGROUND_COLOR)
    right_frame.pack(side='right')

    canvas = tk.Canvas(left_frame, width=220, height=300, bg=config.UI_BACKGROUND_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(left_frame, command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=config.UI_BACKGROUND_COLOR)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both')
    scrollbar.pack(side='right', fill='y')

    image_canvas = tk.Canvas(right_frame, width=250, height=250, bg="white")
    image_canvas.pack(padx=4, pady=4)
    image_canvas.bind("<ButtonPress-1>", start_drag)
    image_canvas.bind("<B1-Motion>", do_drag)

    zoom_frame = tk.Frame(right_frame, bg=config.UI_BACKGROUND_COLOR)
    zoom_frame.pack()
    tk.Button(zoom_frame, text="🔍 +", command=zoom_in).pack(side='left')
    tk.Button(zoom_frame, text="🔍 -", command=zoom_out).pack(side='left')

    bottom = tk.Frame(win, bg=config.UI_BACKGROUND_COLOR)
    bottom.pack(pady=4)
    tk.Button(bottom, text="Exportar paleta seleccionada", command=export_selected_palette, bg=config.BUTTON_BG_COLOR, fg=config.BUTTON_FG_COLOR).pack(pady=5)

    tk.Button(bottom, text="🧩 Pixelar esta imagen", command=lambda: open_pixelator_window(win, current_image_path, [color for var, color in check_vars if var.get()]), bg=config.BUTTON_BG_COLOR, fg=config.BUTTON_FG_COLOR).pack(pady=5)

    extra = tk.Frame(win, bg=config.UI_BACKGROUND_COLOR)
    extra.pack(pady=2)
    tk.Button(extra, text="Seleccionar todo", command=lambda: [var.set(True) for var, _ in check_vars]).pack(side='left', padx=2)
    tk.Button(extra, text="Deseleccionar todo", command=lambda: [var.set(False) for var, _ in check_vars]).pack(side='left', padx=2)
    tk.Button(extra, text="Ordenar por R", command=lambda: show_palette_selection(sorted([color for _, color in check_vars], key=lambda c: c[0]))).pack(side='left', padx=2)
    tk.Button(extra, text="Ordenar por G", command=lambda: show_palette_selection(sorted([color for _, color in check_vars], key=lambda c: c[1]))).pack(side='left', padx=2)
    tk.Button(extra, text="Ordenar por B", command=lambda: show_palette_selection(sorted([color for _, color in check_vars], key=lambda c: c[2]))).pack(side='left', padx=2)

