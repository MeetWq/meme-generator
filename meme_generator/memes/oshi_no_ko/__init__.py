from pathlib import Path
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.utils import make_png_or_gif
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

help = "指定名字"

parser = MemeArgsParser()
parser.add_argument("-n", "--name", type=str, default="", help=help)


class Model(MemeArgsModel):
    name: str = Field("", description=help)


def OSHI_NO_KO(images: List[BuildImage], texts, args: Model):
    name = args.name or "网友"

    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (430, 28, 614, 175),
            name,
            max_fontsize=200,
            min_fontsize=76,
            stroke_ratio=0.05,
            stroke_fill="white",
        )
    except ValueError:
        raise TextOverLength(name)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((691, 691), keep_ratio=True)
        return frame.copy().paste(img, (0, 0), alpha=True, below=True)

    return make_png_or_gif(images[0], make)


add_meme(
    "oshi_no_zo",
    OSHI_NO_KO,
    min_images=1,
    max_images=1,
    max_texts=1,
    default_texts=["网友"],
    args_type=MemeArgsType(parser, Model),
    keywords=["我推的网友"],
)