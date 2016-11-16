#Code for HW1 CS561 -- Nicky Singh
#Code takes input file as an input
#Players can be X or O,option 1-GBFS,option 2- Minimax 3-Alphabeta 4 - Simulation
from sys import argv
__author__ = "ADD(Amit Deepak Deshmukh)"

script,opt,inputfilename = argv
#READ Input contents
global log_min_max
log_min_max = str()
log_alpha_beta = str()
f = open(inputfilename, 'r')

algo_type = int(f.readline().rstrip('\n'))


if algo_type <> 4:
    current_player = f.readline().rstrip()
    depth = int(f.readline().rstrip('\n'))
    max_depth = depth
    board_weights = []
    start_state = []
    n = 1

# GET the board weights and starting state of the game
    while n <= 5:
        myLines = f.readline().rstrip().split()
        weight_int_List = [int(i) for i in myLines]
        board_weights.append(weight_int_List)
        n= n+1
    n= 1
    while n<=5:
        start_state.append(list(f.readline().rstrip()))
        n += 1
    f.close()
    if current_player == 'X':
        opp_player ='O'
    else:
        opp_player ='X'
else:
    first_player = f.readline().rstrip()
    first_player_algo = f.readline().rstrip('\n').rstrip("\r")
    first_player_depth = int(f.readline().rstrip('\n'))
    second_player = f.readline().rstrip()
    second_player_algo = f.readline().rstrip('\n').rstrip("\r")
    second_player_depth = int(f.readline().rstrip('\n'))
    f1 = open("trace_state.txt","w")
    f1.close()
    board_weights =[]
    start_state=[]
    n = 1
    while n <= 5:
        myLines = f.readline().rstrip().split()
        weight_int_List = [int(i) for i in myLines]
        board_weights.append(weight_int_List)
        n = n+1
    n= 1
    while n <= 5:
        start_state.append(list(f.readline().rstrip()))
        n += 1
    f.close()
# SET the opponent player

def setCurrentPlayer(currentPlayer):
    global current_player
    global opp_player
    current_player = currentPlayer
    opp_player = opponent1(currentPlayer)


##to be used in the log for getting board cell name
rows = [1, 2, 3, 4, 5]
columns = ['A', 'B', 'C', 'D', 'E']

#THIS is the evaluation function to check h value for any state of the board
#Board Value = MyPoints-OpponentPoints
def evaluation_function(current, opponent, board):
    curr_score, opponent_score = 0, 0
    i, j = 0, 0
    while i < 5:
        j = 0
        while j < 5:
            if board[i][j] == '*':
                pass
            elif board[i][j] == current:
                curr_score += board_weights[i][j]
            else:
                opponent_score += (board_weights[i][j])
            j += 1
        i += 1

    return curr_score-opponent_score

#print evaluation_function(current_player,opp_player,start_state)

#Get all the available Moves on current board state

def available_moves(board, player):
    if player == 'X':
        opp = 'O'
    else:
        opp = 'X'

    avail_moves = []
    for i in range(0,5):
        for j in range(0,5):
            if board[i][j] == '*':
                avail_moves.append((i,j))

    if not avail_moves:
        avail_moves = []

    return avail_moves

#print available_moves(start_state,current_player)

##Create a DeepCopy of gameboard

def deep_copy(board):
    temp_board = []
    for obj in board:
        if isinstance(obj,list):
            temp_board.append(deep_copy(obj))
        else:
            temp_board.append(obj)
    return temp_board

