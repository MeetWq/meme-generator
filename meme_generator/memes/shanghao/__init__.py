from pathlib import Path
from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.utils import FrameAlignPolicy, Maker, make_gif_or_combined_gif


img_dir = Path(__file__).parent / "images"


def shanghao(images: list[BuildImage], texts, args):
    width, height = BuildImage.open(img_dir / "0.png").size
    rmin = 225
    rmax = 825
    r_list = (
        36 * [rmin]
        + [
            236,
            260,
            329,
            434,
            526,
            526,
            668,
            716,
            716,
            742,
            760,
            791,
            805,
            805,
            815,
            822,
        ]
        + 8 * [rmax]
    )
    loc0 = (356, 366)
    loc1 = (19, 149)
    loc_list = (
        36 * [loc0]
        + [
            (354, 362),
            (338, 352),
            (300, 328),
            (240, 290),
            (179, 250),
            (179, 250),
            (105, 210),
            (78, 191),
            (78, 191),
            (62, 180),
            (55, 174),
            (38, 158),
            (30, 158),
            (30, 158),
            (24, 148),
            (16, 149),
        ]
        + 8 * [loc1]
    )

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            r = r_list[i]
            loc = (
                int(width * loc_list[i][0] / 1000),
                int(height * loc_list[i][1] / 1000),
            )
            game = (
                img.square()
                .convert("RGBA")
                .resize(
                    (int(r * width / 1000), int(r * height / 1000)), keep_ratio=True
                )
            )
            frame = BuildImage.open(img_dir / f"{i}.png").convert("RGBA")
            frame.paste(game, loc, below=True)
            return frame

        return make

    return make_gif_or_combined_gif(
        images[0], maker, 60, 0.066, FrameAlignPolicy.extend_loop
    )


add_meme("shanghao", shanghao, min_images=1, max_images=1, keywords=["上号"])
