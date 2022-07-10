#pylint:disable=E0401
import os
import random
import pickle
from linklist import LinkList
import PySimpleGUI as sg
from pytube import YouTube, Playlist
from re import search


MAGICK = "https://youtube.com/playlist?list=PLXS7fy2pHgKch6L4xtvybDqxo4tVWAoKK"

GREEN = "#6CD700"
RED = "#D70010"
BLUE = "#0800D7"

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".", ".data"))
completed = f"{data_dir}/.completed.fa"
BKP = f"{data_dir}/.links.fa.bak"


class Link_GUI:
    def __init__(self, linklist = None):
        print = sg.Print
        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)
        if linklist == None:
            self.LL = LinkList()
        else:
            self.LL = linklist
        if not self.hasSaved:
            self.load()


    @property
    def LL(self):
        return self._LL
    @LL.setter
    def LL(self, new_LL):
        self._LL = new_LL

    @property
    def hasSaved(self):
        return not os.path.exists(f"{data_dir}/.links.fa")

    def save(self, fname = ".links.fa"):
        with open(f"{data_dir}/{fname}", "wb") as file:
            pickle.dump(self.LL, file)
            file.close()
        sg.popup("SAVED")

    def load(self):
        with open(f"{data_dir}/.links.fa", "rb") as file:
            self.LL = pickle.load(file)
            file.close()

    def add(self, url: str):
        PL = "playlist"
        if search(PL, url):
            p = Playlist(url)
            videos = list(p.video_urls)
            for link in videos:
                self.LL.add_cur(link)
                print(f"{link} added")
        else:
            self.LL.add_cur(url)
            print(f"{url} added")

#
#    YT
#
    def download(self, link):
        yt = YouTube(link)
        #video = yt.streams.filter(only_audio=True).first()
        video = yt.streams.get_audio_only()
        destination = data_dir
        try:
            out_file = video.download(output_path=destination)
        except:
            return False
        base, ext = os.path.splitext(out_file)
        print(ext)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        name = os.path.split(new_file)
        self.LL.add_com(link, name[1])
        return True        

#
#    GUI
#
    def makeLayout(self):
        font = sg.DEFAULT_FONT
        font = (font[0], (font[1]//2) + 1)
        sg.set_options(font = font)

        layout_left = [
        [sg.Text("Enter a link: "), sg.Input(key = "-LINK-")],
        [sg.Multiline("", size = (50, 25), key = "-console-", reroute_cprint=True, reroute_stdout=True, autoscroll = True, disabled = True)]
        ]
        
        list_size = (50,13)

        layout_right = [
        [sg.TabGroup([
        [sg.Tab("Current", [[sg.Listbox(self.LL.current, size = list_size, enable_events = True, key = "-LIST-")]]),
        sg.Tab("Completed", [[sg.Listbox(self.LL.completedNames(), size = list_size, enable_events = True, key = "-COMP-")]])]])]
        ]

        layout_bottom = [
        [sg.Button("Add", key = "-ADD-", bind_return_key=True), sg.Button("Save", key = "-SAVE-"), sg.Button("Load", key = "-LOAD-"), sg.Button("Clear", key = "-CLEAR-")],
        [sg.Text(""), sg.Button("DL LINKS", key = "-RUN-"),sg.Button("Quit", key = "-QUIT-"), sg.Text("")]
        ]

        layout = [
        [sg.Column(layout_left, size = (520, 300), justification = "left", pad = (5,5)), sg.Column(layout_right, size = (520, 300), justification = "right", pad = (5,5))],
        [sg.Column(layout_bottom, element_justification = "center", justification = "center", pad = (5,5))],
        [sg.StatusBar("", key = "-STAT1-", size = (50,3)), sg.StatusBar("", key = "-STAT2-", size = (50,3))]
        ]
        return layout

    def makeWindow(self):
        sg.theme(random.choice(sg.theme_list()))
        lo = self.makeLayout()
        win = sg.Window("YT Downloader", lo, size = (980, 450), resizable = False, finalize = True)
        return win

    def run(self):
        window = self.makeWindow()
        while True:
            event, values = window.read()
            runBtn = window["-RUN-"]
            loadBtn = window["-LOAD-"]
            listBox = window["-LIST-"]
            comBox = window["-COMP-"]
            stat1 = window["-STAT1-"]
            stat2 = window["-STAT2-"]

            if event in (None, "-QUIT-", sg.WIN_CLOSED):
                if len(self.LL.current) > 0:
                    choice = sg.popup_yes_no("Save the list?")
                    if choice == "Yes":
                        self.save()
                break

            if event == "-SAVE-":
                print("Save pressed")
                self.save()

            if event == "-LOAD-":
                print("Load pressed")
                self.load()

            if event == "-CLEAR-":
                print("Clear pressed")
                choice = sg.popup_yes_no("Clear the current link list?")
                if choice == "Yes":
                    self.LL.current.clear()
                    print("Link List is cleared")

            if event == "-ADD-":
                print("Add pressed")
                l = values["-LINK-"]
                self.add(l)

            if event == "-RUN-":
                print("Download pressed")
                if len(self.LL.current) <= 0:
                    sg.popup("HEY! Link List is EMPTY!")
                runBtn.update(disabled = True)
                for link in self.LL.current:
                    window.perform_long_operation(lambda :self.download(link), "-END-")
                runBtn.update(disabled = False)

            if event is not None:
                loadBtn.update(disabled = self.hasSaved)
                listBox.update(self.LL.current)
                comBox.update(self.LL.completedNames())
                print("....update....")


if __name__ == "__main__":
    gui = Link_GUI()
    gui.run()