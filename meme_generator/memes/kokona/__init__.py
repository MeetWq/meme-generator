import random
from typing import Literal
from pathlib import Path
from pydantic import Field
from meme_generator import add_meme, MemeArgsModel, MemeArgsType, ParserArg, ParserOption
from arclet.alconna import store_value
from pil_utils import BuildImage
from meme_generator.exception import MemeFeedback, TextOverLength


img_dir = Path(__file__).parent / "images"

help_text = "消息框的位置，包含 left、right、both"


class Model(MemeArgsModel):
    position: Literal["left", "right", "both"] = Field("both", description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[
        Model(position="left"),
        Model(position="right"),
        Model(position="both"),
    ],
    parser_options=[
        ParserOption(
            names=["-p", "--position"],
            args=[ParserArg(name="position", value="str")],
            help_text=help_text,
        ),
        ParserOption(
            names=["--left", "左边"], dest="position", action=store_value("left")
        ),
        ParserOption(
            names=["--right", "右边"], dest="position", action=store_value("right")
        ),
        ParserOption(
            names=["--both", "两边"], dest="position", action=store_value("both")
        ),
    ],
)

def kokona(images: list[BuildImage], texts, args: Model):
    position = args.position 
    left = position in ["left", "both"]
    right = position in ["right", "both"]

    img_name = "01.png" if left and not right else "02.png" if right and not left else f"{random.randint(1, 2):02d}.png"

    frame = BuildImage.open(img_dir / img_name)
    text = texts[0]

    try:
        if left and img_name == "01.png":
            frame.draw_text(
                (0, 0, 680, 220),
                text,
                max_fontsize=70,
                min_fontsize=30,
                fill="black",
                lines_align="center"
            )
        if right and img_name == "02.png":
            frame.draw_text(
                (frame.height - 680, 0, frame.height, 220),
                text,
                max_fontsize=70,
                min_fontsize=30,
                fill="black",
                lines_align="center"
            )
    except TextOverLength:
        raise TextOverLength(text)

    return frame.save_png()


add_meme(
    "kokona",  
    kokona,  
    min_texts=1, 
    max_texts=1, 
    default_texts=["那我问你"], 
    args_type=args_type,
    keywords=["春原心奈", "春原心菜"], 
)
