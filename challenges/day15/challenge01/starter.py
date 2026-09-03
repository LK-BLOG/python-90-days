"""Challenge 1: 温度转换器"""
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        # TODO
        pass

    @celsius.setter
    def celsius(self, value):
        # TODO: 验证 >= -273.15
        pass

    @property
    def fahrenheit(self):
        # TODO
        pass

    @property
    def kelvin(self):
        # TODO
        pass
