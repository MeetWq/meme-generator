from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def love_you(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    frames: list[IMG] = []
    locs = [(68, 65, 70, 70), (63, 59, 80, 80)]
    for i in range(2):
        heart = BuildImage.open(img_dir / f"{i}.png")
        frame = BuildImage.new("RGBA", heart.size, "white")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True).paste(heart, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.2)


add_meme(
    "love_you",
    love_you,
    min_images=1,
    max_images=1,
    keywords=["永远爱你"],
    date_created=datetime(2022, 3, 13),
    date_modified=datetime(2023, 2, 14),
)
