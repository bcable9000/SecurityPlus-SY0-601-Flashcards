# Studying Flashcards
# Author: Bryce Cable
# Created - 1/11/2023
# Updated - 1/18/2023
import json
import random
from datetime import date
import shutil
import statistics as stats

#Creating backup of json file just in case
shutil.copyfile("Flashcards.json","backup.json")

#Clears the terminal before starting
def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


#opens file and loads dictionary
fjson = open("Flashcards.json")
jflash = json.load(fjson)
flashcards = jflash["Flashcards"]
switch = {
        'quit' : "Quits program",
        1: "See all flashcards",
        2: "Test flashcards",
        3: "Add flashcards",
        4: "Reset date/frequency of cards"
    }
switchPrint = json.dumps(switch, indent=4)

def getInput():
    clear()
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
#Updates the file. In case something goes wrong (mostly for when I'm testing my code), the backup will be restored instead (since using open(...,"w") erases the file before writing)
def updateFile (): 
    try:
        with open("Flashcards.json", "w") as outfile:
            outfile.write(json.dumps(jflash, indent = 4))
        shutil.copyfile("flashcards.json","backup.json")
    except:
        print("\nERROR: Something went wrong when writing to file, restoring backup file\n")
        shutil.copyfile("backup.json","Flashcards.json")
        input("Press ENTER to continue")
#My customized random function. In short, cards that have been less studied are less likely to appear, while cards that have been more studied are more likely
def cRandom () :
    ranNum = []
    Freqs = []
    Dates = []
    for i in flashcards:
        Freqs.append(i["Frequency"])
        Dates.append(i["Date"])
    Freq4 = stats.quantiles(Freqs, n = 3)
    Date4 = stats.quantiles(Dates, n = 3)
    for x in flashcards:
        
        if (x["Frequency"] >= Freq4[1] and x["Date"] >= Date4[1]):
            for i in range(0,1):
                ranNum.append(x["ID"])
        elif ((x["Frequency"] >= Freq4[1] and x["Date"] >= Date4[0]) or (x["Frequency"] >= Freq4[0] and x["Date"] >= Date4[1])):
            for i in range(0,2):
                ranNum.append(x["ID"])
        elif (x["Frequency"] >= Freq4[0] and x["Date"] > Date4[0]):
            for i in range(0,3):
                ranNum.append(x["ID"])
        elif ((x["Frequency"] >= Freq4[0] and x["Date"] < Date4[0]) or (x["Frequency"] < Freq4[0] and x["Date"] >= Date4[0])):
            for i in range(0,4):
                ranNum.append(x["ID"])
        elif (x["Frequency"] < Freq4[0] and x["Date"] < Date4[0]):
            for i in range(0,5):
                ranNum.append(x["ID"])
        
    #after putting them all into a list, with less-studied questions appearing more frequenctly, I let the actual random tool do it's work
    #print(f"List: {ranNum}\nDateq: {Date4}\nFreqq: {Freq4}\n")
    return random.choice(ranNum)

def main():
    #Initialization
    clear()
    option = getInput()

    #Selection with loop
    while (option != 'quit'):
        #both initializing and resetting variables here
        mod = ""
        q = ""
        a = ""
        n = "" 
        #this is to get todays date since json can't store the date class. To avoid larger numbers, the year starts at 2023
        today = (date.today().year - 2023) * 365 + date.today().month * 12 + date.today().day
        #See all flashcards
        if (option == 1):
            print(f"Current flashcards: \n(Press ENTER to go to next card)\n")
            for i in flashcards:
                clear() #clears screen for readability while still allowing user to scroll up
                print(f"\nID: {i['ID']}")
                print(f"Question: {i['Question']}")
                print(f"Answer: {i['Answer']}")
                print(f"Notes: {i['Notes']}")
                try:
                    print(f"Date: {i['Date']}")
                    print(f"Frequency: {i['Frequency']}\n")
                except:
                    print("There is no time and/or date")
                    i["Date"] = today
                    i["Frequency"] = 0


                input()
            input("(end of cards)")
            updateFile()

        #Test the flashcards
        elif (option == 2):
            guess = ""
            while ((mod.lower() != "quit") and (guess.lower() != "quit")):
                clear()
                #chooses a random card
                card = flashcards[cRandom()-1]

                print(f"Let's see if you know flashcard #{card['ID']}")
                print(f"\nQuestion: {card['Question']}")
                guess = input("Guess: ")
                print(f"Answer: {card['Answer']}")
                print(f"Note: {card['Notes']}\n")

                #updates date, frequency, and file
                card.update({"Date":today})
                card.update({"Frequency":card["Frequency"] + 1})
                mod = input("(Press ENTER to continue or 'quit' to go back to the menu)\n")
                updateFile()
        #Adding a flashcard
        elif (option == 3):
            newID = jflash["Flashcards"][len(jflash["Flashcards"]) - 1]["ID"] + 1
            while ((mod.lower() != "quit") and (q.lower() != "quit") and (a.lower() != "quit") and (n.lower() != "quit")):
                clear()
                
                print("Adding a new flashcard")
                q = input("Please enter the new question.\n")
                a = input("Please enter the answer\n")
                n = input("Please enter any notes.\n")

                mod = input("Press ENTER to add this card and another, 'quit' to add this card and go back to menu, or 'abort' to not add this card and go back to the menu'\n")
                if (mod.lower() != "abort"):
                    jflash["Flashcards"].append({"ID":newID,"Question":q,"Answer":a,"Notes":n,"Date":today,"Frequency":0})
                    newID = newID + 1
                    updateFile()
        elif (option == 4):
            for x in flashcards:
                x.update({"Date":today})
                x.update({"Frequency":0})
                print(x["Date"])
                print(x["Frequency"])
            input()
        option = getInput() # I decided to put this at the end so if the user does 'quit', it won't run through the loop again
    


main()
updateFile()