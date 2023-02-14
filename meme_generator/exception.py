from typing import Optional


class MemeGeneratorException(Exception):
    def __str__(self) -> str:
        return self.__repr__()


class NoSuchMeme(MemeGeneratorException):
    def __init__(self, meme_key: str):
        self.meme_key = meme_key

    def __repr__(self) -> str:
        return f'No such meme with key="{self.meme_key}"'


class TextOverLength(MemeGeneratorException):
    def __init__(self, text: str):
        self.text = text

    def __repr__(self) -> str:
        return f'Text "{self.text}" is too long!'


class ParamsMismatch(MemeGeneratorException):
    def __init__(self, meme_key: str, message: Optional[str] = None):
        self.meme_key = meme_key
        self.message = message

    def __repr__(self) -> str:
        return (
            f"ParamsMismatch(key={self.meme_key}"
            + (f", message={self.message!r}" if self.message else "")
            + ")"
        )


class ImageNumberMismatch(ParamsMismatch):
    def __init__(self, meme_key: str, min_images: int = 0, max_images: int = 0):
        message = (
            "The number of images is incorrect, "
            f"it should be no less than {min_images} and no more than {max_images}"
        )
        super().__init__(meme_key, message)


class TextNumberMismatch(ParamsMismatch):
    def __init__(self, meme_key: str, min_texts: int = 0, max_texts: int = 0):
        message = (
            "The number of texts is incorrect, "
            f"it should be no less than {min_texts} and no more than {max_texts}"
        )
        super().__init__(meme_key, message)


class TextOrNameNotEnough(ParamsMismatch):
    def __init__(self, meme_key: str, message: Optional[str] = None):
        self.meme_key = meme_key
        self.message = message or "The number of texts or user names is not enough"


class ArgMismatch(ParamsMismatch):
    pass


class ArgParserExit(ArgMismatch):
    def __init__(
        self, meme_key: str, status: int = 0, error_message: Optional[str] = None
    ):
        self.status = status
        self.error_message = error_message
        message = (
            f"Argument parser failed to parse. (status={self.status}"
            + (f", message={self.error_message!r}" if self.error_message else "")
            + ")"
        )
        super().__init__(meme_key, message)


class ArgModelMismatch(ArgMismatch):
    def __init__(self, meme_key: str, error_message: Optional[str] = None):
        self.error_message = error_message
        message = f"Argument model validation failed." + (
            f" (message={self.error_message!r})" if self.error_message else ""
        )
        super().__init__(meme_key, message)


class OpenImageFailed(ParamsMismatch):
    def __init__(self, meme_key: str, error_message: Optional[str] = None):
        self.error_message = error_message
        message = f"Error opening images." + (
            f" (message={self.error_message!r})" if self.error_message else ""
        )
        super().__init__(meme_key, message)
