from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import CommandShortcut, add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def speechless(images: list[BuildImage], texts: list[str], args):
    text = "无语，和你说不下去"
    if texts:
        text += "\n" + texts[0]
    sweat = BuildImage.open(img_dir / "sweat.png").resize((80, 80))

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize_width(500)
        text_img = BuildImage(
            Text2Image.from_text(text, 45, align="center")
            .wrap(480)
            .to_image(bg_color="white")
        )
        frame_h = img.height + text_img.height + 10
        frame = BuildImage.new("RGBA", (500, frame_h), "white")
        frame.paste(img, (0, 0), alpha=True)
        frame.paste(text_img, ((500 - text_img.width) // 2, img.height), alpha=True)
        frame.paste(sweat, (300, 120), alpha=True)
        return frame

    return make_jpg_or_gif(images, make)


add_meme(
    "speechless",
    speechless,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["无语"],
    shortcuts=[
        CommandShortcut(
            key=r"(?P<text>典型的\S+思维)",
            args=["{text}"],
            humanized="典型的xx思维",
        )
    ],
    date_created=datetime(2024, 11, 12),
    date_modified=datetime(2024, 11, 12),
)
