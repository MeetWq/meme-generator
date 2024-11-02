from datetime import datetime

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif


def charpic(images: list[BuildImage], texts, args):
    str_map = "@@$$&B88QMMGW##EE93SPPDOOU**==()+^,\"--''.  "
    num = len(str_map)
    t2m = Text2Image.from_text("@", 15, font_families=["Consolas"])
    ratio = t2m.longest_line / t2m.height

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize_width(150).convert("L")
        img = img.resize((img.width, round(img.height * ratio)))
        lines = []
        for y in range(img.height):
            line = ""
            for x in range(img.width):
                gray = img.image.getpixel((x, y))
                line += str_map[int(num * gray / 256)] if gray != 0 else " "  # type: ignore
            lines.append(line)
        text = "\n".join(lines)
        return BuildImage(
            Text2Image.from_text(text, 15, font_families=["Consolas"]).to_image(
                bg_color="white"
            )
        )

    return make_jpg_or_gif(images, make)


add_meme(
    "charpic",
    charpic,
    min_images=1,
    max_images=1,
    keywords=["字符画"],
    date_created=datetime(2022, 7, 21),
    date_modified=datetime(2024, 11, 1),
)
