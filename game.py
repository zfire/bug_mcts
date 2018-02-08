import hex

class Board(object):
    moveCache = {}
    def __init__(self, *args, **kwargs):
        pass

    def starting_state(self):
        return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1)

    def display(self, state, action):
        out = '  '
        for i in xrange(18,-1,-1):
            if i in [15,11,6,2]:
                out += "\n"
                if i in [15,6]:
                    out += ' '
                if i == 2:
                    out += '  '
            if state[i] == -1:
                out += 'X '
            elif state[i] == 1:
                out += 'O '
            else:
                out += '. '
        return out

    def pack_state(self, data):
        return data

    def unpack_state(self, state):
        return state

    def pack_action(self, notation):
        return hex.cordToI3[notation]

    def unpack_action(self, action):
        return str(action)

    def is_legal(self, history, action):
        state = history[-1]
        player = state.pop()
        possible_moves = hex.get_possible_moves(state,player)
        return action in possible_moves

    def legal_actions(self, history):
        state = list(history[-1])
        statecopy = tuple(state)
        if statecopy in self.moveCache:
            return self.moveCache[statecopy]
        player = state.pop()
        moves = hex.get_possible_moves(state,player)
        self.moveCache[statecopy] = moves
        return moves
        

    def next_state(self, state, action):
        board = list(state)
        player = board.pop()
        actions = action.split(';')
    	hex.place(board,actions[0],player)
    	actions.pop(0)
    	while len(actions) > 0:
    		a = actions.pop()
    		bugs = hex.get_bugs(board)
    		hex.bug_eat(board,bugs,player)
    		hex.bug_grow(board,a,player)
        return tuple(board) + (-player,)
		

    def previous_player(self, state):
        return -state[-1]

    def current_player(self, state):
        return state[-1]

    def winner(self, history):
        possible_moves = self.legal_actions(history)
        if len(possible_moves) == 0:
            return history[-1][-1]
        return 0

    def is_ended(self, history):
        return bool(self.winner(history))

    def win_values(self, history):
        winner = self.winner(history)
        if not winner:
            return

        return {winner: 1, -winner: 0}

    points_values = win_values

    def winner_message(self, winner):
        if winner == -1:
            win = 'X'
        elif winner == 1:
            win = 'O'
        return "Winner: Player {0}.".format(win)