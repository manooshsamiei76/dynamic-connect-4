# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 05:47:16 2020

@author: ASUS
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 12:44:18 2020

@author: ASUS
"""
import manual_init as mn
from math import inf
import timeit
from random import choice
import matplotlib.pyplot as plt
import numpy as np
import random

board = [[' ',' ',' ',' ',' ',' ','X'],
         ['X',' ',' ',' ',' ',' ','O'],
         ['O',' ',' ',' ',' ',' ','X'],
         ['X',' ',' ',' ',' ',' ','O'],
         ['O',' ',' ',' ',' ',' ','X'],
         ['X',' ',' ',' ',' ',' ','O'],
         ['O',' ',' ',' ',' ',' ',' ']]

from matplotlib.ticker import MaxNLocator
X_CENTER_INDEX= 4
Y_CENTER_INDEX = 4
COUNTER =0
MIN_DEPTH = 3
MAX_DEPTH = 6
 
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
       
    return board       

def evaluate (state, comp_p , human_p):
    """
    Simple Evaluation of the score for the current sate
    This function is now replaced by a more complex heuristic function below
    :param state: the current state of the board
    :param comp_p: the piece that AI agent plays with(='O' or 'X')
    :param human_p: the piece that human plays with
    :return: the score of the current state
    """     
    if win(state , comp_p):
        score = +1
    elif win(state , human_p):
        score = -1
    else:
        score = 0

    return score

def heuristic_count (state, comp_p , human_p):
  """
  Evaluation of the value for the current sate, based on some heuristics that
  specify how close each state is to a win state
  :param state: the current state of the board
  :param comp_p: the piece that AI agent plays with(='O' or 'X')
  :param human_p the piece that human plays with
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

    for i in range(7): 
        for j in range(4):
            #horizontal line up winning 
            win_states.append([state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]])
            #vertical line up winning
            win_states.append([state[j][i], state[j+1][i], state[j+2][i], state[j+3][i]])
            if(i < 4) :             
            #diagonal line up winning
                win_states.append([state[j][i], state[j+1][i+1], state[j+2][i+2], state[j+3][i+3]])
                win_states.append([state[j][6-i], state[j+1][5-i], state[j+2][4-i], state[j+3][3-i]])
                
    row_two = [row[i:i+2] for row in win_states for i in range(3)] 
    row_three = [row[i:i+3] for row in win_states for i in range(2)] 
    row_four = [row[i:i+4] for row in win_states for i in range(1)]
    
    if [piece,piece] in row_two:
        for k in range(row_two.count([piece, piece])):
            count+=1
    if [piece, piece, piece]  in row_three:        
        for k in range(row_three.count([piece, piece, piece])):
            count+=5
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
    sum_dis =0
    dist_c=0  
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell==piece:
#                if dist==0:
#                    x1=x
#                    y1=y
#                    dist=1
#                dist=abs(x1-x)+abs(y1-y)
#                sum_dis+=dist 
                dist_c= (2*abs(x-X_CENTER_INDEX))+(abs(y-Y_CENTER_INDEX))
                sum_dis+=dist_c
                       
    return sum_dis
  if COUNTER <= 4:
##  
      return 2*heuristic_center_dist(state,human_p) -2*heuristic_center_dist(state,comp_p)+ count_pieces (state,comp_p) - count_pieces (state,human_p)
#            
  elif COUNTER > 4:
##      
      return count_pieces (state,comp_p)**2 -  50*count_pieces (state,human_p)**2+ heuristic_center_dist(state,human_p) -heuristic_center_dist(state,comp_p)

def random_heuristic_count ():
    
    return random.randint(-100, 100)
            
def win(state, piece):
    """
    Checks if the pieces are in winning states
    :param state: the current state of the board
    :param piece: the piece of the player('X' or 'O')
    :return: True if the player won and False if it did not
    """
    win_states = []
    
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

