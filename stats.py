from __future__ import division
import os
import sys
import hex

wins = {'O':0,'X':0}
movesCount = 0
games = 0
minMoves = sys.maxint
minMovesGame = None
maxMoves = 0
maxMovesGame = None
largestBug = 0
largestBugGame = None
for file in os.listdir('logs/'):
    f = open('logs/'+file)
    lines = f.readlines()
    if 'X' in lines[-1]:
        wins['X'] += 1
    elif 'O' in lines[-1]:
        wins['O'] += 1
    movesThisGame = 0
    board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    currentplayer = -1
    for line in lines:
        if '(' in line:
            movesCount += 1
            movesThisGame += 1
            actions = line.split(';')
            hex.place(board,actions[0],currentplayer)
            actions.pop(0)
            while len(actions) > 0:
                a = actions.pop()
                bugs = hex.get_bugs(board)
                for bug in bugs:
                    if len(bug['cords']) > largestBug:
                        largestBug = len(bug['cords'])
                        largestBugGame = file
                hex.bug_eat(board,bugs,currentplayer)
                hex.bug_grow(board,a,currentplayer)
            currentplayer = -currentplayer

    if movesThisGame > maxMoves:
        maxMoves = movesThisGame
        maxMovesGame = file
    if movesThisGame < minMoves:
        minMoves = movesThisGame
        minMovesGame = file
    games += 1
print('Games: '+str(games))
print('X wins: '+str(wins['X'])+' - '+str(round(wins['X']/games*100,2))+'%')
print('O wins: '+str(wins['O'])+' - '+str(round(wins['O']/games*100,2))+'%')
print('Avg moves in games: '+str(round(movesCount/games,2)))
print('Lowest number of moves in a game:'+str(minMoves)+' in game '+minMovesGame)
print('Highest number of moves in a game:'+str(maxMoves)+' in game '+maxMovesGame)
print('Largest bug size: '+str(largestBug)+' in game '+largestBugGame)