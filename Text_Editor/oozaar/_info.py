import tkinter as Tkinter
from tkinter import ttk

class helps(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self, className='About')
        Tkinter.Label(self, text='https://hackworldwithssb.blogspot.in\nsurajsinghbisht054@gmail.com\nS.S.B', foreground='SkyBlue', borderwidth=4, background='black').pack(pady=10,padx=10, ipady=10,ipadx=10,expand='yes', fill='both')
        ttk.Button(self, text='Close', command=lambda:self.destroy()).pack(side='bottom')
class about(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self, className='About')
        Tkinter.Label(self, text='This Editor is Written in Python Language\n And This Editor is Cross-Platform Supported \n Only For Practise And Educational Purpose Only \n By S.S.B', foreground='SkyBlue', borderwidth=4, background='black').pack(pady=10,padx=10, ipady=10,ipadx=10,expand='yes', fill='both')
        ttk.Button(self, text='Close', command=lambda:self.destroy()).pack(side='bottom')
class window:
    def __init__(self):
        pass
    def helps(self,event=None):
        storeobj=helps()
        storeobj.mainloop()
    def about(self,event=None):
        storeobj=about()
        storeobj.mainloop()
