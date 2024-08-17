from datetime import datetime
from pathlib import Path

from arclet.alconna import store_true
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsType, ParserOption, add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"

help_text = "是否将图片变为黑白"


class Model(MemeArgsModel):
    black: bool = Field(False, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(black=False), Model(black=True)],
    parser_options=[
        ParserOption(
            names=["--black", "黑白"],
            default=False,
            action=store_true,
            help_text=help_text,
        ),
    ],
)


def mourning(images: list[BuildImage], texts, args: Model):
    frame = BuildImage.open(img_dir / "0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0]
        img = img.convert("L") if args.black else img.convert("RGBA")
        img = img.resize((635, 725), keep_ratio=True)
        return frame.copy().paste(img, (645, 145), below=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "mourning",
    mourning,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["上香"],
    date_created=datetime(2023, 7, 29),
    date_modified=datetime(2023, 7, 29),
)
