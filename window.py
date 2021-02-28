from tkinter import *
import tkinter
from Speech2Text import speech2Text
from typing_text import typeText
# from codeDictation import startCode

# import platform
# Platform = platform.system()
# if Platform == 'Windows':
#     Platform = 0
# elif Platform == 'Darwin':
#     Platform = 1
# else:
#     print("This Tool will not work in this OS")
#     exit()

isListening = False # Flag variable to check state of Tool

# Tkinter Window Specifications
friday = Tk()
friday.geometry('500x600')
friday.resizable(width=False, height=False)
friday.title("F.R.I.D.A.Y")
canvas_1 = Canvas(friday,background='black',height=510)
canvas_2 = Canvas(friday,background='white',height=70)

# List of messages
messages = tkinter.Listbox(canvas_1,height=31,bg='black',fg='white')
messages.pack(fill=BOTH)
msg_count = 1

# Input Field
msg_fieldText = tkinter.StringVar()
msg_fieldText.set('')
msg_inputField = tkinter.Entry(canvas_2,font=('Helvetica','14'),width=40,textvariable=msg_fieldText)

    # +++++++++++++++++++++++++ Add Message to Tkinter window ++++++++++++++++++++++++++++++++++++++++++++++
def addMsg(msgr,type,msg):
    global msg_count

    messanger = {0:'F.R.I.D.A.Y  =>',1:'USER  =>'}
    messanger_color = {0:'orange',1:'yellow'}
    typE = {0:'white',1:'red'}
    messages.insert(msg_count,messanger[msgr])
    messages.itemconfig(msg_count-1,fg=messanger_color[msgr])
    msg_count += 1
    messages.insert(msg_count,"")
    msg_count += 1
    while len(msg) > 60: # Divide message to fit in window
        messages.insert(msg_count,msg[:60])
        messages.itemconfig(msg_count-1,fg=typE[type])
        msg_count += 1
        msg = msg[60:]
                    
    messages.insert(msg_count,msg)
    messages.itemconfig(msg_count-1,fg=typE[type])
    msg_count += 1
    messages.insert(msg_count,"")
    msg_count += 1

    # +++++++++++++++++++++++++ Typing System ++++++++++++++++++++++++++++++++++++++++++++++
def typing():
    global isListening
    isTyping = True

    while isTyping == True:
        msg_fieldText.set('Mode: typing  | State: listening ') # Set mode and state
        friday.update()

        text = speech2Text() # Get text from Speech Detection module
        msg_fieldText.set('Mode: typing  | State: processing ') # Set mode and state
        friday.update()

        if text == -1: # if text not detected
            msg_fieldText.set("Error: Didn't understand, Please try again ")
            friday.update()
            i = 0
            for _ in range(50000000):
                i += 1
        else: # if text detected
            if text.lower() == 'stop typing': # Exit Typing mode
                msg_fieldText.set('')
                isTyping = False
            else:
                typeText(text) # Type text using typeText module

    # +++++++++++++++++++++++++ Detecting Message Type ++++++++++++++++++++++++++++++++++++++++++++++
def message_recieved(msg):
    global msg_count
    if msg.lower() == 'start typing':
        typing()
    elif msg.lower() == 'start coding':
        message = 'Started Coding'
        addMsg(0,0,message)
        # startCode()
    else:
        addMsg(1,0,msg)

    # +++++++++++++++++++++++++ Mic button Action ++++++++++++++++++++++++++++++++++++++++++++++
def speak():
    global msg_count
    global isListening

    if isListening == False: # check state
        isListening = True # change state

        msg_fieldText.set('Listening in 2sec...')
        msg_inputField.config(state=DISABLED)
        friday.update()

        msg = speech2Text() # Get message from speech detection module
        if msg == -1:
            error = "Didn't understand, Please Try Again"
            addMsg(0,1,error)
        else:
            message_recieved(msg)

        msg_fieldText.set("")
        msg_inputField.config(state=NORMAL)
        isListening = False

    # +++++++++++++++++++++++++ Send Button Action ++++++++++++++++++++++++++++++++++++++++++++++
def send():
    global msg_count
    global isListening

    msg = msg_fieldText.get() # Get message from Input Field

    # Check if message is empty spaces
    words = msg.split(' ')
    i = 0
    while i < len(words):
        if words[i] == '':
            words.remove(words[i])
            i -= 1
        i += 1
    msg = ' '.join(words)

    if isListening == False and len(msg) != 0:
        msg_inputField.config(state=DISABLED)
        message_recieved(msg)
        msg_fieldText.set("")
        msg_inputField.config(state=NORMAL)

# Mic button UI
photo = PhotoImage(file = "microphone.png")
mic_button = tkinter.Button(canvas_2,text='Speak',height=70,padx=10,image=photo,command=speak)
mic_button.image = photo
mic_button.pack(side=LEFT)
msg_inputField.pack(side=LEFT,fill=BOTH)

# Send Button UI
send_photo = PhotoImage(file = "send.png")
send_button = tkinter.Button(canvas_2,text='Speak',height=70,padx=10,image=send_photo,command=send)
send_button.image = send_photo
send_button.pack(side=RIGHT)

# Window UI
canvas_1.pack(side=TOP,fill=BOTH)
canvas_2.pack(side=BOTTOM,fill=BOTH)
friday.mainloop()