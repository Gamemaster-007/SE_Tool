# Import Required Libraries and Functions
import sys
import tkinter
import playsound
from tkinter import *
from tkinter import font as tkfont
from Speech2Text import speech2Text
from typing_text import typeText
from codeDictation import dictatingCode
from dictateText import dictate
from tkinter import ttk
from Editor_Tools import scrollingtext,ColorLight
import multiprocessing

# Main App Class
class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):

        # Creating Main Window
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.attributes("-topmost",True)

        # Modify Title of Window
        self.title("F.R.I.D.A.Y")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic") # Styling Window Title

        # Creating Container to Stack Frames [ Assistant , Text Editor ]
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Creating Frames
        self.frames = {}
        for F in (Assistant, TextEditor):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.isProcessStarted = False # To Check if Second Process has Started

        self.show_frame("Assistant") # Initially Show Assistant Frame
        self.update() # Update Window GUI
        # dictate('This is FRIDAY, your personal voice assistant. My special feature is to code when you dictate.') # Dictate Start Message

    # [ Function to Pause Process ]
    def pause_Process(self):
        if self.isProcessStarted:
            self.dictationProcess.terminate() # Terminate Process
            self.isProcessStarted = False

    # [ Function to Resume Process ]
    def resume_Process(self):
        print('starting Process')
        if self.isProcessStarted == False:
            self.dictationProcess = multiprocessing.Process(target=dictatingCode,daemon=True) # Create New Process
            self.dictationProcess.start() # Start Process
            self.isProcessStarted = True

    # Function to Switch between Frames
    def show_frame(self, page_name):

        if page_name == 'Assistant':
            if self.isProcessStarted:
                self.dictationProcess.terminate() # Terminate Process
                self.isProcessStarted = False
            # Resize the Window
            self.minsize(500,600)
            self.geometry('500x600+350+10')
            self.resizable(width=False, height=False)
        else:
            # Resize Window
            self.resizable(width=True, height=True)
            self.minsize(1000,600)
            self.geometry('1000x600+350+10')
            self.dictationProcess = multiprocessing.Process(target=dictatingCode,daemon=True) # Create New Process
            self.dictationProcess.start() # Start Process
            self.isProcessStarted = True
            self.lift()
            self.update()
        frame = self.frames[page_name] # Select Desired Frame
        frame.tkraise() # Display Selected Frame

