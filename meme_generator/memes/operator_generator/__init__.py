import random
from datetime import datetime
from pathlib import Path

from meme_generator import add_meme
from pil_utils import BuildImage

img_dir = Path(__file__).parent / "images"


def operator_generator(images: list[BuildImage], texts: list[str], args):
    img = images[0].convert("RGBA").circle().resize((80, 80))
    name = texts[0] if texts else "你好"

    frame = BuildImage.new("RGBA", (640, 640), (160, 160, 160))
    frame.paste(img, (20, 10), alpha=True)
    frame.draw_text(
        (120, 0, 620, 100),
        f"{name}，你的干员信息如下：",
        fontsize=80,
        fill="white",
        stroke_fill="black",
        stroke_ratio=0.1,
        weight="bold",
        allow_wrap=True,
        lines_align="center",
    )

    rrange = BuildImage.open(
        img_dir / f"1范围/范围101-25-{random.randint(0, 24):04d}.jpg"
    ).resize_width(320)
    frame.paste(rrange, (0, 100))
    rcharacteristic = BuildImage.open(
        img_dir / f"2特性/特性202-25-{random.randint(0, 24):04d}.jpg"
    ).resize_width(320)
    frame.paste(rcharacteristic, (320, 100))
    rvalue = BuildImage.open(
        img_dir / f"3基础数值/基础数值3031-{random.randint(0, 24):04d}.jpg"
    ).resize_width(320)
    frame.paste(rvalue, (0, 280))
    rtalent = BuildImage.open(
        img_dir / f"4天赋/天赋404-25-{random.randint(0, 24):04d}.jpg"
    ).resize_width(320)
    frame.paste(rtalent, (320, 280))
    rskill = BuildImage.open(
        img_dir / f"5技能/技能505-25-{random.randint(0, 24):04d}.jpg"
    ).resize_width(320)
    frame.paste(rskill, (0, 460))
    rspecail = BuildImage.open(
        img_dir / f"6亮点毒点/亮点毒点606-{random.randint(0, 24):04d}.jpg"
    ).resize_width(320)
    frame.paste(rspecail, (320, 460))

    return frame.save_jpg()


add_meme(
    "operator_generator",
    operator_generator,
    min_images=1,
    max_images=1,
    max_texts=1,
    keywords=["合成大干员"],
    date_created=datetime(2023, 3, 28),
    date_modified=datetime(2023, 3, 28),
)
