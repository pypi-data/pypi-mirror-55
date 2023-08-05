
import pkg1
from consolejs import Consolejs

class EnvVar:
    def __init__(self, ):
        self.envcopy = {}
        

    def getVar(self, name):
        console = Consolejs.get_console(pkg1, self)
        console.debug("{name=} ")
        return name
    
    def setVar(self, name, val ) :
        console = Consolejs.get_console(pkg1, self)
        self.envcopy["name"] = val
        console.debug("{self.envcopy=}{name=} ")
