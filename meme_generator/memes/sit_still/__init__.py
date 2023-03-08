from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def sit_still(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    name = texts[0] if texts else args.user_infos[0].name if args.user_infos else ""
    frame = BuildImage.open(img_dir / "0.png")
    if name:
        try:
            frame.draw_text(
                (100, 170, 600, 330),
                name,
                valign="bottom",
                max_fontsize=75,
                min_fontsize=30,
            )
        except ValueError:
            raise TextOverLength(name)
    img = images[0].convert("RGBA").circle().resize((150, 150)).rotate(-10, expand=True)
    frame.paste(img, (268, 344), alpha=True)
    return frame.save_jpg()


add_meme(
    "sit_still",
    sit_still,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["坐得住", "坐的住"],
)
