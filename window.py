from tkinter import *
import tkinter
import speech_recognition as sr
from typing_text import typeText

# import platform
# Platform = platform.system()
# if Platform == 'Windows':
#     Platform = 0
# elif Platform == 'Darwin':
#     Platform = 1
# else:
#     print("This Tool will not work in this OS")
#     exit()

r = sr.Recognizer()

isListening = False

friday = Tk()
friday.geometry('400x600')
friday.resizable(width=False, height=False)
friday.title("F.R.I.D.A.Y")

canvas_1 = Canvas(friday,background='black',height=510)
canvas_2 = Canvas(friday,background='yellow',height=70)

messages = tkinter.Listbox(canvas_1,height=31,bg='black',fg='white')
messages.pack(fill=BOTH)
msg_count = 1

msg_fieldText = tkinter.StringVar()
msg_fieldText.set('')

msg_inputField = tkinter.Entry(canvas_2,font=('Helvetica','14'),width=36,textvariable=msg_fieldText)

def typing():
    global isListening
    isTyping = True

    while isTyping == True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            # audio = r.listen(source)
            audio = r.record(source,duration=5)

            try:
                text = r.recognize_google(audio)
                if text.lower() == 'stop typing':
                    msg_fieldText.set('')
                    isTyping = False
                else:
                    typeText(text)
            except:
                print("Try Again")

    
def message_recieved(msg):
    global msg_count
    if msg.lower() == 'start typing':
        msg_fieldText.set('Typing...')
        friday.update()
        typing()

    else:
        messages.insert(msg_count,'USER  =>')
        messages.itemconfig(msg_count-1,fg='green')
        msg_count += 1
        messages.insert(msg_count,"")
        msg_count += 1
        while len(msg) > 60:
            messages.insert(msg_count,msg[:60])
            msg_count += 1
            msg = msg[60:]
                    
        messages.insert(msg_count,msg)
        msg_count += 1
        messages.insert(msg_count,"")
        msg_count += 1

def speak():
    global msg_count
    global isListening

    if isListening == False:
        isListening = True

        msg_fieldText.set('Listening...')
        msg_inputField.config(state=DISABLED)
        friday.update()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source, duration=5)

            try:
                msg = r.recognize_google(audio)
                message_recieved(msg)
                
            except:
                messages.delete(first=msg_count-1)
                messages.insert(msg_count,'Try Again')
                messages.itemconfig(msg_count-1,fg='red')
                msg_count += 1
                messages.insert(msg_count,"")
                msg_count += 1
        msg_fieldText.set("")
        msg_inputField.config(state=NORMAL)
        isListening = False


def send():
    global msg_count
    global isListening

    if isListening == False:
        msg = msg_fieldText.get()
        message_recieved(msg)
        msg_fieldText.set('')

photo = PhotoImage(file = "microphone.png")
mic_button = tkinter.Button(canvas_2,text='Speak',height=70,padx=10,image=photo,command=speak)
mic_button.pack(side=LEFT)
msg_inputField.pack(side=LEFT,fill=BOTH)

send_photo = PhotoImage(file = "send.png")
send_button = tkinter.Button(canvas_2,text='Speak',height=70,padx=10,image=send_photo,command=send)
send_button.pack(side=RIGHT)

canvas_1.pack(side=TOP,fill=BOTH)
canvas_2.pack(side=BOTTOM,fill=BOTH)

friday.mainloop()