import random
from typing import List
from pathlib import Path
from pil_utils import BuildImage
from argparse import ArgumentParser

from meme_generator import add_meme, MemeArgsType, MemeArgsModel


img_dir = Path(__file__).parent / "images"


parser = ArgumentParser()
parser.add_argument("-n", "--number", type=int, default=0)


class Model(MemeArgsModel):
    number: int = 0


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
