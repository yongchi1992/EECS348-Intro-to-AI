# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 22:14:02 2016

@author: Administrator
"""
import copy
import time


def act_select(now_state,n_col,n_stack):
    selectable=[]
    for i in range(0,n_col):
        for j in range(0,n_col):
            if( now_state[i][0]>0 and ( (now_state[i][0]<now_state[j][0] and now_state[j][0]>0) or (now_state[j][0]==0)) and (not(i==0 and j!=n_col-1 and now_state[i][0]==n_stack ) )  and (not(i==0 and j==n_col-1 and now_state[i][0]==n_stack-1 ) )  ):
                selectable.append([i,j])
    return selectable


def act_move(_state,act):
    state=copy.deepcopy(_state)
    temp=state[act[0]][0]
    state[act[0]].pop(0)
    if(len(state[act[0]])==0):
        state[act[0]].insert(0,0)
    if(state[act[1]][0]==0):
        state[act[1]].pop(0)
    state[act[1]].insert(0,temp)
    return state


if __name__ =="__main__":          
    
    start_time=time.clock()
    init_state=[]
    end_state=[]
    state=[]
    now_state=[]
    selectable=[]
    select_num=[]
    new_state=[]
    total_select=[]
    start_p=0
    end_p=0
    n_col=int(input('Please input the num of pegs:'))        
    for i in range(0,n_col):
        init_state.append([0])              
        end_state.append([0]) 
    n_stack=int(input('Please input the num of stacks:')) 
    init_state[0].pop(0)
    end_state[n_col-1].pop(0)
    for i in range(0,n_stack):
        init_state[0].append(i+1)
        end_state[n_col-1].append(i+1)
    state.append(copy.deepcopy(init_state))
    now_state=copy.deepcopy(init_state)
    
    while(not(end_state in state)):
        if(len(select_num)==0):
            selectable=act_select(state[0],n_col,n_stack)
            select_num.append(len(selectable))
            start_p=1;
            end_p=len(selectable);
            for each_choice in selectable:
                new_state=act_move(state[0],each_choice)
                state.append(copy.deepcopy(new_state))
                total_select.append(copy.deepcopy(each_choice))
            
        else:    
            pointer=start_p
            while(pointer<=end_p):
                selectable=[]
                selectable=act_select(state[pointer],n_col,n_stack)
                temp_num=len(selectable)
                
                for each_choice in selectable:
                    new_state=[]
                    new_state=act_move(state[pointer],each_choice)
                    if(not(new_state in state)):
                        state.append(copy.deepcopy(new_state))
                        total_select.append(copy.deepcopy(each_choice))
                    else:
                        temp_num-=1
                select_num.append(temp_num)
                pointer+=1
            act_sum=0
            for i in range(start_p,end_p+1):
                act_sum+=select_num[i]
            start_p=end_p+1
            end_p+=act_sum
    
    time_sum=0
    for i in select_num:
        time_sum+=i
    number=[]
    temp=[]
    times=0
    count=0
    for i in range(0,select_num[0]):
        temp.append(i)
        number.append(copy.deepcopy(temp))
        temp=[]
        count+=1
        
    b_pointer=0
    bb_pointer=1
    n_pointer=0
    
    while(count<time_sum):
        for i in range(0,select_num[b_pointer]):
            for j in range(0,select_num[bb_pointer]):
                temp=copy.deepcopy(number[n_pointer])
                temp.append(count)
                number.append(copy.deepcopy(temp))
                count+=1
            bb_pointer+=1
            n_pointer+=1
        b_pointer+=1
            
    index=0
    
    while(state[index]!=end_state):
        index+=1
    k=0
    while(not(index-1 in number[k])):
        k=k+1;
    
    end_time=time.clock()
    print('\n\nRunning time: %s Seconds'%(end_time-start_time))
    print('\n\nThe min steps to complete the Hanoi Tower is: '+str(len(number[k])))
    print('\nThe solution is:\n')
    for i in number[k]:
        print('Move stack from peg '+str(total_select[i][0])+' to peg '+str(total_select[i][1]))
