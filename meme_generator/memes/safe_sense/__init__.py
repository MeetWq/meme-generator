from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

default_text = "你给我的安全感\n远不及{ta}的万分之一"


def safe_sense(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    img = images[0].convert("RGBA").resize((215, 343), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (215, 135))

    ta = "它"
    if args.user_infos:
        gender = args.user_infos[0].gender
        ta = "他" if gender == "male" else "她" if gender == "female" else "它"
    text = texts[0] if texts else default_text.format(ta=ta)
    try:
        frame.draw_text(
            (30, 0, 400, 130),
            text,
            max_fontsize=50,
            allow_wrap=True,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)
    return frame.save_jpg()


add_meme(
    "safe_sense",
    safe_sense,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["安全感"],
    date_created=datetime(2022, 3, 14),
    date_modified=datetime(2023, 2, 14),
)
