

import pytest

import consolejs

__module__ = __import__(__name__)

def is_other_user(user):
    console = consolejs.get_console(__module__)
    console.debug("{user=}")
    return True

class Env:
    def __init__(self):
        # Importing functions
        pass

    def get_shell(self):
        console = consolejs.get_console(__module__)
        console.log('it works')
        is_other_user('test')
        return "shell"

def test_all_instance():
    cjs = consolejs.create(__module__)
    cjs.level = consolejs.DEBUG

    env_map = Env()
    env_map.get_shell()
