from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def pat(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    locs = [(11, 73, 106, 100), (8, 79, 112, 96)]
    img_frames: list[IMG] = []
    for i in range(10):
        frame = BuildImage.open(img_dir / f"{i}.png")
        x, y, w, h = locs[1] if i == 2 else locs[0]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        img_frames.append(frame.image)
    # fmt: off
    seq = [0, 1, 2, 3, 1, 2, 3, 0, 1, 2, 3, 0, 0, 1, 2, 3, 0, 0, 0, 0, 4, 5, 5, 5, 6, 7, 8, 9]
    # fmt: on
    frames = [img_frames[n] for n in seq]
    return save_gif(frames, 0.085)


add_meme(
    "pat",
    pat,
    min_images=1,
    max_images=1,
    keywords=["拍"],
    date_created=datetime(2021, 12, 1),
    date_modified=datetime(2023, 2, 14),
)
