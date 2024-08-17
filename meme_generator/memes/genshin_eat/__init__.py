import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
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
from meme_generator.tags import MemeTags
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif

img_dir = Path(__file__).parent / "images"

help_text = "角色编号：1、八重神子，2、胡桃，3、妮露，4、可莉，5、刻晴，6、钟离"


class Model(MemeArgsModel):
    character: int = Field(0, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(character=i) for i in range(1, 7)],
    parser_options=[
        ParserOption(
            names=["-c", "--character", "角色"],
            args=[ParserArg(name="character", value="int")],
            help_text=help_text,
        ),
    ],
)


def genshin_eat(images: list[BuildImage], texts, args: Model):
    names = ["yae_miko", "hutao", "nilou", "klee", "keqing", "zhongli"]
    if args.character == 0:
        name = random.choice(names)
    elif args.character not in range(1, 7):
        raise MemeFeedback("角色编号错误，请选择1-6")
    else:
        name = names[args.character - 1]

    position_list = [(106, 245), (115, 224), (116, 205), (115, 198), (120, 217)]

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            chara = BuildImage.open(img_dir / name / f"{i:02d}.png")
            if i in range(4, 9):
                food = (
                    imgs[0].convert("RGBA").circle().resize((44, 44), keep_ratio=True)
                )
                if i == 8:
                    food = food.resize((44, 33))
                chara.paste(food, position_list[i - 4], alpha=True)
            return chara

        return make

    return make_gif_or_combined_gif(
        images, maker, 16, 0.08, FrameAlignPolicy.extend_loop
    )


add_meme(
    "genshin_eat",
    genshin_eat,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["原神吃"],
    shortcuts=[
        CommandShortcut(
            key=r"(?:八重神子|神子|八重)吃",
            args=["--character", "1"],
            humanized="八重神子吃",
        ),
        CommandShortcut(key="胡桃吃", args=["--character", "2"]),
        CommandShortcut(key="妮露吃", args=["--character", "3"]),
        CommandShortcut(key="可莉吃", args=["--character", "4"]),
        CommandShortcut(key="刻晴吃", args=["--character", "5"]),
        CommandShortcut(key="钟离吃", args=["--character", "6"]),
    ],
    tags=MemeTags.yae_miko
    | MemeTags.hutao
    | MemeTags.nilou
    | MemeTags.klee
    | MemeTags.keqing
    | MemeTags.zhongli,
    date_created=datetime(2024, 8, 6),
    date_modified=datetime(2024, 8, 10),
)
