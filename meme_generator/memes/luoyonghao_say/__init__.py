from pathlib import Path
from typing import List

from PIL import ImageFilter
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def luoyonghao_say(images, texts: List[str], args):
    text = texts[0]
    frame = BuildImage.open(img_dir / "0.jpg")
    text_frame = BuildImage.new("RGBA", (365, 120))
    try:
        text_frame.draw_text(
            (40, 10, 325, 110),
            text,
            allow_wrap=True,
            max_fontsize=50,
            min_fontsize=10,
            valign="top",
        )
    except ValueError:
        raise TextOverLength(text)
    text_frame = text_frame.perspective(
        ((52, 10), (391, 0), (364, 110), (0, 120))
    ).filter(ImageFilter.GaussianBlur(radius=0.8))
    frame.paste(text_frame, (48, 246), alpha=True)
    return frame.save_jpg()


add_meme(
    "luoyonghao_say",
    luoyonghao_say,
    min_texts=1,
    max_texts=1,
    default_texts=["又不是不能用"],
    keywords=["罗永浩说"],
)
