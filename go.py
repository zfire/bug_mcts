import mcts
import game
import gc
import sys
name = sys.argv[1]
handle = open('logs/'+name,'w')
board = game.Board()
player = mcts.UCTWins(board,time=10)
player2 = mcts.UCTWins(board,time=10)
players = {-1:player,1:player2}
state = board.starting_state()
while board.is_ended([state]) == False:
    players[state[-1]].update(state)
    action = players[state[-1]].get_action()
    state = board.next_state(state,action)
    handle.write(board.display(state,'')+"\n")
    handle.write(action+"\n")
    handle.flush()
handle.write(board.winner_message(board.winner([state])))
handle.flush()
handle.close()