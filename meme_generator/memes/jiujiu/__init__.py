from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def jiujiu(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((75, 51), keep_ratio=True)
    frames: list[IMG] = []
    for i in range(8):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.06)


add_meme(
    "jiujiu",
    jiujiu,
    min_images=1,
    max_images=1,
    keywords=["啾啾"],
    date_created=datetime(2022, 4, 20),
    date_modified=datetime(2023, 2, 14),
)
