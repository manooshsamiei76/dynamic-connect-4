# -*- coding: utf-8 -*-
"""
Created on Jan 19 12:44:18 2020

@author: ASUS
"""
import manual_init as mn
from math import inf
import timeit
from random import choice
import telnetlib
import random
board = [[' ',' ',' ',' ',' ',' ','X'],
         ['X',' ',' ',' ',' ',' ','O'],
         ['O',' ',' ',' ',' ',' ','X'],
         ['X',' ',' ',' ',' ',' ','O'],
         ['O',' ',' ',' ',' ',' ','X'],
         ['X',' ',' ',' ',' ',' ','O'],
         ['O',' ',' ',' ',' ',' ',' ']]

#list_v contains eligible move commands to be recieved by telnet
list_v =[]   
for i in range(1,8):
     for j in range(1,8):
            list_v.append(str(i)+str(j)+'N'+'\n')
            list_v.append(str(i)+str(j)+'S'+'\n')
            list_v.append(str(i)+str(j)+'E'+'\n')
            list_v.append(str(i)+str(j)+'W'+'\n')
            
X_CENTER_INDEX= 4
Y_CENTER_INDEX = 4
COUNTER =0

def print_board(state):
    
    """
    Printing the board 
    :param state: the current state of the board
    
    """
    for i in range(7):
        for j in range(7): 
           if j==6:
              print(state[i][j].strip('\n'))
           else:
              print(state[i][j], end=',')
        
def initial_state(board):
    
    """
    defining the initial state of the board 
    :param board: the initial state of the board
    
    """
    print('The initial state is:')
    print_board(board)
    
    init=input('Do you like to enter a new initial state? y/n \n')
    
    if init=='y':
       ch=input('press "f" is you like to open a file \n press "m" to enter manually? f/m \n')
       '''
        build an arrangement like below in a txt file and import it here
        you can change the sample file 'state.txt' provided in code folder.
         , , , , , ,X
        X, , , , , ,O
        O, , , , , ,X
        X, , , , , ,O
        O, , , , , ,X
        X, , , , , ,O
        O, , , , , , 

       '''
       if ch=='f':
          filename = input('enter the name of the file E.g: stateA.txt \n')
          # change the below file for a new state!
          with open(filename, 'r') as init_state:
             a = init_state.read()
             list_a= a.split('\n')
             board=[item.split(',') for item in list_a]
          print('The initial state is:')
          print_board(board)
          
       elif ch=='m': mn.manual_init_state(board)

def evaluate (state, comp_p , remote_p):
    
    """
    Simple Evaluation of the score for the current sate
    This function is now replaced by a more complex heuristic function below
    :param state: the current state of the board
    :param comp_p: the piece that AI agent plays with(='O' or 'X')
    :param remote_p: the piece that remute agent plays with
    :return: the score of the current state
    """    
    if win(state , comp_p):
        score = +1
        
    elif win(state , remote_p):
        score = -1
        
    else:
        score = 0

    return score

def heuristic_count (state, comp_p , remote_p):
    
    """
    Evaluation of the value for the current sate, based on some heuristics that
    specify how close each state is to a win state
    :param state: the current state of the board
    :param comp_p: the piece that AI agent plays with(='O' or 'X')
    :param remote_p the piece that remute agent plays with
    :return: the value of the current state
    """    
    
    def count_pieces (state, piece):
      
        """ 
        This heuristic counts for each player how many pieces are placed in a
        row as part of the winning states.
        :param state: the current state of the board
        :param piece: the piece of the player('X' or 'O')
        :return: the number of pieces in a row
        """    
        count=0
        win_states = []
        #generating the winning states
        for i in range(7): 
            for j in range(4):
                #horizontal line up winning state
                win_states.append([state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]])
                #vertical line up winning state
                win_states.append([state[j][i], state[j+1][i], state[j+2][i], state[j+3][i]])
                if(i < 4) :             
                    #diagonal line up winning state
                    win_states.append([state[j][i], state[j+1][i+1], state[j+2][i+2], state[j+3][i+3]])
                    win_states.append([state[j][6-i], state[j+1][5-i], state[j+2][4-i], state[j+3][3-i]])
        
        #two pieces in a row as part of winning states            
        row_two = [row[i:i+2] for row in win_states for i in range(3)]
        #three pieces in a row as part of winning states 
        row_three = [row[i:i+3] for row in win_states for i in range(2)]
        #four pieces in a row as part of winning states 
        row_four = [row[i:i+4] for row in win_states for i in range(1)]
        
        #check if the player's pieces are placed two in a row
        if [piece,piece] in row_two:
            for k in range(row_two.count([piece, piece])):
                count+=2
        #check if the player's pieces are placed three in a row        
        if [piece, piece, piece]  in row_three:        
            for k in range(row_three.count([piece, piece, piece])):
                count+=5
        #check if the player's pieces are placed four in a row (winning state)        
        if [piece, piece, piece, piece]  in row_four:
            count+=15
        
        return count

    def heuristic_center_dist (state, piece):
        """ 
        This heuristic calculates the sum of the distance (in x direction) of 
        pieces from the center of the board (less distance is better) plus the 
        number if pieces that are more than 1 square away from the x center.  
        :param state: the current state of the board
        :param piece: the piece of the player('X' or 'O')
        :return: the number of pieces in a row
        """  
        dist =0
        num_dis =0
        sum_dis =0
        for y, row in enumerate(state):
            for x, cell in enumerate(row):
                if cell==piece:
                    dist= (x-X_CENTER_INDEX)**2+(y-Y_CENTER_INDEX)**2
                    if (dist>1): num_dis+=1 
                    sum_dis+=dist                    
        return sum_dis+num_dis
  
    if COUNTER <=4:
