from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def blamed_mahiro(images, texts: list[str], args):
    text = "傻逼" if not len(texts) else texts[0]
    params = [
        None,
        None,
        ([(70, 0), (50, 84), (50, 84), (0, 1)], (98, 94)),
        ([(70, 0), (50, 84), (50, 84), (0, 1)], (98, 94)),
        ([(55, 0), (55, 128), (45, 208), (0, 32)], (183, 16)),
        ([(58, 0), (98, 148), (76, 162), (0, 34)], (254, -4)),
        ([(68, 0), (114, 164), (95, 172), (0, 46)], (244, 4)),
        ([(64, 0), (126, 156), (98, 172), (0, 54)], (240, 20)),
        ([(71, 0), (159, 185), (129, 203), (0, 40)], (202, 70)),
        ([(71, 0), (159, 185), (129, 203), (0, 40)], (202, 70)),
        ([(67, 0), (143, 187), (111, 201), (0, 33)], (198, 91)),
        ([(66, 0), (131, 195), (98, 211), (0, 33)], (186, 83)),
        ([(66, 0), (131, 195), (98, 211), (0, 33)], (186, 83)),
        ([(65, 0), (108, 195), (81, 204), (0, 28)], (166, 37)),
        ([(66, 0), (96, 190), (68, 197), (0, 28)], (164, 8)),
        ([(66, 0), (96, 190), (68, 197), (0, 28)], (164, 8)),
        ([(70, 0), (91, 186), (65, 197), (0, 26)], (162, -6)),
        ([(70, 0), (91, 187), (65, 197), (0, 27)], (158, -20)),
        ([(70, 0), (91, 187), (65, 197), (0, 27)], (158, -20)),
        ([(74, 0), (82, 190), (58, 197), (0, 30)], (174, -13)),
        ([(74, 0), (84, 192), (59, 200), (0, 35)], (182, -12)),
        ([(74, 0), (84, 192), (59, 200), (0, 35)], (182, -12)),
        ([(78, 0), (86, 196), (62, 205), (0, 35)], (182, -10)),
        ([(76, 0), (84, 194), (58, 205), (0, 36)], (188, -9)),
    ]
    frames = []
    text_frame = BuildImage.new("RGBA", (400, 80))
    try:
        text_frame.draw_text(
            (0, -5, 350, 85),
            text,
            max_fontsize=80,
            min_fontsize=60,
            allow_wrap=False,
            font_families=["FZKaTong-M19S"],
            halign="left",
            fill=(108, 60, 82, 255),
            stroke_ratio=0.01,
            stroke_fill=(255, 255, 255, 255),
        )
    except ValueError:
        raise TextOverLength(text)
    for i, param in enumerate(params):
        bg = BuildImage.open(img_dir / f"{i}.png")
        if i > 1:
            frame = text_frame.perspective(param[0])
            bg.paste(frame, param[1], alpha=True)
        frames.append(bg.image)
    return save_gif(frames, 0.08)


add_meme(
    "blamed_mahiro",
    blamed_mahiro,
    min_texts=1,
    max_texts=1,
    tags=MemeTags.mahiro,
    keywords=["真寻挨骂"],
    default_texts=["傻逼"],
    date_created=datetime(2024, 8, 26),
    date_modified=datetime(2024, 8, 26),
)
