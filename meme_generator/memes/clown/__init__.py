from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme

IMG_DIR = Path(__file__).parent / "images"
CIRCLE_PATH = IMG_DIR / "circle.png"
PERSON_PATH = IMG_DIR / "person.png"


@dataclass
class PicInfo:
    frame_path: Path
    avatar_size: Tuple[int, int]
    avatar_rotate: int
    avatar_left_center: Tuple[int, int]  # top right 直接算镜像


CIRCLE_INFO = PicInfo(CIRCLE_PATH, (554, 442), 26, (153, 341))
PERSON_INFO = PicInfo(PERSON_PATH, (434, 467), 26, (174, 378))


HELP_PERSON = "是否使用爷爷头轮廓"

parser = MemeArgsParser(prefix_chars="-/")
parser.add_argument("--person", "/爷", action="store_true", help=HELP_PERSON)


class Model(MemeArgsModel):
    person: bool = Field(False, description=HELP_PERSON)


def clown(images: List[BuildImage], texts, args: Model):  # noqa: ARG001
    info = PERSON_INFO if args.person else CIRCLE_INFO
    avatar = images[0].convert("RGBA").resize(info.avatar_size, keep_ratio=True)
    frame = BuildImage.open(info.frame_path).convert("RGBA")

    img_size = frame.size
    bg = BuildImage.new("RGBA", img_size, (255, 255, 255))  # white bg

    left_part = avatar.crop(
        (0, 0, avatar.width // 2, avatar.height),
    ).rotate(info.avatar_rotate, expand=True)
    right_part = avatar.crop(
        (avatar.width // 2, 0, avatar.width, avatar.height)
    ).rotate(-info.avatar_rotate, expand=True)

    img_w = bg.width
    left_center_x, center_y = info.avatar_left_center  # 左半边中心 x, 中心 y
    left_top_x = left_center_x - left_part.width // 2  # 左半边左上 x
    top_y = center_y - left_part.height // 2  # 左上 y
    right_top_x = img_w - left_top_x - right_part.width  # 右半边左上 x

    bg.paste(left_part, (left_top_x, top_y), alpha=True)
    bg.paste(right_part, (right_top_x, top_y), alpha=True)
    bg.paste(frame, alpha=True)

    return bg.save_png()


add_meme(
    "clown",
    clown,
    min_images=1,
    max_images=1,
    args_type=MemeArgsType(parser, Model, [Model(person=False), Model(person=True)]),
    keywords=["小丑"],
)
