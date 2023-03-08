from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def run(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.png")
    text_img = BuildImage.new("RGBA", (122, 53))
    try:
        text_img.draw_text(
            (0, 0, 122, 53),
            text,
            allow_wrap=True,
            max_fontsize=50,
            min_fontsize=10,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)
    frame.paste(text_img.rotate(7, expand=True), (200, 195), alpha=True)
    return frame.save_jpg()


add_meme("run", run, min_texts=1, max_texts=1, default_texts=["快跑"], keywords=["快跑"])
