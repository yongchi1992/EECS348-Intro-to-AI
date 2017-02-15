##  Team Member:
##  Yongchi Zhang
##  Yikun Cao
##  Weixiang Zhang


import copy
import GameApp      ## need to use check_win() in GameApp.py


## use alpha-beta pruning to optimize the min max algorithm
def SearchMove(board,side,alpha,beta,pos,prev_pos):  
    
    i=0
    tmp=[1]
    cnt=0
    
    if(side==1):
        countersym="O"
    elif(side==-1):
        countersym="X"
    
    for k in range(0,9):
        if(board[k]==1 or board[k]==-1):
            cnt+=1       ## count how many steps
    
    if (prev_pos != -1 and GameApp.check_win(board)==countersym):
        return -1      ## Lose
    if(cnt==9):
        return 0       ## Draw
        
    
    while(i<9 and alpha < beta):
        if (board[i]==1 or board[i]==-1):
            i+=1
            continue     # If there has been a step,then continue the loop
        temp_board=copy.deepcopy(board)   ## use deepcopy to avoid change the board
        temp_board[i] = side
        res = -SearchMove(temp_board,-side, -beta, -alpha, tmp, i)   #the best of adversary is the worst of my side
        if (res > alpha):    #find a better step
            alpha = res
            pos[0] = i
        i+=1

    return alpha


def mymove(board,mysymbol):
    print "Board as seen by the machine:",
    print board
    print "The machine is playing:",
    print mysymbol
    if(mysymbol=="X"):
        side=1
    elif(mysymbol=="O"):
        side=-1
    pos=[1]
    SearchMove(board,side, -1, 1, pos, -1)
    return pos[0]+1
