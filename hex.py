from __future__ import print_function
import re

iToCord3 = {0:(0,-2,2),1:(-1,-1,2),2:(-2,0,2),3:(1,-2,1),4:(0,-1,1),5:(-1,0,1),6:(-2,1,1),7:(2,-2,0),8:(1,-1,0),
9:(0,0,0),10:(-1,1,0),11:(-2,2,0),12:(2,-1,-1),13:(1,0,-1),14:(0,1,-1),15:(-1,2,-1),16:(2,0,-2),17:(1,1,-2),
18:(0,2,-2)}
cordToI3 = {y:x for x,y in iToCord3.iteritems()}
axialToI3 = {"A1":0,"A2":1,"A3":2,"B1":3,"B2":4,"B3":5,"B4":6,"C1":7,"C2":8,"C3":9,"C4":10,"C5":11,"D1":12,"D2":13,
"D3":14,"D4":15,"E1":16,"E2":17,"E3":18}
directions = [
    (1,-1,0),(1,0,-1),(0,1,-1),
    (-1,1,0),(-1,0,1),(0,-1,1)
]

def are_cords_adjescent(cord1,cord2):
    for d in directions:
        if (cord1[0]-d[0],cord1[1]-d[1],cord1[2]-d[2]) == cord2:
            return True
    return False

def get_bugs(board):
    possiblebugstarts = {key:val for key,val in enumerate(board)}
    bugs = []
    while len(possiblebugstarts) > 0:
        key,val = possiblebugstarts.popitem()
        if (val == 0): #hex is empty so we ignore it
            continue
        cord = iToCord3[key]
        bug = [cord]
        possiblecords = []
        for d in directions:
            cc = (cord[0]-d[0],cord[1]-d[1],cord[2]-d[2])
            if cc in cordToI3:
                possiblecords.append(cc)
        while len(possiblecords) > 0:
            c = possiblecords.pop()
            if board[cordToI3[c]] == val:
                if c not in bug:
                    bug.append(c)
                    possiblebugstarts.pop(cordToI3[c],None) #c is part of this bug, so we can remove it from possible other bugs
                for d in directions:
                    cc = (c[0]-d[0],c[1]-d[1],c[2]-d[2])
                    if cc in cordToI3 and cc not in bug:
                        possiblecords.append(cc)
        bugs.append({'player':val,'cords':bug})
    return bugs

def parse_coordinate(cord):
    if '(' in cord:
        return cordToI3[tuple(map(int, re.findall(r'-?[0-9]+', cord)))]
    elif cord.isdigit():
        return int(cord)
    else:
        return axialToI3[cord]

def place(board,action,player):
    board[parse_coordinate(action)] = player

def bug_grow(board,action,player): #same as place
    place(board,action,player)

def rotate(bug):
    for i,b in enumerate(bug):
        bug[i] = (-b[1],-b[2],-b[0])
    return bug

def move_to_zero(bug,i):
    moveX = bug[i][0]
    moveY = bug[i][1]
    moveZ = bug[i][2]
    for i,b in enumerate(bug):
        bug[i] = (b[0]-moveX,b[1]-moveY,b[2]-moveZ)
    return bug

def bug_match(a,b):
    bug1 = list(a)
    bug2 = list(b)
    bug1 = move_to_zero(bug1,0)
    for i,cc in enumerate(bug2):
        copybug = list(bug2)
        copybug = move_to_zero(copybug,i)
        for y in range(0,6):
            tuple1 = [tuple(a) for a in copybug]
            tuple2 = [tuple(a) for a in bug1]
            if set(tuple1) == set(tuple2):
                return True
            copybug = rotate(copybug)
    return False

def are_bugs_adjescent(bug1,bug2):
    for c in bug1:
        for d in directions:
            if (c[0]-d[0],c[1]-d[1],c[2]-d[2]) in bug2:
                return True
    return False