#     
       return 2*count_pieces(state,comp_p) + 2*heuristic_center_dist(state,remote_p) -10*heuristic_center_dist(state,comp_p) - count_pieces (state,remote_p)
#             
    elif COUNTER >4:
      
       return count_pieces (state,comp_p)**2 -  50*count_pieces (state,remote_p)**2+ heuristic_center_dist(state,remote_p) -heuristic_center_dist(state,comp_p)

        
def win(state, piece):
    win_states = []
    """
    Checks if the pieces are in winning states
    :param state: the current state of the board
    :param piece: the piece of the player('X' or 'O')
    :return: True if the player won and False if it did not
    """
    for i in range(7): 
        for j in range(4):
            #horizontal line up winning 
            win_states.append([state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]])
            #vertical line up winning
            win_states.append([state[j][i], state[j+1][i], state[j+2][i], state[j+3][i]])
            if(i < 4) :               
            #diagonal line up winning
                win_states.append([state[i][j], state[i+1][j+1], state[i+2][j+2], state[i+3][j+3]])
                win_states.append([state[i][6-j], state[i+1][5-j], state[i+2][4-j], state[i+3][3-j]])
    if [piece, piece, piece, piece] in win_states:
        return True
    else:
        return False

       
def interpret_move(direc, x, y, board):
    """
    changes the state of the board based on the new movement
    :param direc: the direction of movement(West,East,...)
    :param x: the position of the moving piece in x axis, column-wise
    :param y: the position of the moving piece in y axis, row-wise
    :param board: the current state of the board
    """    
    
    if direc=='E':
        board[y][x+1]= board[y][x]
        board[y][x] = ' '
        
    elif direc=='W':
        board[y][x-1]= board[y][x]
        board[y][x] = ' '
        
    elif direc=='N':
        board[y-1][x]= board[y][x]
        board[y][x] = ' '
        
    elif direc=='S':
        board[y+1][x]= board[y][x]
        board[y][x] = ' '
              
    print_board(board)

                       
def max_alpha_beta(state, alpha, beta, remote_p, comp_p, depth, start):
    """
    minimax algorithm with alpha-beta pruning, Max player
    :param state: the current state of the board
    :param alpha: the alpha parameter for pruning
    :param beta: the beta parameter for pruning
    :param remote_p: the piece that remote player plays with
    :param comp_p: the piece that AI agent plays with
    :param depth: the maximum depth search of the tree
    :param start: the starting time of minimax search to cut the search after 10 sec
    :return: the best movement with highest value for the max player 
    """      
    best = [None, None, None , -inf]
    stop = timeit.default_timer()
    if depth<=0 or win(state , comp_p) or stop-start>=8.5:
          score = heuristic_count(state, comp_p , remote_p)
          return [-1, -1, -1 , score]
        
    m =[(-1,0),(0,-1),(0,1),(1,0)]
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell==comp_p: 
                for (i ,j) in m:
                    if (y+i)>(6) or (x+j)>(6) or (y+i)<0 or (x+j)<0:
                       continue
                    if state[y+i][x+j]==' ':
                        state[y+i][x+j]= comp_p
                        state[y][x] = ' '
                        score = min_alpha_beta(state, alpha, beta, remote_p, comp_p, depth-1, start)
                        state[y+i][x+j]= ' '
                        state[y][x] = comp_p
                        score[0], score[1], score[2] = y, x, m.index((i ,j))
                        
                        if score[3] > best[3]: 
                            best = score
                        
                        if best [3] >= beta:
                            return [y,x , m.index((i ,j)), best[3]]
                        
                        if best[3] > alpha:
                            alpha = best[3] 
                
    return best

