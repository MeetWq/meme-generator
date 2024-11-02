from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from PIL.Image import Resampling, Transform
from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.tags import MemeTags

img_dir = Path(__file__).parent / "images"


def bluearchive(images, texts: list[str], args):
    fontsize = 168
    font_families = ["Ro GSan Serif Std", "Glow Sans SC"]
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

    text_t2m = Text2Image.from_bbcode_text(
        f"[color={color_blue}]{texts[0]}[/color][color={color_gray}][stroke=white]{texts[1]}[/stroke][/color]",
        fontsize,
        font_families=font_families,
        stroke_ratio=0.07,
    )
    text_img = transform(text_t2m.to_image())

    padding_x = 50
    img_w = text_img.width + padding_x * 2
    img_h = 450
    text_y = 120
    logo_y = 10
    left_x = Text2Image.from_text(
        texts[0], fontsize, font_families=font_families
    ).longest_line
    logo_x = round(padding_x + left_x - 100)
    halo = BuildImage.open(img_dir / "halo.png").convert("RGBA")
    cross = BuildImage.open(img_dir / "cross.png").convert("RGBA")

    frame = BuildImage.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
    frame.paste(halo, (logo_x, logo_y), alpha=True)
    frame.paste(text_img, (padding_x, text_y), alpha=True)
    frame.paste(cross, (logo_x, logo_y), alpha=True)
    return frame.save_jpg()


add_meme(
    "bluearchive",
    bluearchive,
    min_texts=2,
    max_texts=2,
    default_texts=["Blue", "Archive"],
    keywords=["蔚蓝档案标题", "batitle"],
    tags=MemeTags.blue_archive,
    date_created=datetime(2023, 10, 14),
    date_modified=datetime(2024, 11, 2),
)
