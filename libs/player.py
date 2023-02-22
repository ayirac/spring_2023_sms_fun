from libs.actor import actor
from libs.stats import Stats
from dataclasses import dataclass
import json

@dataclass
class Location:
    planet: str
    zone: str
    level: str

class player(actor):
    def __init__(self, phone_number):
        super().__init__(phone_number)
        self.location = Location('planet0', 'start', 'start')
        self.stats = Stats(5, 5, 5, 5, 5, 5, 5, 5, 5, 5)	# HP, DMG, CRIT, DEX, AGI, ACC, STR, INT, CHR, CHS
        self.weapon =  'none'					            # Current equipped weapon
        self.armor =  'shirt'					            # Current equipped armor
        self.inventory = []					                # Non-equipped weapons/armor and other items
        self.action = 'default'
        self.subject = 'default'
        self.first = False                                  # First time getting prompt response or not

    def get_output(self, msg_input):
        msg_input = msg_input.lower()
        with open('test_prompts.json', 'r') as f:
            prompts = json.load(f)
        # Check state
        if (self.state == 'init'):
            output = prompts["init"][self.state]['prompt'] 
            self.state = prompts["init"][self.state]['next']
        elif (self.state == 'init-c'): # Not in a game or in char creation
            output = prompts["init"][self.state]['prompt']
            if (msg_input == 'yes'):
                self.state = prompts["init"][self.state]['next']
        elif (self.state == 'in-game'): # In a game
            sentenceTokens = msg_input.split()
            self.action = ''
            self.subject = ''

            for w in sentenceTokens:
                # Search sentence for an action (first thing)
                for a in prompts["planets"][self.location.planet][self.location.zone][self.location.level]:
                    if (w.find(a) != -1):                 # (w == a) Check for exact same OR (w.find(a) != -1) if part of the word contains the action 
                        self.action = a
                        break
                # Search sentence for a subject (second thing)
                if (self.action != ''):
                    for s in prompts["planets"][self.location.planet][self.location.zone][self.location.level][action]:
                        if (w.find(s) != -1):
                            self.subject = s
                            break

            if (self.action in prompts["planets"][self.location.planet][self.location.zone][self.location.level]):
                if (self.subject in prompts["planets"][self.location.planet][self.location.zone][self.location.level][self.action]):
                    if isinstance(prompts["planets"][self.location.planet][self.location.zone][self.location.level][self.action][self.subject], list): # There is some command associated with the prompt
                        for i, o in enumerate(prompts["planets"][self.location.planet][self.location.zone][self.location.level][self.action][self.subject][1]):
                            print(prompts["planets"][self.location.planet][self.location.zone][self.location.level][self.action][self.subject][0])  # Print prompt
                            if (o == "JUMP"):                                                               # Execute commands, Jump to new level
                                i+= 1
                                self.location = prompts["planets"][self.location.planet][self.location.zone][self.location.level][self.action][self.subject][1][i]
                                self.action = 'default'
                                self.subject = 'default'
                                first = 1
                                break
                            i+= 1
                        # Add later commands
                else:
                    if (conAction == "attack"): # Combat isn't finished/in prototype stage
                        output = "Attack debug txt"
                        #attack("player")
                        #attack(conSubject)
                    else:
                        output = prompts["planets"][self.location.planet][self.location.zone][self.location.level][self.action][self.subject]
            else:
                output = prompts["planets"][self.location.planet][self.location.zone][self.location.level][self.action]["default"]
        elif ("default" in prompts["planets"][self.location.planet][self.location.zone][self.location.level]):
            output = prompts["planets"][self.location.planet][self.location.zone][self.location.level]['default']
        else:
            output = "Error, no prompt found!"
        return output