def min_alpha_beta(state, alpha, beta, remote_p, comp_p, depth, start):
    """
    minimax algorithm with alpha-beta pruning, Min player
    :param state: the current state of the board
    :param alpha: the alpha parameter for pruning
    :param beta: the beta parameter for pruning
    :param remote_p: the piece that remote player plays with
    :param comp_p: the piece that AI agent plays with
    :param depth: the maximum depth search of the tree
    :param start: the starting time of minimax search to cut the search after 10 sec
    :return: the best movement with lowest value for the min player 
    """ 
    best = [None, None, None , +inf]
    stop = timeit.default_timer()
    if depth<=0 or win(state , remote_p) or stop-start>=8.5:
          score=heuristic_count(state, comp_p , remote_p)
          return [-1, -1, -1 , score]
    m =[(-1,0),(0,-1),(0,1),(1,0)]
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell==remote_p: 
                for (i ,j) in m:
                    if (y+i)>(6) or (x+j)>(6) or (y+i)<0 or (x+j)<0:
                       continue
                    if state[y+i][x+j]==' ':
                        state[y+i][x+j]= remote_p
                        state[y][x] = ' '
                        score = max_alpha_beta(state, alpha, beta, remote_p, comp_p, depth-1, start)
                        state[y+i][x+j]= ' '
                        state[y][x] = remote_p
                        score[0], score[1], score[2] = y, x, m.index((i ,j))
                        
                        if score[3] < best[3]: 
                            best = score
                        
                        if best [3] <= alpha:
                            return [y,x , m.index((i ,j)), best[3]]
                        
                        if best[3] < beta:
                            beta= best[3] 
                
    return best

def comp_turn(tn, remote_p, comp_p):
    """
    Computes a move for AI agent through Minimax+alpha_beta pruning
    sends the move command to the Telnet client and draws the new board 
    :param remote_p: the piece that remote agent plays with
    :param comp_p: the piece that AI agent plays with
    """
    
    print('Computer turn [%s]' %comp_p)
    direction=['N', 'W', 'E','S']# with the order of m arrangement in minimax function
    if (win(board, remote_p) or win(board, comp_p)):
        return
    depth = 10
    start = timeit.default_timer()
    move = max_alpha_beta(board ,-inf, +inf, remote_p, comp_p, depth, start)
    y = move[0]
    x= move[1]
    direc = direction[move[2]]
    #print the command on game server through telnet
    tn.write((str(x+1)+str(y+1)+str(direc) + '\n').encode('ascii'))
    end = timeit.default_timer()
    print('runtime:' , end - start)
    #read the telnet buffer to empty it for further communications
    tn.read_until('\n'.encode('ascii'))
    #to interpret move command and move the piece on the board    
    interpret_move(direc, x, y , board)
    #count the number of movement to change the heuristics
    global COUNTER
    COUNTER=1+COUNTER
            
def remote_move(tn,remote_p):
    """
    recieves a move from a remote player, interprets the command and
    draws the new board.
    :param tn: the telnet client
    :param remote_p: the piece that remote agent plays with
    """
    string_move = None
    print('Waiting for move from remote player...')
    while string_move not in list_v:
         string_move = tn.read_until('\n'.encode("ascii"))
         string_move = string_move.decode('ascii') 

    move=['','','']
    move[:] =string_move
    #subtracting one to match array index numbers
    x , y = int(move[0])-1, int(move[1])-1 
    direc = move[2]
      
    interpret_move(direc, x, y , board)    
    
def ai_vs_remote():
    
    """
    rules the game rounds between remote agent and AI agent
    and prints the result of the game.
    """
    #the initial state is set
    initial_state(board)
    
    remote_p = '' # remote agent plays this
    comp_p = '' # ai plays this
    
    #the address of game server + the port number
    host = 'localhost'
    port = 12345
    colour = input("enter the color you'd like to play:")
    game_id = input('enter the game id:')

    print('connecting to host, port...')
    tn = telnetlib.Telnet(host, port)

    print('Sending game information (game ID, colour)...')
    varab = game_id + ' ' + colour + '\n'
    tn.write(varab.encode("ascii"))
    #reading to clean the buffer for further communications
    tn.read_until('\n'.encode("ascii"))
    
    #'X' piece is equal to black pieces & 'O' is equal to white pieces
    if colour== 'black':
        remote_p = 'O'
        comp_p = 'X'
        start = 0
    else:
        comp_p= 'O'
        remote_p = 'X'
        start = 1
    #while no one has won the game continue the game    
    while not(win(board , remote_p) or win(board, comp_p)):
    #'O' or 'white' player always starts the game
        if start==1:
            #random choice by AI agent for the first node of game
           (x , y , direction) =choice([(0, 2,'E'),(0, 4,'E'),
                                        (0, 6,'E'),(6, 1,'W'),
                                        (6, 3,'W'),(6, 5,'W')])
           #write the command on telnet 
           if tn is not None:
                tn.write((str(x+1)+str(y+1)+str(direction) + '\n').encode("ascii"))
                tn.read_until('\n'.encode("ascii"))
           # interpret the move command and draw the new board
           interpret_move(direction, x, y , board)
           start = None
 
        remote_move(tn,remote_p)
        comp_turn(tn, remote_p, comp_p)
        
    if win(board , remote_p):
        
        print_board(board)
        print('YOU WIN!')
    elif win (board, comp_p):
        
        print_board(board)
        print('YOU WIN!')
    else: 
        print_board(board)
        print('DRAW!')

    exit()
    
if __name__ == '__main__':
    
    ai_vs_remote()
    



