from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import random_text, save_gif

img_dir = Path(__file__).parent / "images"


def repeat(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    def single_msg(img: BuildImage, name: str) -> BuildImage:
        user_img = img.convert("RGBA").circle().resize((100, 100))
        user_name_img = Text2Image.from_text(f"{name}", 40).to_image()
        time = datetime.now().strftime("%H:%M")
        time_img = Text2Image.from_text(time, 40, fill="gray").to_image()
        bg = BuildImage.new("RGB", (1079, 200), (248, 249, 251, 255))
        bg.paste(user_img, (50, 50), alpha=True)
        bg.paste(user_name_img, (175, 45), alpha=True)
        bg.paste(time_img, (200 + user_name_img.width, 50), alpha=True)
        bg.paste(text_img, (175, 100), alpha=True)
        return bg

    text = texts[0]
    text_img = Text2Image.from_text(text, 50).to_image()
    if text_img.width > 900:
        raise TextOverLength(text)

    users: List[Tuple[BuildImage, str]] = []
    user_infos = args.user_infos
    for i, image in enumerate(images):
        name = user_infos[i].name if len(user_infos) > i else random_text()
        users.append((image, name))

    msg_img = BuildImage.new("RGB", (1079, 1000))
    for i in range(5):
        index = i % len(users)
        msg_img.paste(single_msg(*users[index]), (0, 200 * i))
    msg_img_twice = BuildImage.new("RGB", (msg_img.width, msg_img.height * 2))
    msg_img_twice.paste(msg_img).paste(msg_img, (0, msg_img.height))

    input_img = BuildImage.open(img_dir / "0.jpg")
    self_img = images[0].convert("RGBA").circle().resize((75, 75))
    input_img.paste(self_img, (15, 40), alpha=True)

    frames: List[IMG] = []
    for i in range(50):
        frame = BuildImage.new("RGB", (1079, 1192), "white")
        frame.paste(msg_img_twice, (0, -20 * i))
        frame.paste(input_img, (0, 1000))
        frames.append(frame.image)

    return save_gif(frames, 0.08)


add_meme(
    "repeat",
    repeat,
    min_images=1,
    max_images=5,
    min_texts=1,
    max_texts=1,
    default_texts=["救命啊"],
    keywords=["复读"],
)
