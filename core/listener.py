
import sounddevice as sd
import speech_recognition as sr

class Listener:
    def __init__(self) :
       self.r = sr.Recognizer() 
       self.samplerate = 16000 # frequency 16Khz 

    def record_audio(self,seconds ):
        print("\nRecording .......")
        data = sd.rec((seconds*self.samplerate) , samplerate= self.samplerate ,channels=1, dtype="int16")           # 16 bits audio 
        sd.wait()  # wait for recording to stop before continuing 

        return sr.AudioData(data.tobytes(),self.samplerate , 2)  # 2bytes int16 16 bit = 2 bytes


    def speech_to_text(self,seconds = 15) : 
       audio = self.record_audio(seconds) 

       try :
           text = self.r.recognize_google(audio)
           print("User : " , text)
           return text 
       except sr.UnknownValueError:
           print("Couldnt reconise ")
           return False 

       except sr.RequestError :
           print("Couldnt connect \nCheck internet connection ") 
           return False 

       except Exception as e :
           print(f"An error {e} has occured ")
           return False 

