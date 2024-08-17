from datetime import datetime

from PIL import Image, ImageDraw
from pil_utils import BuildImage
from pil_utils.fonts import Font

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif


def charpic(images: list[BuildImage], texts, args):
    str_map = "@@$$&B88QMMGW##EE93SPPDOOU**==()+^,\"--''.  "
    num = len(str_map)
    font = Font.find("Consolas").load_font(15)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize_width(150).convert("L")
        img = img.resize((img.width, img.height // 2))
        lines = []
        for y in range(img.height):
            line = ""
            for x in range(img.width):
                gray = img.image.getpixel((x, y))
                line += str_map[int(num * gray / 256)] if gray != 0 else " "  # type: ignore
            lines.append(line)
        text = "\n".join(lines)
        text_img = Image.new("RGB", (2000, 2000), "white")
        draw = ImageDraw.Draw(text_img)
        _, _, w, h = draw.multiline_textbbox((0, 0), text, font=font)
        draw.multiline_text((0, 0), text, font=font, fill="black")
        text_img = text_img.crop((0, 0, w, h))
        return BuildImage(text_img)

    return make_jpg_or_gif(images, make)


add_meme(
    "charpic",
    charpic,
    min_images=1,
    max_images=1,
    keywords=["字符画"],
    date_created=datetime(2022, 7, 21),
    date_modified=datetime(2023, 10, 2),
)
