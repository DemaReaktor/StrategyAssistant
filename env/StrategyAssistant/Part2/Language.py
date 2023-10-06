class LanguageController:
    __texts = dict()
    __is_ukrainian = True

    @staticmethod
    def add(text, translate):
        Language.__texts[text] = translate

    @staticmethod
    def lan(text):
        return text if LanguageController.__is_ukrainian else __texts[text]

    @staticmethod
    def change_language():
        LanguageController.__is_ukrainian = not LanguageController.__is_ukrainian