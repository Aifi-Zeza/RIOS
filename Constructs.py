class Struct:
    object = {}
    def __init__(self,*args):
        for a in args:
            self.object[a] = 'none'
    
    def destroy(self):
        """Work with tkinter"""
        for io in self.object:
            try:
                self.object[io].destroy()
            except:
                pass
            finally:
                self.object[io] = 'none'

class Switch:
    def __init__(self,object_1):
        self.object = object_1
    def case(self,object_1):
        if self.object == object_1:
            return True
        else:
            return False