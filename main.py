from enum import Enum
from asciimatics.screen import Screen
import asyncio

class BlockType(Enum):
    HASHTAG = "#"
    CIRCLE = "O"
    EMPTY = ""

class DirectionVector(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

level_1 = [[0, 0, BlockType.HASHTAG], [1, 0, BlockType.CIRCLE], [2, 0, BlockType.EMPTY], [3, 0, BlockType.HASHTAG]] # A 2d array consisting of [x value, y value, BlockType]

playerX = 1
playerY = 1

def draw_level(screen):
    for i in level_1: 
            screen.print_at(i[2].value, # Enum BlockType, which value represents characters, e.g.: '#' or 'O'
                            i[0], i[1], # Represents the x and y value of a currently selected 2d array (in order)
                            colour=screen.COLOUR_WHITE,
                            bg=screen.COLOUR_BLACK)
            
def clear_old_position(screen):
    # Gets the player position from a global scope
    global playerX
    global playerY

    # Saves the old position
    oldX = playerX
    oldY = playerY

    # Clears the space at the old position
    screen.print_at(" ", oldX, oldY, colour=screen.COLOUR_BLACK, bg=screen.COLOUR_BLACK)

def collision_check(screen, vector: DirectionVector):
    match vector:
        case DirectionVector.LEFT:
            if(chr(screen.get_from(playerX - 1, playerY)[0]) in BlockType._value2member_map_):
                return True
            pass
        case DirectionVector.RIGHT:
            if(chr(screen.get_from(playerX + 1, playerY)[0]) in BlockType._value2member_map_):
                return True
            pass
        case DirectionVector.UP:
            if(chr(screen.get_from(playerX, playerY - 1)[0]) in BlockType._value2member_map_):
                return True
            pass
        case DirectionVector.DOWN:
            if(chr(screen.get_from(playerX, playerY + 1)[0]) in BlockType._value2member_map_):
                return True
            pass
    return False


def draw_player(screen):
    # Gets the player position from a global scope
    global playerX
    global playerY  
    screen.print_at("P",
                    playerX, playerY,
                    colour=screen.COLOUR_YELLOW,
                    bg=screen.COLOUR_BLACK)
    
def check_for_player_movement(keyboardInput, screen):
    # Gets the player position from a global scope
    global playerX
    global playerY


    if keyboardInput in (ord('A'), ord('a')):
        if(not collision_check(screen, DirectionVector.LEFT)):
            clear_old_position(screen)
            playerX -= 1
    elif keyboardInput in (ord('D'), ord('d')):
        if(not collision_check(screen, DirectionVector.RIGHT)):
            clear_old_position(screen)
            playerX += 1
    elif keyboardInput in (ord('W'), ord('w')):
        if(not collision_check(screen, DirectionVector.UP)):
            clear_old_position(screen)
            playerY -= 1
    elif keyboardInput in (ord('S'), ord('s')):
        if(not collision_check(screen, DirectionVector.DOWN)):
            clear_old_position(screen)
            playerY += 1

def draw_map(screen):
    while True:
        keyboardInput = screen.get_key()
        draw_level(screen)
        check_for_player_movement(keyboardInput, screen)
        draw_player(screen)
        
        if keyboardInput == screen.KEY_ESCAPE: # Quits the application if pressed
            return

        screen.refresh()
        

Screen.wrapper(draw_map)