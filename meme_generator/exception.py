from typing import Optional


class MemeGeneratorException(Exception):
    status_code: int = 520

    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"表情制作出错！{self.message}"


class NoSuchMeme(MemeGeneratorException):
    status_code: int = 531

    def __init__(self, meme_key: str):
        self.meme_key = meme_key
        message = f"表情“{self.meme_key}”不存在"
        super().__init__(message)


class TextOverLength(MemeGeneratorException):
    status_code: int = 532

    def __init__(self, text: str):
        self.text = text
        message = f"文本“{self.text}”过长"
        super().__init__(message)


class OpenImageFailed(MemeGeneratorException):
    status_code: int = 533

    def __init__(self, error_message: str):
        self.error_message = error_message
        message = f"图片加载失败（{self.error_message}）"
        super().__init__(message)


class ParamsMismatch(MemeGeneratorException):
    status_code: int = 540

    def __init__(self, meme_key: str, message: str):
        self.meme_key = meme_key
        message = f"表情“{self.meme_key}”参数不匹配：{message}"
        super().__init__(message)


class ImageNumberMismatch(ParamsMismatch):
    status_code: int = 541

    def __init__(self, meme_key: str, min_images: int = 0, max_images: int = 0):
        message = f"图片数量不符，图片数量应为 {min_images}" + (
            f" ~ {max_images}" if max_images > min_images else ""
        )
        super().__init__(meme_key, message)


class TextNumberMismatch(ParamsMismatch):
    status_code: int = 542

    def __init__(self, meme_key: str, min_texts: int = 0, max_texts: int = 0):
        message = f"文本数量不符，文本数量应为 {min_texts}" + (
            f" ~ {max_texts}" if max_texts > min_texts else ""
        )
        super().__init__(meme_key, message)


class TextOrNameNotEnough(ParamsMismatch):
    status_code: int = 543

    def __init__(self, meme_key: str, message: Optional[str] = None):
        message = message or "文本或用户名数量不足"
        super().__init__(meme_key, message)


class ArgMismatch(ParamsMismatch):
    status_code: int = 550
    pass


class ArgParserMismatch(ArgMismatch):
    status_code: int = 551

    def __init__(self, meme_key: str, error_message: str):
        self.error_message = error_message
        message = f"参数解析失败（{self.error_message}）"
        super().__init__(meme_key, message)


class ArgModelMismatch(ArgMismatch):
    status_code: int = 552

    def __init__(self, meme_key: str, error_message: str):
        self.error_message = error_message
        message = f"参数模型验证失败（{self.error_message}）"
        super().__init__(meme_key, message)
