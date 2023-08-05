import pkg1
import consolejs
     
def wait(self,  s):
    console = Consolejs.get_console(pkg1) 
    console.debug(r'{s=}')
    print("waiting")


def retry(self,  n):
    console = Consolejs.get_console(pkg1) 
    console.debug(r'{n=}')
    print("rettrun")

 
def sleep(self, secs, minutes):
    console = Consolejs.get_console(pkg1) 
    print("I am Sleeping")
    return secs+minutes
