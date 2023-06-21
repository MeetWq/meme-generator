from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

def add_confusion(images, texts: List[str], args):
    frame = BuildImage.new("RGBA", (240, 240))
    img = images[0].convert("RGBA").resize((240,240))
    img1 = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (0, 0), below=True)
    frame.paste(img1, (0, 0))
    return frame.save_jpg()

add_meme(
    "add_confusion",
    add_confusion,
    min_images=1,
    max_images=1,
    keywords=["给社会添乱", "添乱"],
)