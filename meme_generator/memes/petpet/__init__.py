from datetime import datetime
from pathlib import Path

from arclet.alconna import store_true
from PIL.Image import Image as IMG
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsType, ParserOption, add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

help_text = "是否将图片变为圆形"


class Model(MemeArgsModel):
    circle: bool = Field(False, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(circle=False), Model(circle=True)],
    parser_options=[
        ParserOption(
            names=["--circle", "圆"],
            default=False,
            action=store_true,
            help_text=help_text,
        ),
    ],
)


def petpet(images: list[BuildImage], texts, args: Model):
    img = images[0].convert("RGBA").square()
    if args.circle:
        img = img.circle()

    frames: list[IMG] = []
    locs = [
        (14, 20, 98, 98),
        (12, 33, 101, 85),
        (8, 40, 110, 76),
        (10, 33, 102, 84),
        (12, 20, 98, 98),
    ]
    for i in range(5):
        hand = BuildImage.open(img_dir / f"{i}.png")
        frame = BuildImage.new("RGBA", hand.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True)
        frame.paste(hand, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.06)


add_meme(
    "petpet",
    petpet,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["摸", "摸摸", "摸头", "rua"],
    date_created=datetime(2021, 5, 4),
    date_modified=datetime(2023, 2, 11),
)
