from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import CommandShortcut, add_meme
from meme_generator.utils import make_png_or_gif

img_dir = Path(__file__).parent / "images"

default_text = "心脏病 高血压 心律不齐 心肌梗塞 失眠 脱发 呼吸困难 胸闷气短 缺氧 躁郁 焦虑 脑供血不足 心慌心悸 心脑血管炸裂"


def caused_by_this(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = texts[0] if texts else default_text
    frame.draw_text(
        (130, 760, 400, 1000), text, max_fontsize=60, min_fontsize=10, allow_wrap=True
    )

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((550, 360), keep_ratio=True)
        result = BuildImage.new("RGBA", frame.size, (255, 255, 255, 255))
        result.paste(img, (122, 9), alpha=True).paste(frame, alpha=True)
        return result

    return make_png_or_gif(images, make)


add_meme(
    "caused_by_this",
    caused_by_this,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["这个引起的"],
    shortcuts=[
        CommandShortcut(
            key=r"你的(?P<text>.+?)(?:主要)?都?是由?这个引起的",
            args=["{text}"],
            humanized="你的xx主要都是由这个引起的",
        ),
    ],
    date_created=datetime(2024, 11, 18),
    date_modified=datetime(2024, 11, 18),
)
