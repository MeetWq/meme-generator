from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif


def funny_mirror(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((500, 500))
    frames: List[IMG] = [img.image]
    coeffs = [0.01, 0.03, 0.05, 0.08, 0.12, 0.17, 0.23, 0.3, 0.4, 0.6]
    borders = [25, 52, 67, 83, 97, 108, 118, 128, 138, 148]
    for i in range(10):
        new_size = 500 - borders[i] * 2
        new_img = img.distort((coeffs[i], 0, 0, 0)).resize_canvas((new_size, new_size))
        frames.append(new_img.resize((500, 500)).image)
    frames.extend(frames[::-1])
    return save_gif(frames, 0.05)


add_meme("funny_mirror", funny_mirror, min_images=1, max_images=1, keywords=["哈哈镜"])
