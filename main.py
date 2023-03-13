from enum import Enum
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
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

playerX = 2
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
    
def check_for_player_movement(event, screen):
    # Gets the player position from a global scope
    global playerX
    global playerY

    if event.key_code == ord('a') or event.key_code == ord('A'):
        if(not collision_check(screen, DirectionVector.LEFT)): # If player is not colliding with a wall on the left
            clear_old_position(screen)
            playerX -= 1
    elif event.key_code == ord('d') or event.key_code == ord('D'):
        if(not collision_check(screen, DirectionVector.RIGHT)): # If player is not colliding with a wall on the right
            clear_old_position(screen)
            playerX += 1
    elif event.key_code == ord('w') or event.key_code == ord('W'):
        if(not collision_check(screen, DirectionVector.UP)): # If player is not colliding with a wall above him
            clear_old_position(screen)
            playerY -= 1
    elif event.key_code == ord('s') or event.key_code == ord('S'):
        if(not collision_check(screen, DirectionVector.DOWN)): # If player is not colliding with a wall below him
            clear_old_position(screen)
            playerY += 1

def draw_map(screen):
    while True:
        event = screen.get_event()
        draw_level(screen)
        
        draw_player(screen)
    

        if event is not None and isinstance(event, KeyboardEvent):
            check_for_player_movement(event, screen)
            if event.key_code == screen.KEY_ESCAPE:
                return

        screen.refresh()
        

Screen.wrapper(draw_map)