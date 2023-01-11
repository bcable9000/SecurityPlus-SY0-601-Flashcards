# Studying Flashcards
# Author: Bryce Cable
# Created - 1/11/2023
# Updated - 1/11/2023
import json
import random

#Clears the terminal before starting
def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


##initialize flashcard list and flashcards file
flashcard = []
flashFile = open('Flashcards.txt', 'r')
switch = {
        'quit' : "Quits program",
        1: "See all flashcards",
        2: "Test flashcards"
    }
switchPrint = json.dumps(switch, indent=4)
#Takes the question, answers, and notes from the document and puts them into the list
def extractflash():
    while (flashcard.count(('','','')) == 0):
        try :
                question = flashFile.readline().rstrip()
                answer = flashFile.readline().rstrip()
                note = flashFile.readline().rstrip()
                flashcard.append((question, answer, note))
                #print(flashcard)
        except:
            print("Empty file.")
            break
    flashcard.remove(('','',''))

def getInput():
    temp = 0
    count = 0
    for x in enumerate(switch):
        count += 1
    while (temp == 0):
        try:
            result = input(f"Please select an option\n {switchPrint}\n")
            result = int(result)
            if ((result < count)):
                return result
                temp = 1 # It shouldn't get to this line either way, but just in case it does there's not an infinite loop
            print(f"ERROR: Number must be between 1 and {count - 1}\n")
        except:
            result = result.lower()
            if result == 'quit':
                return result
            print("Please enter a valid number.\n")

def main():
    #Initialization
    clear()
    extractflash()
    option = getInput()
    
    #Selection with loop
    while (option != 'quit'):
        #See all flashcards
        if (option == 1):
            print(f"Current flashcards: \n")
            for x in range(0, len(flashcard)):
                print(f"Flashcard {x+1}")
                print(f"Q: {flashcard[x][0]}")
                print(f"A: {flashcard[x][1]}")
                print(f"Note: {flashcard[x][2]}\n")

        #Test the flashcards
        elif (option == 2):
            card = random.choice(flashcard)
            print(f"\nQuestion: {card[0]}")
            guess = input("Guess: ")
            if (guess.lower() == card[1].lower()):
                print("Congratulations! You got it right! (Press enter to continue)\n")
            else:
                print(f"Answer: {card[1]}")
                print(f"Note: {card[2]}\n(Press enter to continue)\n")
            input()
        option = getInput() # I decided to put this at the end so if the user does 'quit', it won't run through the loop again
    


main()