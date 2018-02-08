import mcts
import game
import sys
import random
import re
import hex
time = 15
verbose = False
playouts = 0
if len(sys.argv) > 1:
    time = sys.argv[1]
if len(sys.argv) > 2:
    playouts = sys.argv[2]
if len(sys.argv) > 3:
    if (sys.argv[3]) == 'v':
        verbose = True
board = game.Board()
player2 = mcts.UCTWins(board,time=time,verbose=verbose,playouts=playouts)
bot = random.choice([-1,1])
state = board.starting_state()
while board.is_ended([state]) == False:
    if state[-1] == bot:
        player2.update(state)
        action = player2.get_action()
        print(action)
        state = board.next_state(state,action)
        print(board.display(state,''))
    else:
        legal_moves = board.legal_actions([state])
        inp = raw_input('Enter move:')
        inp = inp.strip()
        action = None
        if '(' in inp:
            inp = inp
        elif len(re.findall('[a-zA-Z]',inp)) > 0:
            split = inp.split(';')
            converted = []
            for s in split:
                converted.append(str(hex.iToCord3[hex.axialToI3[s]]))
            inp = ';'.join(converted)
        else:
            split = inp.split(';')
            converted = []
            for s in split:
                converted.append(str(hex.iToCord3[int(s)]))
            inp = ';'.join(converted)
        if inp in legal_moves:
            action = inp
        else:
            print('Illegal move')
        if action != None:
            state = board.next_state(state,action)
            print(board.display(state,''))

print(board.winner_message(board.winner([state])))