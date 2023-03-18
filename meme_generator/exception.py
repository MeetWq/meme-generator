from typing import Optional


class MemeGeneratorException(Exception):
    status_code: int = 520

    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Error in meme_generator: {self.message}"


class NoSuchMeme(MemeGeneratorException):
    status_code: int = 531

    def __init__(self, meme_key: str):
        self.meme_key = meme_key
        message = f'No such meme with key="{self.meme_key}"'
        super().__init__(message)


class TextOverLength(MemeGeneratorException):
    status_code: int = 532

    def __init__(self, text: str):
        self.text = text
        message = f'Text "{self.text}" is too long!'
        super().__init__(message)


class OpenImageFailed(MemeGeneratorException):
    status_code: int = 533

    def __init__(self, error_message: str):
        self.error_message = error_message
        message = f'Error opening images: "{self.error_message}"'
        super().__init__(message)


class ParserExit(MemeGeneratorException):
    status_code: int = 534

    def __init__(self, status: int = 0, error_message: Optional[str] = None):
        self.status = status
        self.error_message = error_message or ""
        message = (
            f"Argument parser failed to parse. (status={self.status}"
            + (f", message={self.error_message!r}" if self.error_message else "")
            + ")"
        )
        super().__init__(message)


class ParamsMismatch(MemeGeneratorException):
    status_code: int = 540

    def __init__(self, meme_key: str, message: str):
        self.meme_key = meme_key
        self.message = message

    def __repr__(self) -> str:
        return f'ParamsMismatch(key="{self.meme_key}", message="{self.message}")'


class ImageNumberMismatch(ParamsMismatch):
    status_code: int = 541

    def __init__(self, meme_key: str, min_images: int = 0, max_images: int = 0):
        message = (
            "The number of images is incorrect, "
            f"it should be no less than {min_images} and no more than {max_images}"
        )
        super().__init__(meme_key, message)


class TextNumberMismatch(ParamsMismatch):
    status_code: int = 542

    def __init__(self, meme_key: str, min_texts: int = 0, max_texts: int = 0):
        message = (
            "The number of texts is incorrect, "
            f"it should be no less than {min_texts} and no more than {max_texts}"
        )
        super().__init__(meme_key, message)


class TextOrNameNotEnough(ParamsMismatch):
    status_code: int = 543

    def __init__(self, meme_key: str, message: Optional[str] = None):
        message = message or "The number of texts or user names is not enough"
        super().__init__(meme_key, message)


class ArgMismatch(ParamsMismatch):
    status_code: int = 550
    pass


class ArgParserExit(ArgMismatch):
    status_code: int = 551

    def __init__(self, meme_key: str, error_message: str):
        self.error_message = error_message
        message = f"Argument parser failed to parse: {self.error_message}"
        super().__init__(meme_key, message)


class ArgModelMismatch(ArgMismatch):
    status_code: int = 552

    def __init__(self, meme_key: str, error_message: str):
        self.error_message = error_message
        message = f"Argument model validation failed: {self.error_message}"
        super().__init__(meme_key, message)
