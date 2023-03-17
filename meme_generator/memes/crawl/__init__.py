import random
from pathlib import Path
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme

img_dir = Path(__file__).parent / "images"


help = "图片编号，范围为 1~92"

parser = MemeArgsParser()
parser.add_argument("-n", "--number", type=int, default=0, help=help)


class Model(MemeArgsModel):
    number: int = Field(0, description=help)


def crawl(images: List[BuildImage], texts: List[str], args: Model):
    total_num = 92
    if 1 <= args.number <= total_num:
        num = args.number
    else:
        num = random.randint(1, total_num)

    img = images[0].convert("RGBA").circle().resize((100, 100))
    frame = BuildImage.open(img_dir / f"{num:02d}.jpg")
    frame.paste(img, (0, 400), alpha=True)
    return frame.save_jpg()


add_meme(
    "crawl",
    crawl,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(parser, Model),
    keywords=["爬"],
)
