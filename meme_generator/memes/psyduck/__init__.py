from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def psyduck(images, texts: List[str], args):
    left_img = BuildImage.new("RGBA", (155, 100))
    right_img = BuildImage.new("RGBA", (155, 100))

    def draw(frame: BuildImage, text: str):
        try:
            frame.draw_text(
                (5, 5, 150, 95),
                text,
                max_fontsize=80,
                min_fontsize=30,
                allow_wrap=True,
                fontname="FZSJ-QINGCRJ",
            )
        except ValueError:
            raise TextOverLength(text)

    draw(left_img, texts[0])
    draw(right_img, texts[1])

    params = [
        ("left", ((0, 11), (154, 0), (161, 89), (20, 104)), (18, 42)),
        ("left", ((0, 9), (153, 0), (159, 89), (20, 101)), (15, 38)),
        ("left", ((0, 7), (148, 0), (156, 89), (21, 97)), (14, 23)),
        None,
        ("right", ((10, 0), (143, 17), (124, 104), (0, 84)), (298, 18)),
        ("right", ((13, 0), (143, 27), (125, 113), (0, 83)), (298, 30)),
        ("right", ((13, 0), (143, 27), (125, 113), (0, 83)), (298, 26)),
        ("right", ((13, 0), (143, 27), (125, 113), (0, 83)), (298, 30)),
        ("right", ((13, 0), (143, 27), (125, 113), (0, 83)), (302, 20)),
        ("right", ((13, 0), (141, 23), (120, 102), (0, 82)), (300, 24)),
        ("right", ((13, 0), (140, 22), (118, 100), (0, 82)), (299, 22)),
        ("right", ((9, 0), (128, 16), (109, 89), (0, 80)), (303, 23)),
        None,
        ("left", ((0, 13), (152, 0), (158, 89), (17, 109)), (35, 36)),
        ("left", ((0, 13), (152, 0), (158, 89), (17, 109)), (31, 29)),
        ("left", ((0, 17), (149, 0), (155, 90), (17, 120)), (45, 33)),
        ("left", ((0, 14), (152, 0), (156, 91), (17, 115)), (40, 27)),
        ("left", ((0, 12), (154, 0), (158, 90), (17, 109)), (35, 28)),
    ]

    frames: List[IMG] = []
    for i in range(18):
        frame = BuildImage.open(img_dir / f"{i}.jpg")
        param = params[i]
        if param:
            side, points, pos = param
            if side == "left":
                frame.paste(left_img.perspective(points), pos, alpha=True)
            elif side == "right":
                frame.paste(right_img.perspective(points), pos, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.2)


add_meme(
    "psyduck",
    psyduck,
    min_texts=2,
    max_texts=2,
    default_texts=["来份", "涩图"],
    keywords=["可达鸭"],
)
