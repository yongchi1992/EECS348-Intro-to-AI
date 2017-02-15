Function wumpus_in_sight is incorrect in updatewumpus.py and updatewumpusNowWithRocks.py
 
def wumpus_in_sight(world, location, orientation):
next_location = world[location][orientation]
if next_location == "Void":
return False
elif world[location]["Wumpus"] is True:
return True
else:
return wumpus_in_sight(world, next_location, orientation)
 
 
It is incorrect in updatewumpus.py. Because if I'm in Cell 23 and face left to shoot the wumpus, it will fail to kill the wumpus.
 
The code should be:
 
 
def wumpus_in_sight(world, location, orientation):
next_location = world[location][orientation]
if next_location == "Void":
return False
elif world[next_location]["Wumpus"] is True:
return True
else:
return wumpus_in_sight(world, next_location, orientation)


We have revised the code in our upload file updatewumpus.py and updatewumpusNowWithRocks.py