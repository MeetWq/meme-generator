from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def father_work(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    text = texts[0] if texts else "此处添加文字"
    try:
        frame.draw_text(
            (195, frame.height - 110, frame.width - 10, frame.height - 20),
            text,
            min_fontsize=10,
            max_fontsize=50,
            fill="black",
            allow_wrap=True,
            lines_align="center",
        )
    except ValueError:
        raise TextOverLength(text)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((230, 96), keep_ratio=True)
        return frame.copy().paste(img, (252, 150), below=False)

    return make_jpg_or_gif(images[0], make)


add_meme(
    "father_work",
    father_work,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=["此处添加文字"],
    keywords=["闭嘴", "我爸爸"],
)
