from typing import List

from PIL.Image import Transpose
from pil_utils import BuildImage

from meme_generator import add_meme


def keep_away(images: List[BuildImage], texts: List[str], args):
    def trans(img: BuildImage, n: int) -> BuildImage:
        img = img.convert("RGBA").square().resize((100, 100))
        if n < 4:
            return img.rotate(n * 90)
        else:
            return img.transpose(Transpose.FLIP_LEFT_RIGHT).rotate((n - 4) * 90)

    def paste(img: BuildImage):
        nonlocal count
        y = 90 if count < 4 else 190
        frame.paste(img, ((count % 4) * 100, y))
        count += 1

    text = texts[0] if texts else "如何提高社交质量 : \n远离以下头像的人"
    frame = BuildImage.new("RGB", (400, 290), "white")
    frame.draw_text((10, 10, 390, 80), text, max_fontsize=40, halign="left")
    count = 0
    num_per_user = 8 // len(images)
    for image in images:
        for n in range(num_per_user):
            paste(trans(image, n))
    num_left = 8 - num_per_user * len(images)
    for n in range(num_left):
        paste(trans(images[-1], n + num_per_user))

    return frame.save_jpg()


add_meme(
    "keep_away",
    keep_away,
    min_images=1,
    max_images=8,
    min_texts=0,
    max_texts=1,
    default_texts=["如何提高社交质量 : \n远离以下头像的人"],
    keywords=["远离"],
)
