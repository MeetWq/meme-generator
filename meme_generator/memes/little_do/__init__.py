from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from meme_generator.utils import save_gif
from PIL.Image import Image as IMG
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def little_do(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((21, 21))
    user_head = images[1].convert("RGBA").circle().resize((21, 21)).rotate(90)
    frames: list[IMG] = []
    for i in range(7):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(self_head, (40, 4), alpha=True)
        frame.paste(user_head, (6, 46), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "little_do",
    little_do,
    min_images=2,
    max_images=2,
    keywords=["小撅", "轻撅", "滑稽撅"],
    date_created=datetime(2024, 7, 12),
    date_modified=datetime(2024, 7, 12),
)
