from pathlib import Path
from typing import List

from pil_utils import BuildImage, Text2Image
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsParser, MemeArgsType, add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

help = "指定名字"

parser = MemeArgsParser()
parser.add_argument("-n", "--name", type=str, default="", help=help)


class Model(MemeArgsModel):
    name: str = Field("", description=help)


def my_friend(images: List[BuildImage], texts: List[str], args: Model):
    name = args.name or (args.user_infos[-1].name if args.user_infos else "") or "朋友"
    img = images[0].convert("RGBA").circle().resize((100, 100))

    name_img = Text2Image.from_text(name, 25, fill="#868894").to_image()
    name_w, name_h = name_img.size
    if name_w >= 600:
        raise TextOverLength(name)

    corner1 = BuildImage.open(img_dir / "corner1.png")
    corner2 = BuildImage.open(img_dir / "corner2.png")
    corner3 = BuildImage.open(img_dir / "corner3.png")
    corner4 = BuildImage.open(img_dir / "corner4.png")
    label = BuildImage.open(img_dir / "label.png")

    def make_dialog(text: str) -> BuildImage:
        text_img = Text2Image.from_text(text, 40).wrap(600).to_image()
        text_w, text_h = text_img.size
        box_w = max(text_w, name_w + 15) + 140
        box_h = max(text_h + 103, 150)
        box = BuildImage.new("RGBA", (box_w, box_h))
        box.paste(corner1, (0, 0))
        box.paste(corner2, (0, box_h - 75))
        box.paste(corner3, (text_w + 70, 0))
        box.paste(corner4, (text_w + 70, box_h - 75))
        box.paste(BuildImage.new("RGBA", (text_w, box_h - 40), "white"), (70, 20))
        box.paste(BuildImage.new("RGBA", (text_w + 88, box_h - 150), "white"), (27, 75))
        box.paste(text_img, (70, 17 + (box_h - 40 - text_h) // 2), alpha=True)

        dialog = BuildImage.new("RGBA", (box.width + 130, box.height + 60), "#eaedf4")
        dialog.paste(img, (20, 20), alpha=True)
        dialog.paste(box, (130, 60), alpha=True)
        dialog.paste(label, (160, 25))
        dialog.paste(name_img, (260, 22 + (35 - name_h) // 2), alpha=True)
        return dialog

    dialogs = [make_dialog(text) for text in texts]
    frame_w = max((dialog.width for dialog in dialogs))
    frame_h = sum((dialog.height for dialog in dialogs))
    frame = BuildImage.new("RGBA", (frame_w, frame_h), "#eaedf4")
    current_h = 0
    for dialog in dialogs:
        frame.paste(dialog, (0, current_h))
        current_h += dialog.height
    return frame.save_jpg()


add_meme(
    "my_friend",
    my_friend,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=10,
    default_texts=["让我康康"],
    args_type=MemeArgsType(parser, Model),
    keywords=["我朋友说"],
)
