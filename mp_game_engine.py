"""
This module contains the game engine for a multiplayer Battleship game. 
It includes functions to initialize the game board, create and place battleships, 
process player input, and handle the game logic for player and AI attacks. It also 
includes a function to generate random attack coordinates for the AI.
"""
import random
from log_config import logger
from components import initialise_board, create_battleships, place_battleships, process_coordinates, end_game_check
from game_engine import attack, cli_coordinates_input

players = {}
def generate_attack(boardsize, previous_coordinates):
    """
    Generates new coordinates for the AI's attack that have not been attacked before.

    Parameters:
    boardsize (int): The size of the board.
    previous_coordinates (list): A list of coordinates that have already been attacked.

    Returns: a tuple of coordinates for the AI's attack.
    """
    if not isinstance(previous_coordinates, list):
        logger.error("previous_coordinates must be a list")
    while True:
        # Generate random x and y coordinates within the board size
        xcord = random.randint(0, boardsize - 1)
        ycord = random.randint(0, boardsize - 1)
        coordinates = (xcord, ycord)
        # Check if the generated coordinates have not been attacked before and are within the board size
        if coordinates not in previous_coordinates and xcord < boardsize and ycord < boardsize:
            # Add the coordinates to the list of attacked coordinates
            previous_coordinates.append(coordinates)
            logger.info('Generated new attack coordinates: %s', coordinates)
            # Return the coordinates
            return coordinates

def ai_opponent_game_loop():
    """
    This function runs the main game loop for a battleship game against an AI opponent.

    The function first initializes the game boards and ships for both the player and the AI. 
    The player's ships are placed according to a custom algorithm, while the AI's ships are placed randomly.

    The game then enters a loop where the player and the AI take turns attacking each other's ships. 
    The player inputs their attack coordinates, and the AI generates its attack coordinates randomly. 
    If an attack hits a ship, the corresponding cell on the game board is marked with an 'X'. 
    If an attack misses, the cell is marked with an 'O'. 
    The game continues until all ships of a player are destroyed.

    After each turn, the function prints the current state of the player's game board. 
    When the game ends, the function prints a message indicating whether the player won or lost.

    Parameters:
    None

    Returns:
    None
    """
    #arrays to store the coordinates that have already been attacked by the player and the AI.
    try:
        player1_coordinates_attempts = []
        ai_coordinates_attempts = []
    #welcome message as per requirement but asking for name as a extra bit.
        player1 = input("Welcome to Suraj's Battleship Game, please enter your name: ")
    #Prompy for the board size
        sizeboard = int(input(f"Hello {player1}, enter the size of the board: "))
    except ValueError as e:
        logger.error('Invalid input: %s', e)
        return

    try:
    #Initialising the board and the boats for the Player(Client) and placing them using placement.json specifications.
        player1_gameboard = initialise_board(sizeboard)
        logger.info('player board initialised')
        player1_ships = create_battleships()
        logger.info('player ships created')
        place_battleships(player1_gameboard, player1_ships, algorithm='custom')
        logger.info('player ships placed')
    #Initialising the board and the boats for the AI and placing them randomly.
        ai_gameboard = initialise_board(sizeboard)
        logger.info('AI board initialised')
        ai_ships = create_battleships()
        logger.info('AI ships created')
        place_battleships(ai_gameboard, ai_ships, algorithm='random')
        logger.info('AI ships placed')
    #Initialising both players in the dictionary created above 
        players[player1] =  {"board": player1_gameboard,  "battleships": player1_ships}
        logger.info('player added to players dictionary')
        players["AI"] = {"board": ai_gameboard, "battleships": ai_ships}
        logger.info('AI added to players dictionary')
    except ValueError as ve:
        logger.error('ValueError occurred: %s', ve)
        return
    except TypeError as te:
        logger.error('TypeError occurred: %s', te)
        return
    #Looping until one of the player has no ships left.
    while end_game_check(player1_ships) is False and end_game_check(ai_ships) is False:
    #Player 1's turn, fetching the coordinates using cli_coordinates_input() & checking validity through process_coordinates().
        player1_coordinates = cli_coordinates_input()
        logger.info('player1 coordinates input')
        while process_coordinates(player1_coordinates, sizeboard, player1_coordinates_attempts) is False:
            print("Please enter new coordinates.")
            player1_coordinates = cli_coordinates_input()
        player1_attack = attack(player1_coordinates, ai_gameboard, ai_ships)
    #If the attack is true, the player has hit a ship, if not, the player has missed.
        if player1_attack is True:
            print("That was a hit, well done!")
            logger.info('player hit')
        else:
            print("That was a miss, let's try again!")
            logger.info('player miss')  
    #Ai's turn, generating and checking the coordinates for the attack using generate_attack_ai().
        ai_attack_cords = generate_attack(sizeboard, ai_coordinates_attempts)
        x, y = ai_attack_cords
        #To return the ascii representation of the board, after every AI attack.
        while player1_gameboard[x][y] == ' [O] ' or player1_gameboard[x][y] == ' [X] ':
    #If the generated coordinates have already been attacked, generate new ones
            ai_attack_cords = generate_attack(sizeboard, ai_coordinates_attempts)
            x, y = ai_attack_cords
        ai_attack = attack(ai_attack_cords, player1_gameboard, player1_ships)
    #If the attack is true, the AI has hit a ship, if not, the AI has missed and prints the ascii representation on the playerboard acccordigly.
        if ai_attack is True:
            player1_gameboard[x][y] = ' [X] '
            logger.info('AI hit')
            print("Hit, Guess what? i can see where the ships are :)")
        else:
            player1_gameboard[x][y]= ' [O] '
            logger.info('AI miss')
            print("and missed, trust me just going easy on you!")
    #Joining the list of lists to print the ascii representation of the board.
        representation = '\n'.join(['  '.join('  ' if cell is None else cell for cell in row) for row in player1_gameboard])
        print(representation)
    #Checking if the game is over and printing the appropriate message.
    if end_game_check(player1_ships):
        logger.info('player1 lost')
        print("Game Over! Try again.")
    else:
        logger.info('player1 won')
        print(f"Congratulations {player1}! You beat AI, you smart you!.")


if __name__ == "__main__":
    ai_opponent_game_loop()





    
