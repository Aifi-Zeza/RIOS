from tkinter import *
from tkinter import ttk
from types import *
from PIL import Image 
from PIL import ImageTk as itk
import subprocess
import threading
from nnm import *
from Constructs import *

from tkinter import ttk

class LabelImage(ttk.Label):
    def __init__(self, master, path, size, anchor=S,sizeY = None, **kwargs):
        self.path = path
        self.sizeX = size
        self.sizeY = sizeY
        super().__init__(master=master, **kwargs)
        self['anchor'] = anchor

        # Загрузка основного изображения
        self.defaultImage = self.load_image(path)
        self['image'] = self.defaultImage

    def load_image(self, path):
        image = Image.open(path)
        if self.sizeY != None:
            image = image.resize((self.sizeX, self.sizeY))
        else:
            image = image.resize((self.sizeX, self.sizeX))     
        return itk.PhotoImage(image)


class LabelButton(ttk.Label):
    def __init__(self, path, size, master, position=0, anchor=S,sizeY = None, **kwargs):
        self.path = path
        self.sizeX = size
        self.sizeY = sizeY
        self.position = position
        super().__init__(master=master, **kwargs)
        self['anchor'] = anchor

        # Загрузка основного изображения
        self.defaultImage = self.load_image(path)
        self['image'] = self.defaultImage

        # Создание затемненного изображения
        self.Activ = self.create_dimmer_image(self.defaultImage, 0.5)  # 50% затемнение

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def load_image(self, path):
        image = Image.open(path)
        if self.sizeY != None:
            image = image.resize((self.sizeX, self.sizeY))
        else:
            image = image.resize((self.sizeX, self.sizeX))     
        return itk.PhotoImage(image)

    def create_dimmer_image(self, image, opacity):
        # Преобразуем PhotoImage обратно в PIL-объект
        original_image = itk.getimage(image).convert("RGBA")

        # Создаем новое изображение для выходного результата
        dimmed_image = Image.new("RGBA", original_image.size)

        for x in range(original_image.width):
            for y in range(original_image.height):  
                r, g, b, a = original_image.getpixel((x, y))
                # Проверяем если пиксель непрозрачный
                if a > 0:  
                    # Применяем затемнение
                    r = int(r * (1 - opacity))
                    g = int(g * (1 - opacity))
                    b = int(b * (1 - opacity))
                # Устанавливаем новый пиксель
                dimmed_image.putpixel((x, y), (r, g, b, a))

        return itk.PhotoImage(dimmed_image)

    def on_enter(self, e):
        self['image'] = self.Activ  # меняем на затемненное изображение

    def on_leave(self, e):
        self['image'] = self.defaultImage  # возвращаем оригинальное изображение


class ComboboxFrame:
    """Create a frame with combobox"""
    currentType = 0
    def __init__(self,master,devices,variants = {'options':['1','2','3'],'lvar2':[],'lvar3':[[],[]]}):
        self.opt = variants['options']
        self.vars2 = variants['lvar2']
        self.vars3_1 = variants['lvar3'][0]
        self.vars3_2 = variants['lvar3'][1]
        self.devices = True if len(devices) > 0 else False 

        self.bvc = master.register(base_validate_input)
        self.svc = master.register(spec_validate_input)
        

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
            self.variant1.object['entry'] = Entry(self.mainframe,validate="key", validatecommand=(self.svc, '%P'))
            self.variant1.object['label'] = Label(self.mainframe,text='Command')
            self.variant1.object['label'].pack(anchor=N,expand=True,fill=X)
            self.variant1.object['entry'].pack(anchor=N,expand=True,fill=X)
        elif self.devices:
            if(switch.case(self.opt[1])):
                self.variant1.destroy()
                self.variant3.destroy()
                self.currentType = 1
                self.variant2.object['entry'] = Entry(self.mainframe,validate="key", validatecommand=(self.svc, '%P'))
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
        else:
            self.variant1.destroy()
            self.currentType = 3
            self.variant2.object['label0'] = Label(self.mainframe,text='Devices not Found')
            self.variant2.object['label0'].pack(anchor=N,expand=True,fill=X)
    def get(self):
        switch = Switch(self.currentType)
        if switch.case(0):
            return self.variant1.object['entry'].get()
        elif switch.case(1):
            return self.variant2.object['entry'].get() + '`' + self.variant2.object['combobox'].get()
        elif switch.case(2):
            return self.variant3.object['combobox1'].get() + '`' + self.variant3.object['combobox2'].get()
        elif switch.case(3):
            return 'devnotfou'
        else:
            return 'error cf'
        

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


