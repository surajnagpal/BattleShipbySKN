"""
Verifies attack, and checks for ship sank
Prompts user for coordinates
Runs a simple one player game loop
"""
from components import initialise_board, create_battleships, place_battleships, end_game_check, process_coordinates
from log_config import logger

def attack(coordinates, board, ships):
    """
    Performs an attack on the given coordinates of the game board.

    This function takes the coordinates of the attack, the game board, and the dictionary of ships. It checks if there is a ship at the given coordinates. If there is, it 'hits' the ship by setting the board cell to None and decrements the ship's size in the ships dictionary. If the ship's size reaches zero, it prints a message that the ship has been sunk. If there is no ship at the given coordinates, it returns False.

    Parameters:
    coordinates: Tuple of x and y coordinates of the attack.
    board: 2D list representing the game board.
    ships: Dictionary representing the ships. The keys are the ship names and the values are the ship sizes.

    Returns:
    True if the attack was a hit, False if the attack was a miss or if the coordinates were invalid or not integers.

    Raises:
    IndexError: If the coordinates are outside the range of the board.
    ValueError: If the coordinates are not integers.
    """
    try:
        x, y = coordinates
        x = int(x)  # Convert the x-coordinate to an integer
        y = int(y)  # Convert the y-coordinate to an integer
        # Check if there is a ship at the given coordinates
        if board[x][y] is not None:
            ship_name = board[x][y]  # Get the name of the ship
            board[x][y] = None  # 'Hit' the ship by setting the board cell to None
            ships[ship_name] = ships[ship_name] - 1  # Decrement the ship's size
            # If the ship's size reaches zero, print a message that the ship has been sunk
            if ships[ship_name] == 0:
                print(f"You have sunk the {ship_name}!")
                logger.info("You have sunk the %s!", {ship_name})
            return True  # The attack was a hit
        else:
            return False  # The attack was a miss
    except IndexError:
        print("Invalid coordinates. Please try again.")
        logger.error("Invalid coordinates. Please try again.")
        return False
    except ValueError:
        print("Coordinates must be integers. Please try again.")
        logger.error("Coordinates must be integers. Please try again.")
        return False

def cli_coordinates_input():
    """
    This function prompts the user to input coordinates for the game and validates if the are integers and fit on the board.

    It doesn't take any parameters.

    Returns:
    tuple: A tuple containing the x and y coordinates input by the user.
    """
    while True:
        x = input("It's your turn!, Enter the row you want to attack: ")
        y = input("what column? ;) : ")
        #Check if the inputs are digits
        if x.isdigit() and y.isdigit():
            x = int(x)
            y = int(y)
            if x < 0 or y < 0:
                # Raise an error if the inputs are negative
                logger.error("Invalid coordinates")
                continue
            logger.info("Coordinates entered %s:", ({x}, {y}))
            #Return the inputs as a tuple
            return (x, y)
        else:
            print("Coordinates entered are not integers, please try again")
            logger.error("Coordinates entered are not integers, please try again")
               
def simple_game_loop():
    """
    This function runs a simple game loop for a battleship game.

    Set's up components and runs a simple game with a simple algorithm.

    The function doesn't return anything.
    """
    #Start the game with a welcome message.
    player_name = input("Welcome To Suraj's Battleship Game, Enter your name: ")
    logger.info("Player name entered")
    #Initialising the board, the ships and placing the ships using the default settings to create the game components.
    sizeboard = int(input(f"{player_name} please enter the size of the board: "))
    logger.info("Board size entered")
    player_gameboard = initialise_board(sizeboard)
    player_battleships = create_battleships(filename="battleships.txt")
    place_battleships(player_gameboard, player_battleships)
    attacked_coordinates = []
    #Looping until all battleships have been sunken.
    while not end_game_check(player_battleships):
    #Prompting the user to input coordinates of their attack through the cli_coordinates_input().
        coordinates = cli_coordinates_input()
    #validating the coordinates through the process_coordinates() function.
        while not process_coordinates(coordinates, sizeboard, attacked_coordinates):
            logger.error("Invalid coordinates entered. Please enter new coordinates.")
            print("Please enter new coordinates.")
            coordinates = cli_coordinates_input()
    #Attack on the single board created above & Printing a hit or miss message to the user each time.
        players_attack = attack(coordinates, player_gameboard, player_battleships) 
        if players_attack:
            logger.info("player hit")
            print("That was a hit, well done!")
        else:
            logger.info("player miss")
            print("That was a miss, let's try again!")
    #Printing a message to the user when game's over.
    logger.info("sank all the battleships!")
    print("Congratulations Game Over!, you sank all the battleships!")

if __name__ == "__main__":
    simple_game_loop()