def bug_eat(board,bugs,current_player):
    current_player_bugs = []
    other_player_bugs = {}
    bug_ate = False
    i = 0
    for bug in bugs:
        if bug['player'] == current_player:
            current_player_bugs.append(bug)
        else:
            other_player_bugs[i] = bug
            i += 1
    for bug in current_player_bugs:
        for i,obug in other_player_bugs.items():
            if len(bug['cords']) == len(obug['cords']) and are_bugs_adjescent(bug['cords'],obug['cords']) and bug_match(bug['cords'],obug['cords']):
                for c in obug['cords']:
                    board[cordToI3[c]] = 0
                other_player_bugs.pop(i,None)
                bug_ate = bug
    return bug_ate

#returns grow actions if any otherwise returns the action without growing
def get_grow_actions(board,bugs,action,current_player):
    
    actions = []
    bug_who_ate = bug_eat(board,bugs,current_player)#eat if possible
    
    if bug_who_ate != False: #a bug ate from previous placement, we need to check all possible grow placements
        cords = []#possible grow placements
        for c in bug_who_ate['cords']:#for each hex in bug
            for d in directions:#in each direction
                cc = (c[0]-d[0],c[1]-d[1],c[2]-d[2])
                if cc in cordToI3 and board[cordToI3[cc]] == 0 and cc not in cords:#hex is empty and not already in list
                    cords.append(cc)
        current_bug_size = len(bug_who_ate['cords'])
        
        for c in cords:
            copyboard = list(board)#make a copy of the board
            place(copyboard,str(c),current_player)#simulate placement
            newbugs = get_bugs(copyboard)#get all bugs in new board
            our_bug = None
            for bug in newbugs:#we need to find our bug in the new bugs
                if our_bug != None:#early break
                    break
                for cc in bug['cords']:
                    if cc in bug_who_ate['cords']:#this is our bug(e.g. a cord matched)
                        our_bug = bug
                        break
            if len(our_bug['cords']) == current_bug_size+1:#our bug must have only grown by 1 in size
                #check if this grow placement will lead to further eating
                actions += get_grow_actions(copyboard,newbugs,action+';'+str(c),current_player)
    else: #this placement did not lead to an eating therefore it must be valid
        actions.append(action)

    return actions

def get_possible_moves(board,current_player):
    bugs = get_bugs(board)
    largest_our_bugs = []
    largest_bug = 0
    #find every of our bugs that are largest or tied for largest
    for bug in bugs:
        if len(bug['cords']) > largest_bug:
            largest_bug = len(bug['cords'])
            largest_our_bugs = []
        if bug['player'] == current_player and len(bug['cords']) == largest_bug:
            largest_our_bugs.append(bug)
    #start with all empty hexes as possible placements
    possible_place_cords = []
    for i,c in enumerate(board):
        if c == 0:
            possible_place_cords.append(iToCord3[i])
    #remove all placements that are adjescent to our largest bugs
    temp_cords = []
    for c in possible_place_cords:
        found_adjescent = False
        for bug in largest_our_bugs:
            if are_bugs_adjescent([c],bug['cords']):
                found_adjescent = True
                break
        if found_adjescent == False:
            temp_cords.append(c)
    possible_place_cords = temp_cords
    #for each placement find out if it leads to eating and if so if a grow is possible
    actions = []
    for c in possible_place_cords:
        copyboard = list(board)#make a duplicate board
        place(copyboard,str(c),current_player)#simulate placement
        copybugs = get_bugs(copyboard)#make new bugs
        actions += get_grow_actions(copyboard,copybugs,str(c),current_player)
        
    return actions

def display_board(board):
    out = '  '
    for i in xrange(18,-1,-1):
        if i in [15,11,6,2]:
            out += "\n"
            if i in [15,6]:
                out += ' '
            if i == 2:
                out += '  '
        if board[i] == -1:
            out += 'X '
        elif board[i] == 1:
            out += 'O '
        else:
            out += '. '
    return out