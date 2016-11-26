import botinput
def main():
    while True:
        inputSentence = raw_input("what did you eat?: ")
        if inputSentence == "quit":
            break
        #  botinput.print_guess(inputSentence)
        foodList = botinput.parse_input(inputSentence)
        for item in foodList:
            print item

if __name__ == "__main__":
        main()
