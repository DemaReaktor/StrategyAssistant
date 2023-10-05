class Strategy:
    def __init__(self, input, output, remove):
        self.__input = input
        self.__output = output
        self.__remove = remove

    @property
    def input(self):
        return self.__input

    @property
    def output(self):
        return self.__output

    @property
    def remove(self):
        return self.__remove
