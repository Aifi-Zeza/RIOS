from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
from PIL import Image 
from PIL import ImageTk as itk
from tkinterButton import LabelButton
import os
from multiprocessing import Process


class RIOS:
    _with = None
    _height = None
    def __init__(self,w=1280,h=720):
        self._with = str(w)
        self._height = str(h)
        self.window = Tk()
        self.window.resizable(False,False)
        
        self.mainframe = ttk.Frame(self.window,height=self._height,width=self._with)
        self.mainframe.pack(fill=BOTH,expand=True,anchor=SW)
        self.winbutns = ttk.Frame(self.mainframe,height=self._height,width=25,)
        self.wintabs = ttk.Notebook(self.mainframe,width=int(self._with)-25,height=self._height)
        self.winbutns.place(x=0,y=0)
        self.wintabs.place(x=25,y=0)
        self.opened_images = None
        self._init()

    def _init(self):
        self.window.title("RIOS-ALPHA v0.0.1")
        self.window.geometry(self._with+'x'+self._height)
        self.window.iconphoto(True,PhotoImage(file="files/icon.png"))
        self.wintabs.enable_traversal()

    def run(self):
        self._start()
        self._drawApp()
        self._drawDocPanel()
        self.window.mainloop()
    

    def _start(self):
        pass

    def _drawApp(self): 
        _frameMain = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0)
        _frameCmd = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0,)
        _frameMain.pack(fill=Y, expand=True)
        _frameCmd.pack(fill=X, expand=True)

        self.wintabs.add(_frameMain, text="Main", compound=LEFT)
        self.wintabs.add(_frameCmd, text="cmd",compound=LEFT)
        _scrollBarMain = ttk.Scrollbar(_frameMain,orient="vertical")
        _scrollBarMainCanvas = Canvas(_frameMain,width=(int(self._with)/2)/1.5,height=int(self._height)-200,yscrollcommand=_scrollBarMain.set,bg='red')
        _scrollBarMain.configure(command=_scrollBarMainCanvas.yview)
        _scrollBarMain.grid(row=0,column=4,sticky=NS)
        _scrollBarMainCanvas.grid(row=0,column=5,sticky=NSEW)


      
        

       
    
        
        
    
    def _drawDocPanel(self):
        self.mc = Canvas(self.winbutns,background='#ebfffe',width=25,height=self._height)
        _exitb = LabelButton("files/icons/exit.png",self.mc)#,command=self._close)
        _cmdb = LabelButton("files/icons/cmd.png",self.mc)#,command=self._start)
        self.mc.place(x=0,y=0)
        _cmdb.bind('<Button-1>',self._cmd)
        _exitb.bind('<Button-1>',self._close)
        _exitb.place(x=0,y=0)
        _cmdb.place(x=0,y=25)
        
    #mp/thr
    


    #comands of buttons
    def _close(self,event=None):
        self.window.quit()

    def _cmd(self,event,arg):
        p = Process(target=os.system,args=(arg,),daemon=True)
        p.start()
        p.join()



if __name__ == "__main__":
   RIOS().run()