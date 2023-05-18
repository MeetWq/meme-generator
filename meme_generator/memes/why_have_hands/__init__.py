from pathlib import Path
from typing import List

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOrNameNotEnough, TextOverLength

img_dir = Path(__file__).parent / "images"


def why_have_hands(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    img = images[0].convert("RGBA")

    if not texts and not args.user_infos:
        raise TextOrNameNotEnough("why_have_hands")
    name = texts[0] if texts else args.user_infos[0].name

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img.circle().resize((250, 250)), (350, 670), alpha=True)
    frame.paste(
        img.resize((250, 250), keep_ratio=True).rotate(15), (1001, 668), below=True
    )
    frame.paste(img.resize((250, 170), keep_ratio=True), (275, 1100), below=True)
    frame.paste(
        img.resize((300, 400), keep_ratio=True, inside=True, direction="northwest"),
        (1100, 1060),
        alpha=True,
    )
    try:
        text_frame = BuildImage.new("RGBA", (600, 100)).draw_text(
            (0, 0, 600, 100),
            f"摸摸{name}!",
            max_fontsize=70,
            min_fontsize=30,
            halign="left",
            weight="bold",
        )
        frame.paste(text_frame.rotate(-15, expand=True), (75, 825), alpha=True)
        frame.draw_text(
            (840, 960, 1440, 1060),
            f"托托{name}!",
            max_fontsize=70,
            min_fontsize=30,
            weight="bold",
        )
        frame.draw_text(
            (50, 1325, 650, 1475),
            f"赞美{name}!",
            max_fontsize=90,
            min_fontsize=30,
            weight="bold",
            valign="top",
        )
        frame.draw_text(
            (700, 1340, 1075, 1490),
            f"为{name}奉献所有财产!",
            max_fontsize=70,
            min_fontsize=30,
            weight="bold",
            allow_wrap=True,
        )
    except ValueError:
        raise TextOverLength(name)

    return frame.save_jpg()


add_meme(
    "why_have_hands",
    why_have_hands,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["为什么要有手"],
)
