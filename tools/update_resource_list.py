import hashlib
import json
from pathlib import Path

dir_path = Path(__file__).parent
project_path = dir_path.parent
memes_path = project_path / "meme_generator" / "memes"
resource_list_path = project_path / "resources" / "resource_list.json"


def update():
    resource_list = []
    for file in memes_path.rglob("*"):
        if not file.is_file() or file.suffix not in [".jpg", ".png", ".gif"]:
            continue
        resource_list.append(
            {
                "path": str(file.relative_to(memes_path).as_posix()),
                "hash": hashlib.md5(file.read_bytes()).hexdigest(),
            }
        )
    resource_list.sort(key=lambda i: i["path"])
    with open(resource_list_path, "w", encoding="utf-8") as f:
        json.dump(resource_list, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    update()
