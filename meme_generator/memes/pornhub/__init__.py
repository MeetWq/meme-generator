from datetime import datetime

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme


def pornhub(images, texts: list[str], args):
    left_img = Text2Image.from_text(texts[0], 200, fill="white").to_image(
        bg_color="black", padding=(20, 10)
    )

    right_img = Text2Image.from_text(
        texts[1], 200, fill="black", font_style="bold"
    ).to_image(bg_color=(247, 152, 23), padding=(20, 10))
    right_img = BuildImage(right_img).circle_corner(20)

    frame = BuildImage.new(
        "RGBA",
        (left_img.width + right_img.width, max(left_img.height, right_img.height)),
        "black",
    )
    frame.paste(left_img, (0, frame.height - left_img.height)).paste(
        right_img, (left_img.width, frame.height - right_img.height), alpha=True
    )
    frame = frame.resize_canvas(
        (frame.width + 100, frame.height + 100), bg_color="black"
    )
    return frame.save_jpg()


add_meme(
    "pornhub",
    pornhub,
    min_texts=2,
    max_texts=2,
    default_texts=["You", "Tube"],
    keywords=["ph", "pornhub"],
    date_created=datetime(2022, 10, 27),
    date_modified=datetime(2023, 2, 14),
)
