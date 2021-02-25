import speech_recognition as sr

r = sr.Recognizer()

def speech2Text():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source, duration=5)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return -1
    
if __name__=='__main__':
    text = speech2Text()
    if text == -1:
        print("Sorry didn't get you, Please Try Again")
    else:
        print(text)