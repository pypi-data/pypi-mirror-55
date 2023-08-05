__version__ = "1.0.7"



from .disabled import ConlogDummy, ConsoleDummy
from conlog.impl import ConlogImpl

class Conlog:

    _state_ = dict()

    @classmethod 
    def get_console(cls, name):
        if name in cls._state_: 
            console =  cls._state_[name].console
            return console
        return ConsoleDummy()

    @classmethod
    def create(cls, name):
        inst =  ConlogImpl(name)

        cls._state_[name] = inst
        return inst

    @classmethod
    def disabled(cls):
        inst = ConlogDummy()
        return inst

