import botinput

# TODO think about for spoken word input, will commas be able to deliminate foods?

def main():
    with open("train/train.txt", "a") as myfile:
        while True:
            inputSentence = raw_input("what did you eat?: ")
            if inputSentence == "quit":
                break
            #  botinput.print_guess(inputSentence)
            foodList = botinput.parse_input(inputSentence, True)
            for item in foodList:
                print item
            myfile.write(inputSentence + "\n")
            myfile.flush()

if __name__ == "__main__":
        main()
