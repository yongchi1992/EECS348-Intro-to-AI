##  Team Member:
##  Yongchi Zhang
##  Yikun Cao
##  Weixiang Zhang

import updatewumpusNowWithRocks

def orientation_infer(target_location,now_location):
    if(int(target_location[5])==int(now_location[5])):
        if(int(target_location[6])==int(now_location[6])+1):
            orientation = "Up"
        elif(int(target_location[6])==int(now_location[6])-1):
            orientation = "Down"
    elif(int(target_location[6])==int(now_location[6])):
        if(int(target_location[5])==int(now_location[5])+1):
            orientation = "Right"
        elif(int(target_location[5])==int(now_location[5])-1):
            orientation = "Left"  
    return orientation

def ask_location(situation):
    return situation[5]

def infer_next_location(knowledge,around,path,unvisited,return_flag,get_gold): 
    next_go = ''
    for location in around:
        if(('no_wumpus' in knowledge[location]) and ('no_pit' in knowledge[location]) and (location in unvisited) and (get_gold ==0)):
            next_go = location
            return_flag[0] = 0
            break
    if(next_go == '' or get_gold==1):
        return_flag[0] = 1
        path.pop(len(path)-1)
        next_go = path[len(path)-1]
    return next_go
        
def infer_unvisited(knowledge,around,unvisited):
    for location in around:
        if(not(location in knowledge)):
            knowledge[location]=[]
            unvisited.append(location)
        elif(not('clean' in knowledge[location]) and not('nasty' in knowledge[location]) and not(location in unvisited)):
            unvisited.append(location)

def ask_around(name):
    return updatewumpusNowWithRocks.look_ahead(name)

def establish_kb(situation,knowledge):
    now_location = situation[5]
    smell = situation[0]
    air = situation[1]
    glitter = situation[2]
    bump = situation[3]
    scream = situation[4]    
    knowledge[now_location].extend([smell,air,glitter,bump,scream])
                     
def infer_wumpus(knowledge,now_location,around,wumpus_exist,wumpus_possibility):
    if('clean' in knowledge[now_location]):
        if(not('no_wumpus' in knowledge[now_location])):
            knowledge[now_location].append('no_wumpus')
        for location in around:
            if(not('no_wumpus' in knowledge[location])):
                knowledge[location].append('no_wumpus')
            for elem in wumpus_possibility:
                while(location in elem):
                    elem.remove(location)
    elif('nasty' in knowledge[now_location] ):
        if(wumpus_exist==0):
            for location in around:
                if(not('no_wumpus' in knowledge[location])):
                    knowledge[location].append('no_wumpus')
        elif(wumpus_exist==1):
            if(not(around in wumpus_possibility)):
                wumpus_possibility.append(around)
                
def wumpus_confirm(knowledge,wumpus_possibility):
    if(len(wumpus_possibility)==2):
        for elem1 in wumpus_possibility[0]:
            for elem2 in wumpus_possibility[1]:
                if(elem1==elem2):
                    if(not('no_wumpus' in knowledge[elem1])):
                        return elem1
    return 'not_confirm'
    
def shoot_wumpus(name,wumpus_location,now_location):
    orientation = orientation_infer(wumpus_location,now_location)
    updatewumpusNowWithRocks.take_action(name, orientation)  
    updatewumpusNowWithRocks.take_action(name, 'Shoot')     
                     
def infer_pit(name,knowledge,now_location,around,rock_num):
    if('calm' in knowledge[now_location]):
        if(not('no_pit' in knowledge[now_location])):
            knowledge[now_location].append('no_pit')
        for location in around:
            if(not('no_pit' in knowledge[location])):
                knowledge[location].append('no_pit')   
    elif('breeze' in knowledge[now_location] and rock_num[0]>0):                        
        for location in around:
            if(not('no_pit' in knowledge[location]) and not('pit' in knowledge[location])):
                if(int(location[5])==int(now_location[5])):
                    if(int(location[6])==int(now_location[6])+1):
                        orientation = "Up"
                    elif(int(location[6])==int(now_location[6])-1):
                        orientation = "Down"
                elif(int(location[6])==int(now_location[6])):
                    if(int(location[5])==int(now_location[5])+1):
                        orientation = "Right"
                    elif(int(location[5])==int(now_location[5])-1):
                        orientation = "Left"        
                updatewumpusNowWithRocks.take_action(name, orientation)
                result=updatewumpusNowWithRocks.take_action(name, 'Toss')
                if(result=='Quiet'):
                    knowledge[location].append('pit') 
                elif(result=='Clink'):
                    knowledge[location].append('no_pit') 
                rock_num[0] -= 1
                
                
def infer_gold(name,knowledge,now_location):
    get_gold=0
    if('glitter' in knowledge[now_location]):
        updatewumpusNowWithRocks.take_action(name, 'PickUp')
        get_gold=1
    return get_gold
     
def move_to_next(name, orientation):
    updatewumpusNowWithRocks.take_action(name, orientation)
    return updatewumpusNowWithRocks.take_action(name, 'Step')
                           
def main():
    ############################################### initialization
    name = updatewumpusNowWithRocks.intialize_world()
    initial = u'Cell 11'
    knowledge = {}
    knowledge[initial]=[]
    unvisited = []
    path = []
    wumpus_possibility = []
    wumpus_exist = 1
    wumpus_location = 'False'
    get_gold=0
    return_flag = [0]
    rock_num=[5]
    
    ############################################### take the first action to acquire knowledge
    orientation = "Up"
    situation = updatewumpusNowWithRocks.take_action(name, orientation)
    
    ############################################### loop to acquire information, establish knowledge-based agent, infer
    while 1 :
        
        ############################################### establish the knowledge-based agent
        now_location = ask_location(situation)
        establish_kb(situation,knowledge)
        around = ask_around(name)
        if(get_gold == 0 and return_flag[0] == 0):
            path.append(now_location)                           ## record the path
        else:
            if(now_location == initial and get_gold ==1):       ## get the gold and return to Cell 11
                updatewumpusNowWithRocks.take_action(name, 'Exit')          ## then we can exit
                return
                
        ############################################### inference engine
        infer_unvisited(knowledge,around,unvisited)
        infer_wumpus(knowledge,now_location,around,wumpus_exist,wumpus_possibility)
        infer_pit(name,knowledge,now_location,around,rock_num)
        if(get_gold == 0):
            get_gold=infer_gold(name,knowledge,now_location) 
        wumpus_location = wumpus_confirm(knowledge,wumpus_possibility)     
        
        ############################################### confirm the wumpus location and shoot
        if(wumpus_location != 'not_confirm' and wumpus_exist==1):  
            shoot_wumpus(name,wumpus_location,now_location)                  
            wumpus_exist=0
            for location in knowledge:
                if(not('no_wumpus' in knowledge[location])):
                    knowledge[location].append('no_wumpus')
                    
        ############################################### output actions
        next_go=infer_next_location(knowledge,around,path,unvisited,return_flag,get_gold)                       
        orientation = orientation_infer(next_go,now_location)
        while(next_go in unvisited):
            unvisited.remove(next_go)
        situation = move_to_next(name,orientation)
    
    
    
if __name__ == "__main__":
    
    main()
