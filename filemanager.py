def writefile(fileopen,val):
    try:
        with open("files/"+fileopen,'w') as file:
         file.write(str(val))
    except:
        print('Filemanager:coud not open and write file')
def readfile(fileopen):
    try:
        with open("files/"+fileopen,'r') as file:
            gi = file.read()
        return gi
    except:
        print("Filemanager:file not found")
        return "error"

