import sys
import os
import marshal
import tkinter.ttk as ttk
from tkinter import FLAT,Y,LEFT
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
class inModule():
    object = {}
    master = None
    def __init__(self, name,description = ''):
        self.name = name
        self.description = description
#пустышка

              

class ModuleManager:
    def __init__(self, master):
        self.master = master
        self.modules = []
        module_frame = ttk.Frame(self.master,relief=FLAT,borderwidth=0)

    def load_modules(self,path_to_module = []):
        for path in path_to_module:
            self.load_module(path)

    def load_module(self, path_to_module):
        module_namespace = {}
        with open(path_to_module, 'rb') as f:
            code = marshal.load(f)
        exec(code, module_namespace)  # Выполнение кода модуля

        if 'thisModule' in module_namespace:
            module_instance = module_namespace['Module']()
            frame = ttk.Frame(self.master,relief=FLAT,borderwidth=0)
            frame.pack(fill=Y, expand=True)
            module_instance.inModule.master = frame  # Установка master
            self.modules.append(module_instance)  # Запуск инициализации модуля
            module_namespace = None
            module_instance = None
        for module in self.modules:
            module.start()   
            
            self.master.add(module.inModule.master, text=module.inModule.name,compound=LEFT)




        