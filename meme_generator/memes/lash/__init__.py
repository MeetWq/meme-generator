from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from meme_generator.utils import save_gif
from PIL.Image import Image as IMG
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def lash(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((22, 22))
    user_head = images[1].convert("RGBA").circle().resize((22, 22))
    # fmt: off
    self_locs = [
        (84,25), (87,23), (87,27), (86,28), (62,26),
        (59,28), (76,20), (85,24), (80,23),
    ]
    user_locs = [
        (12,69), (15,66), (14,67), (15,66), (17,67),
        (14,63), (21,56), (15,62), (17,69)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(9):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(self_head, self_locs[i], alpha=True)
        frame.paste(user_head, user_locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "lash",
    lash,
    min_images=2,
    max_images=2,
    keywords=["鞭笞", "鞭打", "鞭挞", "鞭策"],
    date_created=datetime(2024, 7, 23),
    date_modified=datetime(2024, 7, 23),
)
