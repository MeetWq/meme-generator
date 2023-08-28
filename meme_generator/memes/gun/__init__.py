from pathlib import Path
from typing import List, Literal

from PIL.Image import Transpose
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme

img_dir = Path(__file__).parent / "images"


help = "枪的位置"

parser = MemeArgsParser(prefix_chars="-/")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-p",
    "--position",
    dest="position",
    type=str,
    choices=["left", "right", "both"],
    default="left",
    help=help,
)
group.add_argument("--left", "/左手", action="store_const", const="left", dest="position")
group.add_argument(
    "--right", "/右手", action="store_const", const="right", dest="position"
)
group.add_argument("--both", "/双手", action="store_const", const="both", dest="position")


class Model(MemeArgsModel):
    position: Literal["left", "right", "both"] = Field("left", description=help)


def gun(images: List[BuildImage], texts, args: Model):
    frame = images[0].convert("RGBA").resize((500, 500), keep_ratio=True)
    gun = BuildImage.open(img_dir / "0.png")
    position = args.position
    left = position in ["left", "both"]
    right = position in ["right", "both"]
    if left:
        frame.paste(gun, alpha=True)
    if right:
        frame.paste(gun.transpose(Transpose.FLIP_LEFT_RIGHT), alpha=True)
    return frame.save_jpg()


add_meme(
    "gun",
    gun,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(
        parser,
        Model,
        [Model(position="left"), Model(position="right"), Model(position="both")],
    ),
    keywords=["手枪"],
)
