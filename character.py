import json
import random
import difflib
from tools.logging import logger

MY_GAME_LOGIC = {}
with open('map.json', 'r') as my_file:
    MY_GAME_LOGIC = json.loads(my_file.read())


class Enemy():
    def __init__(self, enemyName, enemyHP, enemyDMG):
        self.name = enemyName
        self.hp = enemyHP
        self.damage = enemyDMG

#base class
class Character:
    def __init__(self, phone_number, attack, health):

        self.phone_number = phone_number
        self.attack = attack
        self.health = health

    def attack_sequence():
        pass
    def dialogue():
        pass

#child class
class player(Character):
    
    def __init__(self, phone_number, attack, health):

        self.phone = phone_number
        self.hp = 5
        self.damage = 5
        self.dexterity = 5
        self.accuracy = 5
        self.strength = 5
        self.intelligence = 5
        self.charisma = 5
        self.chaos = 5
        self.inventory = ["sword"]
        
        self.current_weapon = "sword"
        self.armor = "scrap metal"
        
        self.battle_in_prog = 0
        #self.battle_state_loop = False
        self.battle_state_counter = 0
        self.currentEnemy = None

        self.state = "start"
        self.prev_state = None
        super().__init__(phone_number, attack, health)
    def attack_sequence(self):
        roll = random.randint(0,20)
        self.battle_in_prog = 1
        if roll > 10:
            #you win fight
            self.battle_in_prog = 2
            resp = f"rolled a {roll} for a fatal blow against {self.currentEnemy.name}"
            return resp

        return f"rolled a {roll} but did  not land fatal blow"


    def get_inventory(self):
        inv = ""
        for items in self.inventory:
            inv = inv + " " + items
        return inv

    def get_stats(self):
        stats = f'hp: {self.hp} damage:{self.damage} dexterity: {self.dexterity} accuracy: {self.accuracy} strength: {self.strength} intelligence: {self.intelligence} charisma: {self.charisma} chaos: {self.chaos}'

        return stats

    # Parses a string to determine if input is valid utilizing difflib
    # Input: A string that will be split & checked for valid input in the json game logic. A float for the acceptable ratio of how likely a match is
    # Output: Index of the likely input or -1 if no input is found (implement default behaivor when the function returns -1)
    def check_input(self, input, acceptableRatio):
        sentenceTokens = input.split()
        ratios = []
        for t in sentenceTokens:
            if isinstance(MY_GAME_LOGIC[self.state]['next_state'], str): # String, potentially useless depending on json implementation
                matcher = difflib.SequenceMatcher(None, MY_GAME_LOGIC['self.state']['next_state'], t)
                ratio = matcher.ratio()
                if (ratio > acceptableRatio):
                    return 0
            else:                                                   # Array
                for s in MY_GAME_LOGIC[self.state]['next_state']:
                    matcher = difflib.SequenceMatcher(None, s['input'], t)
                    ratio = matcher.ratio()
                    ratios.append(ratio)
                    print("%s vs %s\nRatio: %f" % (s['input'], t, ratio))
                mostLikely = max(ratios)
                print(mostLikely)
                if (mostLikely > acceptableRatio):
                    return ratios.index(mostLikely)
        return -1

    def get_output(self,msg_input):
        output = []
        if type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str: # we have choices
            
            likelyInputIDX = self.check_input(msg_input.lower(), 0.7)
            if (likelyInputIDX != -1): # Input found above the threshold (NOT TESTED & Removed previous if check)    
                if (MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['next_state'] == 'battle_state' or MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['next_state'] == 'dialogue1'):
                    self.currentEnemy = Enemy(self.state, MY_GAME_LOGIC[self.state]['hp'], MY_GAME_LOGIC[self.state]['dmg'])
                    print("DEBUG, ENEMY SELECTED!")
                self.state = MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['next_state']

                if self.state == "battle_state" and self.battle_state_counter is 0:
                    self.battle_state_counter += 1

                if 'point_delta' in MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]:
                    self.score += MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['point_delta']
                    output.append(f"Your Score {self.score}" )
            else:
                return ['Ooops.. Not a valid choice...']

        while True:
            print('Current state DEBUG: %s\n' % self.state)
            output.append( MY_GAME_LOGIC[ self.state ]['prompt'])
            if self.battle_state_counter == 0:
                self.prev_state = self.state

            if 'next_state' not in MY_GAME_LOGIC[ self.state ] or type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str:
                break
            
            if self.state == "attack_state":
                output.append(self.attack_sequence())
                if self.battle_in_prog == 1: # Fight ongoing
                    # Scan array at MY_GAME_LOGIC['battle_state']['next_state'] for 'fight'
                    for s in MY_GAME_LOGIC['battle_state']['next_state']:
                        if (s['input'] == 'fight'):
                            break
                    self.state = s['next_state']
                    output.append(s['prompt'])
                    self.battle_state_counter = 0
                    break
                if self.battle_in_prog == 0 or self.battle_in_prog == 2:                           # Fight over, victory
                    self.state = MY_GAME_LOGIC[self.currentEnemy.name]['victory_state']
                    self.battle_in_prog = 0
                    currentEnemy = None #  Remove the defeated enemy
                    output.append(MY_GAME_LOGIC[self.state]['prompt'])
                    break
                
            elif self.state == "inventory":
                output.append(self.get_inventory())

            elif self. state == "stats":
                output.append(self.get_stats())

            self.state = MY_GAME_LOGIC[ self.state]['next_state']

        return output

class Monster(Character):
    def __init__(self, attack, health):
        super().__init__(attack, health)

class Alien(Character):
    def __init__(self, attack, health):
        super().__init__(attack, health)