def move_func(board_2, human_p, comp_p):
    """
    recieves a move from a human player, interprets the command and
    draws the new board.
    :param human_p: the piece that human plays with
    :param comp_p: the piece that ai agent plays with
    """
    
    print('Human turn [%s]' %human_p) 
    print("Enter <x,y> of piece you'd like to move + direction (e.g. 72W)")
    move=['','','']
    move[:] = str(input())
    
    x , y = int(move[0])-1, int(move[1])-1 #we subtract one to match 'board' array index numbers
    direc = move[2]
    
    while validate_move (board_2, direc, x, y,human_p):
        print("movement isn't valid. Try again!\n")
        print("Enter <x,y> of piece you'd like to move + direction (e.g. 72W)")
        move=['','','']
        move[:] = str(input())
        x , y = int(move[0])-1, int(move[1])-1 #we subtract one to match 'board' array index numbers
        direc = move[2]
    
    interpret_move(direc, x, y , board_2) 

def validate_move (board_2, direc, x, y , piece):
    """
    validates if a move from a human player is eligible
    :param direc: the direction of movement(West,East,...)
    :param x: the position of the moving piece in x axis, column-wise
    :param y: the position of the moving piece in y axis, row-wise
    :param piece: the piece that player plays with
    :return: True if the movements are not eligible, False when movements are fine
    """
    
    valid_direc=['N','E','W','S']
    if(
     (x==6 and direc=='E') or
     (x==0 and direc=='W') or
     (y==0 and direc=='N') or 
     (y==6 and direc=='S') or
     (y not in range(7)) or
     (x not in range (7)) or 
     (direc not in valid_direc) or
     (board_2[y][x]==' ') or
     (board_2[y][x]!=piece)
     ):
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

    
def comp_turn(board_2, human_p, comp_p , d):

    """
    Computes a move for AI agent through Minimax+alpha_beta pruning
    sends the move command to the Telnet client and draws the new board 
    :param remote_p: the piece that remote agent plays with
    :param comp_p: the piece that AI agent plays with
    """
    
    print('Computer turn [%s]' %comp_p)
    direction=['N', 'W', 'E','S']# with the order of m arrangement in minimax function
    if (win(board_2, human_p) or win(board_2, comp_p)):
        return
    start = timeit.default_timer()
    move = [0 , 0 , 0 ,0]
    count =0
    move , count = max_alpha_beta(board_2,-inf, +inf, human_p, comp_p, d, start,count)
    end = timeit.default_timer()
    print('with alpha-beta pruning runtime:' , end - start)
    start = timeit.default_timer()
    count2 =0
    move , count2 = max_minimax(board_2, human_p, comp_p, d, start,count2)
    end = timeit.default_timer()
    print('without alpha-beta runtime:' , end - start)

    #interpret_move(direc, x, y , board)
    
    global COUNTER
    COUNTER=1+COUNTER
    
    return count , count2
    #return max_alpha_beta.counter+min_alpha_beta.counter

                      
def max_alpha_beta(state, alpha, beta, human_p, comp_p, depth, start, count):
    """
    minimax algorithm with alpha-beta pruning, Max player
    :param state: the current state of the board
    :param alpha: the alpha parameter for pruning
    :param beta: the beta parameter for pruning
    :param human_p: the piece that human player plays with
    :param comp_p: the piece that AI agent plays with
    :param depth: the maximum depth search of the tree
    :param start: the starting time of minimax search to cut the search after 10 sec
    :param count: if true count the number of states explored
    :return: the best movement with highest value for the max player 
    """ 
    count+=1
    best = [None, None, None , -inf]
    p = comp_p
    #score=heuristic_count(state, comp_p , human_p)
    stop = timeit.default_timer()
    if depth<=0 or win(state , p):# or stop-start>=8.5:
          score = heuristic_count(state, comp_p , human_p)
          return [-1, -1, -1 , score] , count
        
    m =[(-1,0),(0,-1),(0,1),(1,0)]
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell==p: 
                for (i ,j) in m:
                    if (y+i)>(6) or (x+j)>(6) or (y+i)<0 or (x+j)<0:
                       continue
                    if state[y+i][x+j]==' ':
                        state[y+i][x+j]= p
                        state[y][x] = ' '
                        score , count = min_alpha_beta(state, alpha, beta, human_p, comp_p, depth-1, start,count)
                        state[y+i][x+j]= ' '
                        state[y][x] = p
                        score[0], score[1], score[2] = y, x, m.index((i ,j))
                        
                        if score[3] > best[3]: 
                            best = score
                        
                        if best [3] >= beta:
                            return [y,x , m.index((i ,j)), best[3]], count
                        
                        if best[3] > alpha:
                            alpha = best[3] 
    
    #print('number of explored states:', explored)           
    return best , count

