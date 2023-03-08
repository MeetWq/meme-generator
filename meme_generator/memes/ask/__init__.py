from typing import List

from PIL import ImageFilter
from pil_utils import BuildImage, Text2Image
from pil_utils.gradient import ColorStop, LinearGradient

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOrNameNotEnough, TextOverLength


def ask(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    if not texts and not args.user_infos:
        raise TextOrNameNotEnough("ask")

    name = texts[0] if texts else args.user_infos[0].name
    ta = "他" if args.user_infos and args.user_infos[0].gender == "male" else "她"

    img = images[0].resize_width(640)
    img_w, img_h = img.size
    gradient_h = 150
    gradient = LinearGradient(
        (0, 0, 0, gradient_h),
        [ColorStop(0, (0, 0, 0, 220)), ColorStop(1, (0, 0, 0, 30))],
    )
    gradient_img = gradient.create_image((img_w, gradient_h))
    mask = BuildImage.new("RGBA", img.size)
    mask.paste(gradient_img, (0, img_h - gradient_h), alpha=True)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=3))
    img.paste(mask, alpha=True)

    start_w = 20
    start_h = img_h - gradient_h + 5
    text1 = name
    text2 = f"{name}不知道哦。"
    text2img1 = Text2Image.from_text(text1, 28, weight="bold")
    text2img2 = Text2Image.from_text(text2, 28, weight="bold")
    img.draw_text(
        (start_w + 40 + (text2img2.width - text2img1.width) // 2, start_h),
        text1,
        fontsize=28,
        fill="orange",
        weight="bold",
    )
    img.draw_text(
        (start_w + 40, start_h + text2img1.height + 10),
        text2,
        fontsize=28,
        fill="white",
        weight="bold",
    )

    line_h = start_h + text2img1.height + 5
    img.draw_line(
        (start_w, line_h, start_w + text2img2.width + 80, line_h),
        fill="orange",
        width=2,
    )

    sep_w = 30
    sep_h = 80
    frame = BuildImage.new("RGBA", (img_w + sep_w * 2, img_h + sep_h * 2), "white")
    try:
        frame.draw_text(
            (sep_w, 0, img_w + sep_w, sep_h),
            f"让{name}告诉你吧",
            max_fontsize=35,
            halign="left",
        )
        frame.draw_text(
            (sep_w, img_h + sep_h, img_w + sep_w, img_h + sep_h * 2),
            f"啊这，{ta}说不知道",
            max_fontsize=35,
            halign="left",
        )
    except ValueError:
        raise TextOverLength(name)
    frame.paste(img, (sep_w, sep_h), alpha=True)
    return frame.save_png()


add_meme(
    "ask", ask, min_images=1, max_images=1, min_texts=0, max_texts=1, keywords=["问问"]
)
