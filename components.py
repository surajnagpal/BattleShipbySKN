"""
contains initilise board, place battleships and create battleships functions
componenets for game functionality
"""
import json
import random
from log_config import logger

def initialise_board(board_size=10):
    """
    Takes an integer (boardsize) as argument and returns a 2D list with None values.
    """
    if isinstance(board_size, int) is False or board_size <= 0:
        logger.error('ValueError: boardsize must be a positive integer')
        raise ValueError("boardsize must be a positive integer")
    
    #The initial board state should be empty so the list will full of None values. 
    one_place = [None]
    board = [one_place * board_size for x in range(board_size)]
    return board

#takes optional argument, filename, which has a default value “battleships.txt”
def create_battleships(filename="battleships.txt"):
    """
    Takes a filename and returns a dictionary of battleship_names in key and their ship_sizes in value.
    """
    battleship_dictionary = {}
    try:
        #'utf-8'usual method used for encoding, just added to satisfy pylint
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                #stripping from ':' for key and value
                ship_name, ship_size = line.strip().split(':')
                battleship_dictionary[ship_name] = int(ship_size)
    #Handle basic file exceptions
    except FileNotFoundError:
        logger.error('File not found: %s', filename)
        print(f"File not found: {filename}")
    except IOError:
        logger.error('Could not read file: %s', filename)
        print(f"Could not read file: {filename}")
    except ValueError:
        logger.error("Could not convert data to an integer.")
        print("Could not convert data to an integer.")
    #Return the dictionary of battleships
    return battleship_dictionary

class PlacementError(Exception):
    """Exception raised when not all ships could be placed on the board."""
class CoordinatesOutOfRange(Exception):
    """Exception raised when coordinates are out of range."""

