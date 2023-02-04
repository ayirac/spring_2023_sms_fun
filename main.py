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

if __name__ == "__main__":
    main()