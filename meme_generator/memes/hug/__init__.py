from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def hug(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((120, 120))
    user_head = images[1].convert("RGBA").circle().resize((105, 105))
    # fmt: off
    user_locs = [
        (108, 15), (107, 14), (104, 16), (102, 14), (104, 15),
        (108, 15), (108, 15), (103, 16), (102, 15), (104, 14)
    ]
    self_locs = [
        (78, 120), (115, 130), (0, 0), (110, 100), (80, 100),
        (75, 115), (105, 127), (0, 0), (110, 98), (80, 105)
    ]
    rotate_num = [-48, -18, 0, 38, 31, -43, -22, 0, 34, 35]
    # fmt: on
    frames: list[IMG] = []
    for i in range(10):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(user_head, user_locs[i], below=True)
        img = self_head.rotate(rotate_num[i], expand=True)
        frame.paste(img, self_locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "hug",
    hug,
    min_images=2,
    max_images=2,
    keywords=["抱", "抱抱"],
    date_created=datetime(2024, 8, 6),
    date_modified=datetime(2024, 8, 6),
)
