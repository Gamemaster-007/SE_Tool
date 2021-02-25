import speech_recognition as sr
import pyttsx3
from executeCommand import importCommand
from typing_text import typeText

import platform
Platform = platform.system()
if Platform == 'Windows':
    Platform = 0
elif Platform == 'Darwin':
    Platform = 1
else:
    print("This Tool will not work in this OS")
    exit()

r = sr.Recognizer()
# engine = pyttsx3.init()
# engine.say(text)
# engine.runAndWait()

mode = True
isTyping = False

while mode:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("=>   Speak : ")
        audio = r.record(source, duration=5)

        try:
            text = r.recognize_google(audio)
            print(text)

            if isTyping == True:
                typeText(text)
            elif text.lower() == 'start typing':
                isTyping = True
            elif text.lower() == 'stop typing':
                isTyping = False
            else:
                importCommand(text.lower(),Platform)
            
        except:
            print("=>   Try again")