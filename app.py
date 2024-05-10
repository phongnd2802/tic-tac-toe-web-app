from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from game import TicTacToe, GameState
from ai import minimax_alpha_beta_search


app = Flask(__name__)
game = TicTacToe()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/move', methods=['POST'])
@cross_origin()
def make_move():
    data = request.get_json()
    player = data['player']
    utility = int(data['utility'])
    board = dict(data['board'])
    format_board = {}
    for key in board.keys():
        x, y = map(int, key.split(','))
        format_board[(x, y)] = board[key]
    moves = list(data['moves'])
    format_moves = []
    for move in moves:
        move = tuple(move)
        format_moves.append(move)

    state = GameState(to_move=player, utility=utility, board=format_board, moves=format_moves)
    best_move = minimax_alpha_beta_search(game, state)
    state = game.result(state, best_move)
    result = None
    if game.terminal_test(state):
        result = game.utility(state, game.to_move(game.initial))
    return jsonify({'move': best_move,
                    'utility': state.utility, 
                    'moves': state.moves,
                    'result': result,
                    })
if __name__ == '__main__':
    app.run(debug=True)
