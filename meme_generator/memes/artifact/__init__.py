from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme

img_dir = Path(__file__).parent / "images"
font_dir = Path(__file__).parent / "font"


def artifact(images: list[BuildImage], texts, args):
    background_path = img_dir / "0.png"
    frame = BuildImage.open(background_path).convert("RGBA")

    font_path = font_dir / "汉仪文黑-85W.ttf"

    if len(images) > 0:
        img = images[0].convert("RGBA").resize((90, 85), keep_ratio=True).rotate(0)
        frame.paste(img, (130, 40), alpha=True)

    if len(texts) > 0:
        text = texts[0]
        split_texts = text.split(";")

        x1, y1 = 15, 5
        x3, y3 = 10, 160

        text1_position = (x1, y1)
        text2_position = (x3, y3)

        if len(split_texts) > 0:
            text1 = split_texts[0].strip()
            frame.draw_text(
                text1_position, text1, min_fontsize=40, fill=(255, 255, 255)
            )

        if len(split_texts) > 1:
            text2 = split_texts[1:]
            text2 = "\n".join([t.strip() for t in text2])
            frame.draw_text(text2_position, text2, min_fontsize=20, fill=(73, 83, 102))

    if len(images) == 0 and len(texts) == 0:
        raise ValueError(text)

    return frame.save_png()


add_meme(
    "artifact",
    artifact,
    min_images=0,
    max_images=1,
    min_texts=0,
    max_texts=2,
    default_texts=["名称;属性，使用分号分隔"],
    keywords=["圣遗物", "原神圣遗物"],
)
