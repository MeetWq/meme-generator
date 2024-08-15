from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def hutao_bite(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((100, 100))
    frames: list[IMG] = []
    locs = [(98, 101, 108, 234), (96, 100, 108, 237)]
    for i in range(2):
        frame = BuildImage.open(img_dir / f"{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "hutao_bite",
    hutao_bite,
    min_images=1,
    max_images=1,
    keywords=["胡桃啃"],
    tags=MemeTags.hutao,
    date_created=datetime(2022, 11, 29),
    date_modified=datetime(2023, 2, 14),
)
