from pathlib import Path
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

help = "是否将图片变为黑白"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--black", "/黑白", action="store_true", help=help)


class Model(MemeArgsModel):
    black: bool = Field(False, description=help)


def mourning(images: List[BuildImage], texts, args: Model):
    frame = BuildImage.open(img_dir / "0.png")

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("L") if args.black else img.convert("RGBA")
        img = img.resize((635, 725), keep_ratio=True)
        return frame.copy().paste(img, (645, 145), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "mourning",
    mourning,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(parser, Model, [Model(black=False), Model(black=True)]),
    keywords=["上香"],
)
