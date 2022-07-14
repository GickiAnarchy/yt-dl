import os
import PySimpleGUI as sg

DEFAULT_DIR = os.path.dirname(__file__)


def pop_save():
    pop = sg.popup_get_file("Save File: ", title = "Down with YT", default_extension = ".fa", save_as = True)
    if pop in (None, "Cancel"):
        return False
    return pop

def pop_load():
    pop = sg.popup_get_file("Load File: ", title = "Down with YT", default_extension = ".fa")
    if pop in (None, "Cancel"):
        return False
    return pop

def pop_oops(msg = "There was a problem downloading."):
    pop = sg.popup_error(f"OOPS!! {msg}", auto_close = True, auto_close_duration = 5)
    return pop
