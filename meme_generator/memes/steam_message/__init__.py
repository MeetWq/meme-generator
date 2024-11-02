from datetime import datetime
from pathlib import Path

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

img_dir = Path(__file__).parent / "images"

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
    name = args.name or (args.user_infos[0].name if args.user_infos else "好友")
    game = texts[0]

    text_name = Text2Image.from_text(name, 65, fill="#e3ffc2")
    text_play = Text2Image.from_text("正在玩", 62, fill="#d1d1c0")
    text_game = Text2Image.from_text(game, 65, fill="#91c257")

    avatar_w = 280
    padding_h = 50
    padding_v = 80
    margin_rec = 6
    rec_w = 15
    margin_text = 80
    text_w = round(
        max(text_name.longest_line, text_play.longest_line, text_game.longest_line)
    )
    text_w = max(text_w, 1300)
    text_x = padding_h + avatar_w + margin_rec + rec_w + margin_text
    frame_w = text_x + text_w + padding_h
    frame_h = padding_v * 2 + avatar_w

    frame = BuildImage.new("RGBA", (frame_w, frame_h), "#14161f")
    frame.paste(
        BuildImage.new("RGB", (avatar_w, avatar_w), "#191b23"), (padding_h, padding_v)
    )
    avatar = images[0].convert("RGBA").resize((avatar_w, avatar_w), keep_ratio=True)
    frame.paste(avatar, (padding_h, padding_v), alpha=True)
    rec_x = padding_h + avatar_w + margin_rec
    frame.draw_rectangle(
        (rec_x, padding_v, rec_x + rec_w, frame_h - padding_v), fill="#6cbe48"
    )
    logo = BuildImage.open(img_dir / "logo.png")
    frame.alpha_composite(logo, (frame_w - 870, -370))
    text_play.draw_on_image(frame.image, (text_x, (frame_h - text_play.height) // 2))
    text_name.draw_on_image(
        frame.image, (text_x, padding_v + 40 - text_name.height // 2)
    )
    text_game.draw_on_image(
        frame.image, (text_x, frame_h - padding_v - 40 - text_game.height // 2)
    )

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
            args=["--name", "{name}", "{game}"],
            humanized="xx正在玩xx",
        )
    ],
    date_created=datetime(2024, 8, 21),
    date_modified=datetime(2024, 8, 21),
)
