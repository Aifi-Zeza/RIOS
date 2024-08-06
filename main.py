from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
from PIL import Image 
from PIL import ImageTk as itk
from aifi_tkinter_addons import LabelButton
from aifi_file_instruments import FileManager
import os
from multiprocessing import Process
from time import sleep


class RIOS:
    _with = None
    _height = None
    _numcom = 0
    _comWidg = []
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
        self.window.title("RIOS-ALPHA v0.0.2")
        self.window.geometry(self._with+'x'+self._height)
        self.window.iconphoto(True,PhotoImage(file="files/icon.png"))
        self.wintabs.enable_traversal()
        self.FM = FileManager(100)

    def run(self):
        self._creataAppInterface()
        self._start()
        self.window.mainloop()
    

    def _start(self):
        self._initComPanel()

    def _initComPanel(self):
        for i in range(100):
            cnf = self.FM.GetElement(self._numcom)
            if cnf.count('&') > 0:
                self._createConf(cnf)
                
            else:
                continue
        

    def _creataAppInterface(self):
        self._createRootWindow()
        self._createDocPanel() 
        self._createPanelDevices()
        self._createPanelAudioCommands()





    def _createRootWindow(self):
        self._frameMain = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0)
        _frameCmd = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0,)
        self._frameMain.pack(fill=Y, expand=True)
        _frameCmd.pack(fill=X, expand=True)

        self.wintabs.add(self._frameMain, text="Main", compound=LEFT)
        self.wintabs.add(_frameCmd, text="cmd",compound=LEFT)

    def _createPanelDevices(self):
        _maindFrame = ttk.Frame(self._frameMain,height=int(self._height)-250,width=int(self._with)/1.8)
        _threeObjects = Canvas(self._frameMain,height=int(self._height)-250,width=200,bg='red')

        _threeObjects.grid(row=0,column=0,sticky=NSEW)
        _maindFrame.grid(row=0,column=1,sticky=NSEW)

    def _createPanelAudioCommands(self):
        _commandScrollBar = ttk.Scrollbar(self._frameMain,orient="vertical")
        self._CommandBarObject = Canvas(self._frameMain,width=(int(self._with)/4),height=int(self._height)-250,yscrollcommand=_commandScrollBar.set,bg='#d3d3d3',border=0)
        self._CommandPlate = Frame(self._CommandBarObject,background='blue',border=0,bg='#d3d3d3',highlightbackground='#d3d3d3',highlightcolor='#d3d3d3') 
        self._CommandBarObject.create_window((4,4),window=self._CommandPlate,anchor=NW)
        _commandScrollBar.configure(command=self._CommandBarObject.yview)
        _commandScrollBar.grid(row=0,column=2,sticky=NS)
        self._CommandBarObject.grid(row=0,column=3,sticky=NSEW)
        self._CommandBarObject.update_idletasks()
        self._CommandBarObject.configure(scrollregion=self._CommandPlate.bbox('all'))
        
    def _createDocPanel(self):
        self.mc = Canvas(self.winbutns,background='#ebfffe',width=25,height=self._height,border=0)
        _exitb = LabelButton("files/icons/exit.png",20,self.mc)#,command=self._close)
        _cmdb = LabelButton("files/icons/cmd.png",20,self.mc)#,command=self._start)
        self.mc.place(x=0,y=0)
        _cmdb.bind('<Button-1>',self._cmd)
        _exitb.bind('<Button-1>',self._createCommand)
        _exitb.place(x=0,y=0)
        _cmdb.place(x=0,y=25)

    def _EnterDataWindow(self):
        self._enterCommandWindow = Toplevel(self.window)
        self._enterCommandWindow.resizable(True,False)
        self._enterCommandWindow.geometry("400x200")
        self.name = Label(self._enterCommandWindow,text='Name')
        self.Name = Entry(self._enterCommandWindow)
        self.command = Label(self._enterCommandWindow,text='Command')
        self.Command = Entry(self._enterCommandWindow)
        self.audcommand = Label(self._enterCommandWindow,text='AudCommand')
        self.AudCommand = Entry(self._enterCommandWindow)
        Enter = ttk.Button(self._enterCommandWindow,text='Save',command=self._pdmtd)
        self.name.pack(anchor=N,expand=True,fill=X)
        self.Name.pack(anchor=N,expand=True,fill=X)
        self.audcommand.pack(anchor=N,expand=True,fill=X)
        self.AudCommand.pack(anchor=N,expand=True,fill=X) 
        self.command.pack(anchor=N,expand=True,fill=X)
        self.Command.pack(anchor=N,expand=True,fill=X)
        Enter.pack(anchor=N,expand=True,fill=X)
    

    def _pdmtd(self):
        command = self.Name.get() + '&' + self.Command.get()+'&'+self.AudCommand.get()
        self.FM.SetElement(self._numcom,command)
        self.FM.Save()
        self._enterCommandWindow.destroy()
        self._createConf(self.FM.GetElement(self._numcom))
    def _createConf(self,cnf = 'error&error'):
        menubut = Canvas(self._CommandPlate,width=int(self._CommandBarObject['width'])-12,height=60,bg='white',highlightbackground='#d3d3d3',highlightcolor='#d3d3d3')
        self._comWidg.append(menubut)

        cnf = cnf.split('&')
        menubutName = ttk.Label(menubut,justify='left',text=cnf[0])
        menubutCommand = ttk.Label(menubut,justify='left',text='AudCom: '+cnf[2])
        destrButt = LabelButton("files/icons/exit.png",20,menubut,self._numcom)
    
        menubut.grid(row=self._numcom+1,column=0,sticky=EW)
        menubutName.place(x=5,y=5,width=int(self._CommandBarObject['width'])-17)
        menubutCommand.place(x=5,y=30,width=int(self._CommandBarObject['width'])-17)
        destrButt.place(x=int(self._CommandBarObject['width'])-35,y=38)
        destrButt.bind('<Button-1>',lambda event:self._deleteConf(destrButt.positionstd))

        self._numcom += 1
        self._CommandBarObject.update_idletasks()
        self._CommandBarObject.configure(scrollregion=self._CommandPlate.bbox('all'))
    
        
    def _deleteConf(self,position):
        self._comWidg[position].destroy()
        self.FM.SetElement(position,'ready')
        self.FM.Save()
        self._cleanList()
        
            
    def _cleanList(self):
        for i in range(self.FM._paramsNum,0):
            elm = self.FM.GetElement(i)
            print(elm)
            if elm != 'ready':
                self._numcom = i - 1
                print(i)
                break
    #mp/thr
    


    #comands of buttons
    def _close(self,event=None):
        self.window.quit()

    def _cmd(self,event,arg):
        p = Process(target=os.system,args=(arg,),daemon=True)
        p.start()
        p.join()

    def _createCommand(self,event):
        self._EnterDataWindow()

if __name__ == "__main__":
   RIOS().run()