from typing import List

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif


def universal(images: List[BuildImage], texts: List[str], args):
    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize_width(500)
        frames: List[BuildImage] = [img]
        for text in texts:
            text_img = BuildImage(
                Text2Image.from_bbcode_text(text, fontsize=45, align="center")
                .wrap(480)
                .to_image()
            )
            frames.append(text_img.resize_canvas((500, text_img.height)))

        frame = BuildImage.new(
            "RGBA", (500, sum((f.height for f in frames)) + 10), "white"
        )
        current_h = 0
        for f in frames:
            frame.paste(f, (0, current_h), alpha=True)
            current_h += f.height
        return frame

    return make_jpg_or_gif(images[0], make)


add_meme(
    "universal",
    universal,
    min_images=1,
    max_images=1,
    min_texts=1,
    max_texts=10,
    default_texts=["在此处添加文字"],
    keywords=["万能表情", "空白表情"],
)
