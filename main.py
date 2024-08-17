from tkinter import *
from tkinter import ttk
from graph import *

class RIOS:
    def __init__(self, w=1280, h=720):
        self._width = str(w)
        self._height = str(h)
        self.window = Tk()
        
        # Создание основных фреймов
        self.mainframe = ttk.Frame(self.window, height=self._height, width=self._width)
        self.mainframe.pack(fill=BOTH, expand=True, anchor=SW)
        
        self.winbutns = ttk.Frame(self.mainframe, height=self._height, width=25)
        self.wintabs = ttk.Notebook(self.mainframe, width=int(self._width) - 25, height=self._height)
        self.winbutns.place(x=0, y=0)
        self.wintabs.place(x=25, y=0)
        
        self.opened_images = None
        self._init()

    def _init(self):
        """Инициализация основного окна."""
        self.window.title("RIOS-ALPHA v0.0.3v ")
        self.window.geometry(f"{self._width}x{self._height}")
        self.window.iconphoto(True, PhotoImage(file="files/icon.png"))
        self.wintabs.enable_traversal()

    def run(self):
        """Запуск главного цикла приложения."""
        self._createAppInterface()
        self.window.mainloop()

    def _createAppInterface(self):
        """Создание интерфейса приложения."""
        self._createRootWindow()  # Создание корневых фреймов
        self.createFrame()         # Создание фрейма для аудиокоманд
        self._createDocPanel()     # Создание панели с кнопками

    def _createRootWindow(self):
        """Создание основных фреймов для вкладок."""
        self._frameCMenu = ttk.Frame(self.wintabs, relief=FLAT, borderwidth=0)
        self._frameMain = ttk.Frame(self.wintabs, relief=FLAT, borderwidth=0)
        self._frameSettings = ttk.Frame(self.wintabs, relief=FLAT, borderwidth=0)

        # Добавление фреймов во вкладки
        self.wintabs.add(self._frameMain, text="Main", compound=LEFT)
        self.wintabs.add(self._frameCMenu, text="Menu", compound=LEFT)
        self.wintabs.add(self._frameSettings, text="Settings", compound=LEFT)


    def createFrame(self):
        """Создание фрейма для управления аудиокомандами."""
        self.tf = audioPanel(self._frameCMenu, self.window, self._width, self._height)
        self.tf.start()

    def _createDocPanel(self):
        """Создание панели инструментов с кнопками."""
        self.mc = Canvas(self.winbutns, background='#ebfffe', width=25, height=self._height, border=0)
        
        _exitb = LabelButton("files/icons/exit.png", 20, self.mc)
        _cmdb = LabelButton("files/icons/cmd.png", 20, self.mc)
        
        self.mc.place(x=0, y=0)
        _cmdb.bind('<Button-1>', self.tf._cmd)
        _exitb.bind('<Button-1>', self.tf._createCommand)

        _exitb.place(x=0, y=0)
        _cmdb.place(x=0, y=25)

    def _testmodules(self):
        """Тестирование и загрузка модулей."""
        mm = ModuleManager(self.wintabs)
        mm.load_module('modules/file.rpycm')

if __name__ == "__main__":
    RIOS().run()