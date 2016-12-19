# python 2.7
# Austin Wilson
import sys

import botinput
import fetchData
import json
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english", ignore_stopwords = True)

# TODO think about for spoken word input, will commas be able to deliminate foods?
def main():
    if len(sys.argv) > 1:
        amendment_file = sys.argv[1]
        botinput.set_amendments(amendment_file) 

    with open("train/train.txt", "a") as logFile:
        converse(logFile)

def converse(logFile):
    while True:
        inputSentence = raw_input("what did you eat?: ")
        if inputSentence == "quit":
            break
        if len(inputSentence) <= 6:
            continue
        
        
        foodList = botinput.parse_input(inputSentence, False) # verbose
        for food in foodList:
            foodInput = food.pprint()
            if foodInput["food"]:
                nutritionData = fetchData.getNutritionValue(stemmer.stem(foodInput["food"]))
               
                if foodInput["count"]:
                    nutritionData["Protein"] = float(nutritionData["Protein"]) * float(foodInput["count"])
                    nutritionData["Fat"] = float(nutritionData["Fat"]) * float(foodInput["count"])
                    nutritionData["Carbohydrate"] = float(nutritionData["Carbohydrate"]) * float(foodInput["count"])
                    nutritionData["Total_Sugar"] = float(nutritionData["Total_Sugar"]) * float(foodInput["count"])
                    nutritionData["Protein"] = 0
                    print nutritionData
                else:
                	print nutritionData
            continueInputSentence = raw_input("Is that data correct?: ")
            if continueInputSentence == "yes":
                print "Thank you"
            else:
                print "Sorry we got the wrong information. Help us correct it by going to this website"


        logFile.write(inputSentence + "\n")
        logFile.flush()

if __name__ == "__main__":
        main()
