from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from PIL.Image import Resampling, Transform
from pil_utils import BuildImage, Text2Image
from pil_utils.fonts import DEFAULT_FALLBACK_FONTS
from pil_utils.text2image import Line

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def bluearchive(images, texts: List[str], args):
    fontsize = 168
    fontname = "Ro GSan Serif Std"
    fallback_fonts = ["Glow Sans SC"] + DEFAULT_FALLBACK_FONTS
    tilt = 0.4
    color_blue = "#128AFA"
    color_gray = "#2B2B2B"

    def transform(img: IMG) -> IMG:
        dw = round(img.height * tilt)
        return img.transform(
            (img.width + dw, img.height),
            Transform.AFFINE,
            (1, tilt, -dw, 0, 1, 0),
            Resampling.BILINEAR,
        )

    left_t2m = Text2Image.from_text(
        texts[0],
        fontsize,
        fill=color_blue,
        fontname=fontname,
        fallback_fonts=fallback_fonts,
    )
    right_t2m = Text2Image.from_text(
        texts[1],
        fontsize,
        fill=color_gray,
        stroke_width=12,
        stroke_fill="white",
        fontname=fontname,
        fallback_fonts=fallback_fonts,
    )
    new_line = Line(
        left_t2m.lines[0].chars + right_t2m.lines[0].chars,
        fontsize=fontsize,
        fontname=fontname,
    )
    text_t2m = Text2Image([new_line])
    text_img = transform(text_t2m.to_image())
    text_dy = text_t2m.lines[0].ascent

    padding_x = 50
    img_w = text_img.width + padding_x * 2
    img_h = 450
    text_y = 350
    logo_y = 10
    logo_x = padding_x + left_t2m.width - 115
    halo = BuildImage.open(img_dir / "halo.png").convert("RGBA")
    cross = BuildImage.open(img_dir / "cross.png").convert("RGBA")

    frame = BuildImage.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
    frame.paste(halo, (logo_x, logo_y), alpha=True)
    frame.paste(text_img, (padding_x, text_y - text_dy), alpha=True)
    frame.paste(cross, (logo_x, logo_y), alpha=True)
    return frame.save_jpg()


add_meme(
    "bluearchive",
    bluearchive,
    min_texts=2,
    max_texts=2,
    default_texts=["Blue", "Archive"],
    keywords=["蔚蓝档案标题", "batitle"],
)
