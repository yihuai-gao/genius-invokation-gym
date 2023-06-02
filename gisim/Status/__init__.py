# from .FrozenEffect import *


def get_character_status(name: str):
    stripped_name = name.replace(" ", "")
    return globals()[stripped_name]
