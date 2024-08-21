import datetime
import random

from PIL import Image, ImageDraw
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import Maker, make_gif_or_combined_gif


class Dot:
    def __init__(self, positon: tuple[int, int], direction: tuple[float, float]):
        self.px = positon[0]
        self.py = positon[1]
        self.vx = 0
        self.vy = 0
        self.dx = direction[0]
        self.dy = direction[1]
        self.radius = random.randint(1, 3)

    def move(self, step: int):
        a = 0.02 * step / self.radius
        self.vx += a * self.dx
        self.vy += a * self.dy
        self.px += round(self.vx)
        self.py += round(self.vy)
        if random.random() < 0.25:
            self.radius -= 1

    def draw_on(self, img: Image.Image):
        ImageDraw.Draw(img).ellipse(
            (
                self.px - self.radius,
                self.py - self.radius,
                self.px + self.radius,
                self.py + self.radius,
            ),
            fill=(0, 0, 0, 255),
        )

    def out_of_img(self, img: Image.Image) -> bool:
        w, h = img.size
        if (
            self.radius <= 0
            or self.px + self.radius < 0
            or self.px - self.radius > w
            or self.py + self.radius < 0
            or self.py - self.radius > h
        ):
            return True
        return False


def make_dust(dusts: list[Dot], step: int, size: tuple[int, int]) -> Image.Image:
    dust_mask = Image.new("RGBA", size)
    remove_list = []
    for dot in dusts:
        dot.move(step)
        if dot.out_of_img(dust_mask):
            remove_list.append(dot)
        else:
            dot.draw_on(dust_mask)
    for dot in remove_list:
        dusts.remove(dot)
    return dust_mask


def fade_away(images: list[BuildImage], texts, args):
    image = images[0]
    width, height = image.size
    area = width * height
    if area >= 40000:
        width = round(200 * width / (area**0.5))
        height = round(200 * height // (area**0.5))
    o = (width * 2 // 3, height * 3 // 2)
    step = (o[0] ** 2 + o[1] ** 2) ** 0.5 / 24
    dusts = []

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].image.convert("RGBA").resize((width, height))
            if i <= 9:
                return BuildImage(img)
            elif 9 < i < 28:
                new_img = img.copy()
                for x in range(width):
                    for y in range(
                        max(0, min(height, height - round(step * (i + 11)))), height
                    ):
                        pixel = (x, y)
                        if img.getpixel(pixel)[3] == 0:  # type: ignore
                            continue
                        distance = ((x - o[0]) ** 2 + (y - o[1]) ** 2) ** 0.5
                        if distance <= step * (i - 5):
                            new_img.putpixel(pixel, (0, 0, 0, 0))
                        elif distance <= step * (i - 4):
                            new_img.putpixel(pixel, (0, 0, 0, 255))
                            if random.random() <= 0.06:
                                direction = (
                                    (x - o[0]) / distance,
                                    (y - o[1] * 1.5) / distance,
                                )
                                dusts.append(Dot((x, y), direction))
                        elif distance <= step * (i + 2):
                            factor = (distance - step * (i - 11)) / (step * 12)
                            factor = max(0, min(1, factor))
                            factor *= 0.9 + 0.2 * random.random()
                            value = img.getpixel(pixel)
                            gray = (value[0] + value[1] + value[2]) / 3  # type: ignore
                            gray = round(gray * factor)
                            new_color = (gray, gray, gray, value[3])  # type: ignore
                            new_img.putpixel(pixel, new_color)
                        else:
                            continue
                dust_mask = make_dust(dusts, step, img.size)
                new_img.paste(dust_mask, (0, 0), dust_mask)
                return BuildImage(new_img)
            else:
                return BuildImage(make_dust(dusts, step, img.size))

        return make

    return make_gif_or_combined_gif(images, maker, 35, 0.08)


add_meme(
    "fade_away",
    fade_away,
    max_images=1,
    min_images=1,
    keywords=["灰飞烟灭"],
    date_created=datetime.datetime(2024, 8, 20),
    date_modified=datetime.datetime(2024, 8, 21),
)
