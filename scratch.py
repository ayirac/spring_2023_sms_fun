import json
import random
from tools.logging import logger

first_mission = {"east","west","north","south"}

#output = []

MY_GAME_LOGIC = {}
with open('map.json', 'r') as my_file:
    MY_GAME_LOGIC = json.loads(my_file.read())


class Enemy():
    def __init__(self, enemyName, enemyHP, enemyBaseDMG, enemyCRIT=None):
        self.name = enemyName
        self.hp = enemyHP
        self.damage = enemyBaseDMG
        self.crit = enemyCRIT
        self.alive = True

    def enemy_attack(self, main_character):
        crit_dmg = self.damage
        crit_chance = random.randint(1, 10)
        if crit_chance == 1:
            self.damage *= 2
            #output.append("enemy landed critical hit")

        main_character.take_damage(crit_dmg)
        return main_character.alive

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
        #output.append(f'enemy health is now {self.hp}')

#base class
class Character:
    def __init__(self, phone_number, attack, health):

        self.phone_number = phone_number
        self.prev_msgs = []

        self.attack = attack
        self.health = health

    def save_msg(self, msg):
        self.prev_msgs.append(msg)

    def player_attack():
        pass
    def dialogue():
        pass

#child class
class player(Character):

    def __init__(self, phone_number, attack, health):

        self.phone = phone_number
        self.hp = 5
        self.damage = 10

        self.inventory = ["sword"]

        self.current_weapon = "sword"
        self.armor = "scrap metal"

        self.currentEnemy = None
        self.alive = True

        self.state = "start"
        self.visited_states = set()

        super().__init__(phone_number, attack, health)
    def player_attack(self):
        crit_dmg = self.damage

        crit_chance = random.randint(1, 10)
        if crit_chance == 1:
            crit_dmg *= 2
            #output.append("you landed a critical hit")
        #output.append("you landed a basic hit")
        self.currentEnemy.take_damage(crit_dmg)
        return self.currentEnemy.alive

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
        #output.append(f'your health is now at: {self.health}')

    def get_inventory(self):
        inv = ""
        for items in self.inventory:
            inv = inv + " " + items
        return inv    
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
                    if (next_state['next_state'] == 'battle_state' or next_state['next_state'] == 'dialogue1'):
                        self.currentEnemy = Enemy(self.state, MY_GAME_LOGIC[self.state]['hp'], MY_GAME_LOGIC[self.state]['dmg'])

                    #clearing all paths logic
                    if self.state not in self.visited_states:
                        self.visited_states.add(self.state)

                    self.state = next_state['next_state']

                    found_match = True
                    break

            if found_match == False:
                return ['Ooops.. Not a valid choice...']

        while True:
            if "planet a'pholi directions" in self.visited_states and self.visited_states.issuperset(first_mission):
                self.state = "fight_gaurds"

            output.append( MY_GAME_LOGIC[ self.state ]['prompt'])

            if 'next_state' not in MY_GAME_LOGIC[ self.state ] or type( MY_GAME_LOGIC[ self.state ]['next_state'] ) != str:
                break

            if self.state == "attack_state":
                #player attacks
                #method returns if enemy is alive
                enemy_alive = self.player_attack()
                #enemy attacks
                player_alive = self.currentEnemy.enemy_attack(self)

                if enemy_alive is True and player_alive is True:
                    # Scan array at MY_GAME_LOGIC['battle_state']['next_state'] for 'fight'     
                    for s in MY_GAME_LOGIC['battle_state']['next_state']:
                        if (s['input'] == 'fight'):
                            break
                    self.state = s['next_state']
                    output.append(s['prompt'])
                    break

                elif enemy_alive is False:
                    # Fight over, victory
                    self.state = MY_GAME_LOGIC[self.currentEnemy.name]['victory_state']
                    # resetting health
                    self.health = 100

                    output.append(MY_GAME_LOGIC[self.state]['prompt'])
                    output.append(f'you defeated {self.currentEnemy.name}')
                    self.currentEnemy = None #  Remove the defeated enemy
                    break

                elif player_alive is False:
                    #player dies
                    #reset enemy and player health
                    self.currentEnemy.hp = 100
                    self.health = 100
                    output.append("you lost. try again")
                    #trs to battle state again
                    self.state = MY_GAME_LOGIC[self.currentEnemy]['next_state']
                    break

            elif self.state == "inventory":
                output.append(self.get_inventory())

            elif self. state == "stats":
                output.append(self.get_stats())

            if self.state not in self.visited_states:
                self.visited_states.add(self.state)

            self.state = MY_GAME_LOGIC[ self.state]['next_state']

        return output
