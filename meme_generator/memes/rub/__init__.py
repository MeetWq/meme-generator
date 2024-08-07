from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def rub(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle()
    user_head = images[1].convert("RGBA").circle()
    # fmt: off
    user_locs = [
        (39, 91, 75, 75), (49, 101, 75, 75), (67, 98, 75, 75),
        (55, 86, 75, 75), (61, 109, 75, 75), (65, 101, 75, 75)
    ]
    self_locs = [
        (102, 95, 70, 80, 0), (108, 60, 50, 100, 0), (97, 18, 65, 95, 0),
        (65, 5, 75, 75, -20), (95, 57, 100, 55, -70), (109, 107, 65, 75, 0)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(6):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, w, h = user_locs[i]
        frame.paste(user_head.resize((w, h)), (x, y), alpha=True)
        x, y, w, h, angle = self_locs[i]
        frame.paste(
            self_head.resize((w, h)).rotate(angle, expand=True), (x, y), alpha=True
        )
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "rub",
    rub,
    min_images=2,
    max_images=2,
    keywords=["贴", "贴贴", "蹭", "蹭蹭"],
    date_created=datetime(2021, 6, 11),
    date_modified=datetime(2023, 2, 14),
)
