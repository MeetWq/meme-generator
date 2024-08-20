import random
import datetime

from pil_utils import BuildImage
from PIL import Image, ImageDraw

from meme_generator import add_meme
from meme_generator.utils import Maker, make_gif_or_combined_gif, FrameAlignPolicy


class dot:
    def __init__(self, positon, direction):
        self.positon = positon
        self.velocity = (0, 0)
        self.direction = direction
        self.radius = random.randint(1, 3)
    def move(self, step: int) -> None:
        a = 0.02 * step / self.radius
        self.velocity = (
            self.velocity[0] + a * self.direction[0],
            self.velocity[1] + a * self.direction[1],
        )
        self.positon = (
            self.positon[0] + round(self.velocity[0]),
            self.positon[1] + round(self.velocity[1]),
        )
        if random.random() < 0.3:
            self.radius -= 1

    def draw_dot(self, img: Image.Image) -> None:
        ImageDraw.Draw(img).ellipse(
            (
                self.positon[0] - self.radius,
                self.positon[1] - self.radius,
                self.positon[0] + self.radius,
                self.positon[1] + self.radius,
            ),
            fill=(0, 0, 0, 255),
        )

    def out_of_img(self, img: Image.Image) -> bool:
        w, h = img.size
        if (
            self.radius <= 0
            or self.positon[0] + self.radius < 0
            or self.positon[0] - self.radius > w
            or self.positon[1] + self.radius < 0
            or self.positon[1] - self.radius > h
        ):
            return True
        return False


def make_dust(dusts: list[dot], step, size):
    dust_mask = Image.new("RGBA", size)
    remove_list = []
    for dot in dusts:
        dot.move(step)
        if dot.out_of_img(dust_mask):
            remove_list.append(dot)
        else:
            dot.draw_dot(dust_mask)
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
    o = (width * 2 // 3, height)
    step = (o[0] ** 2 + o[1] ** 2) ** 0.5 / 24
    dusts = []

    def maker(i: int) -> Maker:
        def make(imgs: list[BuildImage]) -> BuildImage:
            img = imgs[0].image.convert("RGBA").resize((width, height))
            if i < 36:
                new_img = img.copy()
                for x in range(width):
                    for y in range(
                        max(0, min(height, height - round(step * i))), height
                    ):
                        pixel = (x, y)
                        if img.getpixel(pixel)[3] == 0:
                            continue
                        distance = ((x - o[0]) ** 2 + (y - o[1]) ** 2) ** 0.5
                        if distance <= step * (i - 12):
                            new_img.putpixel(pixel, (0, 0, 0, 0))
                        elif distance <= step * (i - 11):
                            new_img.putpixel(pixel, (0, 0, 0, 255))
                            if random.random() <= 0.06:
                                direction = (
                                    (x - o[0]) / distance,
                                    (y - o[1] * 1.5) / distance,
                                )
                                dusts.append(dot((x, y), direction))
                        elif distance <= step * (i - 1):
                            factor = (distance - step * (i - 11)) / (step * 12)
                            factor = max(0, min(1, factor))
                            original_pixel = img.getpixel(pixel)
                            gray = round(
                                (
                                    original_pixel[0]
                                    + original_pixel[1]
                                    + original_pixel[2]
                                )
                                * factor
                                * (0.9 + 0.2 * random.random())
                                // 3
                            )
                            new_color = (gray, gray, gray, original_pixel[3])
                            new_img.putpixel(pixel, new_color)
                        else:
                            continue
                dust_mask = make_dust(dusts, step, img.size)
                new_img.paste(dust_mask, (0, 0), dust_mask)
                return BuildImage(new_img)
            else:
                return BuildImage(make_dust(dusts, step, img.size))

        return make

    return make_gif_or_combined_gif(images, maker, 50, 0.06, FrameAlignPolicy.no_extend)


add_meme(
    "fade_away",
    fade_away,
    max_images=1,
    min_images=1,
    keywords=["灰飞烟灭"],
    date_created=datetime.datetime(2024, 8, 20),
    date_modified=datetime.datetime(2024, 8, 20),
)
