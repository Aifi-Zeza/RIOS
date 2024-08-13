from tkinter import *
from tkinter import ttk
from aifi_addons import *
from PIL import Image 
from PIL import ImageTk as itk

class LabelButton(ttk.Label):
    def __init__(self,path,size, master,position = 0,anchor=S, **kwargs):
        self.path = path
        self.size = size
        self.currenttype = 0
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

class ComboboxFrame:
    """Create a frame with combobox"""
    currentType = 0
    def __init__(self,master,variants = {'options':['1','2','3'],'lvar2':[],'lvar3':[[],[]]}):
        self.opt = variants['options']
        self.vars2 = variants['lvar2']
        self.vars3_1 = variants['lvar3'][0]
        self.vars3_2 = variants['lvar3'][1]
        

        self.mainframe = Frame(master)
        self.combobox = ttk.Combobox(self.mainframe,values=self.opt, state="readonly")
        self.combobox.current(2)
        self.combobox.bind("<<ComboboxSelected>>", self.callbackFunc)
        
                           
        self.variant1 = Struct('entry','label')

        self.variant2 = Struct('entry','label0','label1','combobox')
    
        self.variant3 = Struct('combobox1','label0','label1','combobox2')



    def pack(self,anchor = N,expand = False,fill = X):
        self.mainframe.pack(anchor=anchor,expand=expand,fill=fill)
        self.combobox.pack(anchor=anchor,expand=expand,fill=fill)
        self.callbackFunc(None)

    def callbackFunc(self,event):
        variant = self.combobox.get()
        switch = Switch(variant)
        if(switch.case(self.opt[0])):
            self.variant2.destroy()
            self.variant3.destroy()
            self.currentType = 0
            self.variant1.object['entry'] = Entry(self.mainframe)
            self.variant1.object['label'] = Label(self.mainframe,text='Command')
            self.variant1.object['label'].pack(anchor=N,expand=True,fill=X)
            self.variant1.object['entry'].pack(anchor=N,expand=True,fill=X)
        if(switch.case(self.opt[1])):
            self.variant1.destroy()
            self.variant3.destroy()
            self.currentType = 1
            self.variant2.object['entry'] = Entry(self.mainframe)
            self.variant2.object['label1'] = Label(self.mainframe,text='Device')
            self.variant2.object['label0'] = Label(self.mainframe,text='Command')
            self.variant2.object['combobox'] = ttk.Combobox(self.mainframe,values=self.vars2, state="readonly")
            self.variant2.object['combobox'].current(0)
            self.variant2.object['label1'].pack(anchor=N,expand=True,fill=X)
            self.variant2.object['combobox'].pack(anchor=N,expand=True,fill=X)
            self.variant2.object['label0'].pack(anchor=N,expand=True,fill=X)
            self.variant2.object['entry'].pack(anchor=N,expand=True,fill=X)
        if(switch.case(self.opt[2])):
            self.variant1.destroy()
            self.variant2.destroy()
            self.currentType = 2
            self.variant3.object['label0'] = Label(self.mainframe,text='Command')
            self.variant3.object['label1'] = Label(self.mainframe,text='Device')
            self.variant3.object['combobox1'] = ttk.Combobox(self.mainframe,values=self.vars3_1, state="readonly")
            self.variant3.object['combobox1'].current(0)
            self.variant3.object['combobox2'] = ttk.Combobox(self.mainframe,values=self.vars3_2, state="readonly")
            self.variant3.object['combobox2'].current(0)  
            self.variant3.object['label1'].pack(anchor=N,expand=True,fill=X)
            self.variant3.object['combobox1'].pack(anchor=N,expand=True,fill=X)
            self.variant3.object['label0'].pack(anchor=N,expand=True,fill=X)
            self.variant3.object['combobox2'].pack(anchor=N,expand=True,fill=X)
    def get(self):
        switch = Switch(self.currentType)
        if switch.case(0):
            return self.variant1.object['entry'].get()
        elif switch.case(1):
            return self.variant2.object['entry'].get() + '`' + self.variant2.object['combobox'].get()
        elif switch.case(3):
            return self.variant2.object['combobox1'].get() + '~' + self.variant2.object['combobox2'].get()
        else:
            return 'error'
        

import subprocess
import threading

class ConsoleFrame:
    def __init__(self, master,widtth,heightt):

        self.widtth = widtth
        self.heightt = heightt

        # Текстовое поле для вывода
        self.text = Text(master, state='disabled', wrap='word',height=12,width=200,relief=FLAT)

        # Поле ввода для команд
        self.entry = Entry(master)
        self.entry.bind("<Return>", self._RAECommand)

        # Вывод приветственного сообщения
        self.toConsole("Welcome to the PowerShell Console! Type a command and press Enter.\n")

    def pack(self):
        self.text.pack(anchor=N,expand=True)
        self.entry.pack(anchor=N,expand=True,fill=X)


    def toConsole(self, message):
        self.text.config(state='normal')  # Разрешаем редактировать текстовое поле
        self.text.insert(END, message + "\n")  # Вставляем сообщение
        self.text.see(END)  # Прокручиваем вниз
        self.text.config(state='disabled')  # Запрещаем редактирование текста

    def _RAECommand(self, event):
        command = self.entry.get()
        self.entry.delete(0, END)  # Очищаем строку ввода
        self.toConsole(f"> {command}")  # Печатаем команду в консоль

        # Запускаем команду в новом потоке
        threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()

    def execute_command(self, command):
        try:
            # Используем команду PowerShell и получаем вывод
            process = subprocess.Popen(
                ["powershell.exe", "-Command", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Буферизация по строкам
                universal_newlines=True  # Используем строковые представления (не байты)
            )

            # Читаем stdout
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    self.toConsole(output.strip())

            # Читаем stderr
            error = process.stderr.read()
            if error:
                self.toConsole("ERROR: " + error.strip())

        except Exception as e:
            self.toConsole("Exception: " + str(e))