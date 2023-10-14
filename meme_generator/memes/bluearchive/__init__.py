from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from PIL.Image import Resampling, Transform
from pil_utils import BuildImage, Text2Image
from pil_utils.fonts import DEFAULT_FALLBACK_FONTS
from pil_utils.types import ColorType

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def bluearchive(images, texts: List[str], args):
    fontsize = 168
    fontname = "Ro GSan Serif Std"
    fallback_fonts = ["Glow Sans SC"] + DEFAULT_FALLBACK_FONTS
    tilt = 0.4
    color_blue = "#128AFA"
    color_gray = "#2B2B2B"

    def draw_text(
        text: str,
        fill: ColorType,
        stroke_width: int = 0,
        stroke_fill: ColorType = "white",
    ) -> Text2Image:
        return Text2Image.from_text(
            text,
            fontsize,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
            fontname=fontname,
            fallback_fonts=fallback_fonts,
        )

    def transform(img: IMG) -> IMG:
        dw = round(img.height * tilt)
        return img.transform(
            (img.width + dw, img.height),
            Transform.AFFINE,
            (1, tilt, -dw, 0, 1, 0),
            Resampling.BILINEAR,
        )

    left_t2m = draw_text(texts[0], color_blue)
    left_img = transform(left_t2m.to_image())
    left_dy = left_t2m.lines[0].ascent
    tilt_dx = round(left_img.height * tilt)

    right_t2m = draw_text(texts[1], color_gray)
    right_img = transform(right_t2m.to_image())
    right_dy = right_t2m.lines[0].ascent

    right_stroke_t2m = draw_text(texts[1], color_gray, 15, "white")
    right_stroke_img = transform(right_stroke_t2m.to_image())

    padding_x = 50
    left_x = padding_x + left_img.width
    img_w = left_img.width + right_img.width - tilt_dx + padding_x * 2
    img_h = 450
    text_y = 350
    logo_y = 10
    logo_x = left_x - 180
    halo = BuildImage.open(img_dir / "halo.png").convert("RGBA")
    cross = BuildImage.open(img_dir / "cross.png").convert("RGBA")

    frame = BuildImage.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
    frame.paste(halo, (logo_x, logo_y), alpha=True)
    frame.paste(
        right_stroke_img,
        (left_x - tilt_dx, text_y - right_dy),
        alpha=True,
    )
    frame.paste(left_img, (padding_x, text_y - left_dy), alpha=True)
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
