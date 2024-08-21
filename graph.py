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

        self._queueCommandDataSlots = queue.Queue()
        self._queueDeviceDataSlots = queue.Queue()
        self.FM = FileManager(self._dataSize, 'commands', 'udat')
        self.FMD = FileManager(self._dataSize, 'devices', 'udat') 


    def start(self):
        self._createSeparators()
        self._createPanelDevices()
        self._createPanelAudioCommands()
        self._initPanels()
        self._createCommandInput()

    def _initPanels(self):
        self.initComPanelData()
        self.initDevicePanelData()

    def initComPanelData(self):
        for i in range(self._dataSize):
            self._queueCommandDataSlots.put(i)

        for elementId in range(self._dataSize):
            cnf = self.FM.GetElement(elementId)
            if cnf.count('&') > 0:
                compos = self._queueCommandDataSlots.get()
                self.commandPanel._Create(compos, cnf)

    def initDevicePanelData(self):
        for i in range(self._dataSizeDevice):
            self._queueDeviceDataSlots.put(i)

        for elementId in range(self._dataSizeDevice):
            cnf = self.FM.GetElement(elementId)
            if cnf.count('&') > 0:
                compos = self._queueDeviceDataSlots.get()
                self.commandPanel._Create(compos, cnf)
        self._devices = self.FMD._Dev_Get()

    def _createSeparators(self):
        self.menuPanel = Canvas(self.master, width=(int(self._width) / 2.5 + 60), height=int(self._height) - 250, bg='red')
        self.menuPanel.grid(row=0, column=2, sticky=NSEW)

    def _createPanelDevices(self):
        self.devicePanel = ElementPanel(self.master,(int(self._width) / 4),int(self._height) - 250,self._queueDeviceDataSlots,self.FMD)
        self.devicePanel.grid(row=0, column=0, sticky=NSEW)

    def _createPanelAudioCommands(self):
        self.commandPanel = ElementPanel(self.master,(int(self._width) / 4),int(self._height) - 250,self._queueCommandDataSlots,self.FM,'left')
        self.commandPanel.grid(row=0, column=3, sticky=NSEW)

    def _createCommandInput(self):
        _ccanvas = Canvas(self.master, width=self._width, height=250)
        _ccanvas.place(x=0, y=int(self._height) - 250)
        _commandFrame = ConsoleFrame(_ccanvas, self._width, 11)
        _commandFrame.pack()

    def _EnterDataWindow(self):
        self._enterCommandWindow = Toplevel(self.root)
        self._enterCommandWindow.grab_set()
        self._enterCommandWindow.protocol("WM_DELETE_WINDOW", self.passm)
        self._enterCommandWindow.resizable(True, False)
        self._enterCommandWindow.geometry("400x250")

        # Creating labels and entries
        self.name = Label(self._enterCommandWindow, text='Name')
        self.Name = Entry(self._enterCommandWindow)
        self.audcommand = Label(self._enterCommandWindow, text='AudCommand')
        self.AudCommand = Entry(self._enterCommandWindow)
        self.type = Label(self._enterCommandWindow, text='Type')

        # Saving button
        Enter = ttk.Button(self._enterCommandWindow, text='Save', command=self._setelement)

        # Command type selection
        self.commandType = ComboboxFrame(self._enterCommandWindow,
                                          variants={'options': self._commandType,
                                                    'lvar2': self._devices,
                                                    'lvar3': [self._devices, ['on', 'off']]})

        # Packing elements
        for widget in [self.name, self.Name, self.audcommand, self.AudCommand, self.type, self.commandType, Enter]:
            widget.pack(anchor=N, expand=True, fill=X)

    def _setelement(self):
        command = self.Name.get() + '&' + self.commandType.get() + '&' + self.AudCommand.get()
        self._enterCommandWindow.grab_release()
        self._enterCommandWindow.destroy()
        self.commandPanel.CreateElement(command)
        

   
    def passm(self):
        pass

    # Commands of buttons
    def _close(self, event=None):
        self.root.quit()

    def _cmd(self, event, arg):
        p = Process(target=os.system, args=(arg,), daemon=True)
        p.start()
        p.join()

    def _createCommand(self, event):
        self._EnterDataWindow()