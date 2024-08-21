from types import inModule
from tkinter import *

class thisModule:
    def __init__(self):
        self.inModule = inModule('text entry','test')
    

    def start(self):
        self.inModule.object['entry'] = Entry(self.inModule.master,)
        self.inModule.object['entry'].pack(expand=True,fill=X)

    def module(self):
        return self.inModule
    