# Assistant Class
class Assistant(tkinter.Frame):
    def __init__(self,parent,controller):

        # Creating Frame
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        canvas_1 = Canvas(self,background='black',height=510) # For Message Display System
        canvas_2 = Canvas(self,background='white',height=70) # For Buttons and Input Field

        # +++++++++++++++++++++++++ Message Display System ++++++++++++++++++++++++++++++++++++++++++++++
        # List of messages
        self.messages = tkinter.Listbox(canvas_1,height=31,bg='black',fg='white')
        self.messages.pack(fill=BOTH)

        self.msg_count = 1 # To keep track of number of messages
        self.isListening = False # Flag variable to check state of Tool

        # Input Field
        self.msg_fieldText = tkinter.StringVar()
        self.msg_fieldText.set('')
        self.msg_inputField = tkinter.Entry(canvas_2,font=('Helvetica','14'),width=40,textvariable=self.msg_fieldText)

        # +++++++++++++++++++++++++ [ Mic Button | Input Field | Send Button ] ++++++++++++++++++++++++++++++++++++++++++++++
        # Mic button UI
        photo = PhotoImage(file = "images/microphone.png")
        mic_button = tkinter.Button(canvas_2,text='Speak',height=70,padx=10,image=photo,command=lambda: self.speak())
        mic_button.image = photo
        mic_button.pack(side=LEFT)
        self.msg_inputField.pack(side=LEFT,fill=BOTH)

        # Send Button UI
        send_photo = PhotoImage(file = "images/send.png")
        send_button = tkinter.Button(canvas_2,text='Send',height=70,padx=10,image=send_photo,command=lambda: self.send())
        send_button.image = send_photo
        send_button.pack(side=RIGHT)

        # Window UI
        canvas_1.pack(side=TOP,fill=BOTH)
        canvas_2.pack(side=BOTTOM,fill=BOTH)

    # Funtion to Add Message to Tkinter window
    def addMsg(self,msgr,type,msg):
        messanger = {0:'F.R.I.D.A.Y  =>',1:'USER  =>'}
        messanger_color = {0:'orange',1:'yellow'}
        typE = {0:'white',1:'red'}

        # [ Add the origin of message ]
        self.messages.insert(self.msg_count,messanger[msgr])
        self.messages.itemconfig(self.msg_count-1,fg=messanger_color[msgr])
        self.msg_count += 1
        self.messages.insert(self.msg_count,"")
        self.msg_count += 1

        # Divide message to fit in window
        while len(msg) > 60:
            self.messages.insert(self.msg_count,msg[:60])
            self.messages.itemconfig(self.msg_count-1,fg=typE[type])
            self.msg_count += 1
            msg = msg[60:]

        # Add message to window        
        self.messages.insert(self.msg_count,msg)
        self.messages.itemconfig(self.msg_count-1,fg=typE[type])
        self.msg_count += 1
        self.messages.insert(self.msg_count,"")
        self.msg_count += 1
    
    # Function For Typing Text
    def typing(self):
        isTyping = True

        while isTyping == True:
            self.msg_fieldText.set('Mode: typing  | State: listening ') # Set mode and state
            self.update()

            text = speech2Text() # Get text from Speech Detection module
            self.msg_fieldText.set('Mode: typing  | State: processing ') # Set mode and state
            self.update()

            if text == -1: # if text not detected
                self.msg_fieldText.set("Error: Didn't understand, Please try again ")
                self.update()
                i = 0
                for _ in range(50000000):
                    i += 1
            else: # if text detected
                if text.lower() == 'stop typing': # Exit Typing mode
                    self.msg_fieldText.set('')
                    self.addMsg(0,0,'Done Typing')
                    dictate('Done Typing')
                    isTyping = False
                else:
                    typeText(text) # Type text using typeText module

    # Opening Text Editor
    def openEditor(self):
        self.controller.show_frame('TextEditor') # Changing Frame

    # Function to Detect Message
    def message_recieved(self,msg):
        if msg.lower() == 'start typing':
            self.addMsg(1,0,msg)
            self.addMsg(0,0,'Started Typing')
            self.update()
            dictate('Started Typing')
            self.typing()
        elif msg.lower() == 'start coding':
            self.addMsg(1,0,msg)
            self.addMsg(0,0,'Started Coding')
            self.update()
            dictate('Started Coding')
            self.addMsg(0,0,'Done Coding')
            self.openEditor()
        elif msg.lower() == 'exit' or msg.lower() == 'close':
            dictate('have a nice day, bye')
            sys.exit()
        else:
            self.addMsg(1,0,msg)

    # Function to Detect Speech
    def speak(self):
        if self.isListening == False: # check state
            self.isListening = True # change state
            self.msg_fieldText.set("go ahead I'm listening")
            self.msg_inputField.config(state=DISABLED)
            self.update()
            playsound.playsound('audio_files/tone.mp3',True)

            msg = speech2Text() # Get message from speech detection module
            if msg == -1:
                error = "Didn't understand, Please Try Again"
                self.addMsg(0,1,error)
            else:
                self.message_recieved(msg)

            self.msg_fieldText.set("")
            self.msg_inputField.config(state=NORMAL)
            self.isListening = False

    # Function to Process Messages Recieved from Input Field
    def send(self):
        msg = self.msg_fieldText.get() # Get message from Input Field

        # Modify the recieved message
        words = msg.split(' ')
        i = 0
        while i < len(words):
            if words[i] == '':
                words.remove(words[i])
                i -= 1
            i += 1
        msg = ' '.join(words)

        # Check state of Tool and [ if message is legit ]
        if self.isListening == False and len(msg) != 0:
            self.msg_inputField.config(state=DISABLED)
            self.message_recieved(msg)
            self.msg_fieldText.set("")
            self.msg_inputField.config(state=NORMAL)

