import os

def openApplicationMac(app):
    d = "/Applications"
    apps = list(map(lambda x: x.split('.app')[0], os.listdir(d)))
    flag = 0
    for x in apps:
        if(app.lower() == x.lower()):
            flag = 1
            app = x
            os.system('open ' +d+'/%s.app' %app.replace(' ','\ '))
            break
    if(flag == 0):
        print("=>   Sorry amigo , unable to find the Application")