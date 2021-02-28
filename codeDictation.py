from Speech2Text import speech2Text
from typing_text import typeText
import time
# Import Required Libraries and Functions
import tkinter

root = ''
lbl = ''

# [ Create State of Tool Window ]
def make():
    global root
    global lbl
    root = tkinter.Tk()
    root.geometry('300x50')
    root.title('State of Tool')
    root.resizable(width=False,height=False)
    lbl = tkinter.Label(root,text='State: - - - ',padx=10,pady=10)
    lbl.pack()

# [ Function to detect Speech and convert it to Text ]
def dictatingCode():
    global root
    global lbl
    make()
    isCoding = True

    while isCoding:
        lbl.configure(text="State: Listening")
        root.update()
        text = speech2Text()

        if text == -1:
            lbl.configure(text="Error: Didn't understand, Please try again")
            root.update()
            time.sleep(2)
        else:
            lbl.configure(text="State: Processing")
            root.update()
            typeText(text)