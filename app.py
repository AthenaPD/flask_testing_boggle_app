"""This is an simply app to make a game of boggle!"""

from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "Orion"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# global boggle_game

@app.route("/")
def home_page():
    """Show home page, where you can set up and start the game."""
    return render_template("home_page.html")

@app.route("/play")
def play_boggle():
    """Show boggle board and allow user to make guesses."""
    # Default board size is 5x5
    board_size = int(request.args['board-size']) if request.args['board-size'] else 5
    global boggle_game 
    boggle_game = Boggle(board_size)
    game_board = boggle_game.make_board()
    session['board'] = game_board
    session['game_times'] = session.get('game_times', 0)
    session['best_score'] = session.get('best_score', 0)
    return render_template("boggle_game.html", game_board=game_board)

@app.route("/play", methods=["POST"])
def check_and_respond():
    """
    Handle user's guesses:
    1. send a guess to the server and check the validity of the guess
    2. send user feedback

    At the end of the game, 
    1. check and update best score sent back by browser
    2. increment the number of played game by 1.
    """
    if request.json['game'] == "on":
        guess = request.json['guess']
        game_board = session['board']
        result = boggle_game.check_valid_word(board=game_board, word=guess)
        return jsonify(result=result)
    else:
        best_score = session.get('best_score', 0)
        total_score = request.json['score']
        session['best_score'] = total_score if total_score > best_score else best_score
        game_times = session.get('game_times', 0)
        session['game_times'] = game_times + 1
        return jsonify(status='ok')
