from pathlib import Path 
import os , json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .valid_emails import valid_emails
from .key import api_key
#cause env wasnt working god knows why 


base_path = Path(__file__).resolve().parent.parent # find the abs path (.parent go one directory up)
json_path = base_path/"core"/"user.json"

class Send_mail:
    def __init__(self,name):
        self.name = name
        if self.name != "Ben":
            text = f"The account {self.name} is not authorised to send mails " 
            print(text )
            print("You'd have to setup manually for security reasons ")
            raise PermissionError(text)
            
        self.user_data = self.load_user_info()
        self.user_email = None 
        if not self.user_data :
            raise ValueError("Couldnt load user info please try again !!")

        self.message = None 

    def load_user_info(self):
        try:
            with open(json_path,"r") as f :
                data = json.load(f)

            return data
        except Exception as e  :
            print(f"An error {e} occured while loading user info ")
            return False 

    def push_user_data(self,data):
        try:
            with open(json_path,"w") as f :
                json.dump(data,f,indent = 4) 

        except Exception as e :
            print(f"An error {e} occured while pushing user data")


    def add_email(self):
        if self.name not in self.user_data.keys(): 
            self.user_data[self.name] = {}

        if "email" not in self.user_data[self.name] :
            self.user_data[self.name]["email"] = None 

        if "recipient" not in self.user_data[self.name] :
            self.user_data[self.name]["recipient"] = []


        if self.user_data[self.name]["email"] :
            self.user_email = self.user_data[self.name]["email"]
            return 

        print("*Note this system is only configured for outlook emails. Doesnt apply to recipients !! \n")
        email = input("Enter your email : ") 

        self.user_data[self.name]["email"] = email 

        print(f"\nEmail : {email} added to user account : {self.name}")
        self.user_email = email 
        self.push_user_data(self.user_data)
        

    def recipient_list(self):
        try:
            text = "List of saved recipient emails \n"

            if self.user_data[self.name]["recipient"] == [] or not self.user_data[self.name]["recipient"] :
                self.user_data[self.name]["recipient"] = []
                self.push_user_data()
                return False 


            return self.user_data[self.name]["recipient"].copy() 


        except Exception as e :
            print(f"An error {e} has occured while listing saved recipients emails ") 
            return []

    def add_recipient(self,email) :
        user_data = self.load_user_info()
        user_data[self.name]["recipient"].append(email)
        self.push_user_data()


    def send_mail(self,text,subj = "",recipient = None):
        try:
            if self.user_email is None or self.user_email == "" :
                self.add_email()

            self.message = text
            if recipient is None :
                recipient = input("Enter recipient email : ")

            print(self.user_email)

            if self.user_email not in valid_emails:
                return f"The email id {self.user_email} is not authorised"

            message = Mail(
                    from_email = self.user_email,
                    to_emails = recipient ,
                    subject = subj,
                    html_content = text
                    )


            sg = SendGridAPIClient(api_key) # getting api

            response = sg.send(message)

            print(response.status_code)
            print(response.body)
            print(response.headers)

            return f"Email sent successfully to {recipient}"

            self.add_recipient(recipient)

        except Exception as e :
            print(str(e))
            return "Email failed !!"


