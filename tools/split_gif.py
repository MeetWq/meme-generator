import argparse
from pathlib import Path

from PIL import Image

from meme_generator.utils import get_avg_duration, split_gif


def split(gif_path: Path, output_path: Path):
    image = Image.open(gif_path)
    if not getattr(image, "is_animated", False):
        print("不是 gif 文件")  # noqa T001
        exit(1)
    duration = get_avg_duration(image)
    print(f"gif 平均帧间隔: {duration} s")  # noqa T001
    frames = split_gif(image)
    output_path.mkdir(parents=True, exist_ok=True)
    for i, frame in enumerate(frames):
        frame.convert("RGBA").save(output_path / f"{i}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gif 分解")
    parser.add_argument(
        "-o", "--output", nargs="?", default="output", help="输出图片的文件夹"
    )
    parser.add_argument("file", help="gif 文件")
    args = parser.parse_args()
    gif_path = Path(args.file)
    output_path = Path(args.output)
    if not gif_path.exists():
        print("文件不存在")  # noqa T001
        exit(1)
    split(gif_path, output_path)
