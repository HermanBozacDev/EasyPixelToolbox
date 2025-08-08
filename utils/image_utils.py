import numpy as np
from PIL import Image


def approximate_image_to_palette(img, palette, block_size=1):
    img_data = np.array(img)
    h, w = img_data.shape[:2]
    palette_arr = np.asarray(palette, dtype=np.float32)

    # Determine number of blocks along each dimension
    bh = (h + block_size - 1) // block_size
    bw = (w + block_size - 1) // block_size

    # Pad image so it divides evenly into blocks
    pad_h = bh * block_size - h
    pad_w = bw * block_size - w
    padded = np.pad(img_data, ((0, pad_h), (0, pad_w), (0, 0)), mode="constant")

    # Compute average color for each block
    reshaped = padded.reshape(bh, block_size, bw, block_size, 3).astype(np.float32)
    sums = reshaped.sum(axis=(1, 3))

    mask = np.ones((h, w, 1), dtype=np.float32)
    mask_padded = np.pad(mask, ((0, pad_h), (0, pad_w), (0, 0)), mode="constant")
    counts = mask_padded.reshape(bh, block_size, bw, block_size, 1).sum(axis=(1, 3))
    avg_blocks = (sums / counts).reshape(-1, 3)

    # Find nearest palette color for each block
    diff = avg_blocks[:, None, :] - palette_arr[None, :, :]
    idx = np.argmin(np.sum(diff ** 2, axis=2), axis=1)
    block_colors = palette_arr[idx].reshape(bh, bw, 3).astype(np.uint8)

    # Expand block colors back to image shape
    new_data = np.repeat(np.repeat(block_colors, block_size, axis=0), block_size, axis=1)
    new_data = new_data[:h, :w]

    return Image.fromarray(new_data)
