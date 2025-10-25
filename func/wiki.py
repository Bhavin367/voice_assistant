import wikipedia 


def wiki(topic) :
    try:
        data = wikipedia.summary(topic,sentences = 3)
        data = data.split(".")
        main_info = data[0] + " " + data[1] 
        additional_info = data[2]

        return main_info , additional_info 

    except :
        return None 

# could add further functions to support searching similar topics


