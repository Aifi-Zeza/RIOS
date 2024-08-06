import cryptography as cript
from cryptography.fernet import Fernet as fern 
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt as skr
import secrets
import base64
import platform
import os



class Crypt:
    def __init__(self,pswrd,key="new",lenth = 16):
        self._pswrd = pswrd
        if key == "new":
            self._key = self._genkey(pswrd,"new",lenth)
        elif key == "old":
            self._key = self._genkey(pswrd,"old")
        else:
            print("Error Key Type")
        


    def _genSlt(self,size = 16):
        return secrets.token_bytes(size)
    def _loadSlt(self):
        return open("files/slt.s","rb").read()
    def _drvKey(self,slt,pswrd):
        kdf = skr(salt=slt,length=32,n=2**14,r=8,p=1)
        return kdf.derive(pswrd.encode())

    def _genkey(self,_pswrd,_ON_slt ="new",_slt_sz=16):
        if _ON_slt == "old":
            _slt = self._loadSlt()
        elif _ON_slt == "new":
            _slt = self._genSlt(_slt_sz)
            with open("files/slt.s","wb") as slts:
                slts.write(_slt)

        _drvd_key = self._drvKey(_slt,_pswrd)
        return base64.urlsafe_b64encode(_drvd_key)
    
    def decrypt(self,file,_key = None):
        if _key == None:
            key = self._key
        else:
            key = _key
        fernt = fern(key)
        try:
            dcr_data  = fernt.decrypt(file)
        except cript.fernet.InvalidToken:
            print("invalid key")
            return
        return dcr_data
    def encrypt(self,file,_key=None):
        if _key == None:
            key = self._key
        else:
            key = _key
        fernt = fern(key)
        encd_data = fernt.encrypt(file)
        return encd_data

class PasswordManager:
    def __init__(self):
        self.cr = Crypt(_password,slt)
        _password, = self.def_password()
        if not os.path.exists("files/slt.s"):
            slt = "new"
        else:
            slt = "old"
        
        with open("files/psd.user","w") as pasword:
            pasword.write(_password)
        del _password
        self.encrypt()

        self.password = self.decrypt()

        del _passwordBuf

    def def_password(self):
        _password = str(platform.node()) + str(platform.platform())
        _password = _password.split("-")
        _passwordBuf = str(1)
        for i in range(len(_password)):
            _passwordBuf = _passwordBuf + str(_password[i])
        _password = _passwordBuf.split(".")
        _passwordBuf = str(1)
        for i in range(len(_password)):
            _passwordBuf = _passwordBuf + str(_password[i])
        _password = _passwordBuf
        _password = _password.capitalize()
        return _password
    def decrypt(self):
        _buffer = None
        ps = None
        with open("files/psd.user","rb") as npdswrd:
            _buffer = npdswrd.read()
        with open("files/psd.user","wb") as password:
            password.write(self.cr.decrypt(_buffer))
        with open("files/psd.user","r") as pasword:
            ps = pasword.read()
        return ps
        

    def encrypt(self):
        _buffer = None
        with open("files/psd.user","rb") as npswrd:
            _buffer = npswrd.read()
        with open("files/psd.user","wb") as password:
            password.write(self.cr.encrypt(_buffer))
            

        #self.crypter = Crypt()
if __name__ == "__main__":
    c = PasswordManager()