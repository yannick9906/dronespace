import tkinter as tk
import tkinter.ttk as ttk
from tk.yannickfelix.tkwrapper.gTextOutput import *
from tk.yannickfelix.tkwrapper.gTextInput import *


class GWindow(object):
    textoutput = None
    textinput = None
    userinput = None
    quitButton = None
    window = None
    mainFrame = None

    def __init__(self, title: str="A Game Window"):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("800x600")
        self.mainFrame = ttk.Frame(master=self.window)
        self.mainFrame.place(x=0, y=0, width=800, height=600)
        self.textoutput = GTextOutput(master=self.mainFrame)
        self.textoutput.label.place(x=0, y=0, width=402, height=550)
        self.textinput = GTextInput(master=self.mainFrame)
        self.textinput.entry.place(x=0, y=550, width=402, height=50)



