from ast import literal_eval
from aifi_fox_crypto import Crypt
class FileManager:
    _bufferStr = None
    _buffer = []
    _filename = None
    _extension = None
    _coding = None
    
    
    #init
    def __init__(self,paramsnum,filename = "settings",extension = "stng",crypt = False,pswrd = "hh.ru"):
        self._filename = filename
        self._pswrd = pswrd
        self._extension = extension
        self._crypt = crypt
        self._paramsNum = paramsnum
        self._Dev_ReOpen()
        self.cr = Crypt(self._pswrd,"old")
        
        
        
    def GetElement(self,index):
        return str(self._buffer[index])
    def SetElement(self,index,val):
            self._buffer.pop(index)
            self._buffer.insert(index,val)

    def Save(self):
        self._writefile(self._filename+'.'+self._extension,self._buffer)
    
    def _Dev_ReOpen(self):
        self._bufferStr = self._readfile(self._filename+'.'+self._extension)
        if (self._bufferStr == None) or (self._bufferStr == "New File"):
            for i in range(self._paramsNum):
               self._buffer.append('ready')
            self.Save()
            
        else:
           self._buffer = literal_eval(self._bufferStr)
           
            

    def _Dev_Get(self):
        return self._buffer
    def _Dev_Set(self,val):
        self._buffer = val
        
        

    #функция записи чтения
    def _writefile(self,fileopen,val):#,_crypt = None):
        try:
            with open("files/"+fileopen,'w') as file:
                file.write(str(val)) 
        except:
            print("Write Error")
    def _readfile(self,fileopen):#,_crypt = 0):
            try:
                with open("files/"+fileopen,'r') as file:
                    gi = file.read()
                return gi
            except:
                with open("files/"+fileopen,'w') as filed:
                    filed.write("New File")

           


    

