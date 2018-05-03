# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify
import PlayerAI
import Grid

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from anywhere"

@app.route('/move', methods=['POST'])
def move():
    Player = PlayerAI.PlayerAI()
    board = request.get_json()['board']
    return jsonify(Player.getMove(Grid.Grid(len(board), board)))

if __name__ == '__main__':
    app.run()

