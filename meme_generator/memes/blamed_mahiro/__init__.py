from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from PIL import Image

from meme_generator.tags import MemeTags
from meme_generator.exception import TextOverLength
from meme_generator import add_meme
from meme_generator.utils import save_gif


img_dir = Path(__file__).parent / "images"


def blamed_mahiro(images, texts: list[str], args):
    text = "ニート" if not len(texts) else texts[0]
    params = [
        None,
        None,
        ([(35, 0), (25, 42), (24, 42), (0, 0)], (49, 47)),
        ([(35, 0), (25, 42), (24, 42), (0, 0)], (49, 47)),
        ([(27, 0), (27, 64), (22, 104), (0, 16)], (92, 8)),
        ([(29, 0), (49, 74), (38, 81), (0, 17)], (127, -2)),
        ([(34, 0), (57, 82), (47, 86), (0, 23)], (122, 2)),
        ([(32, 0), (63, 78), (49, 86), (0, 27)], (120, 10)),
        ([(36, 0), (79, 93), (64, 101), (0, 20)], (101, 35)),
        ([(36, 0), (79, 93), (64, 101), (0, 20)], (101, 35)),
        ([(33, 0), (72, 93), (56, 100), (0, 17)], (99, 46)),
        ([(33, 0), (65, 98), (49, 105), (0, 17)], (93, 42)),
        ([(33, 0), (65, 98), (49, 105), (0, 17)], (93, 42)),
        ([(33, 0), (54, 98), (40, 102), (0, 14)], (83, 18)),
        ([(33, 0), (48, 95), (34, 98), (0, 14)], (82, 4)),
        ([(33, 0), (48, 95), (34, 98), (0, 14)], (82, 4)),
        ([(35, 0), (45, 93), (33, 99), (0, 13)], (81, -3)),
        ([(35, 0), (45, 93), (33, 99), (0, 13)], (79, -10)),
        ([(35, 0), (45, 93), (33, 99), (0, 13)], (79, -10)),
        ([(37, 0), (41, 95), (29, 98), (0, 15)], (87, -6)),
        ([(37, 0), (42, 96), (29, 100), (0, 18)], (91, -6)),
        ([(37, 0), (42, 96), (29, 100), (0, 18)], (91, -6)),
        ([(39, 0), (43, 98), (31, 102), (0, 17)], (91, -5)),
        ([(38, 0), (42, 97), (29, 103), (0, 18)], (94, -4)),
    ]
    frames = []
    text_frame = BuildImage.new("RGBA", (200, 40))
    try:
        text_frame.draw_text(
            (0, -2),
            text,
            fontsize=40,
            spacing=0,
            allow_wrap=False,
            fontname="FZKaTong-M19S",
            halign="left",
            fill=(108, 60, 82, 255),
            stroke_ratio=0.01,
            stroke_fill=(255, 255, 255, 255),
        )
    except ValueError:
        raise TextOverLength(text)
    for i, param in enumerate(params):
        bg = Image.open(img_dir / f"{i}.png")
        if i > 1:
            frame = text_frame.perspective(param[0]).image
            bg.paste(frame, param[1], frame)
        frames.append(bg)
    return save_gif(frames, 0.08)


add_meme(
    "blamed_mahiro",
    blamed_mahiro,
    min_texts=1,
    max_texts=1,
    tags=MemeTags.mahiro,
    keywords=["真寻挨骂"],
    default_texts=["ニート"],
    date_created=datetime(2024, 8, 26),
    date_modified=datetime(2024, 8, 26),
)
