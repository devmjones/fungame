import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

''' Available Game Elements

Wall
Block
GrassBlock
StoneBlock
ShortTree
TallTree
Rock
Chest
DoorClosed
DoorOpen
BlueGem
GreenGem
OrangeGem
Heart
Key

'''

class Rock (GameElement):
    IMAGE = "Rock"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("Oh. You just picked up a rock... Really?! You have %d items." % (len(player.inventory)))

class Character(GameElement):
    IMAGE = "Horns"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up": 
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right": 
            return (self.x+1, self.y)
        return None

class Bluegem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! you have %d items!" % (len(player.inventory)))

class Greengem(GameElement):
    IMAGE = "GreenGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! you have %d items!" % (len(player.inventory)))

class Orangegem(GameElement):
    IMAGE = "OrangeGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! you have %d items!" % (len(player.inventory)))

class Shorttree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True   

class Dude (GameElement):
    IMAGE = "Boy" 
    SOLID = True    

    def interact(self, player):
        player.inventory.append(self)
    # if player.inventory has 3 gems, exhange for heart, say "Gems CAN buy you love!!"
    # elif player.inventory != 3 gems, loop to say "Well, we ARE living in a gem world...So...yeah...", 
    # "I ain't sayin I'm a gold digger", "If you like it you should put more gems on it"
        GAME_BOARD.draw_msg("Well, we ARE living in a gem world...So...yeah...")

class Doorclosed (GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

class Dooropen (GameElement):
    IMAGE = "DoorOpen"
    SOLID = True


def initialize():
    """Put game initialization code here"""

    # placement of rocks
    rock_positions = [
        (0, 0), 
        (6, 6),  
        (2, 3)
    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    # placement of player
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(6, 0, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This game is wicked awesome.")

    # placement of gems
    bluegem = Bluegem()
    GAME_BOARD.register(bluegem)
    GAME_BOARD.set_el(1, 0, bluegem)

    greengem = Greengem()
    GAME_BOARD.register(greengem)
    GAME_BOARD.set_el(4, 2, greengem)

    orangegem = Orangegem()
    GAME_BOARD.register(orangegem)
    GAME_BOARD.set_el(6, 3, orangegem)

    #placement of dude
    dude = Dude()
    GAME_BOARD.register(dude)
    GAME_BOARD.set_el(0, 5, dude)

    # placement of short trees
    shorttree_postions = [
    (1, 2), (1, 6), (2, 0), (2, 1), (2, 2), (3, 5), 
    (4, 1), (4, 4), (4, 5), (5, 1), (5, 2), (5, 3), 
    (5, 4), (6, 2)
    ]
    
    shorttrees = []

    for pos in shorttree_postions:
        shorttree = Shorttree()
        GAME_BOARD.register(shorttree)
        GAME_BOARD.set_el(pos[0], pos[1], shorttree)
        shorttrees.append(shorttree)

    # placement of closed door
    closeddoor = Doorclosed()
    GAME_BOARD.register(closeddoor)
    GAME_BOARD.set_el(0, 4, closeddoor)

def keyboard_handler():
    
    direction = None

    if KEYBOARD[key.UP]:
        GAME_BOARD.draw_msg("You pressed up")
        direction =  "up"
   
    elif KEYBOARD[key.DOWN]:
        GAME_BOARD.draw_msg("You pressed down")
        direction = "down"

    elif KEYBOARD[key.RIGHT]:
        GAME_BOARD.draw_msg("You pressed right")  
        direction = "right"
    
    elif KEYBOARD[key.LEFT]:
        GAME_BOARD.draw_msg("You pressed left")
        direction = "left" 

    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()
    
    if direction: 
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        #check position
        if (next_x > 6 or next_x < 0 or next_y > 6 or next_y < 0):
            # raise "IndexError": 
            GAME_BOARD.draw_msg("Stop running away!  Are you afraid of committment?")
        else:
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER)

            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)

