from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def love_you(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()
    frames: List[IMG] = []
    locs = [(68, 65, 70, 70), (63, 59, 80, 80)]
    for i in range(2):
        heart = BuildImage.open(img_dir / f"{i}.png")
        frame = BuildImage.new("RGBA", heart.size, "white")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True).paste(heart, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.2)


add_meme("love_you", love_you, min_images=1, max_images=1, keywords=["永远爱你"])
