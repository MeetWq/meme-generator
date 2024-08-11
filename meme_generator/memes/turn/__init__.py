import random
from datetime import datetime

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif


def turn(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle()
    frames: list[IMG] = []
    for i in range(0, 360, 10):
        frame = BuildImage.new("RGBA", (250, 250), "white")
        frame.paste(img.rotate(i).resize((250, 250)), alpha=True)
        frames.append(frame.image)
    if random.randint(0, 1):
        frames.reverse()
    return save_gif(frames, 0.05)


add_meme(
    "turn",
    turn,
    min_images=1,
    max_images=1,
    keywords=["转"],
    date_created=datetime(2022, 1, 1),
    date_modified=datetime(2023, 2, 14),
)
