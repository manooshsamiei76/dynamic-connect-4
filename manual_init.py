# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 08:03:23 2020

@author: ASUS
"""
#enter the initial state manually


def board_input(board, k ,m):
    
    board[k][m]=input()

    return str(board[k][m])
    
    
def manual_init_state(board):
        
       #initialize an empty board
       for t in range(7):
           board[t]=[' ' for e in board]
       #ask for inputs fro the user
       print('Press X, O or space tab and press enter to fill the empty squares\n starting from upper left corner to bottom right corner')
       print('\n be careful of the capital format!')
       o=0
       x=0
       for k in range(7):
           for m in range(7):
               board_input(board, k ,m)
               if (board[k][m] =='X'): 
                   x+=1
                    
               if (board[k][m] =='O'): 
                   o+=1
               
               while not(board[k][m]=='O' or board[k][m]=='X' or board[k][m]==' '):
                 print('value error.Try again')
                 board_input(board, k ,m)
                 if (board[k][m] =='X'): 
                     x+=1   
                 if (board[k][m] =='O'): 
                     o+=1
               
               while((o>6 and board[k][m] =='O') or
                     (x>6 and board[k][m] == 'X')
                     ):
                         print('maximum number of pieces exceeded!Try again') 
                         board_input(board, k ,m)
                         
                         print('\n')
                         if (board[k][m] =='X'): 
                             x+=1
                    
                         if (board[k][m] =='O'): 
                             o+=1
               
               if k==6 and m==6:
                   print('the initial state is:')
               #draw pieces arrangement each time            
               for i in range(7):
                   for j in range(7): 
                       if j==6:
                           print(board[i][j].strip('\n'))
                       else:
                           print(board[i][j], end=',')
       return board