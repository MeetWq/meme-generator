from datetime import datetime

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme


def google(images, texts: list[str], args):
    text = texts[0]
    text = " ".join(text.splitlines())
    colors = ["#4285f4", "#db4437", "#f4b400", "#4285f4", "#0f9d58", "#db4437"]
    bbcode_text = "".join(
        f"[color={colors[i % len(colors)]}]{char}[/color]" if char.strip() else char
        for i, char in enumerate(text)
    )
    t2m = Text2Image.from_bbcode_text(bbcode_text, 200)
    return BuildImage(t2m.to_image(bg_color="white", padding=(50, 50))).save_jpg()


add_meme(
    "google",
    google,
    min_texts=1,
    max_texts=1,
    default_texts=["Google"],
    keywords=["google"],
    date_created=datetime(2022, 10, 30),
    date_modified=datetime(2023, 2, 14),
)
