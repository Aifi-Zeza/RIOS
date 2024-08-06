from tkinter import *
from tkinter import ttk
from PIL import Image 
from PIL import ImageTk as itk

class LabelButton(ttk.Label):
    def __init__(self,path,size, master,position = 0,anchor=S, **kwargs):
        self.path = path
        self.size = size
        self.positionstd = position
        ttk.Label.__init__(self, master=master, **kwargs)
        self.pathToImage = self.path
        self['anchor'] = anchor
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        image = Image.open(self.pathToImage)
        image = image.resize((self.size, self.size)) 
        self.defaultImage = itk.PhotoImage(image)
        image = Image.open(self.pathToImage+'.png')
        image = image.resize((self.size, self.size)) 
        self.Activ = itk.PhotoImage(image)
        self['image'] = self.defaultImage
    def on_enter(self, e):
        self['image'] = self.Activ

    def on_leave(self, e):
        self['image'] = self.defaultImage