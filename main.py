#base class
class Character:
    def __init__(self, name, attack, defense, intellect, current_node=None):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.intellect = intellect

        #track the room/mission/state or whatever we want to call each node (object) of the player
        self.current_node = current_node

    def attack_sequence():
        pass
    def dialogue():
        pass

#child class
class Human(Character):
    
    def __init__(self, name, attack, defense, intellect):
        #calling base class construtor
        super().__init__(name, attack, defense, intellect)

class Monster(Character):
    def __init__(self, name, attack, defense, intellect):
        super().__init__(name, attack, defense, intellect)

class Alien(Character):
    def __init__(self, name, attack, defense, intellect):
        super().__init__(name, attack, defense, intellect)

class Node:
    
    # constructor
    # next = None means this parameter doesnt need to passed when created a node object. 

    # parameters default to none if no argument is passed
    # e.g Node = (description) 
    # prompt will be null 
    def __init__(self, description, prompt = None):
        
        # description when intereacting with this environment
        self.description = description

        # prompt that player follows to decide next move
        self.prompt = prompt

        self.next = None

        self.previous = None

# Graph data structure implemented as a doubly-linked list
# node points to another node
class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)
    
    def add_connection(self, node1, node2, node3=None):
        node1.next = node2

        node1.previous = node3
        
# Parses a string to find the 'action' & the 'subject' of a sentence given a list of actions & subjects possible.
# Input: A string 'sentence' is to be parsed. Two lists called actions & subjects that contain valid actions and subjects for the scenario
# Output: A tuple of the action, subject or None if invalid
def determineAction(sentence, actions, subjects):
    sentenceTokens = sentence.split()
    action, subject = None, None                     # Variables that will hold the action/subjects found

    for w in sentenceTokens:
        # Search sentence for an action (first thing)
        if (action == None):
            for a in actions:
                if (w.find(a) != -1):                 # (w == a) Check for exact same OR (w.find(a) != -1) if part of the word contains the action 
                    action = a
                    break
        # Search sentence for a subject (second thing)
        if (action != None):
            for s in subjects:
                if (w.find(s) != -1):
                    subject = s
                    break
    
    return (action, subject)

# Computes the correct prompt to print
# Input: A tuple containing the action, subject. A list of prompts for the scenario to choose from
def computePrompt(actionSubject, prompts):
    for p in prompts:
        for a in p[0]:
            if (actionSubject[0] == a and (actionSubject[1] == p[1] or p[1] == "any")):
                print(p[2])
                break

# Testing code for determineAction/computePrompt, not final
def testScenario():
    weaponType = ("unarmed", "punch")                                                                     # Probably pass this data as value later on to a function
    actions = ["attack", "inspect", "look", "read", "touch", "smell", "open", "wait", "move", "grab"]     # Lists of actions/subjects for this specific scenario  
    subjects = ['wall', 'door', 'window', 'container', "terminal", "container", "first-aid kit"]

    ## Original Prompt with context/clues on what to do next ##
    print("Some long prompt telling you that you can do a variety of options: Like attacking, inpsecting the wall/door/window, etc")
    print("Enter your response:")
    sentence = input()
    actionSubject = determineAction(sentence.lower(), actions, subjects)

    # Response prompts for this specific scenario, find a better way of storing this data perhaps
    # (listActions, subject, prompt)
    prompts = [(["attack"], "any", "You %s the %s, nothing happens" % (weaponType[1], actionSubject[1])), \
        (["inspect"], "wall", "You %s %s walls of the ship, finding that most of the fixtures mounted to the wall are intact." % ((actionSubject[0], "the" if actionSubject[0] == actions[1] else "at"))), 
        (["inspect"], "door", "You inspect the door and see a large metal container blocking the door and a small functioning terminal to the right of the door for opening and closing."),
        (["inspect", "look"], "window", "You look outside the window, a light orange haze loiters in the air and a lush green jungle can be seen fairly close to your ship.")]

    print(actionSubject)
    computePrompt(actionSubject, prompts)

def main():
    # display prompt on screen and grab user input
    player_class = input("Choose player class (Human, Alien, Monster): ")
    player_name = input("Enter player name: ")
    
    # creating a player variable that references a Character object
    if(player_class == "Human"):
        player = Human(player_name, 2, 1, 8)
    
    # root node to our map 
    game_map = Node("introduction")
    # first mission node
    first_mission = Node("First Mission: -place holder- ")

    # Transition from start to first mission
    game_map.next = first_mission 
    print()
    print(game_map.description)
    print()
    print(first_mission.description)
    print()
    print(f'player name: {player.name}, attack rating: {player.attack}, defense rating: {player.defense}, intellect rating: {player.intellect} ')
    testScenario()

if __name__ == "__main__":
    main()