def place_battleships(board, ships, algorithm='simple'):
    """
    Places battleships on the board according to the specified algorithm.

    Parameters:
    board (list): A 2D list representing the game board.
    ships (dict): A dictionary where keys are ship names and values are their sizes.
    algorithm (str, optional): The algorithm to use for placing ships. Options are 'simple', 'random', 'custom', and 'diagonal'. Defaults to 'simple'.

    Returns:
    list: The updated game board with ships placed.

    Raises:
    Exception: If not all ships could be placed on the board in 'simple' mode.
    ValueError: If an invalid algorithm is entered.

    Note:
    In 'simple' mode, function places each battleship horizontally on a new rows starting from (0,0).
    In 'random' mode, ships are placed randomly either horizontally or vertically.
    In 'custom' mode,  battleships are placed according to a placement configuration file, placement.json.
    In 'diagonal' mode, ships are placed diagonally either leftwards or rightwards and this is done randomly.
    """
    if algorithm == 'simple':
        ship_names = list(ships.keys())
        ship_sizes = list(ships.values())
        x = 0
        #looping to check if all the ships were be placed on the board or not
        all_ships_placed = True
        while x < len(ship_names):
            #same thing regardless but just for myself to differentiate between the two. len(board) is (h) & len(board[0]) is (v)
            if x >= len(board) or ship_sizes[x] > len(board[0]):
                logger.error("%s could not be placed, try increasing the size of the board", ship_names[x])
                print(f"{ship_names[x]} could not be placed, try increasing the size of the board")
                all_ships_placed = False
                break
            #if the ship can be placed, then place it on the board
            for y in range(ship_sizes[x]):
                board[x][y] = ship_names[x]
            x = x + 1
            #if not all placed, then raise exception
        if all_ships_placed is False:
            logger.error("Not all ships could be placed on the board")
            raise PlacementError("Not all ships could be placed on the board")
        #Return the updated board
        logger.info('Battleships placed successfully')
        return board
        
    elif algorithm == 'random':
        logger.info('Placing battleships on the board using random algorithm')
        #lengths for the board
        horizontal_len = len(board[0])
        vertical_len = len(board)
        #iterating ships dictionary to extract the ship_name and ship_size and allocate them on the board
        #ship_name being the key and ship_size beinf the value
        for ship_name, ship_size in ships.items():
            #ship_name being the key and ship_size beinf the value
            ship_length = int(ship_size)
            placed = False
            #Keep trying to place the ship until it is successfully placed
            while not placed:
                #Randomly choosing the orientation of the ship
                orientation = random.choice(['h', 'v'])
                if orientation == 'h':
                    #Random Coordinates for the ship to be placed at.
                    x = random.randint(0, horizontal_len - ship_length)  
                    y = random.randint(0, vertical_len - 1) 
                    #Checking if the position is empty for the ship to be placed through an additional function
                    if empty_check(board, y, x, ship_length, orientation): 
                        #If it is, place the ship on the board
                        for i in range(ship_length):
                            board[y][x+i] = ship_name 
                        placed = True
                else:
                    x = random.randint(0, horizontal_len - 1) 
                    y = random.randint(0, vertical_len - ship_length)  
                    if empty_check(board, y, x, ship_length, orientation):  
                        for i in range(ship_length):
                            board[y+i][x] = ship_name  
                        placed = True
        #If a ship could not be placed, raise an exception
        if placed is False:
            logger.error("Not all ships were placed")
            raise PlacementError("Not all ships could be placed on the board")
        #Return the updated board
        logger.info('Battleships placed successfully')
        return board
    
    elif algorithm == 'custom':
        try:
            #opening the placement.json file and loading it into a dictionary
            with open('placement.json', 'r', encoding='utf-8') as f:
                placements = json.load(f)
        except FileNotFoundError:
            print("File not found")
            return
        except json.JSONDecodeError:
            logger.error("Could not decode JSON file")
            print("Could not decode JSON file: placement.json")
            return
        #Loop through each item in the placements dictionary
        for key, place_array in placements.items():
            try:
                #Extract the x and y coordinates and the orientation from the 'value' of the dictionary
                coordinate_x = int(place_array[0])
                coordinate_y = int(place_array[1])
                orientation = place_array[2]
            except(KeyError, TypeError):
                logger.error("Invalid data in placements")
                print("Invalid data in placements for ship: {key}")
                continue
            #The key is the ship name
            ship_name = key
            #Check if the coordinates are within the board size limit
            if coordinate_x > len(board) or coordinate_y > len(board[0]):
                logger.error("Function failed as the coordinates are not within the board size limit")
                raise CoordinatesOutOfRange("coordinates are not within the board size")
            #If the ship name is in the ships dictionary, fetch it's size
            if ship_name in ships:
                ship_size = ships[ship_name]
            #If the orientation is horizontal
            if orientation in {'h'}:
                #Loop through the ship size & check if the ship fits within the board vertically
                for i in range(ship_size):
                    if coordinate_y + i >= len(board[0]):
                        logger.error("Function failed as the ship does not fit within the board vertically")
                        raise PlacementError("Ship could not be placed")
                    #Place the ship on the board
                    board[coordinate_x][coordinate_y + i] = key
            else:
                #Check if the ship fits within the board horizontally
                for i in range(ship_size):
                    if coordinate_x + i >= len(board):
                        logger.error("Functions failed as the ship does not fit within the board horizontally")
                        raise PlacementError("Ship could not be placed")
                    #Place the ship on the board
                    board[coordinate_x + i][coordinate_y] = key
        #Return the updated board
        logger.info('Battleships placed successfully')
        return board

    elif algorithm == 'diagonal':
        logger.info('Placing battleships on the board using diagonal algorithm')
        #same as random, just placememt is diagonal
        #Get the horizontal and vertical lengths of the board
        horizontal_len = len(board)
        vertical_len   = len(board[0])
        #Loop through each ship in the ships dictionary
        for ship_name, ship_size in ships.items():
            placed = False
            #Keep trying to place the ship until it is successfully placed
            while placed is False:
                logger.error("All the battleship_names could not be placed on the board")
                orientation = random.choice(['left', 'right'])
                if orientation == 'left': #placing the ships diagonally but leftwards
                    x = random.randint(0, horizontal_len - ship_size)
                    y = random.randint(0, vertical_len - ship_size)
                    #Check if the chosen position is empty
                    if empty_check_diagonal(board, x, y, ship_size, orientation) is True:
                        for i in range(ship_size):
                            #If it is, place the ship on the board
                            board[x+i][y+i] = ship_name
                        placed = True
                else:  #placing the ships diagonally but rightwards
                    x = random.randint(0, horizontal_len - ship_size)
                    y = random.randint(ship_size - 1, vertical_len - 1)
                    #Check if the chosen position is empty
                    if empty_check_diagonal(board, x, y, ship_size, orientation) is True:
                        for i in range(ship_size):
                            #If it is, place the ship on the board
                            board[x+i][y-i] = ship_name
                        placed = True
            #If a ship could not be placed, return an error message.            
            if placed is False:
                raise PlacementError("Not all ships could be placed on the board")
        # Return the updated board
        logger.info('Battleships placed successfully')
        return board
    else:
        #If an invalid algorithm is entered, raise a ValueError
        logger.error("Invalid algorithm entered, please enter 'simple', 'random' or 'custom'")
        raise ValueError("Invalid algorithm entered, please enter 'simple', 'random' or 'custom'")

