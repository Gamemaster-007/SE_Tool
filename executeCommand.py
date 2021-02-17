from openApplicationMac import openApplicationMac
from openApplicationWindows import openApplicationWindows

def importCommand(command,platform):

    temp = command.split(' ')

    if(temp[0] == 'open'):
        print("\n=>   Opening "+command[5:])
        if platform == 0:
            openApplicationWindows(command[5:])
        else:
            openApplicationMac(command[5:])