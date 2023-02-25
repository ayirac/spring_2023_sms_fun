import json
import random
from tools.logging import logger

MY_GAME_LOGIC = {}
with open('map.json', 'r') as my_file:
    MY_GAME_LOGIC = json.loads(my_file.read())

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
        
        self.battle_in_prog = False
        #self.battle_state_loop = False
        self.battle_state_counter = 0

        self.state = "start"
        self.prev_state = None
        super().__init__(phone_number, attack, health)
    def attack_sequence(self):
        
        self.battle_in_prog = True
        roll = random.randint(0,20)
        if roll > 10:
            #you win fight
            self.battle_in_prog = False
            return f'rolled a {roll} for a fatal blow'

        return "did not land fatal blow"


    def get_inventory(self):
        inv = ""
        for items in self.inventory:
            inv = inv + " " + items
        return inv

    def get_stats(self):
        stats = f'hp: {self.hp} damage:{self.damage} dexterity: {self.dexterity} accuracy: {self.accuracy} strength: {self.strength} intelligence: {self.intelligence} charisma: {self.charisma} chaos: {self.chaos}'

        return stats

    def get_output(self,msg_input):
        found_match = False
        output = []
        if type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str: # we have choices

            for next_state in MY_GAME_LOGIC[ self.state ]['next_state']:
                if msg_input.lower() ==  next_state['input'].lower():
                    self.state = next_state['next_state']

                    if self.state == "battle_state" and self.battle_state_counter is 0:
                        self.battle_state_counter += 1

                    if 'point_delta' in  next_state:
                        self.score += next_state['point_delta']
                        output.append(f"Your Score {self.score}" )
                    found_match = True
                    break

            if found_match == False:
                return ['Ooops.. Not a valid choice...']

        while True:
            output.append( MY_GAME_LOGIC[ self.state ]['prompt'])
            if self.battle_state_counter == 0:
                self.prev_state = self.state

            if 'next_state' not in MY_GAME_LOGIC[ self.state ] or type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str:
                break
            
            if self.state == "attack_state":
                output.append(self.attack_sequence())
                if self.battle_in_prog is False:
                    self.state = MY_GAME_LOGIC['battle_state'][self.prev_state]
                    output.append( MY_GAME_LOGIC[ self.state ]['prompt'])
                    self.battle_state_counter = 0
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

