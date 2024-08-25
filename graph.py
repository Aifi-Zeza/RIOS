import os
import queue
from multiprocessing import Process
from tkinter import *
import tkinter.ttk as ttk
from aifi_file_instruments import FileManager
from Extensions import *



class audioPanel:
    def __init__(self, master, root, width, height):
        self.master = master
        self.root = root
        self._width = width
        self._height = height
        self._dataSize = 200
        self._dataSizeDevice = 50
        self._numcom = 0
        self._commandWidget = []
        self._commandType = ['Console command','Device command','Device state']
        self._devices = []
        self.bvc = master.register(base_validate_input)
        self.svc = master.register(spec_validate_input)

        self._queueCommandDataSlots = queue.Queue()
        self._queueDeviceDataSlots = queue.Queue()
        self.FM = FileManager(self._dataSize, 'commands', 'udat')
        self.FMD = FileManager(self._dataSizeDevice, 'devices', 'udat')
        self.AudioCommands = {} 


    def start(self):
        self._createSeparators()
        self._createPanelDevices()
        self._createPanelAudioCommands()
        self._initPanels()
        self._createCommandInput()

    def _initPanels(self):
        self.initDevicePanelData()
        self.initComPanelData()

    def initComPanelData(self):
        for i in range(self._dataSize):
            self._queueCommandDataSlots.put(i)

        for elementId in range(self._dataSize):
            cnf = self.FM.GetElement(elementId)
            if cnf.count('&') > 0:
                compos = self._queueCommandDataSlots.get()
                self.commandPanel._Create(compos, cnf)
                cnf = cnf.split('&')
                self.AudioCommands[cnf[2]] = elementId
        #print(self.AudioCommands) 

    def initDevicePanelData(self):
        for i in range(self._dataSizeDevice):
            self._queueDeviceDataSlots.put(i)

        for elementId in range(self._dataSizeDevice):
            cnf = self.FMD.GetElement(elementId)
            if cnf.count('&') > 0:
                compos = self._queueDeviceDataSlots.get()
                print(compos)
                self.devicePanel._Create(compos, cnf)
        self._updateListDevice()

    def _createSeparators(self):
        self.menuPanel = Canvas(self.master, width=(int(self._width) / 2.5 + 60), height=int(self._height) - 250, bg='red')
        self.menuPanel.grid(row=0, column=2, sticky=NSEW)

    def _createPanelDevices(self):
        self.devicePanel = ElementPanel(self.master,(int(self._width) / 4),int(self._height) - 250,self._queueDeviceDataSlots,self.FMD,self._enterDeviceDataWindow)
        self.devicePanel.grid(row=0, column=0, sticky=NSEW)

    def _createPanelAudioCommands(self):
        self.commandPanel = ElementPanel(self.master,(int(self._width) / 4),int(self._height) - 250,self._queueCommandDataSlots,self.FM,self._EnterComDataWindow,'left')
        self.commandPanel.grid(row=0, column=3, sticky=NSEW)

    def _createCommandInput(self):
        _ccanvas = Canvas(self.master, width=self._width, height=250)
        _ccanvas.place(x=0, y=int(self._height) - 250)
        _commandFrame = ConsoleFrame(_ccanvas, self._width, 11)
        _commandFrame.pack()

    def _EnterComDataWindow(self,e):
        self._enterCommandWindow = Toplevel(self.root)
        self._enterCommandWindow.grab_set()
        self._enterCommandWindow.resizable(True, False)
        self._enterCommandWindow.geometry("400x250")

        # Creating labels and entries
        self.name = Label(self._enterCommandWindow, text='Name')
        self.Name = Entry(self._enterCommandWindow,validate="key", validatecommand=(self.svc, '%P'))
        self.audcommand = Label(self._enterCommandWindow, text='AudCommand')
        self.AudCommand = Entry(self._enterCommandWindow,validate="key", validatecommand=(self.bvc, '%P'))
        self.type = Label(self._enterCommandWindow, text='Type')

        # Saving button
        Enter = ttk.Button(self._enterCommandWindow, text='Save', command=self._setComElement)

        # Command type selection
        self.commandType = ComboboxFrame(self._enterCommandWindow,self._devices,
                                          variants={'options': self._commandType,
                                                    'lvar2': self._devices,
                                                    'lvar3': [self._devices, ['on', 'off']]})

        # Packing elements
        for widget in [self.name, self.Name, self.audcommand, self.AudCommand, self.type, self.commandType, Enter]:
            widget.pack(anchor=N, expand=True, fill=X)

    def _setComElement(self):
        if self.commandType.get() != 'devnotfou':
            command = self.Name.get() + '&' + self.commandType.get() + '&' + self.AudCommand.get()
            self._enterCommandWindow.grab_release()
            self._enterCommandWindow.destroy()
            self.commandPanel.CreateElement(command)

    def _enterDeviceDataWindow(self,e):
        self._enterDDeviceWindow = Toplevel(self.root)
        self._enterDDeviceWindow.grab_set()
        self._enterDDeviceWindow.resizable(True, False)
        self._enterDDeviceWindow.geometry("400x250")

        self.Dname = Label(self._enterDDeviceWindow, text='Device Name')
        self.DName = Entry(self._enterDDeviceWindow,validate="key", validatecommand=(self.svc, '%P'))
        self.DType = Label(self._enterDDeviceWindow, text='Protocol')
        self.Dcombobox = ttk.Combobox(self._enterDDeviceWindow,values=['COM','ZigBee','chtoto'], state="readonly")
        self.Dcombobox.current(0)

        Enter = ttk.Button(self._enterDDeviceWindow, text='Save', command=self._setDeviceElement)

        for widget in [self.Dname, self.DName, self.DType, self.Dcombobox, Enter]:
            widget.pack(anchor=N, expand=True, fill=X)
        
    def _setDeviceElement(self):
        data = self.DName.get() + '&' + self.Dcombobox.get() + '&' 'xxxxxx'
        self._enterDDeviceWindow.grab_release()
        self._enterDDeviceWindow.destroy()
        self.devicePanel.CreateElement(data)
        self._updateListDevice()
   
    def _updateListDevice(self):
        self._devices = []
        for elementId in range(self._dataSizeDevice):
            cnf = self.FMD.GetElement(elementId)
            if cnf.count('&') > 0:
                data = cnf.split('&')
                self._devices.append(data[0])
                print(len(self._devices))    
                

    # Commands of buttons
    def _close(self, event=None):
        self.root.quit()

    def _cmd(self, event, arg):
        p = Process(target=os.system, args=(arg,), daemon=True)
        p.start()
        p.join()


class mainPanel:
    def __init__(self, master, root, width, height):
        self.master = master
        self.root = root
        self._width = width
        self._height = height
        self.cx,self.cy = int(width/2),int(height/2)
        self._createInterface()

    def _createInterface(self):
        print('init main panel')
        image = LabelImage(self.master,'files/icons/crystall.png',160)
        image.place(x=self.cx-80,y=self.cy-80)

