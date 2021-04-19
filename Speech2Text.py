# Import Required Libraries and Functions
import speech_recognition as sr

# Create Speech Recognizer
r = sr.Recognizer()
# r.energy_threshold = 2500 # Setting Threshold for Microphone
# r.dynamic_energy_threshold = True

# [ Function to Detect Speech and Convert it into Text ]
def speech2Text():
    with sr.Microphone() as source:
        # audio = r.listen(source) # Listen to Microphone audio
        audio = r.record(source,duration=3)
        try:
            text = r.recognize_google(audio) # Convert Audio to Text
            return text
        except:
            return -1
    
if __name__=='__main__':
    text = speech2Text()
    if text == -1:
        print("Sorry didn't get you, Please Try Again")
    else:
        print(text)