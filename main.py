from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
from PIL import Image 
from PIL import ImageTk as itk
from aifi_tkinter_addons import LabelButton
from file_instr import FileManager
import os
from multiprocessing import Process
from time import sleep


class RIOS:
    _with = None
    _height = None
    _numcom = 0
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
        self.FM = FileManager(100)

    def _drawApp(self): 
        self._frameMain = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0)
        _frameCmd = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0,)
        self._frameMain.pack(fill=Y, expand=True)
        _frameCmd.pack(fill=X, expand=True)

        self.wintabs.add(self._frameMain, text="Main", compound=LEFT)
        self.wintabs.add(_frameCmd, text="cmd",compound=LEFT)

        
        _maindFrame = ttk.Frame(self._frameMain,height=int(self._height)-250,width=int(self._with)/1.8)
        _threeObjects = Canvas(self._frameMain,height=int(self._height)-250,width=200,bg='red')


        
        _threeObjects.grid(row=0,column=0,sticky=NSEW)
        _maindFrame.grid(row=0,column=1,sticky=NSEW)
        self._createPanelAudioCommands()

       

      
        

       
    
    def _createPanelAudioCommands(self):
        _scrollBarMain = ttk.Scrollbar(self._frameMain,orient="vertical")
        self._audioFuncSB = Canvas(self._frameMain,width=(int(self._with)/4),height=int(self._height)-250,yscrollcommand=_scrollBarMain.set,bg='#d3d3d3',border=0)
        self._sbf = Frame(self._audioFuncSB,background='blue',border=0,bg='#d3d3d3',highlightbackground='#d3d3d3',highlightcolor='#d3d3d3') 
        self._audioFuncSB.create_window((4,4),window=self._sbf,anchor=NW)
        _scrollBarMain.configure(command=self._audioFuncSB.yview)
        _scrollBarMain.grid(row=0,column=2,sticky=NS)
        self._audioFuncSB.grid(row=0,column=3,sticky=NSEW)
        self._audioFuncSB.update_idletasks()
        self._audioFuncSB.configure(scrollregion=self._sbf.bbox('all'))
        
    
    def _drawDocPanel(self):
        self.mc = Canvas(self.winbutns,background='#ebfffe',width=25,height=self._height,border=0)
        _exitb = LabelButton("files/icons/exit.png",self.mc)#,command=self._close)
        _cmdb = LabelButton("files/icons/cmd.png",self.mc)#,command=self._start)
        self.mc.place(x=0,y=0)
        _cmdb.bind('<Button-1>',self._cmd)
        _exitb.bind('<Button-1>',self._createCommand)
        _exitb.place(x=0,y=0)
        _cmdb.place(x=0,y=25)

    def _EnterWindow(self):
        
        self._wind = Toplevel(self.window)
        self._wind.geometry("400x200")
        self.Name = Entry(self._wind)
        self.Command = Entry(self._wind)
        Enter = ttk.Button(self._wind,text='Save',command=self._pdmtd)
        self.Name.pack(anchor=N,expand=True,fill=X)
        self.Command.pack(anchor=N,expand=True,fill=X)
        Enter.pack(anchor=N,expand=True,fill=X)
    

    def _pdmtd(self):
        command = self.Name.get() + '&' + self.Command.get()
        self.FM.SetElement(self._numcom,command)
        self.FM.Save()
        self._wind.destroy()
        menubut = Canvas(self._sbf,width=int(self._audioFuncSB['width'])-12,height=60,bg='white',highlightbackground='#d3d3d3',highlightcolor='#d3d3d3')
        cnf = self.FM.GetElement(self._numcom)
        
        cnf = cnf.split('&')
        menubutName = ttk.Label(menubut,justify='left',text=cnf[0])
        menubutCommand = ttk.Label(menubut,justify='left',text='command: '+cnf[1])
    
        menubut.grid(row=self._numcom+1,column=0,sticky=EW)
        menubutName.place(x=5,y=5,width=int(self._audioFuncSB['width'])-17)
        menubutCommand.place(x=5,y=30,width=int(self._audioFuncSB['width'])-17)
        

        self._numcom += 1
        self._audioFuncSB.update_idletasks()
        self._audioFuncSB.configure(scrollregion=self._sbf.bbox('all'))
    
        
             


            

        
    #mp/thr
    


    #comands of buttons
    def _close(self,event=None):
        self.window.quit()

    def _cmd(self,event,arg):
        p = Process(target=os.system,args=(arg,),daemon=True)
        p.start()
        p.join()

    def _createCommand(self,event):
        self._EnterWindow()

if __name__ == "__main__":
   RIOS().run()