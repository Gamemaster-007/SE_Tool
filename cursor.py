from tkinter import *
import tkinter

top = tkinter.Tk()
cursor_pos = top.winfo_pointerxy()

def but1():
    print('pressed button 1')
    top.destroy()

def but2():
    print('pressed button 2')
    top.destroy()

top.geometry("+"+str(cursor_pos[0])+"+"+str(cursor_pos[1]))
B1 = tkinter.Button(top, text ="Say 1 => press Enter", relief=RAISED, command=but1)
B2 = tkinter.Button(top, text ="Say 2 => type press enter", relief=RAISED, command=but2)

B1.pack()
B2.pack()
top.mainloop()