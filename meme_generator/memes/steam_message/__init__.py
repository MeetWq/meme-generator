from datetime import datetime

from pil_utils import BuildImage, Text2Image
from pydantic import Field

from meme_generator import (
    CommandShortcut,
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from meme_generator.exception import MemeFeedback

help_text = "指定名字"


class Model(MemeArgsModel):
    name: str = Field("", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    parser_options=[
        ParserOption(
            names=["-n", "--name"],
            args=[ParserArg(name="name", value="str")],
            help_text=help_text,
        ),
    ],
)


def steam_message(images: list[BuildImage], texts: list[str], args: Model):
    name = args.name or (args.user_infos[0].name if args.user_infos else "")
    if not name:
        raise MemeFeedback("请指定名字")
    game = texts[0]
    image = images[0].convert("RGBA").resize((280, 280), keep_ratio=True)

    text_name = Text2Image.from_text(name, 70, fill="#e3ffc2")
    text_play = Text2Image.from_text("正在玩", 60, fill="#d1d1c0")
    text_game = Text2Image.from_text(game, 70, fill="#91c257")

    frame_w = max(text_name.width, text_play.width, text_game.width, 550) + 450
    frame_h = 390
    frame = BuildImage.new("RGB", (frame_w, frame_h), "#14161f")
    frame.paste(BuildImage.new("RGB", (280, 280), "#191b23"), (40, 55))
    frame.paste(image, (40, 55), alpha=True)
    frame.draw_rectangle((330, 55, 348, 335), fill="#6cbe48")

    text_play.draw_on_image(frame.image, (400, (frame_h - text_play.height) // 2))
    text_name.draw_on_image(frame.image, (400, 100 - text_name.height // 2))
    text_game.draw_on_image(frame.image, (400, 290 - text_game.height // 2))
    return frame.save_jpg()


add_meme(
    "steam_message",
    steam_message,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=1,
    default_texts=["黑神话：悟空"],
    args_type=args_type,
    keywords=["steam消息"],
    shortcuts=[
        CommandShortcut(
            key=r"(?P<name>\S+)正在玩(?P<game>\S+)",
            args=["{game}", "--name", "{name}"],
            humanized="xx正在玩xx",
        )
    ],
    date_created=datetime(2024, 8, 21),
    date_modified=datetime(2024, 8, 21),
)
