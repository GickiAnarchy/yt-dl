import os
import random
import pickle
from pytube import YouTube
import time
import PySimpleGUI as sg


L_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".", ".data"))
completed = f"{L_DIR}/.completed.fa"
BKP = f"{L_DIR}/.links.fa.bak"

class LinkList:
    def __init__(self):
        if not os.path.isdir(L_DIR):
            os.makedirs(L_DIR)
        self.links = []
        self.completed = []
        if os.path.isfile(f"{L_DIR}/.links.fa"):
            self.load()


    def save(self, fname = ".links.fa"):
        with open(f"{L_DIR}/{fname}", "wb") as file:
            pickle.dump(self.links, file)
            file.close()

    def load(self):
        with open(f"{L_DIR}/.links.fa", "rb") as file:
            self.links = pickle.load(file)
            file.close()

    def addCompleted(self, com):
        self.completed.append(f"{com}\n")
        self.stat2.update(f"{str(len(self.completed))} completed files.")

    def resetCompFile(self):
        os.remove(completed)
        with open(completed, "w") as file:
            file.close()
        self.completed = []

    def saveCompleted(self):
        with open(completed, "a") as file:
            for l in self.completed:
                file.write(l)
            file.close()
            
    def isDupe(self, chk):
        if chk in self.links:
            return True
        else:
            return False

    def add(self, link):
        if not self.isDupe(link):
            self.links.append(link)

    def getLinks(self):
        for link in self.links:
            print(link)

    def downloadLinks(self):
        if len(self.links) <= 0:
            return
        for link in self.links:
            yt = YouTube(link)
            video = yt.streams.filter(only_audio=True).first()
            destination = L_DIR
            out_file = video.download(output_path=destination)
            # save the file
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            self.addCompleted(link)
            os.rename(out_file, new_file)
        self.clearList()

    def clearList(self):
        self.save(fname = ".links.fa.bak")
        self.saveCompleted()
        self.links.clear()
        self.save()

    def Links(self):
        s = ""
        for l in self.links:
            s += f"{l}\n"
        return s

    @property
    def links(self):
        return self._links
    @links.setter
    def links(self, new_links):
        self._links = new_links
    @property
    def length(self):
        return str(len(self.links))

    def makeLayout(self):
        layout_left = [
        [sg.Text("Enter a link: "), sg.Input(key = "-LINK-")],
        [sg.Text(self.length, key = "-NUM-"), sg.Text(f"{sg.theme()}", key = "-THEME-")]
        ]
        layout_right = [
        [sg.Listbox(self.links, size = (45, 20), enable_events = True, key = "-LIST-")]
        ]
        layout_bottom = [
        [sg.Button("Add", key = "-ADD-"), sg.Button("Save", key = "-SAVE-"), sg.Button("Clear", key = "-CLEAR-"), sg.Button("Quit", key = "-QUIT-")],
        [sg.Text(""), sg.Button("DL LINKS", key = "-RUN-"), sg.Text("")]
        ]
        layout = [
        [sg.Column(layout_left, size = (480, 300), justification = "left"), sg.Column(layout_right, size = (480, 300), justification = "right")],
        [sg.Column(layout_bottom, size = (450, 80), element_justification = "center", justification = "bottom")],
        [sg.StatusBar("", key = "-STAT-", size = (50,3)), sg.StatusBar("", key = "-STAT2-", size = (50,3))]
        ]
        return layout

    def makeWindow(self):
        sg.theme(random.choice(sg.theme_list()))
        lo = self.makeLayout()
        win = sg.Window("__", lo, size = (980, 450), resizable = False, finalize = True)
        return win

    def cleanCom(self):
        com = self.completed
        self.completed = []
        for l in com:
            if l in self.completed:
                continue
            else:
                self.completed.append(l)
        self.stat.update("completed files optimized")

    def run(self):
        win = self.makeWindow()
        while True:
            event, values = win.read(timeout = 5000)
            no_lnks = win["-NUM-"]
            lst = win["-LIST-"]
            self.stat = win["-STAT-"]
            self.stat2 = win["-STAT2-"]
            
            if event in (None, "-QUIT-"):
                break
            
            if event == "-SAVE-":
                self.save()

            if event == "-ADD-":
                lnk = values["-LINK-"]
                if lnk == "BKP":
                    with open(BKP, "rb") as f:
                        backup = pickle.load(f)
                        l = "\n".join(backup)
                        f.close()
                    sg.popup(l)
                elif lnk == "BKPLOAD":
                    with open(BKP, "rb") as f:
                        backup = pickle.load(f)
                        self.links.extend(backup)
                        f.close()
                elif lnk == "COM":
                    with open(completed, "r") as f:
                        while True:
                            co = f.readline()
                            if not co:
                                self.stat2("End of completed links file")
                                break
                            if co not in self.completed:
                                self.completed.append(co)
                        f.close()
                    sc = "\n".join(self.completed)
                    sg.popup(sc)
                elif lnk == "CLEARCOM":
                    self.resetCompFile()
                elif lnk == "CLEANCOM":
                    self.cleanCom()
                else:
                    self.cleanCom()
                    if lnk.startswith("http"):
                        if lnk in self.completed:
                            return
                        else:
                            self.add(lnk)
                            self.stat2.update(f"+++: {lnk}")

            if event == "-CLEAR-":
                self.clearList()

            if event == "-RUN-":
                self.downloadLinks()

            if event in (sg.TIMEOUT_EVENT):
                pass

            if event is not None:
                no_lnks.update(str(len(self.links)))
                lst.update(self.links)

        win.close()




if __name__ == "__main__":
    LL = LinkList()
    LL.run()