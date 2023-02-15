import json
import random

## Original Prompt with context/clues on what to do next ##
global prompts
with open('test_prompts.json', 'r') as f:
    prompts = json.load(f)
# Globals for testing
global conPlanet
global conZone
global conLevel
global conAction
global conSubject
global first
conPlanet = "planet0"
conZone = "jungle"
conLevel = "level0"
conAction = "initial"
conSubject = "default"
first = 1

# Parses a string to find the 'action' & the 'subject' of a sentence given a list of actions & subjects possible.
# Input: A string 'sentence' is to be parsed. Two lists called actions & subjects that contain valid actions and subjects for the scenario
# Output: A tuple of the action, subject or None if invalid
def determineAction(sentence):
    global conPlanet
    global conZone
    global conLevel
    global conAction
    global conSubject

    sentenceTokens = sentence.split()
    action, subject = None, None                     # Variables that will hold the action/subjects found

    for w in sentenceTokens:
        # Search sentence for an action (first thing)
        if (action == None):
            for a in prompts["planets"][conPlanet][conZone][conLevel]:
                if (w.find(a) != -1):                 # (w == a) Check for exact same OR (w.find(a) != -1) if part of the word contains the action 
                    action = conAction = a
                    break
        # Search sentence for a subject (second thing)
        if (action != None):
            
            for s in prompts["planets"][conPlanet][conZone][conLevel][action]:
                if (w.find(s) != -1):
                    subject = conSubject = s
                    break
    
    return (action, subject)

# Filler function for an entity attacking another entity given their name, must match their prompt name
def attack(attacker):
    aRoll = random.randrange(0,20)
    tRoll = random.randrange(0,20)
    if (attacker == "player"):
        attempt = str(prompts["planets"][conPlanet][conZone][conLevel][conAction][conSubject][attacker+"_attempt"]) % ("stab", "sword")
    else:
        attempt = str(prompts["planets"][conPlanet][conZone][conLevel][conAction][conSubject][attacker+"_attempt"])
    status = ""

    if (aRoll >= tRoll):     # Attack win
        result = "succeed with a (%dd20 v %dd20) " % (aRoll, tRoll)
        status = "success"
    else:
        result = "failed with a (%dd20 v %dd20) " % (aRoll, tRoll)
        status = "failure"
     
    flavor = random.choice(prompts["planets"][conPlanet][conZone][conLevel][conAction][conSubject][attacker+"_"+status]) # cont
    print(attempt + result + flavor)

# Computes the correct prompt to print as a response to user input
# Input: A tuple containing the action, subject. A list of prompts for the scenario to choose from
def computePrompt():
    global conPlanet
    global conZone
    global conLevel
    global conAction
    global conSubject
    global first

    if (conAction in prompts["planets"][conPlanet][conZone][conLevel]):
        if (conSubject in prompts["planets"][conPlanet][conZone][conLevel][conAction]):
            if isinstance(prompts["planets"][conPlanet][conZone][conLevel][conAction][conSubject], list): # There is some command associated with the prompt
                for i, o in enumerate(prompts["planets"][conPlanet][conZone][conLevel][conAction][conSubject][1]):
                    print(prompts["planets"][conPlanet][conZone][conLevel][conAction][conSubject][0])  # Print prompt
                    if (o == "JUMP"):                                                               # Execute commands, Jump to new level
                        i+= 1
                        conLevel = prompts["planets"][conPlanet][conZone][conLevel][conAction][conSubject][1][i]
                        conAction = "initial"
                        conSubject = "default"
                        first = 1
                        break
                    i+= 1
                    # Add later commands
            else:
                if (conAction == "attack"): # Combat isn't finished/in prototype stage
                    attack("player")
                    attack(conSubject)
                else:
                    print(prompts["planets"][conPlanet][conZone][conLevel][conAction][conSubject])
        else:
            print(prompts["planets"][conPlanet][conZone][conLevel]["default"])
    elif ("default" in prompts["planets"][conPlanet][conZone][conLevel]):
        print(prompts["planets"][conPlanet][conZone][conLevel])
    else:
        print("Error, no prompt found!")

        

# Testing code
def testScenario():
    global conPlanet
    global conZone
    global conLevel
    global conAction
    global conSubject
    global first

    # Main loop for player
    while (True):
        if first:
            first = 0
            print("%s" % prompts["planets"][conPlanet][conZone][conLevel][conAction])
        else:
            print("What do you wish to do next?")
        print("Enter your response:")
        sentence = input()
        actionSubject = determineAction(sentence.lower())   # sets the conAction & conSubject based on the user input
        #print(actionSubject) debug action/subject tuple
        computePrompt()                                     # grabs the correct prompt from json

def main():
    testScenario()

if __name__ == "__main__":
    main()
