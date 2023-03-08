from datetime import datetime
from pathlib import Path
from typing import List

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def hold_grudge(images, texts: List[str], args):
    date = datetime.today().strftime("%Y{}%m{}%d{}").format("年", "月", "日")
    text = f"{date} 晴\n{texts[0]}\n这个仇我先记下了"
    text2image = Text2Image.from_text(text, 45, fill="black", spacing=10).wrap(440)
    if len(text2image.lines) > 10:
        raise TextOverLength(texts[0])
    text_img = text2image.to_image()

    frame = BuildImage.open(img_dir / "0.png")
    bg = BuildImage.new(
        "RGB", (frame.width, frame.height + text_img.height + 20), "white"
    )
    bg.paste(frame).paste(text_img, (30, frame.height + 5), alpha=True)
    return bg.save_jpg()


add_meme(
    "hold_grudge",
    hold_grudge,
    min_texts=1,
    max_texts=1,
    default_texts=["群友不发涩图"],
    keywords=["记仇"],
)
