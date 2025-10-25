#{
#
#        "time" : ["what is the time","tell me the time" ,"current time ","time now"],
#        "search" : ["search about " ,"look up" ,"what is ","who is ","tell me about",
#                    "give information about " , "show me " ,"find" , "searching",
#                    "need you to search","search something "],
#        "email" :["write an email", "email to " ,"mail","send email to "],
#        "list" : ["can you list","list all ", "can you please list","you to list"],
#        "exit" : ["exit","quite","bye","see you later","leaving"]
#        
#
#}


STOPWORDS = [
    "a", "about", "above", "after", "again", "against", "all", "am",
    "an", "and", "any", "are", "aren't", "as", "at", "be", "because",
    "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "can't", "cannot", "could", "couldn't", "did", "didn't",
    "do", "does", "doesn't", "doing", "don't", "down", "during", "each",
    "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
    "here", "here's", "hers", "herself", "him", "himself", "his", "how",
    "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into",
    "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
    "most", "mustn't", "my", "myself", "no" ]

# For pattern mathcing Ill be using both Jaccard similiarity and fuzzy search 
# sorta hybrid approach 

import re , json ,os   
from difflib import SequenceMatcher 

class NLP : 
    def __init__(self ,user_name = "default"):
        self.user_name = user_name 
        self.data = {}
        self.load_data() 
        self.user_data = {}
        self.load_user_data() 

        self.intents = self.data.keys()
        self.w_jaccard = 2 
        self.w_fuzzy = 1


    def load_user_data(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path,"user.json")
        if os.path.exists(file_path) :
            try:
                with open(file_path,"r") as f :
                    user_data = json.load(f)

                    if self.user_name in user_data :
                        self.w_jaccard = user_data["w_jaccard"]
                        self.w_fuzzy = user_data["w_fuzzy"]

                    else :
                    
                        with open(file_path,"r") as fw :
                            user_data = json.load(fw)

                        with open(file_path ,"w") as fw :
                            user_data[self.user_name] = {"w_jaccard":2,"w_fuzzy" :1}
                            json.dump(user_data,fw,indent = 4) 

            except:
                user_data = {}
                with open(file_path,"w") as fw :
                        user_data[self.user_name] = {"w_jaccard":2,"w_fuzzy" :1}
                        json.dump(user_data,fw,indent = 4) 


        else :
                user_data = {}
                with open(file_path,"w") as fw : 
                    user_data[self.user_name] = {"w_jaccard":2,"w_fuzzy" :1} 
                    json.dump(user_data,fw,indent = 4)

        self.user_data = user_data

    def push_user_data(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path,"user.json")
        with open(file_path,"w") as f :
            json.dump(self.user_data , f , indent = 4)



    def load_data(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path,"intents.json")
        if os.path.exists(file_path) :
            with open(file_path,"r+") as f :
                self.data  = json.load(f) 

        else :
            self.data =  {
        "time" : ["what is the time","tell me the time" ,"current time ","time now"],
        "search" : ["search about " ,"look up" ,"what is ","who is ","tell me about",
                    "give information about " , "show me " ,"find" , "searching"],
        "list" : ["list","list tasks","list all"],
        "joke" : ["tell me a joke","joke","say a joke","how about a joke","make a joke"],
        "email" :["write an email", "email to " ,"mail","send email to "],
        "exit" : ["exit","quite","bye","see you later","leaving"]
        }


    def push_data(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path,"intents.json")
        with open(file_path,"w") as f :
            json.dump(self.data,f,indent = 4)

    def normalise(self,text):
        #re.sub = removes stuff 
        text = re.sub(r"[^\w\s]","",text) # \w = word characters \s = space , ^ = NOT
                                         # removing everything that isnt alphanum or space

        text = re.sub(r"[\d]","",text) # \d = digits , 
        return [t for t in text.split() if t not in STOPWORDS ]

# jaccard_similarity = cardinality of A intersection B by |AUB|
# catches same word phrase

    def jaccard_similarity(self,user_text,phrase) : 

        # split into words and check how many match 
        set_a = set(user_text)   
        set_b = set(phrase.split())
        intersection = set_a & set_b   # sets allow intersection & union 
        union = set_a | set_b

        if(len(union) != 0): 
            return len(intersection)/len(union)
        else :
            return 0 

#SequenceMatcher will be able to identify SIMILAR words 
# Catches spelling error 

    def fuzzy_match(self,user_text,phrase):
        user_text = ''.join(sorted(user_text))
        phrase = self.normalise(phrase)
        phrase = ''.join(sorted(phrase))

        seq_match = SequenceMatcher(None,user_text,phrase) # None means no junk to filter 
        return seq_match.ratio()  # return a ratio between 0-1 

    def find_score(self,user_text,match,weight = 0.5,intent_data = None):
        if intent_data == None :
            intent_data = self.data
        best_score = 0 
        best_intent = None 

        for intent , phrases in intent_data.items():
            for phrase in phrases :
                score = match(user_text,phrase)
                if score > best_score :
                    best_score = score 
                    best_intent = intent 

        return weight* best_score , best_intent 

    def hybrid_match(self,user_text,intent_data = None):
       if intent_data ==None :
           intent_data = self.data
       user_text = self.normalise(user_text)
       jaccard_score = 0 
       jaccard_intent = None

       fuzzy_score  = 0 
       fuzzy_intent = None 

       jaccard_score , jaccard_intent = self.find_score(user_text,self.jaccard_similarity,self.w_jaccard,intent_data)
       fuzzy_score , fuzzy_intent = self.find_score(user_text,self.fuzzy_match,self.w_fuzzy,intent_data)

       print("fuzzy" , fuzzy_score )
       print("jaccar", jaccard_score)


       if fuzzy_intent == jaccard_intent and (jaccard_score + fuzzy_score) > 1.2 :
           print(jaccard_intent," : jaccard_intent & fuzzy_intent")
           return jaccard_intent 

       if abs(fuzzy_score - jaccard_score) > 0.4 :
           if fuzzy_score > jaccard_score :
               print(fuzzy_intent," : fuzzy_intent ")
               return fuzzy_intent 

           else :
               print(jaccard_intent," : jaccard_intent")
               return jaccard_intent

       else :
           return jaccard_intent,fuzzy_intent 
           
    def learn(self,phrase,intent):
        phrase = self.normalise(phrase)
        phrase = " ".join(phrase)
        if intent in self.data.keys():

            self.data[intent].append(phrase) 
            print(f"The phrase '{phrase}' added to intend : {intent}")
            self.push_data()


    def adjust_weight(self,user_ans,jaccard_intent,fuzzy_intent):
        if user_ans == jaccard_intent :
            if self.w_jaccard < 2:
                self.w_jaccard *= 1.1

            if self.w_fuzzy > 1 :
                self.w_fuzzy *= 0.9

        else :
            if self.w_fuzzy < 2 :
                self.w_fuzzy *= 1.1

            if self.w_jaccard > 1 :
                self.w_jaccard *= 0.9 


        self.user_data[self.user_name]["w_jaccard"] = self.w_jaccard
        self.user_data[self.user_name]["w_fuzzy"] = self.w_fuzzy 

        self.push_user_data()
n = NLP()
