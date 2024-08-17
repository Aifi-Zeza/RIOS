import os
import queue
from multiprocessing import Process
from tkinter import *
import tkinter.ttk as ttk
from aifi_file_instruments import FileManager
from aifi_tkinter_addons import *


class audioPanel:
    def __init__(self, master, root, width, height):
        self.master = master
        self.root = root
        self._width = width
        self._height = height
        self._dataSize = 200
        self._numcom = 0
        self._commandWidget = []
        self._commandType = ['Console command','Device command','Device state']

        self._queueCommandDataSlots = queue.Queue()
        self.FM = FileManager(self._dataSize, 'commands', 'udat')

    def start(self):
        self._createSeparators()
        self._createPanelDevices()
        self._createPanelAudioCommands()
        self._initComPanel()
        self._createCommandInput()

    def _initComPanel(self):
        for i in range(self._dataSize):
            self._queueCommandDataSlots.put(i)

        for elementId in range(self._dataSize):
            cnf = self.FM.GetElement(self._numcom)
            if cnf.count('&') > 0:
                compos = self._queueCommandDataSlots.get()
                self._createConf(compos, cnf)

    def _createSeparators(self):
        self.menuPanel = Canvas(self.master, width=(int(self._width) / 2.5 + 60), height=int(self._height) - 250, bg='red')
        self.menuPanel.grid(row=0, column=2, sticky=NSEW)

    def _createPanelDevices(self):
        _deviceScrollBar = ttk.Scrollbar(self.master, orient="vertical")
        self._DeviceBarObject = Canvas(self.master, width=(int(self._width) / 4), height=int(self._height) - 250,
                                        yscrollcommand=_deviceScrollBar.set, bg='#d3d3d3', border=0)
        self._DevicePlate = Frame(self._DeviceBarObject, background='blue', border=0, bg='#d3d3d3',
                                  highlightbackground='#d3d3d3', highlightcolor='#d3d3d3')
        self._DeviceBarObject.create_window((4, 4), window=self._DevicePlate, anchor=NE)
        _deviceScrollBar.configure(command=self._DeviceBarObject.yview)

        _deviceScrollBar.grid(row=0, column=1, sticky=NS)
        self._DeviceBarObject.grid(row=0, column=0, sticky=NSEW)
        self._DeviceBarObject.update_idletasks()
        self._DeviceBarObject.configure(scrollregion=self._DevicePlate.bbox('all'))

        menubutv = Canvas(self._DevicePlate, width=int(self._DeviceBarObject['width']) - 12, height=60, bg='white',
                          highlightbackground='#d3d3d3', highlightcolor='#d3d3d3')
        menubutv.grid(row=self._numcom + 1, column=0, sticky=EW)

    def _createPanelAudioCommands(self):
        _commandScrollBar = ttk.Scrollbar(self.master, orient="vertical")
        self._CommandBarObject = Canvas(self.master, width=(int(self._width) / 4), height=int(self._height) - 250,
                                        yscrollcommand=_commandScrollBar.set, bg='#d3d3d3', border=0)
        self._CommandPlate = Frame(self._CommandBarObject, background='blue', border=0, bg='#d3d3d3',
                                   highlightbackground='#d3d3d3', highlightcolor='#d3d3d3')
        self._CommandBarObject.create_window((4, 4), window=self._CommandPlate, anchor=NW)
        _commandScrollBar.configure(command=self._CommandBarObject.yview)

        _commandScrollBar.grid(row=0, column=3, sticky=NS)
        self._CommandBarObject.grid(row=0, column=4, sticky=NSEW)
        self._CommandBarObject.update_idletasks()
        self._CommandBarObject.configure(scrollregion=self._CommandPlate.bbox('all'))

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
        Enter = ttk.Button(self._enterCommandWindow, text='Save', command=self._pdmtd)

        # Command type selection
        self.commandType = ComboboxFrame(self._enterCommandWindow,
                                          variants={'options': self._commandType,
                                                    'lvar2': ['device1', 'device2'],
                                                    'lvar3': [['device1', 'device4'], ['on', 'off']]})

        # Packing elements
        for widget in [self.name, self.Name, self.audcommand, self.AudCommand, self.type, self.commandType, Enter]:
            widget.pack(anchor=N, expand=True, fill=X)

    def _pdmtd(self):
        command = self.Name.get() + '&' + self.commandType.get() + '&' + self.AudCommand.get()
        datpos = self._queueCommandDataSlots.get()
        self.FM.SetElement(datpos, command)
        self.FM.Save()
        self._enterCommandWindow.grab_release()
        self._enterCommandWindow.destroy()
        self._createConf(datpos, self.FM.GetElement(datpos))

    def _createConf(self, datpos, cnf='error&error'):
        menubut = Canvas(self._CommandPlate, width=int(self._CommandBarObject['width']) - 12, height=60, bg='white',
                         highlightbackground='#d3d3d3', highlightcolor='#d3d3d3')
        self._commandWidget.append(menubut)

        cnf = cnf.split('&')
        menubutName = ttk.Label(menubut, justify='left', text=cnf[0])
        menubutCommand = ttk.Label(menubut, justify='left', text='AudCom: ' + cnf[2])
        destrButt = LabelButton("files/icons/exit.png", 20, menubut, datpos)

        menubut.grid(row=self._numcom + 1, column=0, sticky=EW)
        menubutName.place(x=5, y=5, width=int(self._CommandBarObject['width']) - 17)
        menubutCommand.place(x=5, y=30, width=int(self._CommandBarObject['width']) - 17)
        destrButt.place(x=int(self._CommandBarObject['width']) - 35, y=38)
        destrButt.bind('<Button-1>', lambda event: self._deleteConf(destrButt.positionstd))

        self._numcom += 1
        self._CommandBarObject.update_idletasks()
        self._CommandBarObject.configure(scrollregion=self._CommandPlate.bbox('all'))

    def _deleteConf(self, position):
        self._commandWidget[position].destroy()
        self.FM.SetElement(position, 'ready')
        self.FM.Save()
        self._queueCommandDataSlots.put(position)

    def passm(self):
        pass

    # Commands of buttons
    def _close(self, event=None):
        self.window.quit()

    def _cmd(self, event, arg):
        p = Process(target=os.system, args=(arg,), daemon=True)
        p.start()
        p.join()

    def _createCommand(self, event):
        self._EnterDataWindow()