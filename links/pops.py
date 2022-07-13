import PySimpleGUI as sg

pop_get_file = sg.popup_get_file("Choose a file",
                                                                title = "Down with YT",
                                                                default_extension = ".fa",
                                                                save_as = True)

"""
popup_get_file(message,
    title = None,
    default_path = "",
    default_extension = "",
    save_as = False,
    multiple_files = False,
    file_types = (('ALL Files', '*.* *'),),
    no_window = False,
    size = (None, None),
    button_color = None,
    background_color = None,
    text_color = None,
    icon = None,
    font = None,
    no_titlebar = False,
    grab_anywhere = False,
    keep_on_top = None,
    location = (None, None),
    relative_location = (None, None),
    initial_folder = None,
    image = None,
    files_delimiter = ";",
    modal = True,
    history = False,
    show_hidden = True,
    history_setting_filename = None)
"""