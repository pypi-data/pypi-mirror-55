# -*- coding: utf-8 -*-


class CaptchaError(Exception):
    pass


class CaptchaMissingError(CaptchaError):
    pass


class CaptchaMismatchError(CaptchaError):
    pass
