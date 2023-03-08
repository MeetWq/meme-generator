from typing import List

from pil_utils import BuildImage, Text2Image

from meme_generator import add_meme


def google(images, texts: List[str], args):
    text = texts[0]
    text = " ".join(text.splitlines())
    colors = ["#4285f4", "#db4437", "#f4b400", "#4285f4", "#0f9d58", "#db4437"]
    t2m = Text2Image.from_text(text, 200)
    index = 0
    for char in t2m.lines[0].chars:
        char.fill = colors[index % len(colors)]
        if char.char.strip():
            index += 1
    return BuildImage(t2m.to_image(bg_color="white", padding=(50, 50))).save_jpg()


add_meme(
    "google",
    google,
    min_texts=1,
    max_texts=1,
    default_texts=["Google"],
    keywords=["google"],
)
