# Jonathan Reimer-Berg

'''
Interval Scheduling Problem: Given a list of start times, end times, and weights,
our goal is to find the maximum total weight with none of the time intervals
overlaping and retrieve the solution that gives that weight. The following
solution is based off of the pseudocode given in "Algorithm Design" by Eva Tardos. 

'''

#Bottom up solution: This finds the optimal solution starting with just the 
#first interval and continues on to the next element until it reaches the end.

def bottom_up(j):
    M = [None]*(len(lyst) + 1)
    M[0] = 0   #Used when no intervals are compatible with the current one
    for i in range(1, j + 2):
        M[i] = max(lyst[i - 1][2] + M[p(i - 1) + 1], M[i - 1]) #Compare using this interval with not using it
    return M[-1]

#Retrieves solution by going through M

def find_solution(j):
    if j > 0:
        if p(j) == -1:   #If nothing else is compatible with lyst[j], p(j) returns -1
            if (lyst[j][2] > M[j-1]):
                print(lyst[j], "is part of the solution")
                find_solution(p(j))
            else:
                find_solution(j - 1)
        elif (lyst[j][2] + M[p(j)]) > M[j-1]:
            print(lyst[j], "is part of the solution")
            find_solution(p(j))  #If we used j, find the next compatable interval
        else:
            find_solution(j - 1) #Otherwise, just go to the next
    elif j == 0:
        print(lyst[j], "is part of the solution")  #Use the last one if we can
    

#Top down solution: This recursively finds the optimal solution if we use the given
#element of not, and stores it in M where it can reuse the calculated solutions. 
        
def top_down(j):
    if j == -1:
        return 0
    elif M[j] != None:  #If weve already found M[j], use it instead of re-calculating
        return M[j]
    else:
        M[j] = max(lyst[j][2] + top_down(p(j)),top_down(j-1)) #Recursively finds the optimal solution
        return M[j]


#Helper function that finds how many previus intervals are compatible with the current one.
    
def p(j):
    for i in range(0, len(lyst)):
        if lyst[i][1] > lyst[j][0]:
            return (i-1)


#Runs both solutions for a given test case below.
        
lyst = [[1,2,4],[2,5,1],[2,6,3],[5,9,4],[6,10,4]]

lyst = sorted(lyst, key=lambda tup: tup[1]) #Sort the intervals by end time
M = [None]*len(lyst)
print(top_down(len(lyst) - 1))
find_solution(len(lyst) - 1)

print('\n')

print(bottom_up(len(lyst) - 1))
find_solution(len(lyst) - 1)
