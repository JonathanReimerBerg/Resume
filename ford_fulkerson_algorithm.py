#Jonathan Reimer-Berg

'''
In the case of a natural disaster, there may be a number of injured people in
a given area who need to go to a hospital, with a certain number of hospitals in
the area. Our gaol is to figure out if we can divide these people into the hispitals
such that none of the hospitals are overloaded. Or in otherwards, such that each
hospital recieves no more that ceil(number_injured / total_hospitals) people. In addition,
an injured person can only go to a hospital if it is within 30 minutes from them.

We will use the Ford-Fulkerson algorithm for computing the maximum flow in a flow
network. In this case, we will need to reach a flow equal to the number of injured
people, with the injured nodes only being connected to hospital nodes that are
no more than 30 units (or minutes) apart. There will be a start node (s), connected
to the injured nodes, connected to the hospital nodes, connected to the end
node (t). The maximum capacity on each edge will be one, unless there are duplicates
in which case the capcity is increased by 1 for each duplicate. 
'''

import math
import random

injured = []
hospitals = []
number_injured = 100
total_hospitals = 5

for i in range(0, number_injured):    #create a list of the locations of injured people and hospitals
    injured.append((random.randint(0, 50), random.randint(0, 50))) #each unit represents one unit of travel

for i in range(0, total_hospitals):
    hospitals.append((random.randint(0, 50), random.randint(0, 50)))


dyct = {}    #this will denote all of the vertices conneting each node
maxx = math.ceil(len(injured) / len(hospitals))

for k in hospitals:
    if (k,"t") in dyct:       #removes duplicates and increases capcity on edge
        dyct[k,"t"] += maxx
    else:
        dyct[k,"t"] = maxx    #maximum capicity we are allowing per hospital
        dyct["t",k] = 0    #create backwards edges for later. paths from "t" back aren't used, but are added to shorten later code
for n in injured:
    if ("s",n) in dyct:
        dyct["s",n] += 1
    else:
        dyct["s",n] = 1    #each edge from start (s) has capacity of 1
        dyct[n,"s"] = 0    
    for k in hospitals:
        if math.sqrt((n[0] - k[0])**2 + (n[1] - k[1])**2) <= 30: #if they are within 30 units (minutes)
            if (n,k) in dyct:
                dyct[n,k] += 1
            else:
                dyct[n,k] = 1
                dyct[k,n] = 0

def find_path(path, nots):
    for i in dyct:
        if (path[-1] == i[0]) and (dyct[i] > 0) and (i[1] not in nots):  #if the i'th path is valid 
            path.append(i[1])  #added new node to the path
            nots.append(i[1])  #prevents needless calculation, if the path fails don't retry it
            if path[-1] == "t":  #we completed the path (may recursively return)
                return(path, nots)
            else:
                path = find_path(path, nots)[0] #continue path
                if path[-1] == "t":
                    return(path, nots)
    nots.append(path[-1])
    path = path[:-1]  #if there is no valid path, back up and try again
    return(path, nots)

def augment(path):
    for i in range(0, len(path) - 1):
        dyct[path[i], path[i + 1]] -= 1  #reduce the available flows on used path
        dyct[path[i + 1], path[i]] += 1  #add flow to the backwards paths
    return
        
def ford_fulkerson():
    flow = 0    #total flow, which must reach len(injured) for everything to get matched
    while flow < len(injured):
        path = find_path(["s"], ["s"])[0]
        if len(path) == 0:
            break
        if path[-1] != "t":  #must be able to reach the end, or the matching is not possible
            break
        augment(path)  #update the dyct flow values
        flow += 1
    if flow == len(injured):
        return("Found an optimal routing!")
    else:
        return("No optimal routing found")
            
print(ford_fulkerson())



