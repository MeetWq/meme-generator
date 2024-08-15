from datetime import datetime

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOrNameNotEnough, TextOverLength


def google_captcha(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    if not texts and not args.user_infos:
        raise TextOrNameNotEnough()

    name = texts[0] if texts else args.user_infos[0].name
    image = images[0].convert("RGBA").resize((932, 932), keep_ratio=True)

    canvas = BuildImage.new("RGB", (1000, 1535), "#FFF")
    length = 233
    for i in range(4):
        for j in range(4):
            box = (length * i, length * j, length * (i + 1), length * (j + 1))
            canvas.paste(image.crop(box), (19 + i * (233 + 10), 370 + j * (233 + 10)))

    banner = BuildImage.new("RGB", (962, 332), "#4790E4")
    banner.draw_text(
        (70, 60, 900, 120),
        "请选择包含",
        fill="white",
        max_fontsize=40,
        weight="bold",
        halign="left",
    )
    try:
        banner.draw_text(
            (70, 120, 900, 210),
            name,
            fill="white",
            max_fontsize=80,
            weight="bold",
            halign="left",
        )
    except ValueError:
        raise TextOverLength(name)
    banner.draw_text(
        (70, 210, 900, 270),
        "的所有图块，如果没有，请点击“跳过”",
        fill="white",
        max_fontsize=40,
        weight="bold",
        halign="left",
    )
    canvas.paste(banner, (19, 19))

    bottom = BuildImage.new("RGB", (1000, 182), "#FFF")
    button = BuildImage.new("RGB", (283, 121), "#4790E4")
    button.draw_text(
        (0, 0, 283, 121), "跳过", fill="white", max_fontsize=40, weight="bold"
    )
    bottom.paste(button, (687, 30))
    bottom_border = BuildImage.new("RGB", (1002, 186), "#D5D5D5")
    bottom_border.paste(bottom, (2, 2))
    canvas.paste(bottom_border, (-2, 1353))

    result = BuildImage.new("RGB", (1004, 1539), "#D5D5D5")
    result.paste(canvas, (2, 2))
    return result.save_jpg()


add_meme(
    "google_captcha",
    google_captcha,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["谷歌验证码"],
    date_created=datetime(2024, 8, 15),
    date_modified=datetime(2024, 8, 15),
)
