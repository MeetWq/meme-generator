from io import BytesIO

import anyio
from meme_generator import add_meme
from pil_utils import BuildImage
from pyparsing import List

BACKGROUND_PATH = anyio.Path(__file__).parent / "images" / "osu.png"


async def osu(images, texts: List[str], args) -> BytesIO:  # noqa: ARG001
    return (
        BuildImage.open(BytesIO(await BACKGROUND_PATH.read_bytes()))
        .convert("RGBA")
        .draw_text(
            (80, 80, 432, 432),
            texts[0],
            max_fontsize=192,
            weight="bold",
            fill="white",
            lines_align="center",
            fontname="Aller",
        )
        .save_png()
    )


add_meme(
    "osu",
    osu,
    min_texts=1,
    max_texts=1,
    default_texts=["hso!"],
    keywords=["osu"],
)
