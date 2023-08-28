from pathlib import Path
from typing import List

from PIL.Image import Transpose
from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"


def youtube(images, texts: List[str], args):
    left_img = Text2Image.from_text(texts[0], fontsize=200, fill="black").to_image(
        bg_color="white", padding=(30, 20)
    )

    right_img = Text2Image.from_text(
        texts[1], fontsize=200, fill="white", weight="bold"
    ).to_image(bg_color=(230, 33, 23), padding=(50, 20))
    right_img = BuildImage(right_img).resize_canvas(
        (max(right_img.width, 400), right_img.height), bg_color=(230, 33, 23)
    )
    right_img = right_img.circle_corner(right_img.height // 2)

    frame = BuildImage.new(
        "RGBA",
        (left_img.width + right_img.width, max(left_img.height, right_img.height)),
        "white",
    )
    frame.paste(left_img, (0, frame.height - left_img.height))
    frame = frame.resize_canvas(
        (frame.width + 100, frame.height + 100), bg_color="white"
    )

    corner = BuildImage.open(img_dir / "corner.png")
    ratio = right_img.height / 2 / corner.height
    corner = corner.resize((int(corner.width * ratio), int(corner.height * ratio)))
    x0 = left_img.width + 50
    y0 = frame.height - right_img.height - 50
    x1 = frame.width - corner.width - 50
    y1 = frame.height - corner.height - 50
    frame.paste(corner, (x0, y0 - 1), alpha=True).paste(
        corner.transpose(Transpose.FLIP_TOP_BOTTOM), (x0, y1 + 1), alpha=True
    ).paste(
        corner.transpose(Transpose.FLIP_LEFT_RIGHT), (x1, y0 - 1), alpha=True
    ).paste(
        corner.transpose(Transpose.FLIP_TOP_BOTTOM).transpose(
            Transpose.FLIP_LEFT_RIGHT
        ),
        (x1, y1 + 1),
        alpha=True,
    ).paste(
        right_img, (x0, y0), alpha=True
    )
    return frame.save_jpg()


add_meme(
    "youtube",
    youtube,
    min_texts=2,
    max_texts=2,
    default_texts=["Porn", "Hub"],
    keywords=["yt", "youtube"],
)
