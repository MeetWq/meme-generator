from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme

img_dir = Path(__file__).parent / "images"


def time_to_go(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    img = images[0].circle().resize((105, 105))
    frame = BuildImage.open(img_dir / "time_to_go.png")
    frame.paste(img, (230, 82), below=True)
    return frame.save_jpg()


add_meme(
    "time_to_go",
    time_to_go,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=0,
    keywords=["该走了"],
    date_created=datetime(2024, 9, 4),
    date_modified=datetime(2024, 9, 4),
)