# Extra functions for added functionality of the program have been defined below.
# These are not part of the assignment but  are used along all the modules.

def empty_check(board, x, y, ship_size, orientation):
    """
    Takes a board, set of coordinates, ship_size and orientation to
    checks if the position at/around the coordinate is empty for the ship to be placed RANDOMLY 
    """
    x = int(x)
    y = int(y)
    #looks according to vertix being with row or column, hence orientation
    if orientation.lower() in ['h', 'horizontal']:
        if y + ship_size > len(board[0]): 
            return False
        for i in range(ship_size):
            #checks if the position is empty for the entire length of the ship
            if board[x][y + i] is not None:
                return False
    else: #Vertical here. 
        if x + ship_size > len(board): 
            return False
        for i in range(ship_size):
            if board[x + i][y] is not None:
                return False
    #returns true if the position is empty for the ship to be placed.
    return True

def empty_check_diagonal(board, x, y, ship_size, orientation):
    """
    Takes a board, set of coordinates, ship_size and orientation to
    checks if the position at/around the coordinate is empty for the ship to be placed DIAGONALLY
    """
    if orientation == 'left':
        if x + ship_size > len(board) or y + ship_size > len(board[0]):
            return False
        for i in range(ship_size):
            if board[x+i][y+i] is not None:
                return False
    else:  # placing the ships diagonally but rightwards
        if x + ship_size > len(board) or y - ship_size < 0:
            return False
        for i in range(ship_size):
            if board[x+i][y-i] is not None:
                return False
    return True

def end_game_check(ships):
    """
    Checks if all ships have been sunk to end the game.

    Parameters:
    ships (dict): A dictionary where the keys are the ship names and the values are the ship sizes.

    Returns:
    bool: True if all ships have been sunk or ship_sizze == 0, False if not.
    """
    # Iterate over ships of dictionary in argument
    for ship_name, ship_size in ships.items():
        # If a ship has not been sunk (i.e., its size is not 0), the game is not over
        if ship_size != 0:
            return False
    # If all ships have been sunk, the game is over
    return True

def process_coordinates(coordinates, sizeboard, previous_coordinates):
    """
    Process the coordinates provided by the player.
    
    Parameters:
    coordinates (tuple): The coordinates processed through cli_coordinates_input().
    sizeboard (int): The size of the board.
    previous_coordinates (list): The list of previous coordinates already attacked by the player.
    
    Returns:
    bool: True if the coordinates are valid, False if not.
    """
    #Checks if the coordinates are within the board size
    if coordinates[0] > sizeboard - 1 or coordinates[1] > sizeboard - 1:
        print("Invalid coordinates, please input that lies in the size of the ocean")
        return False
    #Checks if the coordinates have already been attacked
    elif coordinates in previous_coordinates:
        print("You have already bombed this part of the ocean, try a different location.")
        return False
    else:
    #If the coordinates are valid, add them to the list of attacked coordinates
        previous_coordinates.append(coordinates)
        return True


