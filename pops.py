import os
import PySimpleGUI as sg
import base64images

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

def splash():
	DISPLAY_TIME_MILLISECONDS = 4000
	
	layout = [[sg.Image(data = base64images.DWY_LOGO)]]
	win = sg.Window("Down With YT", layout, finalize = True, modal = True, transparent_color=sg.theme_background_color(), no_titlebar=True, keep_on_top=True)

	while True:
		event, values = win.read(timeout=DISPLAY_TIME_MILLISECONDS, close=True)
		if event == sg.WIN_CLOSED:
		    break
	win.close()



'''
sg.Window('Window Title', [[]], ).read(timeout=DISPLAY_TIME_MILLISECONDS, close=True)
'''