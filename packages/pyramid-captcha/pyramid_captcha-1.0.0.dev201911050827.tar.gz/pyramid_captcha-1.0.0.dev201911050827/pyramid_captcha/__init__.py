# -*- coding: utf-8 -*-
import io
from uuid import uuid4

from captcha.image import ImageCaptcha

from pyramid_captcha.exception import CaptchaMissingError, CaptchaMismatchError


class Captcha(object):

    _ERROR_MISSING_SESSION = 'Missing captcha value in session'
    _ERROR_MISSING_FORM = 'No captcha value received in form data'
    _ERROR_MISMATCH = 'Captcha mismatch'

    def __init__(self, request, session_key='captcha', form_key='captcha', length=6):
        self._request = request
        self._captcha = ImageCaptcha()
        self._session_key = session_key
        self._form_key = form_key
        self._length = length

    def generate(self):
        value = uuid4().hex[:self._length]
        image = self._captcha.generate_image(value)
        self._request.session[self._session_key] = value
        response = self._request.response
        with io.BytesIO() as buffer:
            image.save(buffer, format='PNG')
            response.body = buffer.getvalue()
        response.content_type = 'image/png'
        response.content_length = len(response.body)
        return response

    def validate(self):
        if self._session_key in self._request.session:
            session_value = self._request.session[self._session_key]
            del self._request.session[self._session_key]
            if not self._request.POST[self._form_key]:
                raise CaptchaMissingError(self._ERROR_MISSING_FORM)
            elif session_value != self._request.POST[self._form_key]:
                raise CaptchaMismatchError(self._ERROR_MISMATCH)
        else:
            raise CaptchaMissingError(self._ERROR_MISSING_SESSION)
