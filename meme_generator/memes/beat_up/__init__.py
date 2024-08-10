from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def beat_up(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((55, 55))
    user_head = images[1].convert("RGBA").circle().resize((45, 45))
    self_locs = [(100, 43), (110, 46), (101, 40)]
    user_locs = [(99, 136), (99, 136), (89, 140)]
    frames: list[IMG] = []
    for i in range(3):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(user_head, user_locs[i], alpha=True)
        frame.paste(self_head, self_locs[i], alpha=True)
        frames.append(frame.image)

    return save_gif(frames, 0.1)


add_meme(
    "beat_up",
    beat_up,
    min_images=2,
    max_images=2,
    keywords=["揍"],
    tags=MemeTags.tom | MemeTags.jerry,
    date_created=datetime(2024, 4, 9),
    date_modified=datetime(2024, 4, 9),
)
