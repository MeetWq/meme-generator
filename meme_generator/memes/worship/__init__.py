from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def worship(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA")
    points = ((0, -30), (135, 17), (135, 145), (0, 140))
    paint = img.square().resize((150, 150)).perspective(points)
    frames: list[IMG] = []
    for i in range(10):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(paint, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


add_meme(
    "worship",
    worship,
    min_images=1,
    max_images=1,
    keywords=["膜", "膜拜"],
    date_created=datetime(2022, 2, 10),
    date_modified=datetime(2023, 2, 14),
)
