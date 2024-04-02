from pathlib import Path
from typing import List, Literal

from pil_utils import BuildImage

from meme_generator import add_meme, MemeArgsParser, MemeArgsModel, MemeArgsType
from meme_generator.utils import make_jpg_or_gif
from pydantic import Field

img_dir = Path(__file__).parent / "images"
parser = MemeArgsParser(prefix_chars="-/")
group = parser.add_mutually_exclusive_group()

group.add_argument(
    "-d",
    "--direction",
    type=str,
    choices=["left", "right", "center"],
    default="center",
    help=help,
)
group.add_argument(
    "--left", "/左", action="store_const", const="left", dest="direction"
)
group.add_argument(
    "--right", "/右", action="store_const", const="right", dest="direction"
)
group.add_argument(
    "--center", "/中间", action="store_const", const="center", dest="direction"
)


class Model(MemeArgsModel):
    direction: Literal["left", "right", "center"] = Field("center", description=help)


def fight_with_sunuo(images: List[BuildImage], texts, args: Model):
    frame = BuildImage.open(img_dir / "0.png")
    modes = {
        "center": "center",
        "left": "east",
        "right": "west",
    }

    def make(img: BuildImage) -> BuildImage:
        img = (
            img.convert("RGBA")
            .square()
            .resize((565, 1630), keep_ratio=True, direction=modes[args.direction])
        )
        return frame.copy().paste(img, (0, 245), below=True)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "fight_with_sunuo",
    fight_with_sunuo,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(
        parser,
        Model,
        [
            Model(direction="left"),
            Model(direction="right"),
            Model(direction="center"),
        ],
    ),
    keywords=["我打宿傩", "我打宿傩吗"],
)
