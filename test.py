from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleTests(TestCase):

    # tests for every view function / feature!

    def test_root(self):
        """Test home page rendering"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>BOGGLE</h1>', html)

    def test_root_form(self):
        """Test home page form get request."""
        with app.test_client() as client:
            response = client.get('/play', query_string={'board-size': 6})
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form id="guess-form">', html)
            self.assertEqual(session['game_count'], 0)

    def test_guess_form(self):
        """Test the guess form in the game play page."""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['B', 'A', 'D'], ['G', 'C', 'X'], ['H', 'I', 'J']]
            
            # Send a word that exists
            response = client.post('/play', json={'game': 'on', 'guess': 'bad'})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'result': 'ok'})

            # Send a word that does not exist
            response = client.post('/play', json={'game': 'on', 'guess': 'bep'})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'result': 'not-a-word'})

            # Send a word that is not on the board
            response = client.post('/play', json={'game': 'on', 'guess': 'bat'})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'result': 'not-on-board'})

    def test_end_game(self):
        """Test the end of game logic"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['best_score'] = 5
                change_session['game_count'] = 99

            response = client.post('/play', json={'game': 'off', 'score': 10})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'status': 'ok'})
            self.assertEqual(session['game_count'], 100)
            self.assertEqual(session['best_score'], 10)                
