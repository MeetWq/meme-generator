import re
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"

default_text = "エロ本"


def read_book(images: list[BuildImage], texts: list[str], args):
    frame = BuildImage.open(img_dir / "0.png")
    points = ((0, 108), (1092, 0), (1023, 1134), (29, 1134))
    img = (
        images[0]
        .convert("RGBA")
        .resize((1000, 1100), keep_ratio=True, direction="north")
    )
    cover = img.perspective(points)
    frame.paste(cover, (1138, 1172), below=True)

    text = texts[0] if texts else default_text

    chars = list(" ".join(text.splitlines()))
    pieces: list[BuildImage] = []
    for char in chars:
        piece = BuildImage(
            Text2Image.from_text(char, 150, fill="white", weight="bold").to_image()
        )
        if re.fullmatch(r"[a-zA-Z0-9\s]", char):
            piece = piece.rotate(-90, expand=True)
        else:
            piece = piece.resize_canvas((piece.width, piece.height - 40), "south")
        pieces.append(piece)
    w = max(piece.width for piece in pieces)
    h = sum(piece.height for piece in pieces)
    if w > 265 or h > 3000:
        raise TextOverLength(text)

    text_img = BuildImage.new("RGBA", (w, h))
    h = 0
    for piece in pieces:
        text_img.paste(piece, ((w - piece.width) // 2, h), alpha=True)
        h += piece.height
    if h > 780:
        ratio = 780 / h
        text_img = text_img.resize((int(w * ratio), int(h * ratio)))
    text_img = text_img.rotate(3, expand=True)
    w, h = text_img.size
    frame.paste(text_img, (870 + (240 - w) // 2, 1500 + (780 - h) // 2), alpha=True)

    return frame.save_jpg()


add_meme(
    "read_book",
    read_book,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    default_texts=[default_text],
    keywords=["看书"],
    date_created=datetime(2022, 8, 22),
    date_modified=datetime(2023, 10, 25),
)
