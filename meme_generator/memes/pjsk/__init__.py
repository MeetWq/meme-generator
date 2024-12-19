import random
from datetime import datetime
from pathlib import Path

from pydantic import Field

from meme_generator import (
    CommandShortcut,
    MemeArgsModel,
    MemeArgsType,
    ParserArg,
    ParserOption,
    add_meme,
)
from pil_utils import BuildImage

from meme_generator.tags import MemeTags
from meme_generator.exception import MemeFeedback,TextOverLength


img_dir = Path(__file__).parent / "images"

characters = [
    {
        "name_cn": "爱莉",
        "name_en": "airi",
        "color": "#FB8AAC",
        "img_num":15
    },
    {
        "name_cn": "彰人",
        "name_en": "akito",
        "color": "#FF7722",
        "img_num":13
    },
    {
        "name_cn": "杏",
        "name_en": "an",
        "color": "#00BADC",
        "img_num":13
    },
    {
        "name_cn": "梦",
        "name_en": "emu",
        "color": "#FF66BB",
        "img_num":13
    },
    {
        "name_cn": "绘名",
        "name_en": "ena",
        "color": "#B18F6C",
        "img_num":16
    },
    {
        "name_cn": "遥",
        "name_en": "haruka",
        "color": "#6495F0",
        "img_num":13
    },
    {
        "name_cn": "穗波",
        "name_en": "honami",
        "color": "#F86666",
        "img_num":15
    },
    {
        "name_cn": "一歌",
        "name_en": "ichika",
        "color": "#33AAEE",
        "img_num":15
    },
    {
        "name_cn": "KAITO",
        "name_en": "kaito",
        "color": "#3366CC",
        "img_num":13
    },
    {
        "name_cn": "奏",
        "name_en": "kanade",
        "color": "#BB6688",
        "img_num":14
    },
    {
        "name_cn": "心羽",
        "name_en": "kohane",
        "color": "#FF6699",
        "img_num":14
    },
    {
        "name_cn": "连",
        "name_en": "len",
        "color": "#D3BD00",
        "img_num":14
    },
    {
        "name_cn": "流歌",
        "name_en": "luka",
        "color": "#F88CA7",
        "img_num":13
    },
    {
        "name_cn": "真冬",
        "name_en": "mafuyu",
        "color": "#7171AF",
        "img_num":14
    },
    {
        "name_cn": "MEIKO",
        "name_en": "meiko",
        "color": "#E4485F",
        "img_num":13
    },
    {
        "name_cn": "初音未来",
        "name_en": "miku",
        "color": "#33CCBB",
        "img_num":13
    },
    {
        "name_cn": "实乃理",
        "name_en": "minori",
        "color": "#F39E7D",
        "img_num":14
    },
    {
        "name_cn": "瑞希",
        "name_en": "mizuki",
        "color": "#CA8DB6",
        "img_num":14
    },
    {
        "name_cn": "宁宁",
        "name_en": "nene",
        "color": "#19CD94",
        "img_num":13
    },
    {
        "name_cn": "铃",
        "name_en": "rin",
        "color": "#E8A505",
        "img_num":13
    },
    {
        "name_cn": "类",
        "name_en": "rui",
        "color": "#BB88EE",
        "img_num":16
    },
    {
        "name_cn": "咲希",
        "name_en": "saki",
        "color": "#F5B303",
        "img_num":15
    },
    {
        "name_cn": "志步",
        "name_en": "shiho",
        "color": "#A0C10B",
        "img_num":15
    },
    {
        "name_cn": "雫",
        "name_en": "shizuku",
        "color": "#5CD0B9",
        "img_num":13
    },
    {
        "name_cn": "冬弥",
        "name_en": "touya",
        "color": "#0077DD",
        "img_num":15
    },
    {
        "name_cn": "司",
        "name_en": "tsukasa",
        "color": "#F09A04",
        "img_num":15
    }
]

help_text = "角色编号：" + ",".join([f"{i+1}、{characters[i]['name_cn']}" for i in range(26)]) + "。"


class Model(MemeArgsModel):
    character: int = Field(0, description=help_text)
    number: int = Field(0, description="图片编号")

args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(character=i,number=0) for i in range(1, 27)],
    parser_options=[
        ParserOption(
            names=["-c", "--character", "角色编号"],
            args=[ParserArg(name="character", value="int")],
            help_text=help_text,
        ),
        ParserOption(
            names=["-n", "--number", "图片编号"],
            args=[ParserArg(name="number", value="int")],
            help_text="图片编号",
        ),
    ],
)


def pjsk(images, texts: list[str], args:Model):
    text = texts[0]

    character = None
    if args.character == 0:
        character = random.choice(characters)
    elif args.character in range(1, 27):
        character = characters[int(args.character) - 1]
    else:
        raise MemeFeedback(f"角色编号错误，请输入1-26")
    
    if args.number == 0:
        n = random.randint(0, character["img_num"])
    elif args.number in range(1, character["img_num"]+1):
        n = args.number - 1
    else:
        raise MemeFeedback(f"角色{character['name_cn']}的图片编号错误，请输入1-{character['img_num']}。")

    img = BuildImage.open(img_dir / character["name_en"] / f"{n:02d}.png")
    color = character["color"]
    w,h = img.size

    text_frame = BuildImage.new("RGBA", (w-20,50),)
    try:
        text_frame.draw_text(
            (0,0,w-20,50),
            text,
            fill=color,
            max_fontsize=50,
            min_fontsize=20,
            stroke_ratio=0.12,
            stroke_fill="white",
            font_families=["SSFangTangTi"]
        )
    except:
        raise TextOverLength(text)
    
    img.paste(
        text_frame.rotate(
            40 *(0.5- random.random()),
            expand=True
        ),
        (0,10),
        alpha=True
    )
    return img.save_png()


add_meme(
    "pjsk",
    pjsk,
    min_texts=1,
    max_texts=1,
    args_type=args_type,
    keywords=["世界计划"],
    shortcuts=[
        CommandShortcut(
            key="世界计划"+characters[i]['name_cn'],
            args = ["--character",f"{i+1}"]
        )
        for i in range(26)
    ],
    tags=MemeTags.project_sekai,
    date_created=datetime(2024, 12, 19),
    date_modified=datetime(2024, 12, 19),
)
