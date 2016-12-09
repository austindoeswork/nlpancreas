# python 2.7
# Austin Wilson
import sys

import botinput

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
            food.pprint()

        logFile.write(inputSentence + "\n")
        logFile.flush()

if __name__ == "__main__":
        main()
