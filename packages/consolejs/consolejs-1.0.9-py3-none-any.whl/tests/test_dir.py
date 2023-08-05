import consolejs

__module__ = __import__(__name__)

def test_console_dir():

    cjs = consolejs.create(__module__)
    cjs.level = consolejs.DEBUG
    console = cjs.console

    my_dict = {'name':'Jack', 'age': 26}

    console.dir(my_dict)
