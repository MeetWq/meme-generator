from pathlib import Path
from typing import List

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

help = "是否使用默认文字"
default_text = "所谓的男人啊，只要送他们这种东西就会很开心"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("-d", "--default", "/默认", action="store_true", help=help)


class Model(MemeArgsModel):
    default: bool = Field(False, description=help)


def frieren_take(images: List[BuildImage], texts: List[str], args: Model):
    frame = BuildImage.open(img_dir / "0.png")
    text = default_text if args.default else texts[0] if texts else None
    if text:
        try:
            frame.draw_text(
                (100, frame.height - 120, frame.width - 100, frame.height),
                text,
                max_fontsize=50,
                min_fontsize=20,
                fill="white",
                stroke_fill="black",
                stroke_ratio=0.05,
            )
        except ValueError:
            raise TextOverLength(text)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((102, 108), keep_ratio=True)
        return frame.copy().paste(img, (130, 197), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "frieren_take",
    frieren_take,
    min_images=1,
    max_images=1,
    max_texts=1,
    default_texts=[default_text],
    args_type=MemeArgsType(parser, Model, [Model(default=False), Model(default=True)]),
    keywords=["芙莉莲拿"],
)
