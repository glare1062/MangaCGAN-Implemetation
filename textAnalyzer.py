import spacy
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
from colour import Color

filteredSet = []
filteredPOSSet = []
possibleColours = ['blue','brown','blonde','red','black','green','purple','aqua','pink','gray','yellow','white','orange']

def __tokenizeSentence(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entity="Unnamed Entity"
    colourOfHair="404"
    colourOfEyes="404"
    ner= "404"

    # NER model called and doc is parsed
    for ent in doc.ents:
        # if condition to only save entity if its a person
        if ent.label_== "PERSON" or ent.label_=="ORG":
            ner = ent.text
            nerlable= ent.label_

    # tokenizes the sentence and process's it using Spacys pretrained model
    for token in doc:


        headVar =  token.head
        # Checks if the word is a colour
        if __check_color(token.text):
            # if its a colour and is headed by the words hair o er eyes
            if 'hair' in headVar.text:
                colourOfHair = token.text
            if 'eye' in headVar.text:
                colourOfEyes = token.text
        # removes unnecessary words from sentence
        if token.is_stop == False:
            filteredSet.append(token.text)
            filteredPOSSet.append(token.dep_)
            # identifies if the word is a noun and the subject of the description thereby making it an entity
            token_dep = token.dep_
            token_pos = token.pos_
            head = token.head
            if token.dep_=="nsubj" and token.pos_ =="PROPN":
                entity=token.text

    if ner != "404":
        entity = ner

    return entity,colourOfHair,colourOfEyes

def __check_color(color):
    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError:
        # The color code was not found
        return False

def __checkForVariable():
    colourOfEyes ="<UNK>"
    colourOfHair ="<UNK>"
    for x in range(len(filteredSet)):
        # CHECK FOR HAIRCIOLOUR
        if "hair" in filteredSet[x]:
            # before check
            if (((x - 1) >= 0) and __check_color(filteredSet[x - 1])):
                colourOfHair = filteredSet[x - 1]
            # After check
            if (((x + 1) <= (len(filteredSet)) - 1) and __check_color(filteredSet[x + 1])):
                colourOfHair = filteredSet[x + 1]

        # CHECK FOR EYE COLOUR
        if "eye" in filteredSet[x]:
            # before check
            if (((x - 1) >= 0) and __check_color(filteredSet[x - 1])):
                colourOfEyes = filteredSet[x - 1]
            # After check
            if (((x + 1) <= (len(filteredSet)) - 1) and __check_color(filteredSet[x + 1])):
                colourOfEyes = filteredSet[x + 1]

    #     CHECK for if the colours are within the scope of generateable colours
    if (colourOfEyes not in possibleColours) and (colourOfHair not in possibleColours):
        return "404","404"
    return colourOfHair,colourOfEyes

def  startTextBreakdown(text):
    errorFlag="200"
    entity,color_hair,color_eye = __tokenizeSentence(text)
    color_hair= color_hair.lower()
    color_eye=color_eye.lower()
    colourOfHair,colourOfEyes = __checkForVariable()
    if colourOfHair!="<UNK>":
        colourOfHair =colourOfHair.lower()
    if colourOfEyes!="<UNK>":
        colourOfEyes = colourOfEyes.lower()

    if color_hair == "404":
        color_hair=colourOfHair

    # VAlidation CHecks in text anlaysis
    if color_eye == "404":
        color_eye=colourOfEyes
    if color_hair=="404" and color_eye=="404":
        errorFlag="403"
    if color_hair!="404" or color_eye!="404":
        return entity, color_hair, color_eye
    if color_hair=='404' and color_eye=='404' and entity =="Unnamed Entity":
        return  "404", colourOfHair, colourOfEyes
    if errorFlag=="403":
        entity="403"

    return entity,colourOfHair,colourOfEyes


if __name__ == '__main__':
    # text = ("Akira is a girl with green hair, and purple eyes")
    # text = ("Jason is a black haired, and sea blue eyed girl")
    text= "Anne is a girl with hair that is blue as the ocean, and eyes as red as the red sea"
    # text= "She had blue hair and red eyes"
    # text= "She had blue hair"
    text= "She had Blue hair"
    # text= ""
    # text="Bill gates has gray hair"
    # text= "the organization of Apple had blue hair and red eyes"
    # text= "Bill Gates is an entrepreneur"
    # entity,color_hair,color_eye = __tokenizeSentence(text)
    # colourOfHair,colourOfEyes = __checkForVariable()
    # if color_hair == "404":
    #     color_hair=colourOfHair
    # if color_eye == "404":
    #     color_eye=colourOfEyes
    # if color_hair=="404" and color_eye=="404":
    #     entity="403"
    # if color_hair!="404" and color_eye!="404":
    #     entity="200"
    # if color_hair!="404" and color_eye!="404" and entity =="Unnamed Entity":
    #     entity="404"
    entity, hair, eyes = startTextBreakdown(text)

    print(entity)
    print("the end")