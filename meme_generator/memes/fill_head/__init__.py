from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import CommandShortcut, MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def fill_head(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    name = texts[0] if texts else (args.user_infos[0].name if args.user_infos else "它")
    text = f"满脑子都是{name}"
    frame = BuildImage.open(img_dir / "0.jpg")
    try:
        frame.draw_text(
            (20, 458, frame.width - 20, 550), text, max_fontsize=65, min_fontsize=30
        )
    except ValueError:
        raise TextOverLength(name)

    def make(imgs: list[BuildImage]) -> BuildImage:
        img = imgs[0].convert("RGBA").resize((210, 170), keep_ratio=True, inside=True)
        return frame.copy().paste(img, (150, 2), alpha=True)

    return make_jpg_or_gif(images, make)


add_meme(
    "fill_head",
    fill_head,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["满脑子"],
    shortcuts=[
        CommandShortcut(
            key=r"满脑子都是(?P<name>\S+)",
            args=["{name}"],
            humanized="满脑子都是xx",
        )
    ],
    date_created=datetime(2023, 6, 3),
    date_modified=datetime(2023, 6, 3),
)
