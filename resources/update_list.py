import hashlib
import json
from pathlib import Path

dir_path = Path(__file__).parent
memes_path = dir_path.parent / "meme_generator" / "memes"


def update():
    resource_list = []
    for file in memes_path.rglob("*"):
        if not file.is_file() or not file.suffix in [".jpg", ".png", ".gif"]:
            continue
        resource_list.append(
            {
                "path": str(file.relative_to(memes_path).as_posix()),
                "hash": hashlib.md5(file.read_bytes()).hexdigest(),
            }
        )
    resource_list.sort(key=lambda i: i["path"])
    with open(dir_path / "resource_list.json", "w", encoding="utf-8") as f:
        json.dump(resource_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    update()
