"""
main entry point to our project
"""
from flask import Flask, render_template, request, jsonify
from components import initialise_board, create_battleships, place_battleships, end_game_check
from game_engine import attack
from mp_game_engine import generate_attack
from log_config import logger

app = Flask(__name__)
user_board = []
ai_board = []
ai_ships = {}
user_ships = {}
PLACEMENT = None

def custom_placement(board, ships):
    """
    Places the ships on the board according to the custom placement.

    This function iterates over the placement dictionary. 
    For each ship, it gets the coordinates, orientation, and name from the placement. 
    It checks if the ship can be placed within the board. 
    If it can, it places the ship on the board. 
    If it can't, it returns a message indicating that the ship cannot be placed.

    Parameters:
    board: 2D list representing the game board
    ships: Dictionary representing the ships. 
    The keys are the ship names and the values are the ship lengths.

    Returns:
    If a ship cannot be placed within the board, it returns a string indicating that the ship cannot be placed. 
    If all ships are placed successfully, it returns updated board.
    """
    # Iterate over the placement dictionary
    for key, place_array in PLACEMENT.items():
        # Extract the y-coordinate, x-coordinate, and orientation from the placement
        y_cord = int(place_array[0])
        x_cord = int(place_array[1])
        orientation = place_array[2]
        ship_name = key
        # Check if the ship can be placed within the board
        if x_cord > len(board) or y_cord > len(board[0]):
            logger.error(f"Ship {ship_name} does not fit on the board")
            return "does not fit"
        # Get the length of the ship
        if ship_name in ships:
            ship_length = ships[ship_name]
        if orientation in ['h']:
            # Check if the ship can be placed within the board horizontally
            for i in range(ship_length):
                if y_cord + i >= len(board[0]):
                    logger.error(f"Ship {ship_name} not within horizontal limit")
                    return "ship not within limit"
                # Place the ship on the board
                board[x_cord][y_cord + i] = key
        else: #v
            # Check if the ship can be placed within the board vertically
            for i in range(ship_length):
                if x_cord + i >= len(board):
                    logger.error(f"Ship {ship_name} not within vertical limit")
                    return "Ship not within limit"
                # Place the ship on the board
                board[x_cord + i][y_cord] = key
    # Return the board with all ships placed
    logger.info("All ships placed successfully")
    return board
            
@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    """
    Handles GET and POST requests to the '/placement' URL.

    For GET requests, it creates battleships for the user and 
    renders the 'placement.html' template with the user's ships and board size.

    For POST requests, it initializes the user's game board, 
    gets the placement from the request's JSON, places the ships on the board using the 'custom_placement' function,
    and returns a JSON response indicating that the placement was received.

    Global variables:
    user_board: 2D list representing the user's game board
    user_ships: Dictionary representing the user's battleships
    placement: Dictionary representing the placement of the user's battleships

    Returns:
    For GET requests: Rendered 'placement.html' template with the user's ships and board size.
    For POST requests: JSON response with a message indicating that the placement was received.
    """
    global user_board
    global user_ships
    global PLACEMENT
    user_ships = create_battleships()
    if request.method == 'GET':
        #return placement.html with get request
        logger.info("placement template rendered")
        return render_template('placement.html', ships = user_ships, board_size = 10)
        #ininialise board, and placing ships as per user's custom placement
    elif request.method == 'POST':
        user_board = initialise_board(10)
        logger.info("User board initialised")
        #this returns a dictionary of the placement
        PLACEMENT = request.get_json()
        #places the ships on the board
        user_board = custom_placement(user_board, user_ships)
        logger.info("User board placement received")
        return jsonify({'message': 'Received'}), 200
    return jsonify({'message': 'Invalid request method'}), 400

@app.route('/', methods=['GET'])
def root():
    """
    Handles GET requests to the root URL. 

    This function initializes the AI's game board and battleships, 
    places the battleships on the board using a set algorithm, 
    and then renders the main HTML template with the user's game board.

    Global variables:
    user_board: 2D list representing the user's game board
    ai_board: 2D list representing the AI's game board
    ai_ships: Dictionary representing the AI's battleships

    Returns:
    Rendered 'main.html' template with the user's game board.
    """
    global user_board
    global ai_board
    global ai_ships
    if request.method == 'GET':
        #initialise board, and placing ships randomly on the board
        ai_board = initialise_board(10)
        ai_ships = create_battleships()
        ai_board = place_battleships(ai_board, ai_ships, algorithm='random')
        logger.info("AI board initialised and ships placed randomly")
        #return main.html with get request
        logger.info("main template rendered")
        return render_template('main.html', player_board = user_board)
    logger.error("Invalid request method in placement_interface")
    return jsonify({'message': 'Invalid request method'}), 400

previous_coords = []  
@app.route('/attack', methods=['GET'])
def process_attack():
    """
    Handles GET requests to the '/attack' URL.

    This function processes the user's attack and the AI's counterattack. 
    It gets the coordinates of the user's attack from the request, 
    performs the attack, generates the AI's attack, performs the AI's attack, and checks if the game has ended.
    If the AI hits a ship, it appends the coordinates to the 'previous_coords' list. 
    If the game has ended, it returns a JSON response indicating who won. 
    If the user hit a ship, it returns a JSON response indicating that the user hit a ship and the coordinates of the AI's attack. 
    If the user missed, it returns a JSON response indicating that the user missed and the coordinates of the AI's attack.

    Global variables:
    user_board: 2D list representing the user's game board
    ai_board: 2D list representing the AI's game board
    ai_ships: Dictionary representing the AI's battleships
    user_ships: Dictionary representing the user's battleships
    previous_coords: List of coordinates of the AI's successful attacks

    Returns:
    JSON response with the result of the user's attack, the coordinates of the AI's attack, and possibly the result of the game.
    """
    global previous_coords
    global user_board
    global ai_board
    global ai_ships
    global user_ships
    #if request is get x & y are loaded from front end
    if request.method == 'GET':
        x = request.args.get('x')
        y = request.args.get('y')
        coordinates_on_screen = (x,y)
        logger.info("User attack coordinates received")
        #coordinates_on_screen used for user attack on AI board
        user_attack = attack(coordinates_on_screen, ai_board, ai_ships)
        length = len(user_board)
        #ai_cords generated for AI attack on user board
        ai_cords = generate_attack(length, previous_coords) 
        x2, y2 = ai_cords
        attack(ai_cords, user_board, user_ships)
        #check if game has ended
        if end_game_check(ai_ships):
            logger.info("User wins")
            return jsonify({'hit': True, 'AI_Turn': (x2,y2), 'finished': 'You win! woo woo'})
        elif end_game_check(user_ships):
            logger.info("AI wins")
            return jsonify({'hit': True, 'AI_Turn': (x2,y2), 'finished': 'AI wins, boo boo'})  
        elif user_attack is True:
            logger.info("AI hit a ship")
            return jsonify({'hit': True, 'AI_Turn': (x2,y2)})
        logger.info("AI missed")
        return jsonify({'hit': False, 'AI_Turn': (x2,y2)})
    logger.error("Invalid request method in process_attack")
    return jsonify({'message': 'Failed'}), 200

if __name__ == "__main__":
    app.template_folder = 'templates'
    app.run(debug=True)