from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "Orion"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    return render_template("home_page.html")

@app.route("/play")
def play_boggle():
    game_board = boggle_game.make_board()
    session['board'] = game_board
    session['game_times'] = session.get('game_times', 0)
    session['best_score'] = session.get('best_score', 0)
    return render_template("boggle_game.html", game_board=game_board)

@app.route("/play", methods=["POST"])
def check_and_respond():
    if request.json['game'] == "on":
        guess = request.json['guess']
        game_board = session['board']
        result = boggle_game.check_valid_word(board=game_board, word=guess)
        return jsonify(result=result)
    else:
        best_score = session.get('best_score', 0)
        total_score = request.json['score']
        # import pdb
        # pdb.set_trace()
        session['best_score'] = total_score if total_score > best_score else best_score
        game_times = session.get('game_times', 0)
        session['game_times'] = game_times + 1
        return jsonify(status='ok')
