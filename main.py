from enum import Enum
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
import asyncio


# Used for storing the ASCII block type
class BlockType(Enum):
    HASHTAG = "#"
    CIRCLE = "O"
    PLAYER = "P"
    EMPTY = " "


# Used for collision checking
class DirectionVector(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

# Represents a level that is gathered by using the WHGTEditor
level_1 = [[63, 8, BlockType.HASHTAG], [71, 8, BlockType.HASHTAG], [79, 8, BlockType.HASHTAG], [75, 6, BlockType.HASHTAG], [70, 7, BlockType.HASHTAG], [61, 7, BlockType.HASHTAG], [68, 9, BlockType.HASHTAG]]

playerX = 2
playerY = 1

def print_at(screen, posX: int, posY: int, text_color = None, background_color = None, text = None):
    """
    A function that draws a pixel onto the screen.

    This is a wrapper function, that makes the code more readble in the end.
    """
    global selected_block

    if not text_color: text_color = screen.COLOUR_WHITE
    if not background_color: background_color = screen.COLOUR_BLACK
    if not text: text = selected_block.value
    elif isinstance(text, BlockType):
        text = text.value 

    screen.print_at(
        text, # Prints ending point on X-Axis
        posX, posY,
        colour=text_color,
        bg=background_color)
    

def format_level(list_object, direction):
    list_object = str(list_object)
    if direction == 0:
        list_object = list_object.replace("<BlockType.HASHTAG: '#'>", "BlockType.HASHTAG")
        list_object = list_object.replace("<BlockType.CIRCLE: 'O'>", "BlockType.CIRCLE")
        list_object = list_object.replace("<BlockType.PLAYER: 'P'>", "BlockType.PLAYER")
        return list_object
    elif direction == 1:
        list_object = list_object.replace("BlockType.HASHTAG", "<BlockType.HASHTAG: '#'>")
        list_object = list_object.replace("BlockType.CIRCLE", "<BlockType.CIRCLE: 'O'>")
        list_object = list_object.replace("BlockType.PLAYER", "<BlockType.PLAYER: 'P'>")
        return list_object
    
    

def assign_new_array(string: str):
    """
    Transforms the given string into a list of 3D arrays.
    """

    new_array = []
    for i in range(0, len(string), 3):
        temp_array = string[i:i+3]
        new_array.append(temp_array)
    return new_array

def load_level(screen):
    """
    Loads the level.txt file inside of the runtime directory and then
    firstly transforms the string and then passes it to assing_new_array().
    After that it loops through the retrieved list and places a BlockType for every entry.
    """

    global level

    global playerX
    global playerY
    
    file = open("level.txt", "r")

    if file.read() == "":
        return
    file.seek(0) # Making sure that we are not reaching EOF

    # This transforms the save into a for the algorithm readable format.
    no_brackets = file.read().replace("[", "").replace("]", "").split(", ")

    for i in assign_new_array(no_brackets):
        # We are using __members__[] because assign_new_array returns e.g.: `BlockType.HASHTAG` as a string
        # This then has to be transformed into a BlockType. To do this we first split the string at the period.
        # Then we take the second half of the string: `HASHTAG` and then assign that to a BlockType value.
        if BlockType.__members__[str(i[2]).split(".")[1]] == BlockType.PLAYER:
            playerX = int(i[0])
            playerY = int(i[1])
        else:
            print_at(screen, int(i[0]), int(i[1]), text=BlockType.__members__[str(i[2]).split(".")[1]])


def clear_old_position(screen):
    # Gets the player position from a global scope
    global playerX
    global playerY

    # Saves the old position
    oldX = playerX
    oldY = playerY

    # Clears the space at the old position
    print_at(screen, oldX, oldY, text=BlockType.EMPTY)

def collision_check(screen, vector: DirectionVector):
    match vector:
        case DirectionVector.LEFT:
            block = chr(screen.get_from(playerX - 1, playerY)[0])
            if(block in BlockType._value2member_map_ and block != BlockType.EMPTY.value):
                return True
            pass
        case DirectionVector.RIGHT:
            block = chr(screen.get_from(playerX + 1, playerY)[0])
            if(block in BlockType._value2member_map_ and block != BlockType.EMPTY.value):
                return True
            pass
        case DirectionVector.UP:
            block = chr(screen.get_from(playerX, playerY - 1)[0])
            if(block in BlockType._value2member_map_ and block != BlockType.EMPTY.value):
                return True
            pass
        case DirectionVector.DOWN:
            block = chr(screen.get_from(playerX, playerY + 1)[0])
            if(block in BlockType._value2member_map_ and block != BlockType.EMPTY.value):
                return True
            pass
    return False


def draw_player(screen):
    # Gets the player position from a global scope
    global playerX
    global playerY  

    print_at(screen, playerX, playerY, text_color=screen.COLOUR_YELLOW, background_color=screen.COLOUR_BLACK, text=BlockType.PLAYER)
    
    
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

    load_level(screen)

    while True:
        event = screen.get_event()
        
        draw_player(screen)
    

        if event is not None and isinstance(event, KeyboardEvent):
            check_for_player_movement(event, screen)
            if event.key_code == screen.KEY_ESCAPE:
                return

        screen.refresh()
        

Screen.wrapper(draw_map)