from typing import List

from PIL import ImageOps
from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif


def flash_blind(images: List[BuildImage], texts: List[str], args):
    img = images[0].convert("RGB").resize_width(500)
    frames: List[IMG] = []
    frames.append(img.image)
    frames.append(ImageOps.invert(img.image))
    img_enlarge = img.resize_canvas((450, img.height * 450 // 500)).resize(
        (500, img.height)
    )
    frames.append(img_enlarge.image)
    frames.append(ImageOps.invert(img.image))

    if texts and texts[0]:
        text = texts[0]
        text_h = 65

        try:
            text_frame_black = BuildImage.new("RGB", (500, text_h), "black")
            text_frame_white = BuildImage.new("RGB", (500, text_h), "white")
            text_frame_black.draw_text(
                (10, 0, 490, text_h),
                text,
                max_fontsize=50,
                min_fontsize=20,
                fill="white",
            )
            text_frame_white.draw_text(
                (10, 0, 490, text_h),
                text,
                max_fontsize=50,
                min_fontsize=20,
                fill="black",
            )
        except ValueError:
            raise TextOverLength(text)
        frames[0].paste(text_frame_black.image, (0, img.height - text_h))
        frames[1].paste(text_frame_white.image, (0, img.height - text_h))
        frames[2].paste(text_frame_black.image, (0, img.height - text_h))
        frames[3].paste(text_frame_white.image, (0, img.height - text_h))

    return save_gif(frames, 0.03)


add_meme(
    "flash_blind",
    flash_blind,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["闪瞎你们的狗眼"],
    keywords=["闪瞎"],
)
