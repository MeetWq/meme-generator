from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from pydantic import Field

from meme_generator import (
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

help_pron = "人称代词，默认为“我”"
help_name = "称呼，默认为“老婆”"


class Model(MemeArgsModel):
    pronoun: str = Field("我", description=help_pron)
    name: str = Field("老婆", description=help_name)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-p", "--pron"],
            args=[ParserArg(name="pronoun", value="str")],
            dest="pronoun",
            help_text=help_pron,
        ),
        ParserOption(
            names=["-n", "--name"],
            args=[ParserArg(name="name", value="str")],
            dest="name",
            help_text=help_name,
        ),
    ],
)


def my_wife(images: list[BuildImage], texts, args: Model):
    img = images[0].convert("RGBA").resize_width(400)
    img_w, img_h = img.size
    frame = BuildImage.new("RGBA", (650, img_h + 500), "white")
    frame.paste(img, (int(325 - img_w / 2), 105), alpha=True)

    pron = args.pronoun
    name = args.name
    try:
        text = f"如果你的{name}长这样"
        frame.draw_text(
            (27, 12, 27 + 596, 12 + 79),
            text,
            max_fontsize=70,
            min_fontsize=30,
            allow_wrap=True,
            lines_align="center",
            font_style="bold",
        )
        text = f"那么这就不是你的{name}\n这是{pron}的{name}"
        frame.draw_text(
            (27, img_h + 120, 27 + 593, img_h + 120 + 135),
            text,
            max_fontsize=70,
            min_fontsize=30,
            allow_wrap=True,
            font_style="bold",
        )
        text = f"滚去找你\n自己的{name}去"
        frame.draw_text(
            (27, img_h + 295, 27 + 374, img_h + 295 + 135),
            text,
            max_fontsize=70,
            min_fontsize=30,
            allow_wrap=True,
            lines_align="center",
            font_style="bold",
        )
    except ValueError:
        raise TextOverLength(name)

    img_point = BuildImage.open(img_dir / "point.png").resize_width(200)
    frame.paste(img_point, (421, img_h + 270))

    return frame.save_jpg()


add_meme(
    "my_wife",
    my_wife,
    min_images=1,
    max_images=1,
    keywords=["我老婆", "这是我老婆"],
    args_type=args_type,
    date_created=datetime(2022, 7, 29),
    date_modified=datetime(2024, 8, 12),
)
