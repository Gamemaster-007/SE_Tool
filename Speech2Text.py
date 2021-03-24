# Import Required Libraries and Functions
import speech_recognition as sr

# Create Speech Recognizer
r = sr.Recognizer()

# [ Function to Detect Speech and Convert it into Text ]
def speech2Text():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # Adjust Microphne to noise in surroundings
        # Record Audio
        audio = r.record(source, duration=3) # use this line if surroundings noise is high or if microphone takes very long time to process speech
        # Listen to microphone
        # audio = r.listen(source) # use this line if surroundings noise is low and microphone is taking reasonable amount of time to process text
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