__version__ = "1.0.9"


from weakref import WeakKeyDictionary

from consolejs.disabled import ConsolejsDummy, ConsoleDummy
from consolejs.impl import ConsolejsImpl

_state_ = WeakKeyDictionary()

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


def get_console(module, theirs = None):
        if module in _state_: 
            console =  _state_[module].console
            return console
        return ConsoleDummy()


def create(module):
        name = module.__name__
        inst =  ConsolejsImpl(name)
        _state_[module] = inst
        return inst

def disabled():
        inst = ConsolejsDummy()
        return inst

