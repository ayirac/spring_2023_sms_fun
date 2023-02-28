import json
import random
import difflib
from tools.logging import logger

first_mission = {"east","west","north","south"} #first_mission set to compare with visited_states set 

MY_GAME_LOGIC = {}
with open('map.json', 'r') as my_file:
    MY_GAME_LOGIC = json.loads(my_file.read())

class Enemy():
    def __init__(self, enemyName, enemyHP, enemyBaseDMG):
        self.name = enemyName
        self.hp = enemyHP
        self.damage = enemyBaseDMG
        self.alive = True

    def enemy_attack(self, main_character):
        crit_dmg = self.damage
        crit_chance = random.randint(1, 10)
        
        if crit_chance == 1:
            self.damage *= 2

        main_character.take_damage(crit_dmg)
        return f'Enemy landed {crit_dmg} damage. Your health is now {main_character.health}'

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
#base class
class Character:
    def __init__(self, phone_number, attack, health):

        self.phone_number = phone_number
        self.attack = attack
        self.health = health

    def player_attack():
        pass
    def dialogue():
        pass

#child class
class player(Character):
    
    def __init__(self, phone_number, attack, health):

        self.phone = phone_number
        self.damage = 10
        
        self.inventory = ["broadsword"]
        
        self.current_weapon = "broadsword"
        self.armor = "scrap metal"
        
        self.score = 0
        self.alive = True
        self.currentEnemy = None
        self.last_prompt = None
        
        self.visited_states = set()
        self.state = "main_menu"
        super().__init__(phone_number, attack, health)

    def get_mm(self):
        menuItems = []
        menuItems.append('Remnants of a Falling Star⭐')
        menuItems.append('-Main Menu-')
        for p in MY_GAME_LOGIC['main_menu']['next_state']:
            menuItems.append(p['text'])
        menuItems.append('Choose an option from above.')
        return '\n'.join(menuItems)
        
    def player_attack(self):
        crit_dmg = self.damage
        crit_chance = random.randint(1, 10)

        if crit_chance == 1:
            crit_dmg *= 2

        self.currentEnemy.take_damage(crit_dmg)
        return f'you inflicted {crit_dmg} damage. Enemy hp is {self.currentEnemy.hp}'

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def get_inventory(self):
        inv = ""
        for items in self.inventory:
            inv = inv + " " + items
        return inv

    def get_stats(self):
        stats = f'hp: {self.health} damage: {self.damage}'

        return stats
    
    def swap_weapon(self, inp):
        WEAPONS = {}
        input = inp.split()
        with open('RFS.json', 'r') as my_file:
            WEAPONS = json.loads(my_file.read())

        for j in input: # Scan weapons data
            for t in WEAPONS['weapons']:
                for x in WEAPONS['weapons'][t]:
                    if j.lower() in x:
                        for p in self.inventory: # Check if weapon exists in player inventory
                            if p == x:
                                self.current_weapon = x
                                return f'Swapped to {self.current_weapon}'
        return 'Invalid weapons'

    # Parses a string to determine if input is valid utilizing difflib
    # Input: A string that will be split & checked for valid input in the json game logic. A float for the acceptable ratio of how likely a match is
    # Output: Index of the likely input or -1 if no input is found (implement default behaivor when the function returns -1)
    def check_input(self, input, acceptableRatio):
        sentenceTokens = input.split()
        ratios = []
        promptRatios = []
        for t in sentenceTokens:
            if isinstance(MY_GAME_LOGIC[self.state]['next_state'], str): # String, potentially useless depending on json implementation
                matcher = difflib.SequenceMatcher(None, MY_GAME_LOGIC['self.state']['next_state'], t)
                ratio = matcher.ratio()
                if (ratio > acceptableRatio):
                    return 0
            else:                                                   # Array
                for s in MY_GAME_LOGIC[self.state]['next_state']:
                    matcher = difflib.SequenceMatcher(None, s['input'], t)
                    matcherPrompt = difflib.SequenceMatcher(None, 'prompt', t)
                    ratioPrompt = matcherPrompt.ratio()
                    promptRatios.append(ratioPrompt)
                    ratio = matcher.ratio()
                    ratios.append(ratio)
                mostLikely = max(ratios)
                mostLikelyPrompt = max(promptRatios)
                # Check if 'prompt' was attempted to be typed, in future change to check for a 'global_actions' array for more functionality
                if (mostLikelyPrompt > acceptableRatio):
                    return -2 # -2 stands for the 'output last prompt'
                elif (mostLikely > acceptableRatio):
                    return ratios.index(mostLikely)
        return -1

    def get_output(self,msg_input):
        output = []
        if self.state == 'main_menu': # Alternative logic for main-menu
            likelyInputIDX = self.check_input(msg_input.lower(), 0.7)
            if (likelyInputIDX >= 0):
                output.append(MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['prompt'])
            else:
                output.append(['Not a valid choice'])
            if (likelyInputIDX == 0):
                self.state = 'start'
            else:
                return output
            
        if type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str: # we have choices
            
            likelyInputIDX = self.check_input(msg_input.lower(), 0.7)
            if (likelyInputIDX >= 0): # Input found above the threshold (NOT TESTED & Removed previous if check)    
                if (MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['next_state'] == 'battle_state' or MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['next_state'] == 'dialogue1'):
                    self.currentEnemy = Enemy(self.state, MY_GAME_LOGIC[self.state]['hp'], MY_GAME_LOGIC[self.state]['dmg'])
                    print("DEBUG, ENEMY SELECTED!")
                    
                #if msg_input.lower() ==  [self.state]['next_state']['input']
                    #self.state = next_state['next_state']
                 
                #logic to prevent player from revisiting paths
                if self.state not in self.visited_states:
                    self.visited_states.add(self.state)
                        
                self.state = MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['next_state']
                print("MY_GAME_LOGIC[self.state]['next_state'][likelyInputIDX]['next_state'] is: " + self.state)
                    
            elif (likelyInputIDX == -2): ## Print last prompt saved in history, no state change
               if (self.last_prompt != None):
                    resp = self.last_prompt.copy()
                    resp.insert(0, 'Last prompt:')
                    return resp
               else:
                    return ['No prompt saved in history!']
            else:
                return ['Ooops.. Not a valid choice...']

        while True:
            print('Current state DEBUG: %s\n' % self.state)
        
            #logic for clearing all paths
            if self.score >= 9 and self.state == "planet a'pholi directions":
                self.state = "complete_directions"
                output.append( MY_GAME_LOGIC[ self.state ]['prompt'])
                self.state = MY_GAME_LOGIC[self.state]['next_state']
                
            output.append( MY_GAME_LOGIC[ self.state ]['prompt'])
            
            #stealth state point delta
            if 'point_delta' in MY_GAME_LOGIC[self.state]:
                    self.score += MY_GAME_LOGIC[self.state]['point_delta']
                    output.append(f"Congragulations your score is now {self.score}")
                    
            if 'next_state' not in MY_GAME_LOGIC[ self.state ] or type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str:
                break
            
            if self.state == "attack_state":
                #player attacks
                enemy_dmg_taken = self.player_attack()
                
                #enemy attacks
                player_dmg_taken = self.currentEnemy.enemy_attack(self)
                
                if self.alive is True and self.currentEnemy.alive is True:
                    # Scan array at MY_GAME_LOGIC['battle_state']['next_state'] for 'fight'     
                    for s in MY_GAME_LOGIC['battle_state']['next_state']:
                        if (s['input'] == 'fight'):
                            break
                    self.state = s['next_state']
                    
                    output.append(enemy_dmg_taken)
                    output.append(player_dmg_taken)
                    
                    output.append(s['prompt'])
                    break

                elif self.currentEnemy.alive is False:
                    # Fight over, victory
                    self.state = MY_GAME_LOGIC[self.currentEnemy.name]['victory_state']
                    # resetting health
                    self.health = 100
                    self.score +=1
                    
                    output.append(enemy_dmg_taken)
                    output.append(f'you defeated {self.currentEnemy.name}. Your score is {self.score}')
                    output.append(MY_GAME_LOGIC[self.state]['prompt'])
                    self.currentEnemy = None #  Remove the defeated enemy
                    break

                elif self.alive is False:
                    #player dies
                    #reset enemy and player health
                    self.currentEnemy.hp = 100
                    self.health = 100
                    self.alive = True
                    
                    output.append(player_dmg_taken)
                    output.append("you lost. try again")
                    #trs to battle state again
                    self.state = MY_GAME_LOGIC[self.currentEnemy]['next_state']
                    break
                
            elif self.state == "inventory":
                output.append(self.get_inventory())

            elif self. state == "stats":
                output.append(self.get_stats())
                
            elif self.state == "swap":
                output.append(self.swap_weapon(msg_input))
                
            if self.state not in self.visited_states:
                self.visited_states.add(self.state)

            self.state = MY_GAME_LOGIC[ self.state]['next_state']
            
        self.last_prompt = output
        return output
