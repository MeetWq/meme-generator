from typing import List

from pil_utils import BuildImage, Text2Image

from meme_generator import MemeArgsModel, add_meme
from meme_generator.exception import TextOverLength


def follow(images: List[BuildImage], texts: List[str], args: MemeArgsModel):
    img = images[0].circle().resize((200, 200))

    if texts:
        name = texts[0]
    else:
        if args.user_infos:
            user_info = args.user_infos[0]
            name = user_info.name
            if not name:
                name = "女同" if user_info.gender == "female" else "男同"
        else:
            name = "男同"

    name_img = Text2Image.from_text(name, 60).to_image()
    follow_img = Text2Image.from_text("关注了你", 60, fill="grey").to_image()
    text_width = max(name_img.width, follow_img.width)
    if text_width >= 1000:
        raise TextOverLength(name)

    frame = BuildImage.new("RGBA", (300 + text_width + 50, 300), (255, 255, 255, 0))
    frame.paste(img, (50, 50), alpha=True)
    frame.paste(name_img, (300, 135 - name_img.height), alpha=True)
    frame.paste(follow_img, (300, 145), alpha=True)
    return frame.save_jpg()


add_meme(
    "follow",
    follow,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["关注"],
)
