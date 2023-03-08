from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def beat_head(images: List[BuildImage], texts: List[str], args):
    text = texts[0] if texts else "怎么说话的你"
    img = images[0].convert("RGBA")
    locs = [(160, 121, 76, 76), (172, 124, 69, 69), (208, 166, 52, 52)]
    frames: List[IMG] = []
    for i in range(3):
        x, y, w, h = locs[i]
        head = img.resize((w, h), keep_ratio=True).circle()
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(head, (x, y), below=True)
        try:
            frame.draw_text(
                (175, 28, 316, 82),
                text,
                max_fontsize=50,
                min_fontsize=10,
                allow_wrap=True,
            )
        except ValueError:
            raise TextOverLength(text)

        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "beat_head",
    beat_head,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["拍头"],
)