#Set current and opponent player
def opponent1(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

#Here the tentative moves will be played and and evaluation value will be returned with board state
def isaRaid(player,move,temp_board):
    left = move[1] - 1                                          #Check for avail move on each of the left,right,top,bottom for same piece
    right= move[1] + 1                                          #then opp gets converted to player piece.
    top = move[0] - 1
    bottom = move[0] + 1
    bool = False

    if bottom < 5 :
        if temp_board[move[0]+1][move[1]] == player:
            bool = True
    if top > -1:
        if temp_board[move[0]-1][move[1]] == player:
            bool = True
    if right < 5:
        if temp_board[move[0]][move[1]+1] == player:
            bool = True
    if left > -1:
        if temp_board[move[0]][move[1]-1] == player:
            bool = True
    return bool

def do_move_test(board,move,player):
    temp_board = deep_copy(board)
    if move is None:
        return "NoValidMovesLeft"
    temp_board[move[0]][move[1]] = player
    left = move[1] - 1                                          #Check for avail move on each of the left,right,top,bottom for opp piece
    right = move[1] + 1                                          #to convert to player piece.
    top = move[0] - 1
    bottom = move[0] + 1
    if bottom < 5:                                              #convert opponent piece here
        if temp_board[move[0]+1][move[1]] == opponent1(player) and isaRaid(player,move,temp_board):
            temp_board[move[0]+1][move[1]] = player
    if top > -1:
        if temp_board[move[0]-1][move[1]] == opponent1(player) and isaRaid(player,move,temp_board):
            temp_board[move[0]-1][move[1]] = player
    if left > -1:
         if temp_board[move[0]][move[1]-1] == opponent1(player) and isaRaid(player,move,temp_board):
            temp_board[move[0]][move[1]-1] = player
    if right < 5:
         if temp_board[move[0]][move[1]+1] == opponent1(player) and isaRaid(player,move,temp_board):
            temp_board[move[0]][move[1]+1] = player

    #evaluate the board state
    value = evaluation_function(current_player,opp_player,temp_board)
    return value,temp_board,move
##choose algo for a player and return best move
def choose_Algo(board,playerNo):

    if playerNo == "first":

        if first_player_algo == '1':
            best_result = greedy_best_first(board,first_player)
            return best_result[0][0][2]

        elif first_player_algo == '2':
            best_result = mini_Max(board,first_player,first_player_depth)
            return best_result[0]

        elif first_player_algo == '3':
            best_result = alphaBeta(board,first_player,first_player_depth)
            return  best_result[0]

    else:

        if second_player_algo == '1':
            best_result = greedy_best_first(board,second_player)
            return best_result[0][0][2]

        elif second_player_algo == '2':
            best_result = mini_Max(board,second_player,second_player_depth)
            return best_result[0]

        elif second_player_algo == '3':
            best_result = alphaBeta(board,second_player,second_player_depth)
            return best_result[0]

#################write board state to the files
def write_state(state_graph,filename):
        i = 0
        state_graph_str = str()

        while i < len(state_graph):
            line = str(state_graph[i]).replace('[','')
            line = line.replace(']', '')
            line = line.replace(',','')
            line = line.replace("\'",'')
            line = line.replace(" ",'')
            state_graph_str += line+'\n'
            i += 1

        #state_graph_str = state_graph_str.rstrip('\n')
        f = open(filename, "a")
        f.write(state_graph_str)
        f.close()


##Logic for Greedy Best First


def greedy_best_first(board,player):

    avail_moves = available_moves(board,player)
    n_avail_moves = len(avail_moves)
    contender_moves = list()
    best_moves = list()
    final_move = list()
    if n_avail_moves == 0:
        return
    i = 0
    while i < n_avail_moves:
       temp_board = deep_copy(board)
       contender_moves.append([do_move_test(temp_board,avail_moves[i],player),avail_moves[i]])
       i += 1

    if contender_moves[0][0] == "NoValidMovesLeft":
        return "NoMoves"

    i = 0
    bestVal = -9999
    while i < len(contender_moves):
        getVal = contender_moves[i][0][0]
        if getVal >= bestVal:
            bestVal = getVal
            #best_moves.append(contender_moves[i])
        i += 1

    i=0
    while i < len(contender_moves):
        if contender_moves[i][0][0] == bestVal:
            best_moves.append(contender_moves[i])
        i +=1
    i = 1

    final_move_var = best_moves[0][0][2]
    final_move.append(best_moves[0])

    while i < len(best_moves):
        final_move_temp = best_moves[i][0][2]
        if final_move_var[0]> final_move_temp[0]:
            final_move_var = final_move_temp
            del final_move[:]
            final_move.append(best_moves[i])
        elif final_move_var[0] == final_move_temp[0]:
            if final_move_var[1] > final_move_temp[1]:
                final_move_var = final_move_temp
                del final_move[:]
                final_move.append(best_moves[i])
        i += 1
    return final_move

####################################################################################################################################3
#Minmax logic- Minimise opponent score,foresee based on depth
######################
best_moves = []
best_move = []
log_min_max = str()
def mini_Max(board,player,depth):
    global minmax_max_depth
    global log_min_max
    minmax_max_depth = depth
    depth = 0
    moves = available_moves(board,player)
    if len(moves) == 0:
        return
    best_move = moves[0]
    best_score = -9999
    #print "root",0,-9999
    log_min_max = '\n'+"root"+','+str(0)+','+str(best_score)
    for i in range(0,len(moves)):
        temp_board = deep_copy(board)
        result = do_move_test(temp_board,moves[i],player)

        score = min_play(result[1],opponent1(player),depth + 1,moves[i])
        if score > best_score:
            best_move = (moves[i])
            best_score = score
            #print "root",best_score,depth
            log_min_max += '\n'+"root"+','+str(0)+','+str(best_score)
        else:
            #print "root",best_score,depth
            log_min_max += '\n'+"root"+','+str(0)+','+str(best_score)
    return best_move,best_score

def min_play(board,player,depth,move):
    global log_min_max
    moves=available_moves(board,player)
    if depth == minmax_max_depth or len(moves)==0:
        temp_score = evaluation_function(current_player,opp_player,board)
        #print rows[move[0]],columns[move[1]],evaluation_function(current_player,opp_player,board),depth
        log_min_max += '\n'+str(columns[move[1]]) + str(rows[move[0]])+','+ str(depth)+',' + str(temp_score)
        return evaluation_function(current_player,opp_player,board)

    best_score = 9999
    #print rows[move[0]],columns[move[1]],best_score,depth
    log_min_max += '\n'+str(columns[move[1]]) + str(rows[move[0]])+','+ str(depth)+','+ str(best_score)
    for i in range(0,len(moves)):
        temp_board = deep_copy(board)
        result = do_move_test(temp_board,moves[i],player)

        score = max_play(result[1],opponent1(player),depth+1,moves[i])

        if score < best_score:
            best_move = moves[i]
            best_score = score
            #print rows[move[0]],columns[move[1]],best_score,depth
            log_min_max += '\n'+str(columns[move[1]]) + str(rows[move[0]])+','+ str(depth)+',' + str(best_score)
        else:
            #print rows[move[0]],columns[move[1]],best_score,depth
            log_min_max += '\n'+str(columns[move[1]]) + str(rows[move[0]])+','+ str(depth)+',' + str(best_score)
    return best_score
#Make the score maximise here
def max_play(board,player,depth,move):
    global log_min_max
    moves = available_moves(board,player)
    if depth == minmax_max_depth or len(moves)==0:
        temp_score = evaluation_function(current_player,opp_player,board)
        #print rows[move[0]],columns[move[1]],evaluation_function(current_player,opp_player,board),depth
        log_min_max += '\n'+str(columns[move[1]]) + str(rows[move[0]])+','+ str(depth)+',' + str(temp_score)
        return evaluation_function(current_player,opp_player,board)
    best_score = -9999
    #print rows[move[0]],columns[move[1]],best_score,depth
    log_min_max += '\n'+str(columns[move[1]])+ str(rows[move[0]])+','+ str(depth)+',' + str(best_score)
    for i in range(0,len(moves)):
        temp_board = deep_copy(board)
        result = do_move_test(temp_board,moves[i],player)
        score = min_play(result[1],opponent1(player),depth+1,moves[i])
        if score > best_score:
            best_move = moves[i]
            best_score = score
            #print rows[move[0]],columns[move[1]],best_score,depth
            log_min_max += '\n'+str(columns[move[1]])+ str(rows[move[0]])+','+ str(depth)+',' + str(best_score)
        else:
            #print rows[move[0]],columns[move[1]],best_score,depth
            log_min_max += '\n'+str(columns[move[1]])+ str(rows[move[0]])+','+ str(depth)+',' + str(best_score)
    return best_score

#####################################################################
#Alpha beta logic:forsee with pruning
##########################
best_moves =[]
best_move = []
log_alpha_beta = str()
def alphaBeta(board,player,depth):
    global alphabeta_max_depth
    global log_alpha_beta
    alphabeta_max_depth = depth
    depth = 0
    moves =available_moves(board,player)
    if len(moves)==0:
        return
    best_move = moves[0]
    alpha = -9999
    beta = 9999
    best_score = -9999
    #print "root",0,-9999,alpha,beta
    log_alpha_beta = '\n'+"root"+','+str(0)+','+str(best_score)+','+str(alpha)+','+str(beta)
    for i in range(0,len(moves)):
        temp_board = deep_copy(board)
        result = do_move_test(temp_board,moves[i],player)

        score = beta_play(result[1],opponent1(player),depth + 1,moves[i],alpha,beta)
        if score > best_score:
            best_move = moves[i]
            best_score = score
            #print "root",depth,best_score,best_score,beta
            log_alpha_beta += '\n'+"root"+','+str(0)+','+str(best_score)+','+str(best_score)+','+str(beta)
        else:
            #print "root",depth,best_score,best_score,beta
            log_alpha_beta += '\n'+"root"+','+str(0)+','+str(best_score)+','+str(best_score)+','+str(beta)
        alpha = best_score
    return best_move,best_score

def beta_play(board,player,depth,move,alpha,beta):
    global log_alpha_beta
    moves=available_moves(board,player)
    if depth == alphabeta_max_depth or len(moves)==0:
        temp_score = evaluation_function(current_player,opp_player,board)
        #print rows[move[0]],columns[move[1]],evaluation_function(current_player,opp_player,board),depth,alpha,beta
        log_alpha_beta += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(depth)+','+str(temp_score)+','+str(alpha)+','+str(beta)
        return evaluation_function(current_player,opp_player,board)

    best_score = 9999
   # print columns[move[1]],rows[move[0]],depth,best_score,alpha,beta
    log_alpha_beta += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(depth)+','+str(best_score)+','+str(alpha)+','+str(beta)

    for i in range(0,len(moves)):
        temp_board = deep_copy(board)
        result = do_move_test(temp_board,moves[i],player)

        score = alpha_play(result[1],opponent1(player),depth+1,moves[i],alpha,beta)

        if score < best_score:
            #best_move = moves[i]
            best_score = score
            #RETURN THE BEST SCORE HERE
        if best_score <= alpha:
          #  print rows[move[0]],columns[move[1]],best_score,depth,alpha,beta
            log_alpha_beta += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(depth)+','+str(best_score)+','+str(alpha)+','+str(beta)
            return best_score
        beta = min(beta,best_score)

        #print rows[move[0]],columns[move[1]],best_score,depth,alpha,beta
        log_alpha_beta += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(depth)+','+str(best_score)+','+str(alpha)+','+str(beta)
    return best_score



def alpha_play(board,player,depth,move,alpha,beta):
    global log_alpha_beta
    moves=available_moves(board,player)

    if depth == alphabeta_max_depth or len(moves)==0:
        temp_score = evaluation_function(current_player,opp_player,board)
        #print rows[move[0]],columns[move[1]],evaluation_function(current_player,opp_player,board),depth,alpha,beta
        log_alpha_beta += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(depth)+','+str(temp_score)+','+str(alpha)+','+str(beta)
        return evaluation_function(current_player,opp_player,board)
    best_score = -9999
    #print columns[move[1]],rows[move[0]],depth,best_score,alpha,beta
    log_alpha_beta += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(depth)+','+str(best_score)+','+str(alpha)+','+str(beta)

    for i in range(0,len(moves)):
        temp_board = deep_copy(board)
        result = do_move_test(temp_board,moves[i],player)
        score = beta_play(result[1],opponent1(player),depth+1,moves[i],alpha,beta)

        if score > best_score:
            best_move = moves[i]
            best_score = score

        if best_score >= beta:
            log_alpha_beta += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(depth)+','+str(best_score)+','+str(alpha)+','+str(beta)
            return best_score

        alpha = max(alpha,best_score)
        #print rows[move[0]],columns[move[1]],best_score,depth,alpha,beta
        log_alpha_beta += '\n'+str(columns[move[1]])+str(rows[move[0]])+','+str(depth)+','+str(best_score)+','+str(alpha)+','+str(beta)
    return best_score

################################################################################################################################
#2 player simulation: files created - trace_state.txt
###############################33
def simulate():

    result = 0,start_state,0
    no_of_moves = available_moves(start_state,first_player)
    while len(no_of_moves) <> 0:
        setCurrentPlayer(first_player)
        first_player_best_move = choose_Algo(result[1],"first")
        result = do_move_test(result[1],first_player_best_move,first_player)
        write_state(result[1],"trace_state.txt")
        no_of_moves = available_moves(result[1],second_player)
        setCurrentPlayer(second_player)
        if len(no_of_moves) <> 0:
            second_player_best_move = choose_Algo(result[1],"second")
            result = do_move_test(result[1],second_player_best_move,second_player)
            write_state(result[1],"trace_state.txt")
            no_of_moves = available_moves(result[1],first_player)


#################################################################################################################################3
#menu function decides which algorithm will be used
#1- Greedy Best First #2MinmAx with depth #3AlphaBeta Pruning #Battle Simulation with desired algos and cutoff depth
#################################################################################
def Menu():

    if algo_type == 1:
        state = greedy_best_first(start_state,current_player)
        if state == None:
            print "no moves left"
        state_graph = state[0][0][1]

        i = 0
        state_graph_str = str()

        while i < len(state_graph):
            line = str(state_graph[i]).replace('[','')
            line = line.replace(']', '')
            line = line.replace(',','')
            line = line.replace("\'",'')
            line = line.replace(" ",'')
            state_graph_str += line+'\n'
            i += 1

        state_graph_str = state_graph_str.rstrip('\n')
        f = open("next_state.txt", "w")
        f.write(state_graph_str)
        f.close()
    elif algo_type == 2:
        global log_min_max
        best_move = mini_Max(start_state,current_player,depth)

        if best_move == None:
            print "no moves left"
            return
        result = do_move_test(start_state,best_move[0],current_player)
        i = 0
        state_graph_str = str()

        while i < len(result[1]):
            line = str(result[1][i]).replace('[','')
            line = line.replace(']', '')
            line = line.replace(',','')
            line = line.replace("\'",'')
            line = line.replace(" ",'')
            state_graph_str += line+'\n'
            i += 1

        state_graph_str = state_graph_str.rstrip('\n')
        f = open("next_state.txt", "w")
        f.write(state_graph_str)
        f.close()
        f = open("traverse_log.txt","w")
        log_min_max = log_min_max.replace("-9999", "-Infinity")
        log_min_max = log_min_max.replace("9999", "Infinity")
        f.write("Node,Depth,Value"+log_min_max)
        f.close()
    elif algo_type == 3:
        global log_alpha_beta
        best_move = alphaBeta(start_state,current_player,depth)
        if best_move == None:
            print "no moves left"
            return
        result = do_move_test(start_state,best_move[0],current_player)
        i = 0
        state_graph_str = str()

        while i < len(result[1]):
            line = str(result[1][i]).replace('[','')
            line = line.replace(']', '')
            line = line.replace(',','')
            line = line.replace("\'",'')
            line = line.replace(" ",'')
            state_graph_str += line+'\n'
            i += 1

        state_graph_str = state_graph_str.rstrip('\n')
        f = open("next_state.txt", "w")
        f.write(state_graph_str)
        f.close()
        f = open("traverse_log.txt","w")
        log_alpha_beta = log_alpha_beta.replace("-9999","-Infinity")
        log_alpha_beta = log_alpha_beta.replace("9999","Infinity")
        f.write("Node,Depth,Value,Alpha,Beta"+log_alpha_beta)
        f.close()

       #Test Menu

    elif algo_type == 4:
        simulate()
####Everything is driven through menu
Menu()
