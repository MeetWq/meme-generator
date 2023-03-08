from pathlib import Path
from typing import List

from PIL import ImageEnhance
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def incivilization(images: List[BuildImage], texts: List[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    points = ((0, 20), (154, 0), (164, 153), (22, 180))
    img = images[0].convert("RGBA").circle().resize((150, 150)).perspective(points)
    image = ImageEnhance.Brightness(img.image).enhance(0.8)
    frame.paste(image, (137, 151), alpha=True)
    text = texts[0] if texts else "你刚才说的话不是很礼貌！"
    try:
        frame.draw_text(
            (57, 42, 528, 117),
            text,
            weight="bold",
            max_fontsize=50,
            min_fontsize=20,
            allow_wrap=True,
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "incivilization",
    incivilization,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["你刚才说的话不是很礼貌！"],
    keywords=["不文明"],
)
