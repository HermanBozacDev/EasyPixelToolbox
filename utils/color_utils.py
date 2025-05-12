from collections import Counter
from PIL import Image

def quantize_color(r, g, b, step=10):
    return tuple(min(max(round(c / step) * step, 0), 255) for c in (r, g, b))

def extract_palette(image_path, num_colors=32, step=10):
    image = Image.open(image_path).convert('RGBA')
    pixels = list(image.getdata())
    filtered_pixels = [
        quantize_color(r, g, b, step)
        for r, g, b, a in pixels
        if a > 10 and (r + g + b) > 10
    ]
    counter = Counter(filtered_pixels)
    most_common = counter.most_common(num_colors)
    return [tuple(color[:3]) for color, _ in most_common]

def rgb_to_gpl_string(palette, name="exported_palette"):
    lines = ["GIMP Palette", f"Name: {name}", "#"]
    for r, g, b in palette:
        lines.append(f"{r:3d} {g:3d} {b:3d}\tUntitled")
    return "\n".join(lines) + "\n"

def save_gpl_file(palette, output_path, name="exported_palette"):
    with open(output_path, 'w') as f:
        f.write(rgb_to_gpl_string(palette, name))