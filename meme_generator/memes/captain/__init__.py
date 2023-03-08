from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def captain(images: List[BuildImage], texts, args):
    if len(images) == 2:
        images.append(images[-1])

    bg0 = BuildImage.open(img_dir / "0.png")
    bg1 = BuildImage.open(img_dir / "1.png")
    bg2 = BuildImage.open(img_dir / "2.png")

    frame = BuildImage.new("RGBA", (640, 440 * len(images)), "white")
    for i in range(len(images)):
        bg = bg0 if i < len(images) - 2 else bg1 if i == len(images) - 2 else bg2
        images[i] = images[i].convert("RGBA").square().resize((250, 250))
        bg = bg.copy().paste(images[i], (350, 85))
        frame.paste(bg, (0, 440 * i))

    return frame.save_jpg()


add_meme("captain", captain, min_images=2, max_images=5, keywords=["舰长"])
