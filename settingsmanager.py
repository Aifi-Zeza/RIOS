from sys import getdefaultencoding



class settingsmanager:
    _buffer = {}
    _filename = None
    _extension = None
    _coding = None
    #init
    def __init__(self,filename = "settings",extension = "stng",coding = "None"):
        self._filename = filename
        self._extension = extension
        self._coding = coding
        

    #функция записи чтения
    def _writefile(self,fileopen,val):
        try:
            with open("files/"+fileopen,'w') as file:
                file.write(str(val)) 
        except:
            print('Filemanager:coud not open and write file')
    def _readfile(self,fileopen):
        try:
            with open("files/"+fileopen,'r') as file:
                gi = file.read()
            return gi
        except:
            print("Filemanager:file not found")
            return "error"

    def _codingval(self,data,type,mode):
        if (mode == "IN"):
            if (type == "None"):
               self._writefile(self._filename+"."+self._extension,data)
            if (type == "Simbols"):
                pass
        if (mode =="OUT"):
            if (type == "None"):
               _buf = self._readfile(self._filename+"."+self._extension)
               self._buffer = _buf
               
           



    def Set(self,dict):
        self._codingval(dict,"Simbols","IN")
    def Get(self): 
        self._codingval(None,"Simbols","OUT")
        return self._buffer

