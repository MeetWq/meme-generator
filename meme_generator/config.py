import toml
from typing import List
from pathlib import Path
from pydantic import BaseModel, Extra

from .dirs import get_config_file


config_file_path = get_config_file("config.toml")


class MemeConfig(BaseModel):
    load_builtin_memes: bool = True
    meme_dirs: List[Path] = []
    meme_disabled_list: List[str] = []


class ResourceConfig(BaseModel):
    resource_url: str = "https://ghproxy.com/https://github.com/MeetWq/meme-generator"


class GifConfig(BaseModel):
    gif_max_size: float = 10
    gif_max_frames: int = 100


class TranslatorConfig(BaseModel):
    baidu_trans_appid: str = ""
    baidu_trans_apikey: str = ""


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 2233


class Config(BaseModel, extra=Extra.ignore):
    meme: MemeConfig = MemeConfig()
    resource: ResourceConfig = ResourceConfig()
    gif: GifConfig = GifConfig()
    translate: TranslatorConfig = TranslatorConfig()
    server: ServerConfig = ServerConfig()

    @classmethod
    def load(cls) -> "Config":
        return cls.parse_obj(toml.load(config_file_path))

    def dump(self):
        with open(config_file_path, "w", encoding="utf8") as f:
            toml.dump(self.dict(), f)


if not config_file_path.exists():
    meme_config = Config()
else:
    meme_config = Config.load()
meme_config.dump()
