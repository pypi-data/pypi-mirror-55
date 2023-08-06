# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import json


ERROR_MESSAGES = {
    "en": {0: "OK", 1: "Error"},
    "zh-Hans": {0: "OK", 1: "Error"},
}
LANGUAGE = "zh-Hans"


def set_language(language):
    global LANGUAGE
    LANGUAGE = language

def set_error_message(language, code, message):
    if not language in ERROR_MESSAGES:
        ERROR_MESSAGES[language] = {0: "OK", 1: "Error"}
    ERROR_MESSAGES[language][code] = message

def get_error_message(code, language=None):
    return ERROR_MESSAGES.get(language or LANGUAGE, {}).get(code, "No error message...")


class classproperty(property):
    """Subclass property to make classmethod properties possible"""
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class BizError(RuntimeError):
    """Base class of all errors.
    """
    CODE = 1

    @classproperty
    @classmethod
    def MESSAGE(cls):
        return get_error_message(cls.CODE)

    def __init__(self, message=None):
        message = message or get_error_message(self.CODE)
        super().__init__(self.CODE, message)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return json.dumps({
            "code": self.args[0],
            "message": self.args[1]
        }, ensure_ascii=False)

    @property
    def code(self):
        return self.args[0]

    @property
    def message(self):
        return self.args[1]

    @property
    def json(self):
        return {
            "code": self.code,
            "message": self.message,
        }


class OK(BizError):
    CODE = 0

