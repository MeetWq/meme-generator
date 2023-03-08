from pathlib import Path
from typing import List

from PIL.Image import Image as IMG
from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def scroll(images, texts: List[str], args):
    text = texts[0]
    text2image = Text2Image.from_text(text, 40).wrap(600)
    if len(text2image.lines) > 5:
        raise TextOverLength(text)
    text_img = text2image.to_image()
    text_w, text_h = text_img.size

    box_w = text_w + 140
    box_h = max(text_h + 103, 150)
    box = BuildImage.new("RGBA", (box_w, box_h), "#eaedf4")
    corner1 = BuildImage.open(img_dir / "corner1.png")
    corner2 = BuildImage.open(img_dir / "corner2.png")
    corner3 = BuildImage.open(img_dir / "corner3.png")
    corner4 = BuildImage.open(img_dir / "corner4.png")
    box.paste(corner1, (0, 0))
    box.paste(corner2, (0, box_h - 75))
    box.paste(corner3, (text_w + 70, 0))
    box.paste(corner4, (text_w + 70, box_h - 75))
    box.paste(BuildImage.new("RGBA", (text_w, box_h - 40), "white"), (70, 20))
    box.paste(BuildImage.new("RGBA", (text_w + 88, box_h - 150), "white"), (27, 75))
    box.paste(text_img, (70, 17 + (box_h - 40 - text_h) // 2), alpha=True)

    dialog = BuildImage.new("RGBA", (box_w, box_h * 4), "#eaedf4")
    for i in range(4):
        dialog.paste(box, (0, box_h * i))

    frames: List[IMG] = []
    num = 30
    dy = int(dialog.height / num)
    for i in range(num):
        frame = BuildImage.new("RGBA", dialog.size)
        frame.paste(dialog, (0, -dy * i))
        frame.paste(dialog, (0, dialog.height - dy * i))
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "scroll", scroll, min_texts=1, max_texts=1, default_texts=["你们说话啊"], keywords=["滚屏"]
)
