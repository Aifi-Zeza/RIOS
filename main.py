from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
from PIL import Image 
from PIL import ImageTk as itk
from aifi_tkinter_addons import *
from aifi_file_instruments import FileManager
import os
from multiprocessing import Process
from time import sleep
import queue


class RIOS:
    _with = None
    _height = None
    _numcom = 0
    _comWidg = []
    _queCom = queue.Queue()
    _DatSize = 200
    _commandsHistory = []

    def __init__(self,w=1280,h=720):
        self._with = str(w)
        self._height = str(h)
        self.window = Tk()
        #self.window.resizable(False,False)
        
        self.mainframe = ttk.Frame(self.window,height=self._height,width=self._with)
        self.mainframe.pack(fill=BOTH,expand=True,anchor=SW)
        self.winbutns = ttk.Frame(self.mainframe,height=self._height,width=25,)
        self.wintabs = ttk.Notebook(self.mainframe,width=int(self._with)-25,height=self._height)
        self.winbutns.place(x=0,y=0)
        self.wintabs.place(x=25,y=0)
        self.opened_images = None
        self._init()
        self._CommandType = ['Console command','Device command','Other']

    def _init(self):
        self.window.title("RIOS-ALPHA v0.0.3v ")
        self.window.geometry(self._with+'x'+self._height)
        self.window.iconphoto(True,PhotoImage(file="files/icon.png"))
        self.wintabs.enable_traversal()
        self.FM = FileManager(self._DatSize,'commands','udat')
        for i in range(self._DatSize):
            self._queCom.put(i)

    def run(self):
        self._creataAppInterface()
        self._start()
        self.window.mainloop()
    

    def _start(self):
        self._initComPanel()

    def _initComPanel(self): 
        for i in range(self._DatSize):
            cnf = self.FM.GetElement(self._numcom)
            if cnf.count('&') > 0:
                compos = self._queCom.get()
                self._createConf(compos,cnf)
                
                
            else:
                continue
        

    def _creataAppInterface(self):
        self._createRootWindow()
        self._createSeparators()
        self._createDocPanel() 
        self._createPanelDevices()
        self._createPanelAudioCommands()
        self._createCommandInput()





    def _createRootWindow(self):
        self._frameCMenu = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0)
        self._frameMain = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0)
        self._frameSettings = ttk.Frame(self.wintabs,relief=FLAT,borderwidth=0)
        
        self._frameCMenu.pack(fill=Y, expand=True)
        self._frameMain.pack(fill=X, expand=True)
        self._frameSettings.pack(fill=X, expand=True)

        self.wintabs.add(self._frameMain, text="Main",compound=LEFT)
        self.wintabs.add(self._frameCMenu, text="Menu", compound=LEFT)
        self.wintabs.add(self._frameSettings, text="Settings",compound=LEFT)

    def _createSeparators(self):
        self.menuPanel = Canvas(self._frameCMenu,width=(int(self._with)/2.5+60),height=int(self._height)-250,bg='red')
        self.menuPanel.grid(row=0,column=2,sticky=NSEW)
    def _createPanelDevices(self):
        _deviceScrollBar = ttk.Scrollbar(self._frameCMenu,orient="vertical")
        self._DeviceBarObject = Canvas(self._frameCMenu,width=(int(self._with)/4),height=int(self._height)-250,yscrollcommand=_deviceScrollBar.set,bg='#d3d3d3',border=0)
        self._DevicePlate = Frame(self._DeviceBarObject,background='blue',border=0,bg='#d3d3d3',highlightbackground='#d3d3d3',highlightcolor='#d3d3d3') 
        self._DeviceBarObject.create_window((4,4),window=self._DevicePlate,anchor=NE)
        _deviceScrollBar.configure(command=self._DeviceBarObject.yview)
        _deviceScrollBar.grid(row=0,column=1,sticky=NS)
        self._DeviceBarObject.grid(row=0,column=0,sticky=NSEW)
        self._DeviceBarObject.update_idletasks()
        self._DeviceBarObject.configure(scrollregion=self._DevicePlate.bbox('all'))
        menubutv = Canvas(self._DevicePlate,width=int(self._DeviceBarObject['width'])-12,height=60,bg='white',highlightbackground='#d3d3d3',highlightcolor='#d3d3d3')
        menubutv.grid(row=self._numcom+1,column=0,sticky=EW)

    def _createPanelAudioCommands(self):
        _commandScrollBar = ttk.Scrollbar(self._frameCMenu,orient="vertical")
        self._CommandBarObject = Canvas(self._frameCMenu,width=(int(self._with)/4),height=int(self._height)-250,yscrollcommand=_commandScrollBar.set,bg='#d3d3d3',border=0)
        self._CommandPlate = Frame(self._CommandBarObject,background='blue',border=0,bg='#d3d3d3',highlightbackground='#d3d3d3',highlightcolor='#d3d3d3') 
        self._CommandBarObject.create_window((4,4),window=self._CommandPlate,anchor=NW)
        _commandScrollBar.configure(command=self._CommandBarObject.yview)
        _commandScrollBar.grid(row=0,column=3,sticky=NS)
        self._CommandBarObject.grid(row=0,column=4,sticky=NSEW)
        self._CommandBarObject.update_idletasks()
        self._CommandBarObject.configure(scrollregion=self._CommandPlate.bbox('all'))
    
    def _createCommandInput(self):
        _ccanvas = Canvas(self._frameCMenu,width=self._with,height=250)
        _ccanvas.place(x=0,y=int(self._height)-250)
        _commandFrame = ConsoleFrame(_ccanvas,self._with,11)
        _commandFrame.pack()

        
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
        self._enterCommandWindow.geometry("400x250")
        self.name = Label(self._enterCommandWindow,text='Name')
        self.Name = Entry(self._enterCommandWindow)
        self.audcommand = Label(self._enterCommandWindow,text='AudCommand')
        self.AudCommand = Entry(self._enterCommandWindow)
        self.type = Label(self._enterCommandWindow,text='Type')
        Enter = ttk.Button(self._enterCommandWindow,text='Save',command=self._pdmtd)
        self.commandType = ComboboxFrame(self._enterCommandWindow,variants={ 'options': self._CommandType,'lvar2': ['device1','device2'],'lvar3': [['device1','device4'], ['on','off']] })
        self.name.pack(anchor=N,expand=True,fill=X)
        self.Name.pack(anchor=N,expand=True,fill=X)
        self.audcommand.pack(anchor=N,expand=True,fill=X)
        self.AudCommand.pack(anchor=N,expand=True,fill=X)
        self.type.pack(anchor=N,expand=True,fill=X)
        self.commandType.pack(anchor=N,expand=True,fill=X)  
        Enter.pack(anchor=N,expand=True,fill=X)
    

    def _pdmtd(self):
        command = self.Name.get() + '&' + self.commandType.get()+'&'+self.AudCommand.get()
        datpos = self._queCom.get()
        self.FM.SetElement(datpos,command)   
        self.FM.Save()
        self._enterCommandWindow.destroy()
        self._createConf(datpos,self.FM.GetElement(datpos))
    def _createConf(self,datpos,cnf = 'error&error'):
        menubut = Canvas(self._CommandPlate,width=int(self._CommandBarObject['width'])-12,height=60,bg='white',highlightbackground='#d3d3d3',highlightcolor='#d3d3d3')
        self._comWidg.append(menubut)

        cnf = cnf.split('&')
        menubutName = ttk.Label(menubut,justify='left',text=cnf[0])
        menubutCommand = ttk.Label(menubut,justify='left',text='AudCom: '+cnf[2])
        destrButt = LabelButton("files/icons/exit.png",20,menubut,datpos)
    
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
        self._queCom.put(position)
            
        
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