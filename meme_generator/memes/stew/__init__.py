from pathlib import Path
from typing import List

from pil_utils import BuildImage
from pydantic import Field
from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

help = "指定名字"

parser = MemeArgsParser()
parser.add_argument("-n", "--name", type=str, default="", help=help)


class Model(MemeArgsModel):
    name: str = Field("", description=help)

def stew(images: List[BuildImage], texts, args):
    name = args.name or (args.user_infos[-1].name if args.user_infos else "") or "群友"
    if len(name) > 30:
        name = name[:30]
    text = f"生活不易,炖{name}出气"

    frame = BuildImage.open(img_dir / "0.png")
    try:
        frame.draw_text(
            (2, frame.height - 30, frame.width - 2, frame.height),
            text,
            allow_wrap=True,
            max_fontsize=50,
            min_fontsize=6,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((181, 154), keep_ratio=True)
        return frame.copy().paste(img, (9, -2), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme("stew", stew, min_images=1, max_images=1, args_type=MemeArgsType(parser, Model), keywords=["炖"])
