# Python Voice Assistant 

## Requirements 
- Speech Recognition
- gTTS
- smtplib
- playsound
- sounddevice

## Main functionality 
- Voice Assistant uses basic Natural Language Processing (refer nlp.py) to understand user intent , respond and learn accordingly
- Loads data of each user from user.json
- takes a text as input which is converted from audio to text using *speechrecognition* and is normalised using builin *re* lib
- checks similarity using Jaccard similarity and fuzzy match ( to catch spelling errors )
  > Jaccard similarity - (A intersection B )/ (A Union B )
- uses a hybrid matching function to decide the intent
  > weight of Jaccard and fuzzy match could adjust based on user
- if intent unsure , ask user and function with correct intent awarded and wrond intent score substracted , and data logged in user.json
  > functions used  NLP.learn() , NLP.adjust_weight()
  

## Side Features 
- Jokes via pyjokes
- time
- search via ( wikipedia )
- email via sendgrid API

## V2 features ( on the way ) 
- UI with React ( still learning )
- Remind Tasks feature
