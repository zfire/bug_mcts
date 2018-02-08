import hex
# current_player = 1
# board3 = [1,1,-1,-1,0,-1,1,-1,1,-1,-1,1,-1,1,1,0,1,-1,-1]
board3 = [1,0,0,0,0,0,1,0,1,-1,0,1,1,0,1,0,0,1,0]
hex.place(board3,'(-1,1,0)',-1)
print(hex.display_board(board3))
bugs = hex.get_bugs(board3)
hex.bug_eat(board3,bugs,-1)
print(hex.display_board(board3))
# print(get_possible_moves(board3,1))
# place(board3,'8',0)
# place(board3,'(0,0,0)',0)
# bugs = get_bugs(board3)
# print('white:')
# print(get_possible_moves(board3,1))
# print('-------')
# print('black:')
# print(get_possible_moves(board3,-1))
# print(board3)
# bug_eat(board3,bugs,current_player)
# print(board3)