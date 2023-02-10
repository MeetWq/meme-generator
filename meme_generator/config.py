from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    gif_max_size: float = 10
    gif_max_frames: int = 100
    baidu_trans_appid: str = ""
    baidu_trans_apikey: str = ""


meme_config = Config()
