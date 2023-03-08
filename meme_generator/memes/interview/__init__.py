from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def interview(images: List[BuildImage], texts: List[str], args):
    if len(images) == 2:
        self_img = images[0]
        user_img = images[1]
    else:
        self_img = BuildImage.open(img_dir / "huaji.png")
        user_img = images[0]
    self_img = self_img.convert("RGBA").square().resize((124, 124))
    user_img = user_img.convert("RGBA").square().resize((124, 124))

    text = texts[0] if texts else "采访大佬经验"

    frame = BuildImage.new("RGBA", (600, 310), "white")
    microphone = BuildImage.open(img_dir / "microphone.png")
    frame.paste(microphone, (330, 103), alpha=True)
    frame.paste(self_img, (419, 40), alpha=True)
    frame.paste(user_img, (57, 40), alpha=True)
    try:
        frame.draw_text((20, 200, 580, 310), text, max_fontsize=50, min_fontsize=20)
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "interview",
    interview,
    min_images=1,
    max_images=2,
    min_texts=0,
    max_texts=1,
    default_texts=["采访大佬经验"],
    keywords=["采访"],
)