# Text Editor Class
class TextEditor(tkinter.Frame):
    def __init__(self,parent,controller):
        global sps

        # Creating Frame
        tkinter.Frame.__init__(self,parent)
        self.controller = controller
        
        self.filepath=tkinter.StringVar() # For File Name
        self.filepath.set('Unitled.py') # Blank File Name

        # [Shortcut Bar Main Frame]
        self.shortcut_bar=ttk.Frame(self)
        self.shortcut_bar.pack(expand='no', fill='x')

        # +++++++++++++++++++++++++ Text Box System ++++++++++++++++++++++++++++++++++++++++++++++
        # Frame For [Text Box]
        frame=ttk.Frame(self, borderwidth=5)
        frame.pack(expand='yes', fill='both')
        frame1=ttk.Frame(frame)
        frame1.pack(side='top', expand='yes', fill='both')
        self.text_box=tkinter.Text(frame1, wrap='none', undo=1)
        self.text_box.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.text_box.pack()

        # Adding Features On Text Box
        self.box=scrollingtext.featured_text(root=frame1, textbox=self.text_box, main=frame)

        #++++++++++++++++++++++++ [System Close] ++++++++++++++++++++++++++++++++++++++++++++++
        # Function For Scrolling Text widget number line Together
        self.cursurinfo=ttk.Label(self.text_box, text='Line 1 | Column 1',padding=3)
        self.cursurinfo.pack(expand='no', fill=None, side='right',anchor='se')

        self.micState = True # Check mic State

        # Pause/Resume Button
        space1=tkinter.Label(self, text=' ',width=7)
        space1.pack(expand='no', fill=None, side='right')
        self.pauseResumeButton=tkinter.Button(self, text='Pause',padx=10,pady=6,command=self.switch_state)
        self.pauseResumeButton.pack(expand='no', fill=None, side='right')

        # Stop Coding Button
        space2=tkinter.Label(self, text=' ',width=7)
        space2.pack(expand='no', fill=None, side='right')
        stopCodingButton=tkinter.Button(self, text='STOP CODING',padx=10,pady=6,command=self.stopCoding)
        stopCodingButton.pack(expand='no', fill=None, side='right')

        # Adding Syntax Highlighting Feature
        self.syntax_color=ColorLight.ColorLight(txtbox=self.text_box)

        # Binding Triggers
        self.bind_all('<Any-KeyPress>',self.trigger)

    # [ Function to Chnage State of Pause/Resume Button and call Pause/Resume Functions ]
    def switch_state(self):
        if self.micState:
            self.pauseResumeButton.configure(text='Resume')
            self.update()
            self.controller.pause_Process()
            self.micState = False
        else:
            self.pauseResumeButton.configure(text='Pause')
            self.update()
            self.controller.resume_Process()
            self.micState = True

    # [ Function to exit Coding State ]
    def stopCoding(self):
        self.controller.show_frame('Assistant') # Change Frame to Assiatant Frame
        self.update() # Update Window GUI
        dictate('Done Coding')

    # [Function to Update Cursor Position]
    def update_cursor_info_bar(self, event=None):
        row, col = self.text_box.index(tkinter.INSERT).split('.')
        line_num, col_num = str(int(row)), str(int(col)+1) # colstarts at 0
        infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
        self.cursurinfo.configure(text=infotext)

    # All-Key Trigger
    def trigger(self, event):
        self.box.changed()
        self.update_cursor_info_bar()
        self.syntax_color.trigger()
    
if __name__=='__main__':
    app = App() # Main App Class Object
    app.mainloop() # start Main Window GUI