def min_alpha_beta(state, alpha, beta, human_p, comp_p, depth, start , count):
    """
    minimax algorithm with alpha-beta pruning, Min player
    :param state: the current state of the board
    :param alpha: the alpha parameter for pruning
    :param beta: the beta parameter for pruning
    :param human_p: the piece that human player plays with
    :param comp_p: the piece that AI agent plays with
    :param depth: the maximum depth search of the tree
    :param start: the starting time of minimax search to cut the search after 10 sec
    :param count: if true count the number of states explored
    :return: the best movement with lowest value for the min player 
    """ 
    count+=1
    best = [None, None, None , +inf]
    p = human_p
    #score=heuristic_count(state, comp_p , human_p)
    stop = timeit.default_timer()
    if depth<=0 or win(state , p):# or stop-start>=8.5:
          score=heuristic_count(state, comp_p , human_p)
          return [-1, -1, -1 , score] , count
      
    m =[(-1,0),(0,-1),(0,1),(1,0)]
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell==p: 
                for (i ,j) in m:
                    if (y+i)>(6) or (x+j)>(6) or (y+i)<0 or (x+j)<0:
                       continue
                    if state[y+i][x+j]==' ':
                        state[y+i][x+j]= p
                        state[y][x] = ' '
                        score , count = max_alpha_beta(state, alpha, beta, human_p, comp_p, depth-1, start,count)
                        state[y+i][x+j]= ' '
                        state[y][x] = p
                        score[0], score[1], score[2] = y, x, m.index((i ,j))
                        
                        if score[3] < best[3]: 
                            best = score
                        
                        if best [3] <= alpha:
                            return [y,x , m.index((i ,j)), best[3]] , count
                        
                        if best[3] < beta:
                            beta= best[3] 
                
    #print('number of explored states:', explored)
    return best , count
    

def max_minimax(state, human_p, comp_p, depth, start, count):
    """
    minimax algorithm with alpha-beta pruning, Max player
    :param state: the current state of the board
    :param alpha: the alpha parameter for pruning
    :param beta: the beta parameter for pruning
    :param human_p: the piece that human player plays with
    :param comp_p: the piece that AI agent plays with
    :param depth: the maximum depth search of the tree
    :param start: the starting time of minimax search to cut the search after 10 sec
    :param count: if true count the number of states explored
    :return: the best movement with highest value for the max player 
    """ 
    count+=1
    best = [None, None, None , -inf]
    p = comp_p
    #score=heuristic_count(state, comp_p , human_p)
    stop = timeit.default_timer()
    if depth<=0 or win(state , p): #or stop-start>=8.5:
          score = heuristic_count(state, comp_p , human_p)
          return [-1, -1, -1 , score] , count
        
    m =[(-1,0),(0,-1),(0,1),(1,0)]
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell==p: 
                for (i ,j) in m:
                    if (y+i)>(6) or (x+j)>(6) or (y+i)<0 or (x+j)<0:
                       continue
                    if state[y+i][x+j]==' ':
                        state[y+i][x+j]= p
                        state[y][x] = ' '
                        score , count = min_minimax(state, human_p, comp_p, depth-1, start,count)
                        state[y+i][x+j]= ' '
                        state[y][x] = p
                        score[0], score[1], score[2] = y, x, m.index((i ,j))
                        
                        if score[3] > best[3]: 
                            best = score
                        
    
    #print('number of explored states:', explored)           
    return best , count

