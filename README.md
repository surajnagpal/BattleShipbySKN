READ-ME FIle:

game can be run through main.py, by importing 
from flask import Flask, render_template, request, jsonify
from components import initialise_board, create_battleships, place_battleships, end_game_check
from game_engine import attack
from mp_game_engine import generate_attack
from log_config import logger

User will be directed to 'http://127.0.0.1:5000/'  >>>  modify URL  >>>  to 'http://127.0.0.1:5000/placement'


All the other functions are basics as decribed on ELE except 'diagonal' in Components.py (Added For Difficulty). It takes the same parameters and it can easily be tested by:
 (-) In main.py (line 131) replace 'custom' with 'diagonal' - and that should work effectively. (This will affect the front end AI Placement)
 (-) In mp_game_engine.py replace (line 85) 'custom' with 'diagonal'. (This will work in with Game in TERMINAL)


Extra functionality:-

end_game_check checks for end of the game, is supposed to be imported as functions use it to verify the end of the game.
empty_check - verifies places around a target are empty according to the ship size, so it can be placed.
empty_check_diagonal - verifies places leftwards and rightwards of target are empty according to the ship size, so it can be placed.
Module named 'log_config.py' is for logging of the program. (Terminal based)