class ElementPanel(Frame):
    def __init__(self, master, width, height,queue,filemanadger,EnterDataMethod, scrollbar_position='right',):
        super().__init__(master, bg='#d3d3d3')
        self._width = width
        self._height = height
        self._queue = queue
        self.FM = filemanadger
        self.scrollbar_position = scrollbar_position
        self.method = EnterDataMethod

        self.cePosition = self.FM.dataLenth + 2
        print(self.cePosition)
        # Списки для хранения конфигов и виджетов
        self.elementList = []
        self._numcom = 1

        self._createPanel()
        self._createAddElement()

    def _createAddElement(self):
        element = Canvas(self._CommandPlate, width=int(self._CommandBarObject['width']) - 12, height=60,
                            bg='white', highlightbackground='#d3d3d3', highlightcolor='#d3d3d3')
        
        addbuton = LabelButton("files/icons/exit.png", size=int(self._CommandBarObject['width']) - 16, master=element,sizeY=56)
        element.grid(row=self.cePosition, column=0, sticky=EW)
        addbuton.place(x=2, y=2)
        addbuton.bind('<Button-1>',self.method)

        self._CommandBarObject.update_idletasks()
        self._CommandBarObject.configure(scrollregion=self._CommandPlate.bbox('all'))

    def _createPanel(self):
        _commandScrollBar = ttk.Scrollbar(self, orient="vertical")

        self._CommandBarObject = Canvas(self, width=self._width, height=self._height,
                                            yscrollcommand=_commandScrollBar.set, bg='#d3d3d3', border=0)

        self._CommandPlate = Frame(self._CommandBarObject, background='blue', border=0, bg='#d3d3d3',
                                       highlightbackground='#d3d3d3', highlightcolor='#d3d3d3')
        self._CommandBarObject.create_window((4, 4), window=self._CommandPlate, anchor=NW)

        _commandScrollBar.configure(command=self._CommandBarObject.yview)

        if self.scrollbar_position == 'left':
            _commandScrollBar.pack(side=LEFT, fill=Y)
            self._CommandBarObject.pack(side=RIGHT, fill=BOTH, expand=True)
        else:
            _commandScrollBar.pack(side=RIGHT, fill=Y)
            self._CommandBarObject.pack(side=LEFT, fill=BOTH, expand=True)

        self._CommandBarObject.update_idletasks()
        self._CommandBarObject.configure(scrollregion=self._CommandPlate.bbox('all'))
    def CreateElement(self,info):
        datpos = self._queue.get()
        self.FM.SetElement(datpos, info)
        self.FM.Save()
        self._Create(datpos, self.FM.GetElement(datpos))
    
    def _Create(self, datpos, shrinkedData='error&error'):
        element = Canvas(self._CommandPlate, width=int(self._CommandBarObject['width']) - 12, height=60,
                            bg='white', highlightbackground='#d3d3d3', highlightcolor='#d3d3d3')
        self.elementList.append(element)

        shrinkedData = shrinkedData.split('&')
        elementName = ttk.Label(element, justify='left', text=shrinkedData[0])
        elementFunction = ttk.Label(element, justify='left', text='AudCom: ' + shrinkedData[2])
        destroyButton = LabelButton("files/icons/exit.png", 20, element, datpos)

        element.grid(row=datpos + 1, column=0, sticky=EW)
        elementName.place(x=5, y=5, width=int(self._CommandBarObject['width']) - 17)
        elementFunction.place(x=5, y=30, width=int(self._CommandBarObject['width']) - 17)
        destroyButton.place(x=int(self._CommandBarObject['width']) - 35, y=5)
        destroyButton.bind('<Button-1>', lambda event: self.DeleteElement(event,destroyButton.position))

        self._CommandBarObject.update_idletasks()
        self._CommandBarObject.configure(scrollregion=self._CommandPlate.bbox('all'))

    def DeleteElement(self, event,position):
        self.elementList[position].destroy()
        self.FM.SetElement(position, 'ready')
        self.FM.Save()
        self._queue.put(position)

class aidioCommandExecuter:
    def __init__(self,filemanadger,audcommands):
        self.FM = filemanadger
        self.acom = audcommands
        self.voskr = voskRecognition(self.getCommand)
        self.wwp = WakeWordProgramm(self.voskr.record)
        self.voskr.unresult = self.wwp.start
        self.bertp = BERTPrediction()

    def getCommand(self,text):
        self.bertp.basesentece(text)
        for acomakey in self.acom:
            if self.bertp.get_cosine_similarity(acomakey):
                print(self.acom[acomakey])
            else:
                print('loss')

    def start(self):
        self.wwp.start()

def base_validate_input(input_text,):
    # Проверяем, содержит ли вводимый текст запрещённые символы
    forbidden_characters = "0123456789!@#$%^&*()`~"
    for char in forbidden_characters:
        if char in input_text:
            return False
    return True

def spec_validate_input(input_text):
    # Проверяем, содержит ли вводимый текст запрещённые символы
    forbidden_characters = "&`"
    for char in forbidden_characters:
        if char in input_text:
            return False
    return True