def min_minimax(state, human_p, comp_p, depth, start , count):
    """
    minimax algorithm with alpha-beta pruning, Min player
    :param state: the current state of the board
    :param alpha: the alpha parameter for pruning
    :param beta: the beta parameter for pruning
    :param human_p: the piece that human player plays with
    :param comp_p: the piece that AI agent plays with
    :param depth: the maximum depth search of the tree
    :param start: the starting time of minimax search to cut the search after 10 sec
    :param count: if true count the number of states explored
    :return: the best movement with lowest value for the min player 
    """ 
    count+=1
    best = [None, None, None , +inf]
    p = human_p
    #score=heuristic_count(state, comp_p , human_p)
    stop = timeit.default_timer()
    if depth<=0 or win(state , p): #or stop-start>=8.5:
          score=heuristic_count(state, comp_p , human_p)
          return [-1, -1, -1 , score] , count
      
    m =[(-1,0),(0,-1),(0,1),(1,0)]
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell==p: 
                for (i ,j) in m:
                    if (y+i)>(6) or (x+j)>(6) or (y+i)<0 or (x+j)<0:
                       continue
                    if state[y+i][x+j]==' ':
                        state[y+i][x+j]= p
                        state[y][x] = ' '
                        score , count = max_minimax(state, human_p, comp_p, depth-1, start,count)
                        state[y+i][x+j]= ' '
                        state[y][x] = p
                        score[0], score[1], score[2] = y, x, m.index((i ,j))
                        
                        if score[3] < best[3]: 
                            best = score
                        

    #print('number of explored states:', explored)
    return best , count
    

def graph():
    
    """
    rules the game rounds between remote agent and AI agent
    and prints the result of the game.
    """
    board_2 = initial_state(board) #states A , B , C
    
    comp_p= 'X'
    human_p = 'O'
    alpha_beta = []
    minimax = []
    print('to plot the explored states you should first do a move')
    move_func(board_2, human_p, comp_p)
    for d in range(MIN_DEPTH, MAX_DEPTH+1):
        alphabeta_nodes , minimax_nodes = comp_turn(board_2,human_p, comp_p, d)
        alpha_beta.append(alphabeta_nodes)
        minimax.append(minimax_nodes)
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))   
    d= [3 , 4 , 5, 6]
    print(minimax)
    print(alpha_beta)
    plt.plot(d , minimax ,  "o-", label='Minimax')
    plt.plot(d,alpha_beta,  "ro-", label='Alpha-beta')
    plt.xlabel('Depth cutoff')
    plt.ylabel('Number of explored nodes', )
    plt.grid(True)
    
    for x, y in zip(d, minimax):
      if x == 3:
            plt.annotate('{}'.format(y), xy=(x, y), xytext=(0, 3), ha='right', textcoords='offset points', size=10,
                         color='b')
      elif x == 5:
            plt.annotate('{}'.format(y), xy=(x, y), xytext=(-5, 0), ha='right', textcoords='offset points', size=10,
                         color='b')
      else:
            plt.annotate('{}'.format(y), xy=(x, y), xytext=(-5, 5), ha='right', textcoords='offset points', size=10,
                         color='b')

    for x, y in zip(d, alpha_beta):
        plt.annotate('{}'.format(y), xy=(x, y), xytext=(30, -10), ha='right',
                     textcoords='offset points', size=10, color='r')
    plt.show()  

if __name__ == '__main__':
    graph()