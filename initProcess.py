import time
import  imageGenerator
import textAnalyzer

def mainGUI(text):
    # To process and validate the input text
    ent, hair, eyes = textAnalyzer.startTextBreakdown(text)
    if (ent == "404"):
        print("Invalid text, couldnt locate enity/features to generate")
        return "404"
    if (ent == "403" ):
        print("entity has been identified but the features could not")
        return "403"

    print(ent + " " + hair + " " + eyes)
    # To generate the neeeded image
    fileName= imageGenerator.generateImage(eye_color=eyes, hair_color=hair, entity_name=ent)
    print("image Saved as: " + fileName)
    return fileName



if __name__ == '__main__':
    # text= "Akira is a girl with hair that is blue as the ocean, and eyes as red as the red sea"
    # text = "Bill Gates is a person
    text=""
    # text= "she had blue eyes"
    # text= "she had blue hair"
    # ent,hair,eyes = nlpBreakdown.startTextBreakdown(text)
    # print(ent+" "+hair+" "+eyes)
    # fileName = ent+str((round(time.time() * 1000)))
    # print("image Saved as: "+fileName)
    mainGUI(text)


