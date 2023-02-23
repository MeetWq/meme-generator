import toml
from typing import List
from pathlib import Path
from pydantic import BaseModel, Extra

from .dirs import get_config_file


config_file_path = get_config_file("config.toml")


class MemeConfig(BaseModel):
    meme_dirs: List[Path] = []
    meme_disabled_list: List[str] = []


class GifConfig(BaseModel):
    gif_max_size: float = 10
    gif_max_frames: int = 100


class TranslatorConfig(BaseModel):
    baidu_trans_appid: str = ""
    baidu_trans_apikey: str = ""


class Config(BaseModel, extra=Extra.ignore):
    meme: MemeConfig = MemeConfig()
    gif: GifConfig = GifConfig()
    translate: TranslatorConfig = TranslatorConfig()

    @classmethod
    def load(cls) -> "Config":
        return cls.parse_obj(toml.load(config_file_path))

    def dump(self):
        with open(config_file_path, "w", encoding="utf8") as f:
            toml.dump(self.dict(), f)


if not config_file_path.exists():
    meme_config = Config()
    meme_config.dump()
else:
    meme_config = Config.load()
