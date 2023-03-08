from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def bocchi_draft(images: List[BuildImage], texts, args):
    img = images[0].convert("RGBA").resize((350, 400), keep_ratio=True)
    params = [
        (((54, 62), (353, 1), (379, 382), (1, 399)), (146, 173)),
        (((54, 61), (349, 1), (379, 381), (1, 398)), (146, 174)),
        (((54, 61), (349, 1), (379, 381), (1, 398)), (152, 174)),
        (((54, 61), (335, 1), (379, 381), (1, 398)), (158, 167)),
        (((54, 61), (335, 1), (370, 381), (1, 398)), (157, 149)),
        (((41, 59), (321, 1), (357, 379), (1, 396)), (167, 108)),
        (((41, 57), (315, 1), (357, 377), (1, 394)), (173, 69)),
        (((41, 56), (309, 1), (353, 380), (1, 393)), (175, 43)),
        (((41, 56), (314, 1), (353, 380), (1, 393)), (174, 30)),
        (((41, 50), (312, 1), (348, 367), (1, 387)), (171, 18)),
        (((35, 50), (306, 1), (342, 367), (1, 386)), (178, 14)),
    ]
    # fmt: off
    idx = [
        0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(23):
        frame = BuildImage.open(img_dir / f"{i}.png")
        points, pos = params[idx[i]]
        frame.paste(img.perspective(points), pos, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme("bocchi_draft", bocchi_draft, min_images=1, max_images=1, keywords=["波奇手稿"])
