import numpy as np
from PIL import Image

def approximate_image_to_palette(img, palette, block_size=1):
    img_data = np.array(img)
    h, w = img_data.shape[:2]
    new_data = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = img_data[y:y+block_size, x:x+block_size]
            flat = block.reshape(-1, 3)
            avg = np.mean(flat, axis=0)
            avg_int = tuple(map(int, avg))
            new_color = min(palette, key=lambda c: sum((a - b) ** 2 for a, b in zip(avg_int, c)))
            new_data[y:y+block_size, x:x+block_size] = new_color
    return Image.fromarray(new_data)