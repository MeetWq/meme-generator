from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def listen_music(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA")
    frame = BuildImage.open(img_dir / "0.png")
    frames: List[IMG] = []
    for i in range(0, 360, 10):
        frames.append(
            frame.copy()
            .paste(img.rotate(-i).resize((215, 215)), (100, 100), below=True)
            .image
        )
    return save_gif(frames, 0.05)


add_meme("listen_music", listen_music, min_images=1, max_images=1, keywords=["听音乐"])
