from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def potato(images: List[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")
    img = images[0].convert("RGBA").square().resize((458, 458))
    frame.paste(img.rotate(-5), (531, 15), below=True)
    return frame.save_jpg()


add_meme("potato", potato, min_images=1, max_images=1, keywords=["土豆"])
