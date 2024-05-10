def minimax_alpha_beta_search(game, state):
    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -float('inf')
        for action in game.actions(state):
            v = max(v, min_value(game.result(state, action), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v
    
    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        
        v = float('inf')
        for action in game.actions(state):
            v = min(v, max_value(game.result(state, action), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        
        return v
    
    best_score = -float('inf')
    beta = float('inf')
    best_action = None

    for action in game.actions(state):
        v = min_value(game.result(state, action), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = action
    return best_action