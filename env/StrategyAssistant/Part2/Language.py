import requests
from mtranslate import translate as google_translate


class LanguageController:
    __texts = dict()

    def __init__(self):
        self.__is_ukrainian = True

    @staticmethod
    def add(text, translate):
        if not isinstance(text, str):
            raise TypeError('text should have type "str"')
        if not isinstance(translate, str) and not isinstance(translate, list):
            raise TypeError('translate should have type "str" or "list"')
        if isinstance(translate, list) and any(not isinstance(value, str) for value in translate):
            raise TypeError('every translate element should have type "str"')
        Language.__texts[text] = translate

    @staticmethod
    def add(dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError('dictionary should have type "dict"')
        for key, value in dictionary.items():
            if not isinstance(key, str):
                raise TypeError('translate should have key type "str"')
            if not isinstance(value, str) and not isinstance(value, list):
                raise TypeError('value should have type "str" or "list"')
            if isinstance(value, list) and any(not isinstance(element, str) for element in value):
                raise TypeError('every element of translate element should have type "str"')
        LanguageController.__texts.update(dictionary)

    def translate(self, text):
        if not (text in LanguageController.__texts.keys()):
            return text if self.__is_ukrainian else google_translate(text,'en','ua')
        value = LanguageController.__texts[text]
        if isinstance(value, list):
            if not self.__is_ukrainian and value[1 - self.__is_ukrainian] == '':
                # translate with google translater
                value[1] = google_translate(value[0],'en','ua')
            return value[1 - self.__is_ukrainian]
        return text if self.__is_ukrainian else value

    def change(self):
        self.__is_ukrainian = not self.__is_ukrainian