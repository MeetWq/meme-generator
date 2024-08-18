from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def mahiro_readbook(images: list[BuildImage], texts, args):
    positions = [
        (0, 118),
        (0, 117),
        (0, 116),
        (0, 116),
        (-3, 116),
        (-7, 117),
    ]
    img = images[0].convert("RGBA").resize((70, 100), keep_ratio=True)
    img = img.perspective(((0, 6), (77, -5), (100, 100), (32, 100)))

    frames = []
    for i in range(48):
        bg = BuildImage.open(img_dir / f"{i}.png")
        frame = BuildImage.new("RGBA", (240, 240), "white")
        frame.paste(img, positions[min(max(i - 16, 0), 5)], alpha=True).paste(
            bg, alpha=True
        )
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "mahiro_readbook",
    mahiro_readbook,
    min_images=1,
    max_images=1,
    keywords=["真寻看书"],
    tags=MemeTags.mahiro,
    date_created=datetime(2024, 8, 18),
    date_modified=datetime(2024, 8, 18),
)
