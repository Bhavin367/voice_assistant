from gtts import gTTS 
from playsound import playsound 
from datetime import datetime 
from .listener import Listener
import os , json
import time
from .nlp import NLP
import pyjokes
from func import wiki 
from func.send_email import Send_mail

cur_time = datetime.now()

class Response:
    def __init__(self,name) :
        self.name = name


    def speak(self,text) :
        speech = gTTS(text = text ,lang = 'en' , tld= 'co.uk')

        base_path  = os.path.dirname(__file__ )
        file_path  = os.path.join(base_path,"reply.mp3")
        if os.path.exists(file_path) :
            os.remove(file_path)
        speech.save(file_path)

        playsound(file_path)

        print("\n",text,"\n")

    def greet(self) :
        current_time = cur_time.hour 
        
        if(current_time <= 12) :
            text = f"Good Morning {self.name}" 

        elif (12 < current_time and current_time <= 17 ) :
            text = f"Good afternoon {self.name}"


        else :
            text = f"Good evening {self.name}" 
            
        text += " How can I help you ? Say list to list all the task i could help you with "
        self.speak(text)

class Functions :
    def __init__(self) :
        self.l = Listener() 
        self.name = False

        here = os.path.dirname(__file__)
        casual_path = os.path.join(here,"casual.json")
        with open(casual_path,"r") as f :
            self.casual = json.load(f)
        
        self.functions = {"list":self.list_func,"exit":self.exit,"time":self.time,
                          "joke":self.joke,"search":self.search,"email":self.email}


    def learn_intent(self,user_instruction,intents):
        while True :
            try:
                    
                    if intents[0] == intents[1]:
                        self.r.speak(f"Did you mean {intents[0]} , please answer as yes or no ")
                        yes_no = self.l.speech_to_text(3)
                        if yes_no.lower() == "yes" :
                            self.nlp.learn(user_instruction,intents[0])

                        if yes_no.lower() == "no" :
                            self.r.speak("Did you mean list , email,joke , time , search , exit or none , answer in one word please  ")
                            user_intent = self.l.speech_to_text(4)
                            self.nlp.learn(user_instruction,user_intent)


                            if user_intent in self.functions.keys():
                                self.functions[user_intent]()

                    
                        return 

                    self.r.speak(f"Did you mean {intents[0]} or {intents[1]} , please answer in one word ")
                    ask_user = self.l.speech_to_text(3)
                    if intents[0] in ask_user :
                        self.nlp.learn(user_instruction,intents[0])
                        
                    elif intents[1] in ask_user : 
                        self.nlp.learn(user_instruction,intents[1])
                    elif ask_user == "continue" :
                        break 

                    else :
                            self.r.speak(f"Please choose either {intents[0]} or {intents[1]} or say continue ")
                            continue 

            except :
                return 


    def run(self) :
        self.basic_func() 


        self.nlp = NLP(self.name) 
        
        while(True) :
            user_instruction = self.l.speech_to_text(5)
            if not user_instruction :
                self.r.speak("I didnt get you . Can you please repeat ") 
                continue 
            print(user_instruction) 
            intent = self.nlp.hybrid_match(user_instruction) 
            print("intent : ", intent)

            
            if isinstance(intent,tuple):
                self.learn_intent(user_instruction,intent) 
                continue

            check_exit = self.functions[intent]()
            if check_exit == False  : 
                return 


    def basic_func(self):
        print("Tell me your name \n") 
        self.name = self.l.speech_to_text(2) 

        while(not(self.name)):
            print("\nTry spelling your name ")
            self.name = self.l.speech_to_text(5) 

        self.r = Response(self.name) 
        self.r.greet()

    def list_func(self) :
        text = '''I can help you with looking up current time , 
        sending emails , reminding tasks , searching stuff online and I can be funny ''' 

        self.r.speak(text)


    def time(self):
        am_pm = "a m" if cur_time.hour <= 12 else "p m"
        hour = cur_time.hour if cur_time.hour <= 12 else cur_time.hour % 12 
        minute = cur_time.minute

        text = f"It is now {hour}:{minute} {am_pm}"
        self.r.speak(text)

    def search(self):
        try:
            self.r.speak("So what do you want to search about ? ")
            topic = self.l.speech_to_text(3)
            data = wiki.wiki(topic)
            if not isinstance(data,tuple):
                self.r.speak(topic)
                return

            print(data)
        
            self.r.speak(data[0])
            self.r.speak("Do you need additional info on the topic ? ") 
            yes_no  = self.l.speech_to_text(3)
            if not yes_no :
                return
            ans = self.nlp.hybrid_match(yes_no,self.casual)
            print(f"ans : ",ans)
            if ans == "yes":
                self.r.speak(data[1])

        except :
            self.r.speak(f"An error has occured please try again")
            
    def email(self):
        try : 
            send_mail = Send_mail(self.name)
            if not send_mail :
                self.r.speak("The account is not authorised to send emails ")
            r_list = send_mail.recipient_list()
            print(f"Recipients : {r_list}")
            if r_list :
                r_list = " ".join(r_list)
                self.r.speak(f"Reading existing recipient emial list {r_list}")

            try :
                self.r.speak("Tell the subject of the mail")
                subject = self.l.speech_to_text(4)

            except :
                subject = ''
            self.r.speak("Now try to speak the content of the mail in 10 seconds")
            content = self.l.speech_to_text(9)
            self.r.speak(send_mail.send_mail(content,subject))

        except Exception as e:
            print(f"\nAn error {e} has occured ")
            self.r.speak("An error has occured !! email failed try again ")

    
    def joke(self):
        joke = pyjokes.get_joke('en')
        self.r.speak(joke)

    def exit(self):
        text = f"Okay , See ya soon {self.name}"
        self.r.speak(text)
        return False 

    
        
if __name__ == "__main__" : 
    func = Functions() 
    func.run()
