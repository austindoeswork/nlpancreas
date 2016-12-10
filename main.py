# python 2.7
# Austin Wilson
import sys

import botinput
import nutrition_facts.fetchData as ff
from fuzzywuzzy import fuzz

# TODO think about for spoken word input, will commas be able to deliminate foods?
def main():
    if len(sys.argv) > 1:
        amendment_file = sys.argv[1]
        botinput.set_amendments(amendment_file) 
    verbose = False
    if len(sys.argv) > 2:
        verbose = True

    with open("train/train.txt", "a") as logFile:
        converse(logFile, verbose)

def converse(logFile, verbose):
    inputSentence = raw_input("What did you eat?\n")
    while True:
        if inputSentence == "quit":
            break
        if len(inputSentence) <= 6:
            inputSentence = raw_input("What else did you eat?\n")
            continue
        
        foodList, foodTime = botinput.parse_input(inputSentence, verbose)
        if foodTime:
            print "================================================================"
            print "Time:", foodTime
        for food in foodList:
            print "================================================================"
            food.pprint()
            nutrition = ff.getNutritionValue(food.name)
            if nutrition:
                print "================================================================"
                nutrition.pprint()
                print "================================================================"
                confirm = raw_input("Does this information sound correct?\n")
                if botinput.is_confirm(confirm):
                    print "Awesome! Info has been logged into the system."
                else:
                    print "That's too bad."
            else:
                print "================================================================"
                print "Nutrition Info:\nSorry, I couldn't find that."

        logFile.write(inputSentence + "\n")
        logFile.flush()
        inputSentence = raw_input("What else did you eat?\n")

if __name__ == "__main__":
        main()
